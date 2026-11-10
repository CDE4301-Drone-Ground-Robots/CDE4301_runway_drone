"""Validate the proposed YOLO copy against the immutable source manifest."""
import argparse,csv,json,hashlib
from pathlib import Path
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor
import yaml
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument("--config",default=str(ROOT/"similarity_analysis/config.json"))
args=parser.parse_args()
cfg=json.loads(Path(args.config).read_text(encoding="utf-8-sig"))
OUT=ROOT/cfg["output"]
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
records=[json.loads(x) for x in (OUT/"manifest.jsonl").read_text().splitlines()]
target=(ROOT/cfg["corrected_destination"]).resolve()
assert target.is_relative_to(ROOT)
with open(OUT/"proposed_split.csv",newline="") as f: splits=list(csv.DictReader(f))
mapping=json.loads((OUT/"class_mapping.json").read_text())
dataset=yaml.safe_load((target/"dataset.yaml").read_text())
assert Path(dataset["path"]).resolve()==target
assert dataset["names"]=={v:k for k,v in mapping.items()}
def check(row):
    r=records[int(row["index"])]; s=row["split"]
    img=target/"images"/s/(r["id"]+".jpg"); lab=target/"labels"/s/(r["id"]+".txt")
    assert sha(img)==r["image_sha256"],f"Copied image changed: {img}"
    lines=[x.split() for x in lab.read_text().splitlines() if x.strip()]
    assert len(lines)==len(r["objects"])
    for line,o in zip(lines,r["objects"]):
        assert len(line)==5 and int(line[0])==mapping[o["class"]]
        values=list(map(float,line[1:])); a,b,c,d=o["xyxy"]; w,h=r["width"],r["height"]
        expected=[(a+c)/(2*w),(b+d)/(2*h),(c-a)/w,(d-b)/h]
        assert all(abs(x-y)<1e-9 for x,y in zip(values,expected))
        assert all(0<=v<=1 for v in values) and values[2]>0 and values[3]>0
    return s,len(lines)
counts=Counter(); boxes=Counter()
with ThreadPoolExecutor(max_workers=8) as pool:
    for i,(s,n) in enumerate(pool.map(check,splits),1):
        counts[s]+=1; boxes[s]+=n
        if i%2000==0:print(f"Validated {i}/{len(records)}",flush=True)
assert sum(counts.values())==len(records)
for s in ("train","val","test"):
    assert len(list((target/"images"/s).glob("*.jpg")))==counts[s]
    assert len(list((target/"labels"/s).glob("*.txt")))==counts[s]
by_index={int(row["index"]):row["split"] for row in splits}
groups=json.loads((OUT/"groups.json").read_text())
assert all(len({by_index[i] for i in g["members"]})==1 for g in groups)
blocks=json.loads((OUT/"allocation_blocks.json").read_text())
assert all(len({by_index[i] for i in b["members"]})==1 for b in blocks)
strong_cross=0
with open(OUT/"candidate_pairs.csv",newline="") as f:
    for pair in csv.DictReader(f):
        if pair["decision"]!="reject" and (int(pair["exact"]) or int(pair["provisional_strong"]) or pair["decision"]=="accept"):
            strong_cross+=by_index[int(pair["a"])]!=by_index[int(pair["b"])]
assert strong_cross==0
result=dict(status="passed",images=dict(counts),bounding_boxes=dict(boxes),
    groups_crossing_splits=0,strong_pairs_crossing_splits=strong_cross,allocation_blocks_crossing_splits=0,all_exported_images_sha256_verified=True,
    all_yolo_class_ids_and_boxes_verified=True,source_manifest_sha256=sha(OUT/"manifest.jsonl"),
    pipeline_sha256=sha(ROOT/"similarity_analysis/pipeline.py"))
(OUT/"export_validation.json").write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))

