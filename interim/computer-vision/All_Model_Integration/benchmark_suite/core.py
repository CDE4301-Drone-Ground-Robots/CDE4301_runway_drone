"""FOD ARGUS laptop benchmark. Never imports Integration_1 (it opens a camera).
Run with the fod_synthetic Python and -B. Outputs only under benchmark_results.
"""
import os
from pathlib import Path
SUITE = Path(__file__).resolve().parent
ROOT = SUITE.parent
OUT = ROOT / "benchmark_results"
OUT.mkdir(exist_ok=True)
(OUT / "ultralytics").mkdir(exist_ok=True)
os.environ["YOLO_CONFIG_DIR"] = str(OUT / "ultralytics")
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
import argparse, csv, hashlib, importlib.metadata, json, platform, subprocess
import sys, time, traceback
sys.path.insert(0,str(ROOT))
from coordinates import extract as extract_coordinates, remap_box, self_test
from benchmark_labels import display_name
SIMULATION = json.loads((SUITE/"simulation.json").read_text(encoding="utf-8-sig"))
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import cv2
import numpy as np
import psutil
import torch
sys.dont_write_bytecode = True

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, default=str), encoding="utf-8")

def csv_write(path, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def load_image(path):
    if path.suffix.lower() in (".heic", ".heif"):
        from PIL import Image
        from pillow_heif import register_heif_opener
        register_heif_opener()
        # Preserve stored pixel orientation, as cv2 color loading normally does here.
        # Record EXIF in inventory; no source is converted or overwritten.
        with Image.open(path) as im:
            return cv2.cvtColor(np.array(im.convert("RGB")), cv2.COLOR_RGB2BGR)
    x = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if x is None:
        raise ValueError("OpenCV cannot decode " + str(path))
    return x

def paths(branch):
    return sorted(p for p in (ROOT / "Benchmark_inputs" / branch).rglob("*") if p.is_file())

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def inventory():
    items = []
    for branch in ("RGB", "Thermal"):
        for p in paths(branch):
            row = dict(branch=branch, filename=str(p.relative_to(ROOT)), bytes=p.stat().st_size,
                       sha256=sha(p), width="", height="", status="ok", error="")
            try:
                im = load_image(p)
                row.update(width=im.shape[1], height=im.shape[0], dtype=str(im.dtype), channels=im.shape[2])
                if p.suffix.lower() in (".heic", ".heif"):
                    from PIL import Image
                    with Image.open(p) as pil:
                        row["exif_orientation"] = pil.getexif().get(274, 1)
                        row["decoder"] = "pillow-heif RGB converted to BGR; stored orientation"
                else:
                    row["decoder"] = "cv2.IMREAD_COLOR"
            except Exception as exc:
                row.update(status="unreadable", error=repr(exc))
            items.append(row)
    csv_write(OUT / "input_manifest.csv", items)
    record = dict(label="Laptop benchmarking", utc=datetime.now(timezone.utc).isoformat(),
        python=sys.executable, version=sys.version, platform=platform.platform(),
        ram_total_bytes=psutil.virtual_memory().total, cpu=platform.processor(),
        physical_cores=psutil.cpu_count(logical=False), logical_cores=psutil.cpu_count(),
        packages={d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},
        cuda_available=torch.cuda.is_available(), torch_cuda=torch.version.cuda,
        torch_threads=torch.get_num_threads(), opencv_threads=cv2.getNumThreads(),
        original_files={p.name:sha(p) for p in ROOT.iterdir()
                        if p.is_file() and p.suffix in (".py", ".pt", ".pth", ".ckpt")
                        and not p.name.startswith("benchmark_")},
        images=items)
    if torch.cuda.is_available():
        prop = torch.cuda.get_device_properties(0)
        record["gpu"] = dict(name=prop.name, total_memory_bytes=prop.total_memory)
    for key, command in [
        ("nvidia_smi", ["nvidia-smi"]),
        ("cpu_details", ["powershell", "-NoProfile", "-Command",
                        "Get-CimInstance Win32_Processor | Select-Object Name | ConvertTo-Json"])]:
        try:
            record[key] = subprocess.check_output(command, text=True, timeout=20)
        except Exception as exc:
            record[key] = repr(exc)
    write_json(OUT / "machine_software_settings.json", record)
    for branch in ("RGB", "Thermal"):
        selected = [r for r in items if r["branch"] == branch]
        print(branch, len(selected), "files", Counter((r["width"], r["height"]) for r in selected),
              "unreadable", [r["filename"] for r in selected if r["status"] != "ok"], flush=True)
    protected={}
    for p in ROOT.rglob("*"):
        if p.is_file() and p.relative_to(ROOT).parts[0] not in ("benchmark_suite","benchmark_results"):
            protected[str(p.relative_to(ROOT))]=sha(p)
    write_json(OUT/"preservation_baseline.json",protected)
    write_json(OUT/"coordinate_math_test.json",self_test(SIMULATION))
    write_json(OUT/"simulation_settings.json",SIMULATION)
    return record

def sync():
    if torch.cuda.is_available():
        torch.cuda.synchronize(0)

def memory():
    r = dict(rss_bytes=psutil.Process().memory_info().rss,
             available_ram_bytes=psutil.virtual_memory().available)
    if torch.cuda.is_available():
        r.update(cuda_allocated_bytes=torch.cuda.memory_allocated(),
                 cuda_reserved_bytes=torch.cuda.memory_reserved(),
                 cuda_peak_allocated_bytes=torch.cuda.max_memory_allocated(),
                 cuda_peak_reserved_bytes=torch.cuda.max_memory_reserved())
    return r

class ForwardProbe:
    """No device synchronisation inside pipeline hooks, preserving concurrency."""
    def __init__(self, module, split=False):
        self.items = []
        self.calls = []
        self.split = split
        self.a = module.register_forward_pre_hook(self.before)
        self.b = module.register_forward_hook(self.after)
    def before(self, module, inputs):
        if self.split: sync()
        entry = dict(host_start=time.perf_counter(), shape=list(inputs[0].shape),
                     dtype=str(inputs[0].dtype), device=str(inputs[0].device))
        if inputs[0].is_cuda:
            entry["start"] = torch.cuda.Event(enable_timing=True)
            entry["end"] = torch.cuda.Event(enable_timing=True)
            entry["start"].record()
        self.items.append(entry)
    def after(self, module, inputs, output):
        e = self.items[-1]
        if "end" in e: e["end"].record()
        if self.split: sync()
        e["host_end"] = time.perf_counter()
    def clear(self):
        self.items.clear(); self.calls.clear()
    def results(self):
        if not self.items: return dict(model_ms=None)
        return dict(model_ms=sum(e["start"].elapsed_time(e["end"]) if "start" in e
                                  else (e["host_end"]-e["host_start"])*1000 for e in self.items),
                    actual_tensor_settings=[{k:e[k] for k in ("shape","dtype","device")} for e in self.items])
    def close(self):
        self.a.remove(); self.b.remove()

def construct(name):
    if name == "patchcore":
        from Patchcore_Detection import PatchcoreDetector
        return PatchcoreDetector(ROOT/"Anomaly_model.ckpt", score_threshold=.05)
    if name == "fod":
        from FOD_detection import FODDetector
        return FODDetector(str(ROOT/"FOD_yolo11s.pt"), confidence=.30,
                           device=0 if torch.cuda.is_available() else "cpu")
    if name == "crack":
        from Crack_Detection import CrackDetector
        return CrackDetector(str(ROOT/"best_crack_model.pth"), image_size=512, threshold=.5)
    if name == "thermal":
        from ultralytics import YOLO
        class StandaloneThermal:
            def __init__(self):
                self.model = YOLO(str(ROOT/"Thermal_yolo11s.pt"))
            def detect(self, frame):
                return self.model.predict(frame, conf=.25, iou=.7, imgsz=640, half=False,
                    device=0 if torch.cuda.is_available() else "cpu", batch=1,
                    verbose=False, save=False)
        return StandaloneThermal()
    raise ValueError(name)

def module_of(det, name):
    return det.infer_model if name == "patchcore" else det.model.model if name in ("fod","thermal") else det.model

def detect(det, frame):
    # Inference mode is thread local, so enter it in every parallel worker.
    probe = getattr(det, "_bench_probe", None)
    index = len(probe.items) if probe else 0
    start = time.perf_counter()
    with torch.inference_mode():
        output = det.detect(frame)
    end = time.perf_counter()
    if probe and len(probe.items) > index:
        probe.calls.append(dict(pre_ms=(probe.items[index]["host_start"]-start)*1000,
                                post_ms=(end-probe.items[-1]["host_end"])*1000))
    return output

def outputs_brief(name, result):
    if name == "patchcore":
        return dict(score=result["score"], boxes=result["boxes"])
    if name == "crack":
        return None if result is None else dict(bbox=result["bbox"], center=result["center"],
                                                 mask_pixels=int(np.count_nonzero(result["mask"])))
    if name == "fod": return result
    return [dict(boxes=r.boxes.xyxy.cpu().tolist(), classes=r.boxes.cls.cpu().tolist(),
                 confidence=r.boxes.conf.cpu().tolist()) for r in result]

def pack_message(kind,destination,body):
    return dict(type=kind,destination=destination,body=body,
                simulated_transport=True,
                payload=json.dumps(dict(type=kind,destination=destination,body=body,
                                        simulated=True),separators=(",",":"),default=str))

def fod_branch(image,roi,frame_size,detector):
    found=detect(detector,image)
    records=[]; coordinate_ms=0.; message_ms=0.
    for d in found:
        t=time.perf_counter()
        coord=extract_coordinates(d["bbox"],roi,frame_size,SIMULATION)
        coordinate_ms+=(time.perf_counter()-t)*1000
        t=time.perf_counter()
        records.append(pack_message("FOD","UGV",dict(name=d["object"],
            confidence=float(d["confidence"]),coordinates=coord)))
        message_ms+=(time.perf_counter()-t)*1000
    return records,coordinate_ms,message_ms

def pipeline(frame, models, parallel=False, executor=None, streams=None, sequential2=False):
    patch=detect(models["patchcore"],frame)
    details=dict(crop_count=0,stages=["patchcore"],crop_resize_host_ms=0.,
        output_merge_host_ms=0.,coordinate_extraction_ms=0.,coordinate_count=0,
        message_preparation_ms=0.,fod_calls=0,crack_calls=0,fod_positive_crops=0,
        crack_positive_crops=0,neither_detected_crops=0,no_crack_base_crops=0)
    records=[]
    frame_size=(frame.shape[1],frame.shape[0])
    for roi in patch["boxes"]:
        t=time.perf_counter()
        xa,ya,xb,yb=roi
        crop=frame[ya:yb,xa:xb]
        if not crop.size: continue
        zoom=cv2.resize(crop,(1280,720))
        details["crop_resize_host_ms"]+=(time.perf_counter()-t)*1000
        details["crop_count"]+=1
        details["fod_calls"]+=1
        cr=None
        if parallel:
            def task(name):
                if streams:
                    with torch.cuda.stream(streams[name]):
                        return fod_branch(zoom,roi,frame_size,models[name]) if name=="fod" else detect(models[name],zoom)
                return fod_branch(zoom,roi,frame_size,models[name]) if name=="fod" else detect(models[name],zoom)
            f=executor.submit(task,"fod"); c=executor.submit(task,"crack")
            fod_records,coordinate_ms,message_ms=f.result()
            cr=c.result()
            details["crack_calls"]+=1
        else:
            fod_records,coordinate_ms,message_ms=fod_branch(zoom,roi,frame_size,models["fod"])
            # Corrected sequential fallback: run U-Net ONLY if YOLO detects no FOD.
            if sequential2 or not fod_records:
                cr=detect(models["crack"],zoom)
                details["crack_calls"]+=1
        details["coordinate_extraction_ms"]+=coordinate_ms
        details["coordinate_count"]+=len(fod_records)
        details["message_preparation_ms"]+=message_ms
        details["fod_positive_crops"]+=int(bool(fod_records))
        t=time.perf_counter()
        records.extend(fod_records)
        details["output_merge_host_ms"]+=(time.perf_counter()-t)*1000
        # Base receives positive cracks, and residual anomalies when neither detects.
        t=time.perf_counter()
        if cr is not None:
            details["crack_positive_crops"]+=1
            records.append(pack_message("CRACK","BASE",
                dict(bbox_original_px=remap_box(cr["bbox"],roi),roi=roi)))
        elif sequential2:
            details["no_crack_base_crops"]+=1
            if not fod_records:details["neither_detected_crops"]+=1
            records.append(pack_message("NO_CRACK_DETECTED","BASE",
                dict(roi=roi,fod_detected=bool(fod_records))))
        elif not fod_records:
            details["neither_detected_crops"]+=1
            records.append(pack_message("UNCLASSIFIED_ANOMALY","BASE",dict(roi=roi)))
        details["message_preparation_ms"]+=(time.perf_counter()-t)*1000
    if details["fod_calls"]:details["stages"].append("fod")
    if details["crack_calls"]:details["stages"].append("crack")
    if details["coordinate_count"]:details["stages"].append("simulated_coordinate_extraction")
    details["message_count"]=len(records)
    details["ugv_message_count"]=sum(r["destination"]=="UGV" for r in records)
    details["base_message_count"]=sum(r["destination"]=="BASE" for r in records)
    return records,details

def special_cpu_run(args,run_dir,status):
    rows=[]
    if args.config=="thermal_sampling":
        workload=[(str(p.relative_to(ROOT)),p,{}) for p in paths("Thermal")]
        if len(workload)!=30:raise RuntimeError("Expected 30 thermal files")
        operation=lambda item:load_image(item)
    else:
        file=OUT/"coordinate_workload.json"
        if not file.exists():raise RuntimeError("Run isolated FOD first to generate real coordinate workload")
        status["coordinate_workload_sha256"]=sha(file)
        data=json.loads(file.read_text(encoding="utf-8"))
        write_json(run_dir/"coordinate_workload.json",data)
        if not data:raise RuntimeError("No actual FOD detections: coordinate inference workload unavailable; ask user")
        workload=[(d["id"],d,d) for d in data]
        operation=lambda d:extract_coordinates(d["bbox"],d["roi"],d["frame_size"],SIMULATION)
    status["selected_inputs"]=len(workload)
    for _ in range(args.warmups):operation(workload[0][1])
    for repeat in range(args.repeats):
        for key,item,meta in workload:
            try:
                start=time.perf_counter(); result=operation(item); end=time.perf_counter()
                width,height=(result.shape[1],result.shape[0]) if args.config=="thermal_sampling" else meta["frame_size"]
                row=dict(repeat=repeat+1,input=key,source_frame=meta.get("filename",key),
                    width=width,height=height,status="ok",total_ms=(end-start)*1000,**memory())
                if args.config=="coordinates":row.update(coordinate_extraction_ms=row["total_ms"],coordinate_count=1)
                rows.append(row);status["completed"]+=1
                csv_write(run_dir/"raw_timings.csv",rows)
                print(args.config,repeat+1,status["completed"],round(row["total_ms"],6),"ms",flush=True)
            except Exception as exc:
                rows.append(dict(repeat=repeat+1,input=key,source_frame=meta.get("filename",key),
                                 status="failed",error=repr(exc)))
                csv_write(run_dir/"raw_timings.csv",rows);raise
    status["status"]="completed"

def run(args):
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    run_dir=OUT/(stamp+"_"+args.config); run_dir.mkdir()
    status=dict(label="Laptop benchmarking",config=args.config,repeats=args.repeats,
                warmups=args.warmups,device="cuda:0" if torch.cuda.is_available() else "cpu",
                start_utc=stamp, completed=0, failures=[], status="running",
                cli=sys.argv, benchmark_source_sha256=sha(Path(__file__)),
                helper_hashes={p.name:sha(p) for p in SUITE.iterdir() if p.is_file()},
                simulation=SIMULATION,memory_before=memory())
    write_json(run_dir/"status.json",status)
    rows=[]; probes={}; executor=None; models={}; active_streams=None
    try:
        if args.config=="inventory":
            inventory(); status["status"]="completed"; return
        if args.config=="report":
            report(); status["status"]="completed"; return
        if args.config in ("thermal_sampling","coordinates"):
            special_cpu_run(args,run_dir,status);return
        names= {"smoke":["patchcore","fod","crack","thermal"],

                "crops":["patchcore"],"sequential":["patchcore","fod","crack"],
                "parallel":["patchcore","fod","crack"],"sequential2":["patchcore","fod","crack"],
                "smoke_sequential2":["patchcore","fod","crack"]}.get(args.config,[args.config])
        # Test input readability before expensive model loading. No silent omissions.
        source=paths("Thermal" if args.config=="thermal" else "RGB")
        if args.config in ("smoke","smoke_sequential2"):
            source=source[:1]
        images=[(p,load_image(p)) for p in source]
        if args.config in ("sequential","sequential2","parallel","patchcore","crops") and len(images)!=30:
            raise RuntimeError("Expected exactly 30 RGB inputs; found "+str(len(images)))
        if args.config=="thermal" and len(images)!=30:
            raise RuntimeError("Expected exactly 30 thermal inputs")
        workload=[(str(p.relative_to(ROOT)),im,{}) for p,im in images]
        if args.config in ("fod","crack"):
            manifest=OUT/"crop_manifest.csv"
            if not manifest.exists(): raise RuntimeError("Run --config crops first: real PatchCore crops are required")
            with manifest.open(newline="",encoding="utf-8") as f: crop_rows=list(csv.DictReader(f))
            if not crop_rows: raise RuntimeError("No anomaly crops produced. Ask user how to proceed; no full-frame substitution")
            workload=[]
            cache=dict((str(p.relative_to(ROOT)),im) for p,im in images)
            for c in crop_rows:
                roi=json.loads(c["roi"])
                xa,ya,xb,yb=roi
                crop=cache[c["filename"]][ya:yb,xa:xb]
                workload.append((c["crop_id"], cv2.resize(crop,(1280,720)), c))
        status["selected_inputs"]=len(workload)
        status["unique_source_frames"]=len(set(c.get("filename",key) for key,im,c in workload))
        for name in names:
            print("Loading",name,flush=True); models[name]=construct(name)
        if args.config=="smoke_sequential2":
            sync()
            result,detail=pipeline(images[0][1],models,sequential2=True)
            sync()
            assert detail["crack_calls"]==detail["crop_count"]
            assert detail["base_message_count"]==detail["crop_count"]
            write_json(run_dir/"sequential2_output.json",dict(messages=result,routing=detail))
            write_json(run_dir/"coordinate_math_test.json",self_test(SIMULATION))
            status.update(status="completed",completed=1,selected_inputs=1,unique_source_frames=1,
                          smoke_architecture_checks=1)
            print("SMOKE OK sequential2",detail,flush=True)
            return
        if args.config=="smoke":
            for name in names:
                if name=="thermal": im=load_image(paths("Thermal")[0])
                elif name in ("fod","crack"):
                    patch=smoke_results["patchcore"]
                    if not patch["boxes"]: raise RuntimeError("Smoke RGB has no anomaly crops; ask how to proceed")
                    xa,ya,xb,yb=patch["boxes"][0]
                    im=cv2.resize(images[0][1][ya:yb,xa:xb],(1280,720))
                else: im=images[0][1]
                result=detect(models[name],im); sync()
                if name=="patchcore": smoke_results={"patchcore":result}
                write_json(run_dir/(name+"_output.json"),outputs_brief(name,result))
                print("SMOKE OK",name,flush=True)
            for parallel in (False,True):
                with ThreadPoolExecutor(max_workers=2) as pool:
                    streams={k:torch.cuda.Stream() for k in ("fod","crack")} if parallel and torch.cuda.is_available() else None
                    sync()
                    if streams:
                        for stream in streams.values():stream.wait_stream(torch.cuda.current_stream())
                    result,detail=pipeline(images[0][1],models,parallel,pool if parallel else None,streams)
                    sync()
                write_json(run_dir/("parallel_output.json" if parallel else "sequential_output.json"),
                           dict(messages=result,routing=detail))
                print("SMOKE OK", "parallel" if parallel else "sequential",detail,flush=True)
            write_json(run_dir/"coordinate_math_test.json",self_test(SIMULATION))
            status.update(status="completed",completed=2,selected_inputs=2,unique_source_frames=2,smoke_model_checks=4,smoke_architecture_checks=2); return
        integrated=args.config in ("sequential","sequential2","parallel")
        if integrated:
            executor=ThreadPoolExecutor(max_workers=2) if args.config=="parallel" else None
            if executor and torch.cuda.is_available():
                active_streams={k:torch.cuda.Stream() for k in ("fod","crack")}
                for stream in active_streams.values(): stream.wait_stream(torch.cuda.current_stream())
            for i in range(args.warmups):
                pipeline(workload[0][1],models,bool(executor),executor,active_streams,sequential2=args.config=="sequential2"); sync()
                print("Warmup",i+1,flush=True)
        else:
            for i in range(args.warmups):
                detect(models[names[0]],workload[0][1]); sync()
                print("Warmup",i+1,flush=True)
        # Guarantee five isolated warmups for every required detector even when routing skipped it.
        if integrated:
            manifest=OUT/"crop_manifest.csv"
            if not manifest.exists():raise RuntimeError("Generate real crops before architecture tests")
            with manifest.open(newline="",encoding="utf-8") as f:entries=list(csv.DictReader(f))
            if not entries:raise RuntimeError("No real crops; ask user how to proceed")
            entry=entries[0]
            source_image=dict((str(p.relative_to(ROOT)),im) for p,im in images)[entry["filename"]]
            xa,ya,xb,yb=json.loads(entry["roi"])
            representative=cv2.resize(source_image[ya:yb,xa:xb],(1280,720))
            for name in ("fod","crack"):
                for _ in range(args.warmups):detect(models[name],representative);sync()
        for name in names:
            module=module_of(models[name],name); module.eval()
            probes[name]=ForwardProbe(module,split=not integrated)
            models[name]._bench_probe=probes[name]
        model_settings = dict(
            device=status["device"], cudnn_benchmark=torch.backends.cudnn.benchmark,
            cudnn_deterministic=torch.backends.cudnn.deterministic,
            matmul_allow_tf32=torch.backends.cuda.matmul.allow_tf32,
            cudnn_allow_tf32=torch.backends.cudnn.allow_tf32,
            cpu_threads=torch.get_num_threads(), opencv_threads=cv2.getNumThreads(),
            models={})
        for name, det in models.items():
            info=dict(class_name=type(module_of(det,name)).__name__)
            if name=="patchcore":
                info.update(image_size=det.image_size,score_threshold=det.score_threshold,
                    heatmap_percentile=det.heatmap_percentile,min_region_area=det.min_region_area,
                    padding=det.padding,checkpoint_hparams=dict(det.model.hparams),
                    memory_bank_shape=list(det.infer_model.memory_bank.shape))
            if name in ("fod","thermal"):
                info.update(names=det.model.names, architecture_yaml=det.model.model.yaml, overrides=det.model.overrides,
                            predictor_args=vars(det.model.predictor.args))
            if name=="crack": info.update(image_size=det.image_size,threshold=det.threshold)
            model_settings["models"][name]=info
        write_json(run_dir/"model_settings.json",model_settings)
        if torch.cuda.is_available(): torch.cuda.reset_peak_memory_stats()
        crops=[];coordinate_workload=[];output_rows=[]
        for repeat in range(args.repeats):
            for index,(key,im,meta) in enumerate(workload):
                for probe in probes.values(): probe.clear()
                row=dict(repeat=repeat+1,input=key,width=im.shape[1],height=im.shape[0],
                         source_frame=meta.get("filename",key),status="ok")
                try:
                    sync(); start=time.perf_counter()
                    if integrated:
                        result,detail=pipeline(im,models,bool(executor),executor,active_streams,sequential2=args.config=="sequential2")
                    else:
                        result=detect(models[names[0]],im); detail={}
                    sync(); end=time.perf_counter()
                    row.update(total_ms=(end-start)*1000,**detail)
                    for name,probe in probes.items():
                        r=probe.results(); row[name+"_model_ms"]=r["model_ms"]
                        row[name+"_preprocessing_host_ms"]=sum(x["pre_ms"] for x in probe.calls)
                        row[name+"_postprocessing_host_ms"]=sum(x["post_ms"] for x in probe.calls)
                        row[name+"_tensor_settings"]=json.dumps(r.get("actual_tensor_settings",[]))
                        if not integrated and probe.items:
                            row["preprocessing_ms"]=(probe.items[0]["host_start"]-start)*1000
                            row["postprocessing_ms"]=(end-probe.items[-1]["host_end"])*1000
                    if not integrated and names[0]=="patchcore":
                        row.update(crop_count=len(result["boxes"]),score=result["score"],stages="patchcore")
                        if args.config=="crops":
                            for n,roi in enumerate(result["boxes"]):
                                xa,ya,xb,yb=roi
                                if xb<=xa or yb<=ya: continue
                                crops.append(dict(filename=key,crop_id=key+"#"+str(n),roi=json.dumps(roi),
                                    crop_width=xb-xa,crop_height=yb-ya,zoom_width=1280,zoom_height=720))
                    if args.config=="fod" and repeat==0:
                        source=cache[meta["filename"]]
                        for number,d in enumerate(result):
                            coordinate_workload.append(dict(id=key+"#det"+str(number),filename=meta["filename"],
                                bbox=list(map(int,d["bbox"])),roi=json.loads(meta["roi"]),
                                frame_size=[source.shape[1],source.shape[0]],name=d["object"]))
                        write_json(OUT/"coordinate_workload.json",coordinate_workload)
                    if integrated:
                        output_rows.append(dict(repeat=repeat+1,input=key,messages=result))
                        write_json(run_dir/"final_outputs.json",output_rows)
                    row["output_count"]=len(result) if isinstance(result,list) else int(result is not None)
                    row.update(memory()); rows.append(row)
                    status["completed"]+=1
                    print(args.config,repeat+1,index+1,"/",len(workload),round(row["total_ms"],2),"ms",flush=True)
                    # Persistence happens strictly outside the processing timer.
                    csv_write(run_dir/"raw_timings.csv",rows)
                except Exception as exc:
                    row.update(status="failed",error=repr(exc)); rows.append(row)
                    csv_write(run_dir/"raw_timings.csv",rows)
                    raise
        if args.config=="crops":
            csv_write(OUT/"crop_manifest.csv",crops,
                      ["filename","crop_id","roi","crop_width","crop_height","zoom_width","zoom_height"])
            if not crops: raise RuntimeError("No suitable anomaly crops produced. Ask user how to proceed.")
        status["status"]="completed"
    except Exception as exc:
        status.update(status="failed",failures=[dict(error=repr(exc),traceback=traceback.format_exc())])
        print(traceback.format_exc(),flush=True)
    finally:
        for probe in probes.values(): probe.close()
        if executor: executor.shutdown(wait=True)
        status["memory_after"]=memory()
        status["unprocessed_observations"]=max(0,status.get("selected_inputs",0)*args.repeats-status["completed"])
        write_json(run_dir/"status.json",status)
        print("Saved",run_dir,"status",status["status"],flush=True)

def report():
    summary=[]
    for d in sorted(OUT.iterdir()):
        if not d.is_dir() or not (d/"status.json").exists(): continue
        s=json.loads((d/"status.json").read_text(encoding="utf-8-sig"))
        if s["config"] in ("report","inventory","smoke","smoke_sequential2"): continue
        rows=[]
        if (d/"raw_timings.csv").exists():
            with (d/"raw_timings.csv").open(newline="",encoding="utf-8") as f:
                rows=[r for r in csv.DictReader(f) if r["status"]=="ok"]
        times=np.array([float(r["total_ms"]) for r in rows])
        models=np.array([float(r[s["config"]+"_model_ms"]) for r in rows
                         if r.get(s["config"]+"_model_ms") not in (None,"")])
        summary.append(dict(run=d.name,configuration=s["config"],architecture=display_name(s["config"]),status=s["status"],
            unit="crop" if s["config"] in ("fod","crack") else "detection" if s["config"]=="coordinates" else "frame",
            unique_inputs=len(set(r["input"] for r in rows)),
            unique_source_frames=len(set(r.get("source_frame",r["input"]) for r in rows)),
            measured_observations=len(rows),
            mean_ms=float(times.mean()) if len(times) else None,
            median_ms=float(np.median(times)) if len(times) else None,
            p95_ms=float(np.percentile(times,95)) if len(times) else None,
            max_ms=float(times.max()) if len(times) else None,
            processing_throughput_per_s=len(times)/(times.sum()/1000) if len(times) else None,
            coordinate_count=sum(int(r.get("coordinate_count") or 0) for r in rows),
            coordinate_ms_total=sum(float(r.get("coordinate_extraction_ms") or 0) for r in rows),
            coordinate_mean_ms_per_detection=(sum(float(r.get("coordinate_extraction_ms") or 0) for r in rows)/
                 sum(int(r.get("coordinate_count") or 0) for r in rows)) if sum(int(r.get("coordinate_count") or 0) for r in rows) else None,
            fod_calls=sum(int(r.get("fod_calls") or 0) for r in rows),
            crack_calls=sum(int(r.get("crack_calls") or 0) for r in rows),
            model_only_mean_ms=float(models.mean()) if len(models) else None,
            model_only_median_ms=float(np.median(models)) if len(models) else None,
            model_only_p95_ms=float(np.percentile(models,95)) if len(models) else None,
            model_only_max_ms=float(models.max()) if len(models) else None,
            model_only_throughput_per_s=len(models)/(models.sum()/1000) if len(models) else None,
            failures=json.dumps(s["failures"]),unprocessed=s.get("unprocessed_observations",0),
            peak_cuda_allocated_bytes=s.get("memory_after",{}).get("cuda_peak_allocated_bytes"),
            rss_bytes=s.get("memory_after",{}).get("rss_bytes")))
    csv_write(OUT/"summary.csv",summary)
    lines=["# FOD ARGUS laptop benchmarking","",
           "| Configuration | Status | Unit | Unique inputs | Observations | Mean ms | Median ms | P95 ms | Max ms | Throughput/s |",
           "|---|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    def fmt(v): return "" if v is None else f"{v:.3f}" if isinstance(v,float) else str(v)
    for r in summary:
        lines.append("| "+" | ".join((display_name(r["configuration"]) if k=="configuration" else fmt(r[k])) for k in ("configuration","status","unit","unique_inputs",
            "measured_observations","mean_ms","median_ms","p95_ms","max_ms","processing_throughput_per_s"))+" |")
    lines+=["","Throughput = completed observations / sum of directly measured processing seconds.",
            "Each row is one run; repetitions reuse the same unique inputs. Crop throughput is separate from frame throughput.",
            "See status.json for failures and unprocessed counts. No camera, Jetson, accuracy or 5 mm claims."]
    (OUT/"summary.md").write_text("\n".join(lines),encoding="utf-8")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--config",required=True,choices=["inventory","smoke","patchcore","crops","fod",
                                                        "crack","thermal","thermal_sampling","coordinates","sequential","sequential2","parallel","smoke_sequential2","report"])
    parser.add_argument("--repeats",type=int,default=1)
    parser.add_argument("--warmups",type=int,default=5)
    args=parser.parse_args()
    if args.repeats<1 or args.warmups<5: parser.error("At least 1 repeat and 5 warmups are required")
    run(args)



