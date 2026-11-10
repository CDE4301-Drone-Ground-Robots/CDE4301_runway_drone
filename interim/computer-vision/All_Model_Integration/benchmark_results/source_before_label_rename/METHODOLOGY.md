# FOD ARGUS laptop benchmarking — corrected architectures with simulated coordinates

This benchmark suite is separate from the application. Source application files, weights, input images, detections.csv, snapshots and existing settings/caches are preserved and hashed before/after. All script/output work is under benchmark_suite and benchmark_results. No packages, environments, drivers, CUDA Toolkit/SDK, power modes or GPU/CPU configuration are modified. YOLO settings are redirected into benchmark_results before Ultralytics imports.

## Definitive routing supplied on 31 October 2026

Every complete RGB frame goes through the existing PatchCore detector. No anomaly regions means continue inspection: no YOLO, U-Net, coordinates or messages. Every valid anomaly ROI is cropped and normally zoomed to 1280 x 720.

Sequential fallback:
1. Run YOLO on the ROI.
2. If YOLO returns any FOD detections, extract simulated coordinates for every detection and prepare UGV messages. Skip U-Net for that ROI.
3. If YOLO returns no FOD, run U-Net on the same ROI.
4. Prepare a Base message for a crack, or an unclassified anomaly if no crack. Continue inspection.

Parallel:
1. A persistent ThreadPoolExecutor uses two workers and, on CUDA, one persistent stream per downstream model.
2. YOLO and U-Net inspect the same ROI concurrently; each worker enters inference mode.
3. The YOLO branch calculates coordinates and prepares UGV messages whenever it finds FOD; this host computation can overlap with the U-Net branch.
4. A detected crack prepares a Base message, including when FOD is also present. Neither FOD nor crack prepares one unclassified-anomaly Base message.
5. Wait for both branches before the next ROI. Frames and ROIs are losslessly processed in order.

These architectures have different routing and workloads: sequential can skip U-Net. Their comparison is not a pure measurement of concurrency speedup. The original Integration.py calls both detectors sequentially for every ROI; it is left unchanged. Integration_1.py is an older camera entry point importing a missing detect_anomaly function and is not imported.

## Coordinate simulation

Use the supplied worked example: UAV position (3,4) metres, assumed full-frame ground footprint 2 x 2 metres, nominal 5 m AGL. Flat nadir view, zero attitude/rotation, world +X=image-right and +Y=image-down are assumed. These are simulated inputs, not calibrated camera coverage, GPS or physical localisation.

Map each detector's returned box from the normal 1280 x 720 zoom to the actual ROI, add the ROI origin, round mapped endpoints, compute the box centre and its offset from actual source-frame centre, multiply by 2/source_width and 2/source_height, and add (3,4). The formula uses each source image's actual dimensions. It does not resize source images to 1280 x 720.

Important: the existing U-Net wrapper restores raw 512 x 512 segmentation to its supplied image size; its returned box already uses 1280 x 720 coordinates. Never apply a second 512-to-ROI conversion to that returned box. World coordinate extraction is applied to FOD detections only, as shown in the final diagrams. Cracks and residual anomalies go to Base.

Four math checks include the provided raw-512 example: original box (500,280,560,400), centre (530,340), world coordinate (2.828125,3.9444444444) m. Ten routing checks use fake detector returns solely for correctness; fake outputs are never benchmark workloads.

Coordinate_extraction_ms measures the real CPU computation performed with simulated geometry, not an arbitrary delay. Each architecture row records its coordinate_count and total coordinate time; frames with no FOD have zero coordinate calls. A separate coordinate benchmark uses real YOLO bounding boxes generated from real PatchCore crops. It reports latency per detection, distinct from latency per full frame.

"Send" means in-memory message creation and JSON serialization only. No sockets, network transmissions, receiving UGV/Base, radio delay, GPS sampling or artificial sleep is used. Message_preparation_ms is separate from coordinate math, while both are included in pipeline total_ms.

## Models and input validation

Use the existing fod_synthetic environment. All needed dependencies, including the previously approved HEIC decoder, were already present; nothing is installed in this redo.
- PatchCore: Anomaly_model.ckpt; wide_resnet50_2 layer2/layer3, float32, memory bank from checkpoint, 256 x 256 RGB/ImageNet-normalized preprocessing, checkpoint postprocessor. Runtime threshold .05, percentile 95, minimum region area 80, padding 20 and 5 x 5 close, unchanged.
- FOD YOLO: FOD_yolo11s.pt, confidence .30, normal checkpoint/Ultralytics settings unchanged. Record actual predictor arguments and tensor shapes; the supplied checkpoint normally overrides imgsz to 1024.
- U-Net: best_crack_model.pth, ResNet34 encoder, 512 x 512, sigmoid threshold >.50, existing RGB/ImageNet normalization and nearest-neighbor mask restoration.
- Thermal: supplied Thermal_yolo11s.pt person/bird weights; prior user-approved standalone settings conf .25, IoU .70, imgsz 640, float32, batch 1. Application Thermal_Detection.py is a keyboard bypass and has no real thermal image inference/scheduling.

Decode every one of the 30 RGB and 30 thermal inputs, record dimensions/dtypes/decoder/errors and SHA-256. HEIC is decoded to RGB then BGR in memory, respecting decoder orientation; no source conversion or overwrite. Per-configuration preflight stops on unreadable inputs rather than silently omitting them.

## Independent continuous thermal workload

Thermal is benchmarked separately from the RGB architectures and without inventing RGB/thermal pairs.
- thermal_sampling: finite unpaced replay of all 30 thermal files, timing file read plus decoding. Five initial reads warm up the decoder; OS file caches affect these results. This is file sampling/loading throughput, NOT measured camera sampling rate.
- thermal: all 30 decoded thermal frames are preloaded outside timing, then inferred in an unpaced finite replay loop with the model loaded throughout. Record detector latency and model-forward latency separately.
- First run one pass; if practical, replay three passes (90 observations, 30 unique images). These finite tests represent repeated independent processing, not a live sensor, an endless background service or a simultaneous shared-resource integration test. Do not add sampling/inference latencies and label the sum live camera latency.

## Timing and reproducibility

One configuration at a time in a fresh process. Batch 1, evaluation/inference mode, fixed existing precision/device/input settings. Five warm-up passes are excluded. Architecture warmup includes additional five real-crop calls to each downstream detector, including detectors skipped by the first frame's routing. This avoids cold first U-Net calls in a later fallback frame.

Individual model boundary: already-decoded full frame (PatchCore/thermal) or representative real anomaly crop after the normal 1280 x 720 zoom (YOLO/U-Net), to final usable detector output. Model loading, disk decoding, crop generation/initial zoom, GUI, plotting, image/CSV/JSON saving are excluded. Internal resizing, normalization/transfers and detector postprocessing remain included.

Isolated forward hooks synchronize CUDA before/after model forward and use CUDA events for model-only time. CPU preprocessing and postprocessing wall intervals are reported separately. Model event time and CPU segment times may differ slightly from detector total due to dispatch/synchronization instrumentation overhead.

Integrated boundary: already-decoded complete RGB frame to final usable simulated Base/UGV messages. Includes PatchCore, ROI cropping/zoom, transfers, model execution, postprocessing, FOD coordinate math and local message preparation. CUDA synchronization occurs at outer frame boundaries only; forward events do not synchronize model branches. GPU kernel overlap is not independently traced; workers/streams do not prove overlap or guaranteed speedup. Never sum isolated timings or overlapping model event durations to obtain pipeline latency.

Per-model *_preprocessing_host_ms and *_postprocessing_host_ms in architecture rows describe host intervals around forward dispatch; async GPU work can overlap and these are not GPU-separated stage totals. crop_resize_host_ms and output_merge_host_ms record additional CPU work. Coordinate timing may overlap with U-Net in parallel mode, so do not add its duration to measured total_ms.

Raw rows, outputs and memory are persisted outside processing timers. Stop a configuration at its first error/timeout, preserve partial rows, record completed/failed/unprocessed samples, and continue successful independent configurations. No resolution, precision, thresholds or model replacements are silently introduced.

Summary statistics: unique inputs, unique source frames, measured observations, mean/median/p95/max latency and throughput = completed inputs / sum of measured processing seconds. Unit is frame for RGB/thermal, crop for isolated YOLO/U-Net, and detection for coordinate-only math. Keep initial one-pass and subsequent three-pass results separate. Coordinate count, YOLO calls and U-Net calls make the distinct branch workloads explicit.

Memory: record process RSS samples, system available RAM and CUDA allocated/reserved/peak allocator memory where available. GPU peaks reset after warmup. These are not total GPU driver/display memory or a true process RSS peak. Model-loading/autotuning peaks can exceed steady-state measured peaks. Capture machine, package versions, driver, tensor dtype/shape/device, backend flags and model configuration in JSON.

## Reporting limits

Laptop processing throughput only. No Jetson performance, final camera sampling rate, live capture-to-output latency, validated 5 mm detection, physical localisation accuracy or full detection accuracy claims. Coordinate simulation times arithmetic with assumed geometry; it does not validate navigation or coordinate accuracy. Confirm training preprocessing/calibration from HPC records independently.

Repeat on the final camera/Jetson using actual capture, telemetry synchronization, calibration/attitude, sustained power/thermal conditions and real communications. Validate detection/localisation separately against labelled ground truth. Then test meaningful RGB+thermal shared-resource scheduling on the actual implementation.


## Added Sequential 2

Sequential 2 follows the additional diagram: YOLO runs first, every FOD detection gets simulated world coordinates and a local UGV message, then U-Net runs on every ROI regardless of YOLO's result. Every U-Net outcome prepares a Base message, including NO_CRACK_DETECTED. No real transmission is performed.

Run only this extension while retaining the earlier two architecture results:

    & 'C:\Users\Chara\miniconda3\envs\fod_synthetic\python.exe' -B benchmark_suite/run_sequential2.py

It validates unchanged inputs/models/settings/environment, runs routing checks and a real Sequential 2 smoke test, then one measured pass and a practical three-pass run using the same 30 RGB images. Batch 1, five initial warmups plus the same downstream warmup policy, precision/device and timing boundaries are unchanged.

Individual invocation:

    & 'C:\Users\Chara\miniconda3\envs\fod_synthetic\python.exe' -B benchmark_suite/core.py --config sequential2 --repeats 3

The three-way collation is architecture_comparison.csv / architecture_comparison.md in benchmark_results.
The first two architectures retain their earlier sessions; Sequential 2 is a later session, not a simultaneous/back-to-back rerun. Session timestamps, model calls, coordinate calls, memory and failures are retained. OS/background-load drift limits strict cross-session ranking.

Sequential 1 skips U-Net on FOD-positive crops; Sequential 2 and Parallel run it on every crop. Sequential 2 also sends negative U-Net outcomes to Base even if FOD was found, whereas Parallel sends Base messages for cracks and neither-detected anomalies. Thus neural workloads and message workloads must both be considered.

