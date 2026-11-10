"""Fresh laptop runs, serial configurations, finite thermal replay; no camera/services."""
from pathlib import Path
import csv,json,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
SUITE=Path(__file__).resolve().parent
OUT=ROOT/"benchmark_results"
OUT.mkdir(exist_ok=True)

def latest(config):
    dirs=sorted(d for d in OUT.iterdir() if d.is_dir() and d.name.endswith("_"+config) and (d/"status.json").exists())
    return dirs[-1] if dirs else None

def one(config,repeats=1):
    print("START",config,"passes",repeats,flush=True)
    with (OUT/(config+"_passes_"+str(repeats)+".log")).open("w",encoding="utf-8") as log:
        proc=subprocess.Popen([sys.executable,"-B",str(SUITE/"core.py"),"--config",config,
                               "--repeats",str(repeats)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
        try:proc.wait(timeout=900)
        except subprocess.TimeoutExpired:
            proc.kill();proc.wait()
            d=latest(config)
            if d:
                s=json.loads((d/"status.json").read_text(encoding="utf-8-sig"))
                rows=[]
                if (d/"raw_timings.csv").exists():
                    with (d/"raw_timings.csv").open(newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
                completed=sum(r["status"]=="ok" for r in rows)
                s.update(status="stopped_timeout",completed=completed,
                    unprocessed_observations=max(0,s.get("selected_inputs",0)*repeats-completed),
                    failures=[dict(error="Exceeded 900 seconds including loading; partial timings preserved")])
                (d/"status.json").write_text(json.dumps(s,indent=2),encoding="utf-8")
    d=latest(config)
    if not d:raise RuntimeError("No status record for "+config)
    s=json.loads((d/"status.json").read_text(encoding="utf-8-sig"))
    elapsed=0.
    if (d/"raw_timings.csv").exists():
        with (d/"raw_timings.csv").open(newline="",encoding="utf-8") as f:
            elapsed=sum(float(r["total_ms"])/1000 for r in csv.DictReader(f) if r["status"]=="ok")
    print("FINISH",config,s["status"],"observations",s["completed"],"measured_seconds",round(elapsed,6),flush=True)
    return s["status"]=="completed",elapsed

if __name__=="__main__":
    ok,_=one("inventory")
    if not ok:raise RuntimeError("Inventory failed; diagnose before proceeding")
    # Route checks use mocks only for correctness, never as timing samples.
    if not (OUT/"routing_checks.json").exists():
        subprocess.run([sys.executable,"-B",str(SUITE/"routing_checks.py")],cwd=ROOT,check=True)
    ok,_=one("smoke")
    if not ok:raise RuntimeError("Smoke test failed; diagnose before proceeding")
    crops_ok,_=one("crops")
    configs=("patchcore","fod","crack","coordinates","thermal_sampling","thermal","sequential","sequential2","parallel")
    initial={}
    for config in configs:
        if not crops_ok and config in ("fod","crack","coordinates","sequential","sequential2","parallel"):
            print("BLOCKED",config,"requires real anomaly crops",flush=True);continue
        initial[config]=one(config)
    for config,(ok,elapsed) in initial.items():
        if ok and elapsed<=60:one(config,3)
        else:print("NO REPEATS",config,"first pass failed or exceeded 60 measured seconds",flush=True)
    one("report")
    subprocess.run([sys.executable,"-B",str(SUITE/"finalize.py")],cwd=ROOT,check=True)

