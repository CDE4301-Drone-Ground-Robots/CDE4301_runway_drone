"""Responsive UAV RGB prototype: latest-frame threaded processing + CSV + snapshots.

Camera stays on the main thread, heavy ML runs in a worker. Old frames are
DROPPED when inference cannot keep up. Not a lossless video recorder or a
flight-safety loop: actual thermal failsafe requires independent controller.
"""
import csv
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import cv2
from Camera_Selection import find_external_camera
import numpy as np
import torch

from Patchcore_Detection import PatchcoreDetector
from FOD_detection import FODDetector
from Crack_Detection import CrackDetector
from Thermal_Detection import ThermalDetector

ROOT = Path(__file__).resolve().parent
EXTERNAL_CAMERA_USB_ID = 'vid_eba4&pid_6579'  # UGREEN Camera 4K
FRAME_WIDTH, FRAME_HEIGHT = 1280, 720
PATCHCORE_MODEL = ROOT / 'Anomaly_model.ckpt'
YOLO_MODEL = ROOT / 'FOD_yolo11s.pt'
CRACK_MODEL = ROOT / 'best_crack_model.pth'
CSV_PATH = ROOT / 'detections.csv'
SNAPSHOT_DIR = ROOT / 'anomaly_snapshots'
SNAPSHOT_EVERY = 100
ANOMALY_SCORE_THRESHOLD = 0.05  # Needs calibration!
YOLO_CONF = 0.30
CRACK_THRESHOLD = 0.50
LOG_INTERVAL_SECONDS = 1.0
# Downstream models inspect EVERY anomaly ROI (maximum sensitivity), not every frame.
# Set max ROI / consolidation only after evaluating missed-object rate.
ROI_INFERENCE_WIDTH, ROI_INFERENCE_HEIGHT = 1280, 720
FIELDS = ['timestamp_utc','frame_number','type','name','confidence',
          'anomaly_score','center_x_px','center_y_px','offset_x_px',
          'offset_y_px','bbox_x1','bbox_y1','bbox_x2','bbox_y2']


def remap_box(bbox, roi, input_size):
    rx1, ry1, rx2, ry2 = roi
    sw, sh = input_size
    x1,y1,x2,y2 = bbox
    sx, sy = (rx2-rx1)/sw, (ry2-ry1)/sh
    return (round(rx1+x1*sx), round(ry1+y1*sy),
            round(rx1+x2*sx), round(ry1+y2*sy))


def count_existing_records(path):
    if not path.exists() or path.stat().st_size == 0:
        return 0
    with path.open('r', newline='', encoding='utf-8') as f:
        return sum(1 for r in csv.DictReader(f) if any(r.values()))


def save_snapshot(frame, amap, display, row_count):
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    lo, hi = float(np.min(amap)), float(np.max(amap))
    heat = np.uint8(255 * (amap-lo) / max(hi-lo, 1e-8))
    color = cv2.applyColorMap(heat, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(frame, .55, color, .45, 0)
    for suffix, img in [('rgb',frame),('heatmap',color),('overlay',overlay),('detections',display)]:
        path = SNAPSHOT_DIR / f'csv_{row_count:06d}_{suffix}.png'
        if not cv2.imwrite(str(path), img):
            raise RuntimeError(f'Cannot save {path}')
    print(f'Saved snapshots at CSV #{row_count}', flush=True)


def put_latest(q, value):
    try:
        q.put_nowait(value)
    except queue.Full:
        try:
            q.get_nowait()
        except queue.Empty:
            pass
        try:
            q.put_nowait(value)
        except queue.Full:
            pass


MODES = {0: 'PAUSED', 1: 'PATCHCORE ONLY', 2: 'FOD YOLO ONLY',
         3: 'CRACK U-NET ONLY', 4: 'FULL PIPELINE'}


def detection_worker(inbox, results, stopping, mode_state):
    seen = {}
    csv_rows = count_existing_records(CSV_PATH)
    snapshot_tasks = ThreadPoolExecutor(max_workers=1)
    anomaly = fod = crack = None
    previous_mode = None
    try:
        device = 0 if torch.cuda.is_available() else 'cpu'
        print('AI worker ready; press 1/2/3/4 to load and test a model.', flush=True)
        with CSV_PATH.open('a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(FIELDS)
                f.flush()
            while not stopping.is_set():
                try:
                    frame_id, frame = inbox.get(timeout=.1)
                except queue.Empty:
                    continue
                with mode_state['lock']:
                    mode = mode_state['mode']
                    generation = mode_state['generation']
                if mode == 0:
                    continue
                # Load ONLY the models required by the selected test, lazily once.
                if mode in (1, 4) and anomaly is None:
                    print('Loading PatchCore...', flush=True)
                    try:
                        anomaly = PatchcoreDetector(PATCHCORE_MODEL,
                                                   score_threshold=ANOMALY_SCORE_THRESHOLD)
                    except Exception as exc:
                        print(f'PATCHCORE LOAD ERROR: {type(exc).__name__}: {exc}', flush=True)
                        with mode_state['lock']:
                            if mode_state['generation'] == generation:
                                mode_state['mode'] = 0
                        continue
                if mode in (2, 4) and fod is None:
                    print('Loading FOD YOLO...', flush=True)
                    try:
                        fod = FODDetector(str(YOLO_MODEL), confidence=YOLO_CONF, device=device)
                    except Exception as exc:
                        print(f'YOLO LOAD ERROR: {type(exc).__name__}: {exc}', flush=True)
                        with mode_state['lock']:
                            if mode_state['generation'] == generation:
                                mode_state['mode'] = 0
                        continue
                if mode in (3, 4) and crack is None:
                    print('Loading Crack U-Net...', flush=True)
                    try:
                        crack = CrackDetector(str(CRACK_MODEL), image_size=512,
                                              threshold=CRACK_THRESHOLD)
                    except Exception as exc:
                        print(f'CRACK LOAD ERROR: {type(exc).__name__}: {exc}', flush=True)
                        with mode_state['lock']:
                            if mode_state['generation'] == generation:
                                mode_state['mode'] = 0
                        continue
                # If user selected another mode during model load, drop this result.
                with mode_state['lock']:
                    if mode_state['generation'] != generation:
                        continue
                if previous_mode != mode:
                    print('Running:', MODES[mode], flush=True)
                    previous_mode = mode
                try:
                    h, w = frame.shape[:2]
                    center = (w//2, h//2)
                    display = frame.copy()
                    patch = {'boxes': [], 'score': 0.0,
                             'map': np.zeros((h, w), dtype=np.float32)}
                    if mode in (1, 4):
                        patch = anomaly.detect(frame)
                    rois = patch['boxes'] if mode in (1, 4) else [(0, 0, w, h)]
                    records = []
                    for roi in rois:
                        xa, ya, xb, yb = roi
                        crop = frame[ya:yb, xa:xb]
                        if not crop.size:
                            continue
                        # PatchCore-only: draw/log each anomaly directly.
                        if mode == 1:
                            records.append(('ANOMALY', 'patchcore_anomaly', '', roi))
                            continue
                        zoomed = cv2.resize(crop, (ROI_INFERENCE_WIDTH,
                                                   ROI_INFERENCE_HEIGHT))
                        found = []
                        if mode in (2, 4):
                            for det in fod.detect(zoomed):
                                found.append(('FOD', det['object'],
                                              round(float(det['confidence']), 4),
                                              remap_box(det['bbox'], roi,
                                                        (ROI_INFERENCE_WIDTH,
                                                         ROI_INFERENCE_HEIGHT))))
                        if mode in (3, 4):
                            cr = crack.detect(zoomed)
                            if cr is not None:
                                found.append(('CRACK', 'crack', '',
                                              remap_box(cr['bbox'], roi,
                                                        (ROI_INFERENCE_WIDTH,
                                                         ROI_INFERENCE_HEIGHT))))
                        if not found and mode == 4:
                            found = [('UNKNOWN_ANOMALY', 'unknown', '', roi)]
                        records.extend(found)
                    # Keep screen and CSV results from the same selected mode.
                    with mode_state['lock']:
                        if mode_state['generation'] != generation:
                            continue
                    for typ, name, conf, bbox in records:
                        x1, y1, x2, y2 = bbox
                        cx, cy = (x1+x2)//2, (y1+y2)//2
                        color = ((255, 0, 0) if typ == 'CRACK' else
                                 (0, 165, 255) if typ == 'ANOMALY' else
                                 (0, 255, 255))
                        cv2.rectangle(display, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(display, name, (x1, max(20, y1-5)),
                                    cv2.FONT_HERSHEY_SIMPLEX, .55, color, 2)
                        key_id = (mode, typ, name, cx//100, cy//100)
                        now = time.monotonic()
                        if now-seen.get(key_id, -1e9) < LOG_INTERVAL_SECONDS:
                            continue
                        seen[key_id] = now
                        writer.writerow([datetime.now(timezone.utc).isoformat(),
                                         frame_id, typ, name, conf,
                                         round(patch['score'], 6) if mode in (1, 4) else '',
                                         cx, cy, cx-center[0], cy-center[1],
                                         x1, y1, x2, y2])
                        f.flush()
                        csv_rows += 1
                        print(f'[{MODES[mode]}] {typ}: {name}, '
                              f'offset=({cx-center[0]}, {cy-center[1]}) px', flush=True)
                        if csv_rows % SNAPSHOT_EVERY == 0:
                            if mode in (1, 4):
                                task = snapshot_tasks.submit(
                                    save_snapshot, frame.copy(), patch['map'].copy(),
                                    display.copy(), csv_rows)
                                task.add_done_callback(
                                    lambda future: print('Snapshot error:', future.exception(),
                                                         flush=True) if future.exception() else None)
                            else:
                                # Do not fabricate a PatchCore heatmap in YOLO/U-Net-only mode.
                                task = snapshot_tasks.submit(
                                    save_non_patch_snapshot, frame.copy(), display.copy(),
                                    csv_rows, MODES[mode])
                                task.add_done_callback(
                                    lambda future: print('Snapshot error:', future.exception(),
                                                         flush=True) if future.exception() else None)
                    cv2.circle(display, center, 5, (0, 255, 0), -1)
                    label = f'{MODES[mode]}' + (
                        f" score={patch['score']:.3f}" if mode in (1, 4) else '')
                    cv2.putText(display, label, (12, 25),
                                cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 2)
                    put_latest(results, (frame_id, display, patch['score'], mode, records))
                except Exception as exc:
                    print(f'[{MODES[mode]}] INFERENCE ERROR: '
                          f'{type(exc).__name__}: {exc}', flush=True)
                    # Keep the camera responsive; pause only the failing test.
                    with mode_state['lock']:
                        if mode_state['generation'] == generation:
                            mode_state['mode'] = 0
    finally:
        snapshot_tasks.shutdown(wait=True)
        if anomaly is not None:
            anomaly.close()


def save_non_patch_snapshot(frame, display, row_count, mode_name):
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    for suffix, img in [('rgb', frame), ('detections', display)]:
        path = SNAPSHOT_DIR / f'csv_{row_count:06d}_{suffix}.png'
        if not cv2.imwrite(str(path), img):
            raise RuntimeError(f'Cannot save {path}')
    print(f'Saved {mode_name} snapshots at CSV #{row_count} '
          '(no PatchCore heatmap in this test mode)', flush=True)


def main():
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    incoming = queue.Queue(maxsize=1)
    outgoing = queue.Queue(maxsize=1)
    stopping = threading.Event()
    mode_state = {'lock': threading.Lock(), 'mode': 0, 'generation': 0}
    thermal = ThermalDetector()

    print(f'Running: {Path(__file__).resolve()}', flush=True)
    camera_id = find_external_camera(EXTERNAL_CAMERA_USB_ID)
    cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap.release()
        raise RuntimeError(f'Cannot open webcam at index {camera_id}. Close other camera apps or check index.')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    print('Actual camera resolution:', int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
          'x', int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), flush=True)

    worker = threading.Thread(target=detection_worker,
                              args=(incoming, outgoing, stopping, mode_state), daemon=False)
    worker.start()
    frame_id = 0
    latest_result = None
    failures = 0
    window = f'UAV Detection System - External UGREEN Camera 4K (index {camera_id})'
    cv2.namedWindow(window, cv2.WINDOW_AUTOSIZE)
    print('Controls: 1=PatchCore  2=YOLO  3=Crack  4=Full  '
          '0=Pause  5=Thermal simulation  q=Quit', flush=True)
    print('Starting PAUSED. Click the camera window, then press a key.', flush=True)
    try:
        while not stopping.is_set():
            ok, frame = cap.read()
            if not ok or frame is None:
                failures += 1
                if failures >= 3:
                    print('Webcam stopped providing frames. Close other camera apps, '
                          'reconnect webcam, then restart.', flush=True)
                    break
                # A transient dropped frame should not immediately end the session.
                cv2.waitKey(30)
                continue
            failures = 0
            frame_id += 1
            with mode_state['lock']:
                mode = mode_state['mode']
            if mode:
                put_latest(incoming, (frame_id, frame.copy()))
            try:
                while True:
                    result = outgoing.get_nowait()
                    if result[3] == mode:
                        latest_result = result
            except queue.Empty:
                pass

            # The webcam frame is always the live image. Never replay an old frame.
            preview = frame.copy()
            if latest_result is not None and mode and latest_result[3] == mode:
                for typ, name, conf, bbox in latest_result[4]:
                    x1, y1, x2, y2 = map(int, bbox)
                    color = ((255, 0, 0) if typ == 'CRACK' else
                             (0, 165, 255) if typ == 'ANOMALY' else
                             (0, 255, 255))
                    cv2.rectangle(preview, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(preview, str(name), (x1, max(20, y1-5)),
                                cv2.FONT_HERSHEY_SIMPLEX, .55, color, 2)
            cv2.putText(preview, f'{MODES[mode]} | 1 Patch 2 YOLO 3 Crack 4 Full 0 Pause q Quit',
                        (12, 30), cv2.FONT_HERSHEY_SIMPLEX, .55, (0, 255, 255), 2)
            cv2.imshow(window, preview)
            key = cv2.waitKey(1) & 0xff
            if key in (ord('0'), ord('1'), ord('2'), ord('3'), ord('4')):
                new_mode = int(chr(key))
                with mode_state['lock']:
                    mode_state['mode'] = new_mode
                    mode_state['generation'] += 1
                latest_result = None
                print('Selected:', MODES[new_mode], flush=True)
            elif key == ord('5'):
                if thermal.check(ord('1')):
                    print('SIMULATED thermal obstacle: exiting prototype', flush=True)
                    break
            elif key == ord('q'):
                break
    finally:
        stopping.set()
        cap.release()
        worker.join()
        cv2.destroyAllWindows()
        print('CSV:', CSV_PATH, flush=True)


if __name__ == '__main__':
    main()
