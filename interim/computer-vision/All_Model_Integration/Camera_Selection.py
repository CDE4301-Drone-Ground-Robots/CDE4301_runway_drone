"""Resolve a Windows DirectShow camera by USB identity without extra packages."""
import ctypes as c
import uuid


class GUID(c.Structure):
    _fields_ = [('data', c.c_ubyte * 16)]

    def __init__(self, value):
        super().__init__()
        self.data[:] = uuid.UUID(value).bytes_le


def _method(obj, slot, restype, *args):
    table = c.cast(obj, c.POINTER(c.POINTER(c.c_void_p))).contents
    return c.WINFUNCTYPE(restype, c.c_void_p, *args)(table[slot])


def _release(obj):
    if obj:
        _method(obj, 2, c.c_ulong)(obj)


def list_directshow_cameras():
    ole = c.OleDLL('ole32')
    aut = c.OleDLL('oleaut32')
    initialized = ole.CoInitialize(None)
    if initialized < 0:
        raise RuntimeError(f'Cannot initialize camera enumeration: {initialized}')
    factory, enum = c.c_void_p(), c.c_void_p()
    cameras = []
    try:
        clsid = GUID('62BE5D10-60EB-11D0-BD3B-00A0C911CE86')
        iid = GUID('29840822-5B84-11D0-BD3B-00A0C911CE86')
        hr = ole.CoCreateInstance(c.byref(clsid), None, 1, c.byref(iid), c.byref(factory))
        if hr != 0:
            raise RuntimeError(f'Cannot enumerate cameras: {hr}')
        category = GUID('860BB310-5D01-11D0-BD3B-00A0C911CE86')
        hr = _method(factory, 3, c.c_long, c.POINTER(GUID), c.POINTER(c.c_void_p), c.c_ulong)(factory, c.byref(category), c.byref(enum), 0)
        if hr == 1:
            return cameras
        if hr != 0:
            raise RuntimeError(f'Cannot enumerate cameras: {hr}')
        bag_iid = GUID('55272A00-42CB-11CE-8135-00AA004BB851')
        while True:
            moniker, fetched = c.c_void_p(), c.c_ulong()
            hr = _method(enum, 3, c.c_long, c.c_ulong, c.POINTER(c.c_void_p), c.POINTER(c.c_ulong))(enum, 1, c.byref(moniker), c.byref(fetched))
            if hr == 1:
                break
            if hr != 0:
                raise RuntimeError(f'Cannot read camera list: {hr}')
            bag = c.c_void_p()
            try:
                hr = _method(moniker, 9, c.c_long, c.c_void_p, c.c_void_p, c.POINTER(GUID), c.POINTER(c.c_void_p))(moniker, None, None, c.byref(bag_iid), c.byref(bag))
                if hr != 0:
                    raise RuntimeError(f'Cannot read camera identity: {hr}')
                values = {'index': len(cameras)}
                for key in ('FriendlyName', 'DevicePath'):
                    variant = c.create_string_buffer(24)
                    try:
                        hr = _method(bag, 3, c.c_long, c.c_wchar_p, c.c_void_p, c.c_void_p)(bag, key, variant, None)
                        if hr == 0 and c.cast(variant, c.POINTER(c.c_ushort)).contents.value == 8:
                            ptr = c.c_void_p.from_buffer(variant, 8).value
                            values[key] = c.wstring_at(ptr) if ptr else ''
                    finally:
                        aut.VariantClear(variant)
                cameras.append(values)
            finally:
                _release(bag)
                _release(moniker)
        return cameras
    finally:
        _release(enum)
        _release(factory)
        ole.CoUninitialize()


def find_external_camera(usb_identity):
    cameras = list_directshow_cameras()
    for camera in cameras:
        print(f"Camera {camera['index']}: {camera.get('FriendlyName', 'Unknown')}", flush=True)
    matches = [camera for camera in cameras
               if usb_identity.lower() in camera.get('DevicePath', '').lower()]
    if len(matches) != 1:
        raise RuntimeError(f'Expected one external camera ({usb_identity}), found {len(matches)}. Reconnect it and restart.')
    selected = matches[0]
    print(f"Selected external camera: {selected['FriendlyName']} at DirectShow index {selected['index']}", flush=True)
    return selected['index']
