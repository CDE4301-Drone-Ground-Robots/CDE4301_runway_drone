"""Benchmark only Sequential 1; retain earlier two architectures and collate."""
from pathlib import Path
import csv,hashlib,importlib.metadata,json,re,subprocess,sys
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent.parent
SUITE=Path(__file__).resolve().parent
OUT=ROOT/"benchmark_results"
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1048576),b""):h.update(b)
    return h.hexdigest()
def read(path):return json.loads(path.read_text(encoding="utf-8-sig"))
def normalize(name):return re.sub(r"[-_.]+","-",name).lower()
def preflight():
    import torch
    old=read(OUT/"machine_software_settings.json")
    baseline=read(OUT/"preservation_baseline.json")
    changed=[name for name,value in baseline.items() if not (ROOT/name).is_file() or sha(ROOT/name)!=value]
    if changed:raise RuntimeError("Original-file baseline differs; stopping: "+repr(changed))
    current={d.metadata["Name"]:d.version for d in importlib.metadata.distributions()}
    previous={normalize(k):v for k,v in old["packages"].items()}
    versions={normalize(k):v for k,v in current.items()}
    required=("torch","torchvision","ultralytics","anomalib","segmentation-models-pytorch",
              "numpy","opencv-python","pillow-heif","psutil")
    differences={name:dict(previous=previous.get(name),current=versions.get(name))
                 for name in required if previous.get(name)!=versions.get(name)}
    same_simulation=read(SUITE/"simulation.json")==read(OUT/"simulation_settings.json")
    current_gpu=torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    same_device=(torch.cuda.is_available()==old["cuda_available"] and torch.version.cuda==old["torch_cuda"]
                 and current_gpu==old.get("gpu",{}).get("name"))
    if differences or not same_simulation or not same_device:
        raise RuntimeError("Comparison settings differ: "+repr(dict(packages=differences,
                           same_simulation=same_simulation,same_device=same_device)))
    snapshot=dict(label="Sequential 1 extension session; earlier two runs retained",
        utc=datetime.now(timezone.utc).isoformat(),python=sys.executable,packages=current,
        cuda_available=torch.cuda.is_available(),torch_cuda=torch.version.cuda,gpu=current_gpu,
        originals_verified=len(baseline),simulation=read(SUITE/"simulation.json"),
        previous_results="Existing fallback and parallel timing rows are retained, not rerun",
        limit="Cross-session background load and clocks were not isolated")
    try:snapshot["nvidia_smi"]=subprocess.check_output(["nvidia-smi"],text=True,timeout=20)
    except Exception as exc:snapshot["nvidia_smi"]=repr(exc)
    (OUT/"sequential2_session.json").write_text(json.dumps(snapshot,indent=2),encoding="utf-8")
    print("PREFLIGHT: inputs, models, relevant package versions, CUDA/device and simulated geometry match",flush=True)
if __name__=="__main__":
    if "--preflight" in sys.argv:
        preflight()
    else:
        from run_all import one
        subprocess.run([sys.executable,"-B",str(Path(__file__)),"--preflight"],cwd=ROOT,check=True)
        subprocess.run([sys.executable,"-B",str(SUITE/"routing_checks.py")],cwd=ROOT,check=True)
        ok,_=one("smoke_sequential2")
        if not ok:raise RuntimeError("Sequential 1 smoke failed; diagnose before timing")
        ok,elapsed=one("sequential2",1)
        if ok and elapsed<=60:one("sequential2",3)
        else:print("No repeated pass: initial failure or more than 60 measured seconds",flush=True)
        one("report")
        subprocess.run([sys.executable,"-B",str(SUITE/"finalize.py")],cwd=ROOT,check=True)

