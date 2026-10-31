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
