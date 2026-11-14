"""Apply benchmark-only extension; archive the preceding benchmark implementation."""
import ast,json,shutil
from pathlib import Path
SUITE=Path(__file__).resolve().parent
ROOT=SUITE.parent
assert ROOT.name=="All_Model_Integration"
patches=json.loads((SUITE/"sequential2_patches.json").read_text(encoding="utf-8-sig"))
prepared={}
for name,changes in patches.items():
    target=SUITE/name
    assert target.resolve().parent==SUITE.resolve()
    text=target.read_text(encoding="utf-8-sig")
    for change in changes:
        if change["old"] not in text:raise RuntimeError("Missing extension anchor in "+name+": "+change["old"][:100])
        text=text.replace(change["old"],change["new"])
    if name.endswith(".py"):ast.parse(text,filename=str(target))
    prepared[name]=text
archive=ROOT/"benchmark_results"/"source_before_sequential2"
if archive.exists():raise RuntimeError("Refusing to overwrite previous source archive")
archive.mkdir()
for name in ("core.py","coordinates.py","finalize.py","routing_checks.py","run_all.py","METHODOLOGY.md","README.md","simulation.json"):
    shutil.copy2(SUITE/name,archive/name)
for name,text in prepared.items():
    (SUITE/name).write_text(text,encoding="utf-8")
notes=(SUITE/"sequential2_notes.md").read_text(encoding="utf-8-sig")
for name in ("README.md","METHODOLOGY.md"):
    with (SUITE/name).open("a",encoding="utf-8") as f:f.write(notes)
print("Applied benchmark-only Sequential 2 extension; previous benchmark source archived",flush=True)

