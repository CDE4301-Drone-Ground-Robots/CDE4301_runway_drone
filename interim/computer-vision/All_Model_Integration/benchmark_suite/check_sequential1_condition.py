"""Paired laptop benchmark of Sequential 1 reporting-condition revision.
New files only. Existing benchmark sources, reports, models and inputs remain intact.
"""
from pathlib import Path
import csv, hashlib, importlib.metadata, inspect, json, re, sys, time, traceback
from datetime import datetime, timezone
import core
import numpy as np
import torch

ROOT=core.ROOT
STAMP=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
OUT=core.OUT/('sequential1_condition_check_'+STAMP)
OUT.mkdir()
OLD=core.pipeline
source=inspect.getsource(OLD)
old_branch='''        elif sequential2:
            details["no_crack_base_crops"]+=1
            if not fod_records:details["neither_detected_crops"]+=1
            records.append(pack_message("NO_CRACK_DETECTED","BASE",
                dict(roi=roi,fod_detected=bool(fod_records))))
'''
new_branch='''        elif sequential2 and not fod_records:
            details["no_crack_base_crops"]+=1
            details["neither_detected_crops"]+=1
            records.append(pack_message("UNCLASSIFIED_ANOMALY","BASE",dict(roi=roi)))
'''
assert source.count(old_branch)==1, 'Expected previous routing source changed; stop for review'
namespace=dict(vars(core))
revised_source=source.replace(old_branch,new_branch)
exec(compile(revised_source,str(OUT/'revised_pipeline.py'),'exec'),namespace)
NEW=namespace['pipeline']
(OUT/'previous_pipeline.py').write_text(source,encoding='utf-8')
(OUT/'revised_pipeline.py').write_text(revised_source,encoding='utf-8')

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(name,value):core.write_json(OUT/name,value)
def stats(rows):
    a=np.array([r['total_ms'] for r in rows],dtype=float)
    return dict(unique_inputs=len(set(r['input'] for r in rows)),observations=len(a),
        mean_ms=float(a.mean()),median_ms=float(np.median(a)),p95_ms=float(np.percentile(a,95)),
        max_ms=float(a.max()),processing_frames_per_s=float(len(a)/(a.sum()/1000)),
        crop_count=sum(r['crop_count'] for r in rows),fod_calls=sum(r['fod_calls'] for r in rows),
        crack_calls=sum(r['crack_calls'] for r in rows),coordinate_count=sum(r['coordinate_count'] for r in rows),
        base_messages=sum(r['base_message_count'] for r in rows),ugv_messages=sum(r['ugv_message_count'] for r in rows),
        peak_cuda_allocated_bytes=max(r.get('cuda_peak_allocated_bytes',0) for r in rows),
        max_rss_bytes=max(r['rss_bytes'] for r in rows),failures=0,unprocessed=90-len(a))

class Stub:
    def __init__(self,name,result,events):self.name=name;self.result=result;self.events=events
    def detect(self,frame):self.events.append(self.name);return self.result

def logic_checks():
    checks=[]
    for anomaly in (True,False):
        for fod,crack in ((True,True),(True,False),(False,True),(False,False)):
            events=[]
            models=dict(patchcore=Stub('patchcore',dict(boxes=[(0,0,8,8)] if anomaly else []),events),
                fod=Stub('fod',[dict(object='test',confidence=.9,bbox=(0,0,1280,720))] if fod else [],events),
                crack=Stub('crack',dict(bbox=(0,0,1280,720)) if crack else None,events))
            records,d=NEW(np.zeros((8,8,3),dtype=np.uint8),models,sequential2=True)
            assert events==(['patchcore','fod','crack'] if anomaly else ['patchcore'])
            assert d['base_message_count']==int(anomaly and (crack or not fod))
            assert d['ugv_message_count']==int(anomaly and fod)
            assert d['crack_calls']==int(anomaly)
            checks.append(dict(anomaly=anomaly,fod=fod,crack=crack,status='passed',routing=d))
    save('routing_checks.json',checks)

rows=[];outputs=[];probes={};state=dict(status='running',completed=0,expected_observations=180,
    label='Laptop benchmarking: Sequential 1 paired reporting-condition comparison',start_utc=STAMP)
save('status.json',state)
print('OUTPUT',OUT,flush=True)
try:
    baseline=read(core.OUT/'preservation_baseline.json')
    def check_originals():
        bad=[name for name,h in baseline.items() if not (ROOT/name).is_file() or core.sha(ROOT/name)!=h]
        assert not bad, 'Protected files differ: '+repr(bad)
        return dict(verified=len(baseline),changed=bad)
    initial=check_originals()
    previous=read(core.OUT/'machine_software_settings.json')
    normalize=lambda s:re.sub(r'[-_.]+','-',s).lower()
    versions={normalize(d.metadata['Name']):d.version for d in importlib.metadata.distributions()}
    old_versions={normalize(k):v for k,v in previous['packages'].items()}
    needed=('torch','torchvision','ultralytics','anomalib','segmentation-models-pytorch','numpy','opencv-python','pillow-heif','psutil')
    differences={k:[old_versions.get(k),versions.get(k)] for k in needed if old_versions.get(k)!=versions.get(k)}
    assert not differences, 'Environment differs: '+repr(differences)
    assert core.SIMULATION==read(core.OUT/'simulation_settings.json')
    assert torch.cuda.is_available()==previous['cuda_available']
    assert torch.version.cuda==previous['torch_cuda']
    assert torch.cuda.get_device_name(0)==previous['gpu']['name']
    save('session.json',dict(python=sys.executable,packages=versions,device=torch.cuda.get_device_name(0),
        cuda_runtime=torch.version.cuda,originals=initial,simulation=core.SIMULATION,
        benchmark_source_sha256=core.sha(Path(__file__)),core_sha256=core.sha(Path(core.__file__)),
        prior_comparison=read(core.OUT/'sequential2_session.json'),practical_margin_percent=5,
        margin_note='Declared practical tolerance, not an accuracy or statistical equivalence standard'))
    logic_checks()
    images=[(str(p.relative_to(ROOT)),core.load_image(p)) for p in core.paths('RGB')]
    assert len(images)==30
    models={}
    for name in ('patchcore','fod','crack'):
        print('Loading',name,flush=True);models[name]=core.construct(name)
    reference=read(core.OUT/'20261031T070619_481567Z_sequential2'/'model_settings.json')
    # Verify settings set by the original wrappers instead of changing runtime options.
    actual=dict(cudnn_benchmark=torch.backends.cudnn.benchmark,cudnn_deterministic=torch.backends.cudnn.deterministic,
        matmul_allow_tf32=torch.backends.cuda.matmul.allow_tf32,cudnn_allow_tf32=torch.backends.cudnn.allow_tf32,
        cpu_threads=torch.get_num_threads(),opencv_threads=core.cv2.getNumThreads())
    assert all(actual[k]==reference[k] for k in actual), 'Runtime settings differ: '+repr(actual)
    save('runtime_settings.json',dict(actual=actual,original_model_settings=reference))
    variants={'previous':OLD,'revised':NEW}
    smoke=[]
    for variant,fn in variants.items():
        records,d=fn(images[0][1],models,sequential2=True);core.sync()
        assert d['crack_calls']==d['crop_count']
        smoke.append(dict(variant=variant,messages=records,routing=d))
    save('smoke.json',smoke)
    print('SMOKE passed both real pipelines and 8 routing cases',flush=True)
    for variant,fn in variants.items():
        for i in range(5):fn(images[0][1],models,sequential2=True);core.sync()
        print('Warmups',variant,5,flush=True)
    with (core.OUT/'crop_manifest.csv').open(newline='',encoding='utf-8') as f:entry=next(csv.DictReader(f))
    original=dict(images)[entry['filename']]
    xa,ya,xb,yb=json.loads(entry['roi'])
    crop=core.cv2.resize(original[ya:yb,xa:xb],(1280,720))
    for name in ('fod','crack'):
        for _ in range(5):core.detect(models[name],crop);core.sync()
    for name,det in models.items():
        module=core.module_of(det,name);module.eval()
        probes[name]=core.ForwardProbe(module,split=False);det._bench_probe=probes[name]
    torch.cuda.reset_peak_memory_stats()
    start_run=time.perf_counter()
    for repeat in range(3):
        for index,(key,im) in enumerate(images):
            order=('previous','revised') if (repeat+index)%2==0 else ('revised','previous')
            paired={}
            for position,variant in enumerate(order):
                for p in probes.values():p.clear()
                core.sync();start=time.perf_counter()
                result,d=variants[variant](im,models,sequential2=True)
                core.sync();end=time.perf_counter()
                row=dict(variant=variant,repeat=repeat+1,input=key,width=im.shape[1],height=im.shape[0],
                    position_in_pair=position+1,status='ok',total_ms=(end-start)*1000,**d)
                for name,p in probes.items():
                    row[name+'_model_ms']=p.results()['model_ms']
                    row[name+'_preprocessing_host_ms']=sum(c['pre_ms'] for c in p.calls)
                    row[name+'_postprocessing_host_ms']=sum(c['post_ms'] for c in p.calls)
                row.update(core.memory())
                rows.append(row);paired[variant]=(result,d)
                outputs.append(dict(variant=variant,repeat=repeat+1,input=key,messages=result))
                state['completed']=len(rows)
                core.csv_write(OUT/'raw_timings.csv',rows)
                save('final_outputs.json',outputs)
                save('status.json',state)
            old_records,od=paired['previous'];new_records,nd=paired['revised']
            for field in ('crop_count','fod_calls','crack_calls','coordinate_count','fod_positive_crops','crack_positive_crops','ugv_message_count'):
                assert od[field]==nd[field], 'Model routing/output changed: '+field
            assert [r for r in old_records if r['destination']=='UGV']==[r for r in new_records if r['destination']=='UGV']
            assert [r for r in old_records if r['type']=='CRACK']==[r for r in new_records if r['type']=='CRACK']
            print('PAIR',repeat+1,index+1,'/30','previous_ms',round(rows[-2 if order[0]=='previous' else -1]['total_ms'],3),
                'revised_ms',round(rows[-2 if order[0]=='revised' else -1]['total_ms'],3),flush=True)
            if time.perf_counter()-start_run>600:raise RuntimeError('Measured run wall budget exceeded; partial results preserved')
    summaries={v:stats([r for r in rows if r['variant']==v]) for v in variants}
    a=summaries['previous'];b=summaries['revised']
    # Resample whole image groups: three repetitions of one image are not independent images.
    grouped={v:np.array([np.mean([r['total_ms'] for r in rows if r['variant']==v and r['input']==key]) for key,_ in images]) for v in variants}
    rng=np.random.default_rng(4301);indices=rng.integers(0,30,size=(10000,30))
    changes=(grouped['revised'][indices].mean(axis=1)/grouped['previous'][indices].mean(axis=1)-1)*100
    ci=np.percentile(changes,[2.5,97.5]).tolist()
    delta=(b['mean_ms']/a['mean_ms']-1)*100
    p95_delta=(b['p95_ms']/a['p95_ms']-1)*100
    decision=('negligible_within_5_percent' if ci[0]>-5 and ci[1]<5 else
        'material_difference' if ci[0]>5 or ci[1]<-5 else 'inconclusive_due_to_timing_variation')
    save('summary.json',dict(configurations=summaries,mean_change_percent=delta,p95_change_percent=p95_delta,
        paired_image_bootstrap_95_percent_interval=ci,decision=decision,margin_percent=5,
        existing_sequential1_mean_ms=99.18527000037203,original_file_integrity=check_originals(),
        caveat='Timing margin applies to this laptop and simulated local JSON transport; no camera, Jetson or network measured.'))
    core.csv_write(OUT/'summary.csv',[dict(variant=v,**s) for v,s in summaries.items()])
    md=['# Sequential 1 reporting-condition check: laptop benchmarking','',
        'Previous: YOLO then U-Net on every crop; every U-Net outcome prepares a Base message.',
        'Revised: same inference and FOD coordinate/UGV processing; Base receives cracks or anomalies where neither model detects. FOD-positive/no-crack crops produce no Base message.','',
        'Same loaded models, same 30 preloaded RGB frames, batch 1, unchanged precision/input settings/thresholds, five excluded pipeline warmups per variant plus five excluded real-crop downstream warmups. Three paired passes; alternating within-pair order. No images dropped.',
        'The processing interval includes cropping/resizing, normal transfers, model inference, postprocessing, simulated coordinate extraction and local JSON message preparation; CUDA synchronization brackets each complete frame. Model loading, file decoding, persistence and verification are outside timing. GPU event hooks match previous integrated timing.','',
        '| Condition | Unique frames | Observations | Mean ms | Median ms | P95 ms | Max ms | Processing frames/s | Base messages |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for v,s in summaries.items():md.append(f"| {v} | {s['unique_inputs']} | {s['observations']} | {s['mean_ms']:.3f} | {s['median_ms']:.3f} | {s['p95_ms']:.3f} | {s['max_ms']:.3f} | {s['processing_frames_per_s']:.3f} | {s['base_messages']} |")
    md+=['',f'Mean revised-versus-previous change: {delta:+.3f}%. P95 change: {p95_delta:+.3f}%.',
        f'Paired image-group bootstrap 95% interval for mean change: [{ci[0]:+.3f}%, {ci[1]:+.3f}%].',
        f'Decision using a declared 5% practical margin: **{decision}**.',
        'The tolerance is an explicit practical choice. A confidence interval outside neither boundary does not prove the absence of smaller effects. All runs share a finite image set; background activity, clocks and thermal variation remain limitations.',
        'Original historical Sequential 1 mean: 99.185 ms (10.082 frames/s). Historical results and other architecture results have been preserved; cross-session timing shifts should not be attributed to this condition alone.',
        'All 84 protected original files verified unchanged. Standalone models and independent thermal tests were not rerun because their execution is unchanged.',
        'No actual communication, GPS, camera sampling, Jetson performance or localisation accuracy is measured.','']
    (OUT/'comparison.md').write_text('\n'.join(md),encoding='utf-8')
    state.update(status='completed',decision=decision)
    print('RESULT',json.dumps(dict(summary=summaries,mean_change_percent=delta,interval=ci,decision=decision)),flush=True)
except Exception:
    state.update(status='failed',error=traceback.format_exc());print(state['error'],flush=True)
finally:
    for p in probes.values():p.close()
    save('status.json',state)
    print('SAVED',OUT,state['status'],flush=True)
if state['status']!='completed':sys.exit(1)