"""Factual reports and preservation/coverage validation; no model inference."""
import csv,hashlib,json,math,shutil
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent.parent
SUITE=Path(__file__).resolve().parent
OUT=ROOT/"benchmark_results"
def jread(p):return json.loads(p.read_text(encoding="utf-8-sig"))
def cread(p):
    with p.open(newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def jwrite(p,v):p.write_text(json.dumps(v,indent=2),encoding="utf-8")
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda:f.read(1048576),b""):h.update(block)
    return h.hexdigest()
def fmt(v,d=3):
    return "n/a" if v in (None,"") else f"{float(v):.{d}f}"
def integer(r,k):return int(r.get(k) or 0)
baseline=jread(OUT/"preservation_baseline.json")
integrity=[dict(file=k,unchanged=(ROOT/k).is_file() and sha(ROOT/k)==v) for k,v in baseline.items()]
jwrite(OUT/"original_file_integrity.json",integrity)
summary=cread(OUT/"summary.csv")
latest={}
coverage=[];routing=[];all_rows=[];tensor_rows=[]
manifest=cread(OUT/"input_manifest.csv")
crops=cread(OUT/"crop_manifest.csv") if (OUT/"crop_manifest.csv").exists() else []
crop_counts=Counter(c["filename"] for c in crops)
for s in summary:
    config=s["configuration"]
    if config!="crops":latest[config]=s
    folder=OUT/s["run"]
    rows=cread(folder/"raw_timings.csv") if (folder/"raw_timings.csv").exists() else []
    good=[r for r in rows if r["status"]=="ok"];all_rows+=good
    if config in ("fod","crack"):
        expected={r["crop_id"] for r in crops}
    elif config=="coordinates":
        expected={r["id"] for r in jread(folder/"coordinate_workload.json")} if (folder/"coordinate_workload.json").exists() else {r["input"] for r in good}
    else:
        branch="Thermal" if config in ("thermal","thermal_sampling") else "RGB"
        expected={r["filename"] for r in manifest if r["branch"]==branch}
    for repeat in sorted(set(r["repeat"] for r in good)):
        rr=[r for r in good if r["repeat"]==repeat]
        observed=Counter(r["input"] for r in rr)
        coverage.append(dict(run=s["run"],config=config,repeat=repeat,
            expected_unique=len(expected),observations=len(rr),
            all_expected_once=(set(observed)==expected and all(v==1 for v in observed.values()))))
    for r in good:
        for name in ("patchcore","fod","crack","thermal"):
            tensors=json.loads(r.get(name+"_tensor_settings") or "[]")
            for t in tensors:
                tensor_rows.append(dict(run=s["run"],input=r["input"],repeat=r["repeat"],model=name,
                    shape=json.dumps(t["shape"]),dtype=t["dtype"],device=t["device"]))
        if config in ("sequential","parallel"):
            count=integer(r,"crop_count");fod=integer(r,"fod_calls");crack=integer(r,"crack_calls")
            routing.append(dict(run=s["run"],input=r["input"],repeat=r["repeat"],
                crop_count_matches_generation=(count==crop_counts.get(r["input"],0)),
                fod_calls_correct=(fod==count),
                crack_calls_correct=(crack==(count if config=="parallel" else count-integer(r,"fod_positive_crops"))),
                forward_counts_correct=all(
                    len(json.loads(r.get(name+"_tensor_settings") or "[]"))==expected_calls
                    for name,expected_calls in (("patchcore",1),("fod",fod),("crack",crack))),
                coordinate_message_counts_correct=(integer(r,"coordinate_count")==integer(r,"ugv_message_count")),
                base_message_counts_correct=(integer(r,"base_message_count")==
                    integer(r,"crack_positive_crops")+integer(r,"neither_detected_crops"))))
jwrite(OUT/"coverage_validation.json",coverage)
jwrite(OUT/"routing_validation.json",routing)
with (OUT/"model_input_settings.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=["run","input","repeat","model","shape","dtype","device"])
    w.writeheader();w.writerows(tensor_rows)
all_unchanged=all(r["unchanged"] for r in integrity)
all_covered=all(r["all_expected_once"] for r in coverage)
routing_ok=all(all(v for k,v in r.items() if k.endswith("_correct") or k=="crop_count_matches_generation") for r in routing)
machine=jread(OUT/"machine_software_settings.json")
simulation=jread(SUITE/"simulation.json")
try:cpu=json.loads(machine["cpu_details"]).get("Name",machine["cpu"]).strip()
except Exception:cpu=machine["cpu"]
lines=["# FOD ARGUS laptop results: corrected architectures and simulated coordinates","",
    f"Hardware: {cpu}; {machine['ram_total_bytes']/1024**3:.2f} GiB RAM; "
    f"{machine.get('gpu',{}).get('name','CPU only')}. CUDA available: {machine['cuda_available']}.",
    f"Python: {machine['python']}; PyTorch {machine['packages'].get('torch')}, CUDA build {machine.get('torch_cuda')}.",
    "No dependencies, environments, CPU/GPU settings, drivers or SDKs were changed for this redo.",
    "",
    "Sequential now skips U-Net whenever YOLO detects FOD in that crop. Parallel always runs both downstream models on every valid crop.",
    "This routing difference means the comparison is between two architectures with different workloads, rather than an isolated concurrency speedup.",
    "The original integration/model/input files remain untouched. The architectures are implemented only in benchmark_suite.",
    "",
    "Validation:",
    f"- Preserved files unchanged: {sum(r['unchanged'] for r in integrity)}/{len(integrity)}.",
    f"- Complete input-per-pass coverage checks: {sum(r['all_expected_once'] for r in coverage)}/{len(coverage)}.",
    f"- Detailed architecture routing/call-count checks: {'passed' if routing_ok else 'DISCREPANCIES: inspect routing_validation.json'}.",
    "- Four coordinate-math checks and ten routing-unit checks are recorded separately; mocks were used only for correctness checks, never timing samples.",
    ""]
for branch in ("RGB","Thermal"):
    subset=[r for r in manifest if r["branch"]==branch]
    sizes=Counter(str(r["width"])+" x "+str(r["height"]) for r in subset if r["status"]=="ok")
    lines.append(f"{branch}: {len(subset)} input files; dimensions/counts {dict(sizes)}; unreadable {sum(r['status']!='ok' for r in subset)}.")
lines += [f"PatchCore generated {len(crops)} valid crops across {len(crop_counts)} unique RGB images. The other {30-len(crop_counts)} images produced no crops.",
    "The isolated downstream tests use those real crops, zoomed by the normal 1280 x 720 preprocessing path. No full-frame substitution is made.",
    "",
    "The following table selects the latest run of each configuration. Initial one-pass runs are retained separately in summary.csv.",
    "A three-pass RGB/thermal run is 90 observations from 30 unique images; repeated observations are not additional unique inputs.",
    "",
    "| Configuration | Unique inputs | Source frames | Observations | Mean ms | Median ms | P95 ms | Max ms | Throughput/s | Unit |",
    "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
for config in ("patchcore","fod","crack","coordinates","thermal_sampling","thermal","sequential","parallel"):
    r=latest.get(config)
    if not r:continue
    decimals=6 if config=="coordinates" else 3
    lines.append("| "+" | ".join([config,r["unique_inputs"],r["unique_source_frames"],r["measured_observations"]]+
        [fmt(r[k],decimals) for k in ("mean_ms","median_ms","p95_ms","max_ms","processing_throughput_per_s")]+[r["unit"]])+" |")
lines+=["","Processing throughput = completed observations / sum of directly measured processing seconds.",
    "Crop and coordinate/detection throughput are not full-frame throughput. Pipeline totals are measured directly, not estimated by adding isolated model times.",
    "",
    "| Architecture | YOLO crop calls | U-Net crop calls | Coordinate calls | Mean coordinate ms/frame | Mean coordinate ms/detection |",
    "|---|---:|---:|---:|---:|---:|"]
for config in ("sequential","parallel"):
    r=latest.get(config)
    if not r:continue
    n=int(r["measured_observations"])
    lines.append("| "+" | ".join([config,r["fod_calls"],r["crack_calls"],r["coordinate_count"],
        fmt(float(r["coordinate_ms_total"])/n,6) if n else "n/a",
        fmt(r["coordinate_mean_ms_per_detection"],6)])+" |")
lines+=["","Coordinate extraction uses the supplied simulated UAV position (3,4) m and assumed 2 x 2 m footprint at nominal 5 m AGL.",
    "Each actual FOD box is mapped from the normal zoomed image into its source ROI/frame; the pixel centre/offset is scaled using actual frame dimensions and added to the simulated UAV position.",
    "The provided example produces centre (530,340) px and world (2.828125,3.9444444444) m. This verifies arithmetic only, not physical localisation.",
    "No navigation sensor, camera calibration, yaw/roll/pitch, GPS synchronization or physical ground-truth accuracy is measured.",
    "Only FOD detections trigger world-coordinate calculation, as in the final diagrams. Crack/residual-anomaly messages go to Base.",
    "Simulated message preparation creates local JSON payloads only. Its CPU cost and coordinate math are included inside the measured pipeline boundary; no network messages, transmission delays or sleeps are introduced.",
    "Coordinate math may overlap U-Net in parallel mode. Do not add coordinate time onto the already-inclusive pipeline total.",
    "",
    "| Isolated model | Forward mean ms | Forward median ms | Forward P95 ms | Forward max ms |",
    "|---|---:|---:|---:|---:|"]
for config in ("patchcore","fod","crack","thermal"):
    r=latest.get(config)
    if r:lines.append("| "+" | ".join([config]+[fmt(r[k]) for k in (
        "model_only_mean_ms","model_only_median_ms","model_only_p95_ms","model_only_max_ms")])+" |")
lines+=["",
    "Thermal runs independently as finite unpaced replay cycles, with sampling/loading and inference benchmarked separately.",
    "thermal_sampling times file read plus image decoding only; thermal times inference from preloaded images with the model kept loaded. File caches influence loading results.",
    "These are not real camera sampling rates or live capture-to-output latency, and no simultaneous RGB/thermal scheduling or paired observations are claimed.",
    "The application thermal file remains a keyboard bypass. The previously approved standalone thermal weights configuration is conf .25, IoU .70, imgsz 640, float32, batch 1.",
    "",
    "| Configuration | Status | Failures | Unprocessed | Measured CUDA peak MiB | Sampled RSS MiB |",
    "|---|---|---:|---:|---:|---:|"]
for config,r in latest.items():
    failures=json.loads(r["failures"]) if r["failures"] else []
    lines.append("| "+" | ".join([config,r["status"],str(len(failures)),r["unprocessed"],
        fmt(float(r["peak_cuda_allocated_bytes"])/1024**2) if r["peak_cuda_allocated_bytes"] else "n/a",
        fmt(float(r["rss_bytes"])/1024**2) if r["rss_bytes"] else "n/a"])+" |")
available=[int(r["available_ram_bytes"]) for r in all_rows if r.get("available_ram_bytes")]
lines+=["",f"Minimum sampled available system RAM: {min(available)/1024**2:.1f} MiB." if available else "",
    "CUDA peaks cover measured passes after warmup and exclude driver/display/other processes. Initialization/autotuning can require substantially more VRAM. RSS is sampled, not a true process peak.",
    "Background load, CPU/GPU clocks/temperature, OS caches and algorithm choices were not isolated. Short coordinate timings include timer/function overhead and should not be interpreted as deployment guarantees.",
    "Weights, thresholds, resolutions and tensor precision were preserved. Backend settings, actual predictor arguments, tensor shapes/dtypes and checkpoint model metadata are saved per run.",
    "",
    "Successfully completed/failed configurations and partial observations are explicitly recorded above and in status.json; see logs for failures.",
    "These measurements do not establish Jetson performance, real capture/sampling rate, live latency, 5 mm detection, localisation accuracy or full detection accuracy.",
    "When the final camera and Jetson arrive, repeat model and end-to-end timing under sustained power/thermal conditions, using real capture/telemetry and calibrated geometry, real thermal scheduling and real communications. Validate accuracy/localisation independently with labelled physical ground truth.",
    "",
    "See methodology.md for timing boundaries, README.md for commands, raw_timings.csv for every run, final_outputs.json for simulated pipeline outputs, and the preservation/coverage/routing JSON files for verification."]
(OUT/"results_and_limitations.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
shutil.copyfile(SUITE/"METHODOLOGY.md",OUT/"methodology.md")
shutil.copyfile(SUITE/"README.md",OUT/"README.md")
(OUT/"requirements_snapshot.txt").write_text("\n".join(k+"=="+v for k,v in sorted(machine["packages"].items()))+"\n",encoding="utf-8")
print("PRESERVATION",all_unchanged,"COVERAGE",all_covered,"ROUTING",routing_ok,flush=True)
for name in ("sequential","parallel","thermal_sampling","thermal","coordinates"):
    r=latest.get(name)
    if r:print(name,"observations",r["measured_observations"],"mean_ms",r["mean_ms"],"throughput",r["processing_throughput_per_s"],flush=True)
if not all_unchanged or not all_covered or not routing_ok:
    raise RuntimeError("Validation discrepancy; inspect saved verification reports")

