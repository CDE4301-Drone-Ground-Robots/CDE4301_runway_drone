"""Rename display labels only; preserve measurements and legacy run identifiers."""
from pathlib import Path
import ast,csv,hashlib,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
SUITE=ROOT/"benchmark_suite"; OUT=ROOT/"benchmark_results"
LABELS={"sequential2":"Sequential 1 (runs both models)",
        "sequential":"Sequential 2 (skips crack on FOD detection)","parallel":"Parallel"}
def swap(text):
    return re.sub(r"\bSequential ([12])\b",lambda m:"Sequential "+("2" if m[1]=="1" else "1"),text)
def readcsv(path):
    with path.open(newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def writecsv(path,rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def signature(rows):
    return {r["run"]:{k:v for k,v in r.items() if k!="architecture"} for r in rows}
def hashfile(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1048576),b""):h.update(b)
    return h.hexdigest()
archive=OUT/"source_before_label_rename"
if archive.exists():raise RuntimeError("Label rename already applied; refusing duplicate swap")
archive.mkdir()
for path in SUITE.iterdir():
    if path.is_file():shutil.copy2(path,archive/path.name)
csv_before={name:signature(readcsv(OUT/name)) for name in ("summary.csv","architecture_comparison.csv")}
raw_before={str(p.relative_to(OUT)):hashfile(p) for p in OUT.rglob("*")
            if p.is_file() and p.relative_to(OUT).parts[0] not in
            ("source_before_label_rename","source_before_sequential2") and len(p.relative_to(OUT).parts)>1}
module='"""Display names; raw run identifiers remain stable for provenance."""\nDISPLAY_NAMES='+repr(LABELS)+'\ndef display_name(config):\n    return DISPLAY_NAMES.get(config,config)\n'
(SUITE/"benchmark_labels.py").write_text(module,encoding="utf-8")
core=(SUITE/"core.py").read_text(encoding="utf-8-sig")
anchor="from coordinates import extract as extract_coordinates, remap_box, self_test"
assert anchor in core
core=core.replace(anchor,anchor+"\nfrom benchmark_labels import display_name")
anchor='summary.append(dict(run=d.name,configuration=s["config"],status=s["status"],'
assert anchor in core
core=core.replace(anchor,'summary.append(dict(run=d.name,configuration=s["config"],architecture=display_name(s["config"]),status=s["status"],')
anchor='fmt(r[k]) for k in ("configuration","status","unit","unique_inputs",'
assert anchor in core
core=core.replace(anchor,'(display_name(r["configuration"]) if k=="configuration" else fmt(r[k])) for k in ("configuration","status","unit","unique_inputs",')
ast.parse(core)
(SUITE/"core.py").write_text(core,encoding="utf-8")
finalize=swap((SUITE/"finalize.py").read_text(encoding="utf-8-sig"))
finalize=finalize.replace("from collections import Counter","from collections import Counter\nfrom benchmark_labels import display_name")
anchor='for config,label in (("sequential","Sequential 2 (fallback)"),("sequential2","Sequential 1"),("parallel","Parallel")):'
assert anchor in finalize
finalize=finalize.replace(anchor,'for config in ("sequential2","sequential","parallel"):\n    label=display_name(config)')
finalize=finalize.replace('join([config,','join([display_name(config),')
finalize=finalize.replace('for config in ("sequential","sequential2","parallel"):','for config in ("sequential2","sequential","parallel"):')
ast.parse(finalize)
(SUITE/"finalize.py").write_text(finalize,encoding="utf-8")
legend=(
"\nDisplay-label convention (renamed without rerunning inference):\n"
"- Sequential 1 runs YOLO then U-Net on every crop; legacy configuration ID: sequential2.\n"
"- Sequential 2 skips U-Net when YOLO detects FOD; legacy configuration ID: sequential.\n"
"- Parallel runs both concurrently; configuration ID: parallel.\n"
"Historical filenames, raw configuration IDs and measured values are retained unchanged.\n\n")
for name in ("README.md","METHODOLOGY.md","sequential2_notes.md"):
    path=SUITE/name
    text=swap(path.read_text(encoding="utf-8-sig"))
    first,sep,rest=text.partition("\n")
    path.write_text(first+"\n"+legend+rest,encoding="utf-8")
path=SUITE/"run_sequential2.py"
path.write_text(swap(path.read_text(encoding="utf-8-sig")),encoding="utf-8")
for name in ("summary.csv","architecture_comparison.csv"):
    rows=readcsv(OUT/name)
    for row in rows:row["architecture"]=LABELS.get(row["configuration"],row["configuration"])
    if name=="architecture_comparison.csv":
        rows.sort(key=lambda r:{"sequential2":0,"sequential":1,"parallel":2}.get(r["configuration"],3))
    writecsv(OUT/name,rows)
summary_path=OUT/"summary.md"
text=summary_path.read_text(encoding="utf-8-sig")
for config,label in LABELS.items():text=text.replace("| "+config+" |","| "+label+" |")
summary_path.write_text(text,encoding="utf-8")
subprocess.run([sys.executable,"-B",str(SUITE/"finalize.py")],cwd=ROOT,check=True)
for name,before in csv_before.items():
    assert signature(readcsv(OUT/name))==before,"Measurement fields changed: "+name
for relative,expected in raw_before.items():
    assert hashfile(OUT/relative)==expected,"Historical raw artifact changed: "+relative
print("Renamed display labels; all measurement fields and historical raw artifacts verified unchanged",flush=True)

