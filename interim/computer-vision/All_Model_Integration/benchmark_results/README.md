# FOD ARGUS laptop benchmark — simulated coordinates and corrected routing

Display-label convention (renamed without rerunning inference):
- Sequential 1 runs YOLO then U-Net on every crop; legacy configuration ID: sequential2.
- Sequential 2 skips U-Net when YOLO detects FOD; legacy configuration ID: sequential.
- Parallel runs both concurrently; configuration ID: parallel.
Historical filenames, raw configuration IDs and measured values are retained unchanged.


All work remains in this project. Original integration files, models and source images are preserved.
Scripts: benchmark_suite. Results: benchmark_results.
No new packages or CPU/GPU/driver/SDK/environment changes are required.

From PowerShell in All_Model_Integration, run the complete suite with the existing environment:

    & 'C:\Users\Chara\miniconda3\envs\fod_synthetic\python.exe' -B benchmark_suite/run_all.py

The runner performs inventory, real-model/architecture smoke tests, real crop generation, then one measured pass of each configuration followed by three passes if successful/practical. It runs one configuration at a time in fresh processes. Five warmups are excluded; architecture tests additionally warm downstream models on a real crop so skipped stages are not cold when reached later.

Run individual configurations (change the --config value):

    & 'C:\Users\Chara\miniconda3\envs\fod_synthetic\python.exe' -B benchmark_suite/core.py --config inventory
    & 'C:\Users\Chara\miniconda3\envs\fod_synthetic\python.exe' -B benchmark_suite/routing_checks.py
    & 'C:\Users\Chara\miniconda3\envs\fod_synthetic\python.exe' -B benchmark_suite/core.py --config smoke
    & 'C:\Users\Chara\miniconda3\envs\fod_synthetic\python.exe' -B benchmark_suite/core.py --config crops

Other configs: patchcore, fod, crack, coordinates, thermal_sampling, thermal, sequential, parallel.
Add --repeats 3 for three measured passes over the same unique inputs. Defaults are one pass, batch one and five warmups.

Run crops before fod/crack and architecture configs. Run fod before coordinates: its actual detections generate coordinate_workload.json. If no suitable crops/detections exist, the dependent configuration stops and asks how to proceed; it does not silently substitute synthetic or full-frame workloads.

Regenerate summaries and the final report:

    & 'C:\Users\Chara\miniconda3\envs\fod_synthetic\python.exe' -B benchmark_suite/core.py --config report
    & 'C:\Users\Chara\miniconda3\envs\fod_synthetic\python.exe' -B benchmark_suite/finalize.py

Sequential: after YOLO detects FOD, compute coordinates and SKIP U-Net for that ROI. Otherwise run U-Net and send a simulated Base result.
Parallel: both models run on every valid ROI; FOD goes through coordinate extraction to simulated UGV, cracks to simulated Base, and neither-detected anomalies to simulated Base.
These architectures have different workloads; their timing difference is not solely caused by concurrency.

simulation.json records the assumed UAV position (3,4) m and 2 x 2 m coverage used in the supplied worked example. World +X is image-right, +Y is image-down; zero rotation/flat ground is assumed. Source dimensions are used for pixel scales. This is arithmetic with simulated geometry, not measured physical localisation.

Only FOD has world-coordinate extraction, following the final diagrams. U-Net boxes returned by the existing wrapper are already in zoomed-image coordinates. Do not apply a second raw-512 scale.
Base/UGV messages are local JSON payloads only, with no radio/network/socket/GPS operations or invented delays.

thermal_sampling measures file read/decode only. thermal measures inference on preloaded thermal frames, separately from RGB. Finite unpaced replay (30 unique files, 90 observations for three passes) represents repeat processing; it does not measure camera capture/sampling rate or keep a background service running.

Results:
- summary.csv / summary.md: every initial and repeated timing run; latency statistics and observed throughput.
- results_and_limitations.md: report-ready comparison, routing workload counts and limitations.
- methodology.md / simulation_settings.json / machine_software_settings.json: timing boundaries and complete setup.
- input_manifest.csv / crop_manifest.csv / coordinate_workload.json: actual workloads.
- original_file_integrity.json / coverage_validation.json / routing_validation.json: preservation and completeness.
- coordinate_math_test.json / routing_checks.json: correctness tests; mock outputs are not timing samples.
- Timestamped run folders: raw_timings.csv, status.json, model_settings.json and architecture final_outputs.json.
- *_passes_*.log: configuration logs and errors.

Do not compare per-crop or per-detection throughput with full-frame pipeline throughput. Sampling/loading rates from files are not camera sampling rates. All results are laptop benchmarking only.


## Added Sequential 1

Sequential 1 follows the additional diagram: YOLO runs first, every FOD detection gets simulated world coordinates and a local UGV message, then U-Net runs on every ROI regardless of YOLO's result. Every U-Net outcome prepares a Base message, including NO_CRACK_DETECTED. No real transmission is performed.

Run only this extension while retaining the earlier two architecture results:

    & 'C:\Users\Chara\miniconda3\envs\fod_synthetic\python.exe' -B benchmark_suite/run_sequential2.py

It validates unchanged inputs/models/settings/environment, runs routing checks and a real Sequential 1 smoke test, then one measured pass and a practical three-pass run using the same 30 RGB images. Batch 1, five initial warmups plus the same downstream warmup policy, precision/device and timing boundaries are unchanged.

Individual invocation:

    & 'C:\Users\Chara\miniconda3\envs\fod_synthetic\python.exe' -B benchmark_suite/core.py --config sequential2 --repeats 3

The three-way collation is architecture_comparison.csv / architecture_comparison.md in benchmark_results.
The first two architectures retain their earlier sessions; Sequential 1 is a later session, not a simultaneous/back-to-back rerun. Session timestamps, model calls, coordinate calls, memory and failures are retained. OS/background-load drift limits strict cross-session ranking.

Sequential 2 skips U-Net on FOD-positive crops; Sequential 1 and Parallel run it on every crop. Sequential 1 also sends negative U-Net outcomes to Base even if FOD was found, whereas Parallel sends Base messages for cracks and neither-detected anomalies. Thus neural workloads and message workloads must both be considered.

