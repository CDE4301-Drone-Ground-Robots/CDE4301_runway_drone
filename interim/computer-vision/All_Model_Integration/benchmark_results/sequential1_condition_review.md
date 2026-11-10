# Sequential 1 reporting-condition review: laptop benchmark

Retain the historical Sequential 1 comparison values (99.185 ms, 10.082 frames/s) as results of the original test, with a note that a paired laptop rerun found the reporting-condition revision within a declared 5% practical margin. The historical numbers are not exact measurements of the revised code.

| Condition | Unique RGB frames | Observations | Mean ms | Median ms | P95 ms | Max ms | Processing frames/s |
|---|---:|---:|---:|---:|---:|---:|---:|
| previous | 30 | 180 | 96.881 | 78.576 | 224.087 | 312.775 | 10.322 |
| revised | 30 | 180 | 94.844 | 78.256 | 220.951 | 305.629 | 10.544 |

Mean change: -2.103%. P95 change: -1.400%.
Paired image-group bootstrap 95% interval for mean change: [-3.142%, -0.933%].
Decision: **negligible_within_declared_5_percent_margin**. The 5% tolerance was declared before measuring and is a practical choice, not a universal benchmark standard.

Both conditions run YOLO then U-Net on every valid PatchCore anomaly crop. FOD coordinate extraction and UGV message preparation are identical. The previous condition prepares a Base message for every U-Net result. The revised condition prepares Base messages for cracks, or for no-FOD/no-crack anomalies; a FOD-positive/no-crack crop continues without a Base message.
Across six passes per condition: 168 YOLO calls, 168 U-Net calls, 108 coordinate extractions each. Base messages: previous 168, revised 144. No failures, skipped or unprocessed frames.
Same loaded models within each of two sessions; same 30 preloaded RGB inputs, unchanged weights, thresholds, resolutions and precision; batch size 1, evaluation and inference mode. Five excluded pipeline warmups per condition and five excluded real-crop warmups for each downstream model per session. Three paired passes per session; within-pair execution order alternates. The second session was added because the first uncertainty interval slightly exceeded the tolerance.
The full processing timer includes normal crop/resize/device transfer/model/postprocessing operations, simulated planar coordinate extraction and in-memory JSON message preparation. CUDA synchronization brackets each full frame. Model loading, decoding, persistence and validation are excluded. Model GPU timings use the existing nonblocking CUDA-event hooks.
Throughput is total completed frames divided by summed measured processing time. Unique images and repeated observations are distinct. Bootstrap resamples image groups, retaining all six repeated pairs for a selected image; the interval describes this finite workload and does not establish equivalence on arbitrary unseen imagery.
Mean measured message-preparation time per full frame: previous 0.089418 ms, revised 0.084849 ms. Full-frame timing differences cannot be attributed solely to this small CPU operation because run-to-run variation remains.
Historical comparison: Sequential 1 mean 99.185 ms (10.082 frames/s); Sequential 2 and Parallel historical results are untouched. The new old-condition control helps distinguish session variability from a routing revision.
All 84 original application/model/input files verified unchanged by SHA256. No dependencies, drivers, SDKs or device settings changed. Standalone models and thermal execution are unchanged and were not rerun.
No actual communication, camera acquisition, GPS accuracy, 5 mm detection, Jetson performance or detection accuracy is measured. Repeat on the final camera and Jetson, including actual message transport if it belongs in the required latency boundary.

Raw paired runs:
- [sequential1_condition_check_20261101T141724_645321Z](sequential1_condition_check_20261101T141724_645321Z/comparison.md) (raw_timings.csv, final_outputs.json, status.json, routing checks and old/new source snapshots in the same directory)
- [sequential1_condition_check_20261101T142135_859795Z](sequential1_condition_check_20261101T142135_859795Z/comparison.md) (raw_timings.csv, final_outputs.json, status.json, routing checks and old/new source snapshots in the same directory)
