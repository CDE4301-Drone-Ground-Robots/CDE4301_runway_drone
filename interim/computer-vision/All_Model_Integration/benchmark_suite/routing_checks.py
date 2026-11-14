"""Correctness checks only: fake detector outputs are never used as performance samples."""
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import core

class Stub:
    def __init__(self,result):self.result=result;self.calls=0
    def detect(self,frame):self.calls+=1;return self.result

def check(fod,crack,parallel,anomaly=True):
    det=dict(object="test",confidence=.9,bbox=(0,0,1280,720))
    models=dict(patchcore=Stub(dict(boxes=[(0,0,8,8)] if anomaly else [])),
                fod=Stub([det] if fod else []),
                crack=Stub(dict(bbox=(0,0,1280,720)) if crack else None))
    frame=np.zeros((8,8,3),dtype=np.uint8)
    with ThreadPoolExecutor(max_workers=2) as pool:
        records,details=core.pipeline(frame,models,parallel,pool if parallel else None)
    expected_crack=int(anomaly and (parallel or not fod))
    assert models["crack"].calls==expected_crack
    assert models["fod"].calls==int(anomaly)
    assert details["coordinate_count"]==int(anomaly and fod)
    expected_base=int(anomaly and ((crack and expected_crack) or not fod))
    assert details["base_message_count"]==expected_base
    assert details["ugv_message_count"]==int(anomaly and fod)
    assert np.count_nonzero(frame)==0
    return dict(fod=fod,crack=crack,parallel=parallel,anomaly=anomaly,status="passed",routing=details)

def check_sequential2(fod,crack,anomaly=True):
    events=[]
    class Ordered(Stub):
        def __init__(self,name,result):super().__init__(result);self.name=name
        def detect(self,frame):events.append(self.name);return super().detect(frame)
    models=dict(patchcore=Ordered("patchcore",dict(boxes=[(0,0,8,8)] if anomaly else [])),
                fod=Ordered("fod",[dict(object="test",confidence=.9,bbox=(0,0,1280,720))] if fod else []),
                crack=Ordered("crack",dict(bbox=(0,0,1280,720)) if crack else None))
    records,details=core.pipeline(np.zeros((8,8,3),dtype=np.uint8),models,sequential2=True)
    assert events==(["patchcore","fod","crack"] if anomaly else ["patchcore"])
    assert details["crack_calls"]==int(anomaly)
    assert details["coordinate_count"]==int(anomaly and fod)
    assert details["base_message_count"]==int(anomaly)
    assert details["ugv_message_count"]==int(anomaly and fod)
    if anomaly:
        base=[r for r in records if r["destination"]=="BASE"]
        assert base[0]["type"]==("CRACK" if crack else "NO_CRACK_DETECTED")
    return dict(mode="sequential2",fod=fod,crack=crack,anomaly=anomaly,status="passed",routing=details)

if __name__=="__main__":
    checks=[check(f,c,p) for p in (False,True) for f,c in ((True,True),(True,False),(False,True),(False,False))]
    checks += [check(False,False,p,anomaly=False) for p in (False,True)]
    checks += [check_sequential2(f,c) for f,c in ((True,True),(True,False),(False,True),(False,False))]
    checks.append(check_sequential2(False,False,anomaly=False))
    core.write_json(core.OUT/"routing_checks.json",dict(status="passed",checks=checks,
        meaning="logic checks, not model accuracy or timing measurements"))
    core.write_json(core.OUT/"coordinate_math_test.json",core.self_test(core.SIMULATION))
    print("Passed 15 routing checks and 4 coordinate math checks",flush=True)

