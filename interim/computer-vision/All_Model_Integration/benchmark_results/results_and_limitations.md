# FOD ARGUS laptop results: corrected architectures and simulated coordinates

Hardware: AMD Ryzen 9 7845HX with Radeon Graphics; 15.21 GiB RAM; NVIDIA GeForce RTX 4060 Laptop GPU. CUDA available: True.
Python: C:\Users\Chara\miniconda3\envs\fod_synthetic\python.exe; PyTorch 2.11.0+cu128, CUDA build 12.8.
No dependencies, environments, CPU/GPU settings, drivers or SDKs were changed for this redo.

Sequential fallback skips U-Net when YOLO detects FOD. Sequential 1 runs YOLO then U-Net on every crop and sends every U-Net outcome to Base. Parallel runs both models concurrently on every crop.
The existing fallback/parallel measurements were retained; Sequential 1 was measured in a later session. Background-load drift limits strict cross-session ranking.
This routing difference means the comparison is between two architectures with different workloads, rather than an isolated concurrency speedup.
The original integration/model/input files remain untouched. The architectures are implemented only in benchmark_suite.

Validation:
- Preserved files unchanged: 84/84.
- Complete input-per-pass coverage checks: 37/37.
- Detailed architecture routing/call-count checks: passed.
- Four coordinate-math checks and fifteen routing-unit checks are recorded separately; mocks were used only for correctness checks, never timing samples.

RGB: 30 input files; dimensions/counts {'300 x 300': 10, '512 x 512': 10, '3024 x 4032': 10}; unreadable 0.
Thermal: 30 input files; dimensions/counts {'1280 x 1024': 15, '640 x 480': 15}; unreadable 0.
PatchCore generated 28 valid crops across 16 unique RGB images. The other 14 images produced no crops.
The isolated downstream tests use those real crops, zoomed by the normal 1280 x 720 preprocessing path. No full-frame substitution is made.

The following table selects the latest run of each configuration. Initial one-pass runs are retained separately in summary.csv.
A three-pass RGB/thermal run is 90 observations from 30 unique images; repeated observations are not additional unique inputs.

| Configuration | Unique inputs | Source frames | Observations | Mean ms | Median ms | P95 ms | Max ms | Throughput/s | Unit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| patchcore | 30 | 30 | 90 | 29.891 | 25.933 | 45.004 | 49.215 | 33.455 | frame |
| fod | 28 | 16 | 84 | 32.135 | 25.681 | 51.366 | 53.099 | 31.119 | crop |
| crack | 28 | 16 | 84 | 32.169 | 33.352 | 34.560 | 36.020 | 31.086 | crop |
| coordinates | 18 | 15 | 54 | 0.021211 | 0.021200 | 0.024025 | 0.026200 | 47145.100143 | detection |
| thermal_sampling | 30 | 30 | 90 | 4.082 | 4.259 | 7.345 | 7.719 | 244.998 | frame |
| thermal | 30 | 30 | 90 | 30.337 | 22.657 | 47.473 | 151.366 | 32.963 | frame |
| Sequential 2 (skips crack on FOD detection) | 30 | 30 | 90 | 72.870 | 59.338 | 174.765 | 222.852 | 13.723 | frame |
| Sequential 1 (runs both models) | 30 | 30 | 90 | 99.185 | 80.431 | 234.196 | 306.702 | 10.082 | frame |
| Parallel | 30 | 30 | 90 | 87.342 | 72.356 | 189.063 | 236.972 | 11.449 | frame |

Processing throughput = completed observations / sum of directly measured processing seconds.
Crop and coordinate/detection throughput are not full-frame throughput. Pipeline totals are measured directly, not estimated by adding isolated model times.

| Architecture | YOLO crop calls | U-Net crop calls | Coordinate calls | Mean coordinate ms/frame | Mean coordinate ms/detection |
|---|---:|---:|---:|---:|---:|
| Sequential 1 (runs both models) | 84 | 84 | 54 | 0.017153 | 0.028589 |
| Sequential 2 (skips crack on FOD detection) | 84 | 30 | 54 | 0.016340 | 0.027233 |
| Parallel | 84 | 84 | 54 | 0.016463 | 0.027439 |

Coordinate extraction uses the supplied simulated UAV position (3,4) m and assumed 2 x 2 m footprint at nominal 5 m AGL.
Each actual FOD box is mapped from the normal zoomed image into its source ROI/frame; the pixel centre/offset is scaled using actual frame dimensions and added to the simulated UAV position.
The provided example produces centre (530,340) px and world (2.828125,3.9444444444) m. This verifies arithmetic only, not physical localisation.
No navigation sensor, camera calibration, yaw/roll/pitch, GPS synchronization or physical ground-truth accuracy is measured.
Only FOD detections trigger world-coordinate calculation, as in the final diagrams. Crack/residual-anomaly messages go to Base.
Simulated message preparation creates local JSON payloads only. Its CPU cost and coordinate math are included inside the measured pipeline boundary; no network messages, transmission delays or sleeps are introduced.
Coordinate math may overlap U-Net in parallel mode. Do not add coordinate time onto the already-inclusive pipeline total.

| Isolated model | Forward mean ms | Forward median ms | Forward P95 ms | Forward max ms |
|---|---:|---:|---:|---:|
| patchcore | 18.863 | 17.571 | 24.479 | 25.059 |
| fod | 23.752 | 17.698 | 39.877 | 41.076 |
| crack | 18.576 | 19.746 | 20.686 | 21.027 |
| thermal | 25.694 | 18.118 | 40.289 | 147.221 |

Thermal runs independently as finite unpaced replay cycles, with sampling/loading and inference benchmarked separately.
thermal_sampling times file read plus image decoding only; thermal times inference from preloaded images with the model kept loaded. File caches influence loading results.
These are not real camera sampling rates or live capture-to-output latency, and no simultaneous RGB/thermal scheduling or paired observations are claimed.
The application thermal file remains a keyboard bypass. The previously approved standalone thermal weights configuration is conf .25, IoU .70, imgsz 640, float32, batch 1.

| Configuration | Status | Failures | Unprocessed | Measured CUDA peak MiB | Sampled RSS MiB |
|---|---|---:|---:|---:|---:|
| patchcore | completed | 0 | 0 | 182.959 | 2433.375 |
| fod | completed | 0 | 0 | 128.853 | 1763.504 |
| crack | completed | 0 | 0 | 193.016 | 1497.227 |
| coordinates | completed | 0 | 0 | 0.000 | 508.930 |
| thermal_sampling | completed | 0 | 0 | 0.000 | 513.062 |
| thermal | completed | 0 | 0 | 101.747 | 1430.777 |
| Sequential 2 (skips crack on FOD detection) | completed | 0 | 0 | 391.664 | 2314.301 |
| Parallel | completed | 0 | 0 | 532.440 | 2537.668 |
| Sequential 1 (runs both models) | completed | 0 | 0 | 391.665 | 2517.500 |

Minimum sampled available system RAM: 581.0 MiB.
CUDA peaks cover measured passes after warmup and exclude driver/display/other processes. Initialization/autotuning can require substantially more VRAM. RSS is sampled, not a true process peak.
Background load, CPU/GPU clocks/temperature, OS caches and algorithm choices were not isolated. Short coordinate timings include timer/function overhead and should not be interpreted as deployment guarantees.
Weights, thresholds, resolutions and tensor precision were preserved. Backend settings, actual predictor arguments, tensor shapes/dtypes and checkpoint model metadata are saved per run.

Successfully completed/failed configurations and partial observations are explicitly recorded above and in status.json; see logs for failures.
These measurements do not establish Jetson performance, real capture/sampling rate, live latency, 5 mm detection, localisation accuracy or full detection accuracy.
When the final camera and Jetson arrive, repeat model and end-to-end timing under sustained power/thermal conditions, using real capture/telemetry and calibrated geometry, real thermal scheduling and real communications. Validate accuracy/localisation independently with labelled physical ground truth.

See methodology.md for timing boundaries, README.md for commands, raw_timings.csv for every run, final_outputs.json for simulated pipeline outputs, and the preservation/coverage/routing JSON files for verification.


# Three-architecture laptop comparison

Sequential 2 and Parallel retain their earlier measured runs. Sequential 1 was measured subsequently.
All use the same input files, weights, thresholds, precision and simulated coordinate settings; cross-session background load remains a limitation.

| Architecture | Unique RGB | Observations | Mean ms | Median ms | P95 ms | Max ms | Processing frames/s | YOLO calls | U-Net calls | Coordinate calls | Base messages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sequential 1 (runs both models) | 30 | 90 | 99.185 | 80.431 | 234.196 | 306.702 | 10.082 | 84 | 84 | 54 | 84 |
| Sequential 2 (skips crack on FOD detection) | 30 | 90 | 72.870 | 59.338 | 174.765 | 222.852 | 13.723 | 84 | 30 | 54 | 30 |
| Parallel | 30 | 90 | 87.342 | 72.356 | 189.063 | 236.972 | 11.449 | 84 | 84 | 54 | 72 |

Sequential 2: YOLO first; skip U-Net on FOD-positive crops. FOD -> simulated UGV coordinates; fallback outcomes -> Base.
Sequential 1: YOLO first and U-Net next on every crop. FOD -> simulated UGV coordinates; every U-Net outcome -> Base, including no-crack outcomes.
Parallel: YOLO and U-Net concurrently on every crop. FOD -> simulated UGV coordinates; cracks or neither-detected anomalies -> Base.

Sequential 2 has less neural inference work. Sequential 1 and Parallel have equal model-call counts but differ in message routing and scheduling; results are not a perfectly isolated concurrency experiment.
Coordinates are planar arithmetic with simulated position/coverage; messages are local JSON only. No camera, GPS, network or Jetson performance is measured.
Full statistics, memory, failures and source run/session identifiers are in architecture_comparison.csv. Raw observations remain in each timestamped run directory.
