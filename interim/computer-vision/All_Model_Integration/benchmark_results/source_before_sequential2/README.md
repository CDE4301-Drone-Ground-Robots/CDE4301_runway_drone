# FOD ARGUS laptop benchmark — simulated coordinates and corrected routing

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

