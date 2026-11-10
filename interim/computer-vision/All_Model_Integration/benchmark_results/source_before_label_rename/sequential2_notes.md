
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

