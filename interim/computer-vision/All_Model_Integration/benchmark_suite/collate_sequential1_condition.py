"""Collate the two condition checks without overwriting historical benchmark results."""
from pathlib import Path
import csv,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'benchmark_results'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
runs=sorted(p for p in OUT.glob('sequential1_condition_check_*') if p.is_dir() and (p/'status.json').exists())
assert len(runs)==2, 'Expected exactly the original paired check plus one confirmation run'
assert all(read(p/'status.json')['status']=='completed' for p in runs)
rows=[]
for p in runs:
    with (p/'raw_timings.csv').open(newline='',encoding='utf-8') as f:
        rows.extend(dict(r,session=p.name) for r in csv.DictReader(f))
variants=('previous','revised');keys=sorted(set(r['input'] for r in rows));assert len(keys)==30
summary={}
for variant in variants:
    rr=[r for r in rows if r['variant']==variant]
    assert len(rr)==180 and all(r['status']=='ok' for r in rr)
    a=np.array([float(r['total_ms']) for r in rr])
    summary[variant]=dict(unique_inputs=30,measured_observations=len(a),mean_ms=float(a.mean()),
        median_ms=float(np.median(a)),p95_ms=float(np.percentile(a,95)),max_ms=float(a.max()),
        processing_frames_per_s=float(len(a)/a.sum()*1000),failures=0,unprocessed=0,
        peak_cuda_allocated_bytes=max(int(r['cuda_peak_allocated_bytes']) for r in rr),
        max_rss_bytes=max(int(r['rss_bytes']) for r in rr),
        message_preparation_mean_ms=float(np.mean([float(r['message_preparation_ms']) for r in rr])),
        **{k:sum(int(r[k]) for r in rr) for k in ('crop_count','fod_calls','crack_calls','coordinate_count','base_message_count','ugv_message_count')})
groups={v:np.array([np.mean([float(r['total_ms']) for r in rows if r['variant']==v and r['input']==k]) for k in keys]) for v in variants}
rng=np.random.default_rng(4301);ix=rng.integers(0,30,size=(20000,30))
deltas=(groups['revised'][ix].mean(axis=1)/groups['previous'][ix].mean(axis=1)-1)*100
ci=np.percentile(deltas,[2.5,97.5]).tolist()
a,b=summary['previous'],summary['revised'];delta=(b['mean_ms']/a['mean_ms']-1)*100
p95_delta=(b['p95_ms']/a['p95_ms']-1)*100
if ci[0]>-5 and ci[1]<5:
    decision='negligible_within_declared_5_percent_margin'
    recommendation='Retain the historical Sequential 1 comparison values (99.185 ms, 10.082 frames/s) as results of the original test, with a note that a paired laptop rerun found the reporting-condition revision within a declared 5% practical margin. The historical numbers are not exact measurements of the revised code.'
elif ci[0]>5 or ci[1]<-5:
    decision='material_difference'
    recommendation='Use the new revised-condition measurements when reporting revised Sequential 1; keep the historical values labelled as the previous condition. Other architecture results come from earlier sessions, so a new cross-architecture ranking would require a common-session rerun.'
else:
    decision='inconclusive_due_to_timing_variation'
    recommendation='The observed change is small but equivalence within 5% was not established. Report the revised-condition measurements directly for the revised architecture; retain the historical values only as the original implementation measurements.'
originals=read(OUT/'preservation_baseline.json')
changed=[]
for name,h in originals.items():
    p=ROOT/name
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:changed.append(name)
assert not changed
result=dict(label='Laptop benchmarking only',runs=[p.name for p in runs],configurations=summary,
    mean_change_percent=delta,p95_change_percent=p95_delta,paired_image_group_bootstrap_95_percent_interval=ci,
    declared_practical_margin_percent=5,decision=decision,recommendation=recommendation,
    original_files_verified=len(originals),original_files_changed=changed,
    limitations=['No actual radio/network transport','No camera sampling or capture-to-output latency',
        'No Jetson, localisation or accuracy claim','Same finite 30-image workload repeated; clocks and background activity uncontrolled'])
(OUT/'sequential1_condition_review.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
with (OUT/'sequential1_condition_review.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['condition']+list(a));w.writeheader()
    for v,s in summary.items():w.writerow(dict(condition=v,**s))
md=['# Sequential 1 reporting-condition review: laptop benchmark','',recommendation,'',
    '| Condition | Unique RGB frames | Observations | Mean ms | Median ms | P95 ms | Max ms | Processing frames/s |',
    '|---|---:|---:|---:|---:|---:|---:|---:|']
for v,s in summary.items():md.append(f"| {v} | 30 | {s['measured_observations']} | {s['mean_ms']:.3f} | {s['median_ms']:.3f} | {s['p95_ms']:.3f} | {s['max_ms']:.3f} | {s['processing_frames_per_s']:.3f} |")
md+=['',f'Mean change: {delta:+.3f}%. P95 change: {p95_delta:+.3f}%.',
    f'Paired image-group bootstrap 95% interval for mean change: [{ci[0]:+.3f}%, {ci[1]:+.3f}%].',
    f'Decision: **{decision}**. The 5% tolerance was declared before measuring and is a practical choice, not a universal benchmark standard.','',
    'Both conditions run YOLO then U-Net on every valid PatchCore anomaly crop. FOD coordinate extraction and UGV message preparation are identical. The previous condition prepares a Base message for every U-Net result. The revised condition prepares Base messages for cracks, or for no-FOD/no-crack anomalies; a FOD-positive/no-crack crop continues without a Base message.',
    f"Across six passes per condition: {a['fod_calls']} YOLO calls, {a['crack_calls']} U-Net calls, {a['coordinate_count']} coordinate extractions each. Base messages: previous {a['base_message_count']}, revised {b['base_message_count']}. No failures, skipped or unprocessed frames.",
    'Same loaded models within each of two sessions; same 30 preloaded RGB inputs, unchanged weights, thresholds, resolutions and precision; batch size 1, evaluation and inference mode. Five excluded pipeline warmups per condition and five excluded real-crop warmups for each downstream model per session. Three paired passes per session; within-pair execution order alternates. The second session was added because the first uncertainty interval slightly exceeded the tolerance.',
    'The full processing timer includes normal crop/resize/device transfer/model/postprocessing operations, simulated planar coordinate extraction and in-memory JSON message preparation. CUDA synchronization brackets each full frame. Model loading, decoding, persistence and validation are excluded. Model GPU timings use the existing nonblocking CUDA-event hooks.',
    'Throughput is total completed frames divided by summed measured processing time. Unique images and repeated observations are distinct. Bootstrap resamples image groups, retaining all six repeated pairs for a selected image; the interval describes this finite workload and does not establish equivalence on arbitrary unseen imagery.',
    f"Mean measured message-preparation time per full frame: previous {a['message_preparation_mean_ms']:.6f} ms, revised {b['message_preparation_mean_ms']:.6f} ms. Full-frame timing differences cannot be attributed solely to this small CPU operation because run-to-run variation remains.",
    'Historical comparison: Sequential 1 mean 99.185 ms (10.082 frames/s); Sequential 2 and Parallel historical results are untouched. The new old-condition control helps distinguish session variability from a routing revision.',
    f'All {len(originals)} original application/model/input files verified unchanged by SHA256. No dependencies, drivers, SDKs or device settings changed. Standalone models and thermal execution are unchanged and were not rerun.',
    'No actual communication, camera acquisition, GPS accuracy, 5 mm detection, Jetson performance or detection accuracy is measured. Repeat on the final camera and Jetson, including actual message transport if it belongs in the required latency boundary.','',
    'Raw paired runs:']
for p in runs:md.append(f'- [{p.name}]({p.name}/comparison.md) (raw_timings.csv, final_outputs.json, status.json, routing checks and old/new source snapshots in the same directory)')
(OUT/'sequential1_condition_review.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))