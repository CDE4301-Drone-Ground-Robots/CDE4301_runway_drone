# Sequential 1 reporting-condition check: laptop benchmarking

Previous: YOLO then U-Net on every crop; every U-Net outcome prepares a Base message.
Revised: same inference and FOD coordinate/UGV processing; Base receives cracks or anomalies where neither model detects. FOD-positive/no-crack crops produce no Base message.

Same loaded models, same 30 preloaded RGB frames, batch 1, unchanged precision/input settings/thresholds, five excluded pipeline warmups per variant plus five excluded real-crop downstream warmups. Three paired passes; alternating within-pair order. No images dropped.
The processing interval includes cropping/resizing, normal transfers, model inference, postprocessing, simulated coordinate extraction and local JSON message preparation; CUDA synchronization brackets each complete frame. Model loading, file decoding, persistence and verification are outside timing. GPU event hooks match previous integrated timing.

| Condition | Unique frames | Observations | Mean ms | Median ms | P95 ms | Max ms | Processing frames/s | Base messages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| previous | 30 | 90 | 96.208 | 77.282 | 223.181 | 285.421 | 10.394 | 84 |
| revised | 30 | 90 | 93.647 | 77.508 | 222.942 | 264.401 | 10.678 | 72 |

Mean revised-versus-previous change: -2.662%. P95 change: -0.107%.
Paired image-group bootstrap 95% interval for mean change: [-5.540%, +0.367%].
Decision using a declared 5% practical margin: **inconclusive_due_to_timing_variation**.
The tolerance is an explicit practical choice. A confidence interval outside neither boundary does not prove the absence of smaller effects. All runs share a finite image set; background activity, clocks and thermal variation remain limitations.
Original historical Sequential 1 mean: 99.185 ms (10.082 frames/s). Historical results and other architecture results have been preserved; cross-session timing shifts should not be attributed to this condition alone.
All 84 protected original files verified unchanged. Standalone models and independent thermal tests were not rerun because their execution is unchanged.
No actual communication, GPS, camera sampling, Jetson performance or localisation accuracy is measured.
