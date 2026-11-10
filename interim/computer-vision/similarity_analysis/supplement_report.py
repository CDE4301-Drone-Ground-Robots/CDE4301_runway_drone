"""Extra diagnostics and review pages; run after pipeline.py report."""
import argparse,json,csv,random,html
from pathlib import Path
from collections import Counter
import numpy as np
from PIL import Image,ImageDraw,ImageOps
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument("--config",default=str(ROOT/"similarity_analysis/config.json"))
args=parser.parse_args()
cfg=json.loads(Path(args.config).read_text(encoding="utf-8-sig"))
OUT=ROOT/cfg["output"]
records=[json.loads(s) for s in (OUT/"manifest.jsonl").read_text().splitlines()]
summary=json.loads((OUT/"analysis_summary.json").read_text())
split_summary=json.loads((OUT/"split_summary.json").read_text())
blocks=json.loads((OUT/"allocation_blocks.json").read_text())
with open(OUT/"proposed_split.csv",newline="") as f: assignment=list(csv.DictReader(f))
splits={int(r["index"]):r["split"] for r in assignment}
with open(OUT/"candidate_pairs.csv",newline="") as f: pairs=list(csv.DictReader(f))
cross=[p for p in pairs if splits[int(p["a"])]!=splits[int(p["b"])]]
cross.sort(key=lambda p:(-float(p["cosine"]),int(p["phash_distance"])))
with open(OUT/"remaining_cross_split_candidates.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(pairs[0])+["split_a","split_b"]); w.writeheader()
    for p in cross:w.writerow(dict(p,split_a=splits[int(p["a"])],split_b=splits[int(p["b"])]))
e=np.load(OUT/"embeddings.npy",mmap_mode="r")
# Contextual distributions: uniform ordered non-self random pairs.
rng=np.random.default_rng(4301); sample_size=100000
a=rng.integers(len(records),size=sample_size); b=rng.integers(len(records)-1,size=sample_size); b+=b>=a
cos=np.einsum("ij,ij->i",e[a],e[b])
hashes=[int(r["phash"],16) for r in records]
ham=np.array([(hashes[i]^hashes[j]).bit_count() for i,j in zip(a,b)])
np.savez_compressed(OUT/"random_pair_sample.npz",a=a,b=b,cosines=cos,phash_distance=ham)
knn=np.load(OUT/"knn.npz")
fig,ax=plt.subplots(1,2,figsize=(12,4))
ax[0].hist(ham,bins=np.arange(66)-.5,density=True,alpha=.6,label="Uniform random pairs")
ax[0].axvline(4,color="red",label="Provisional strong hash cutoff")
ax[0].set(xlabel="pHash Hamming distance",ylabel="Density");ax[0].legend()
ax[1].hist(cos,bins=80,density=True,alpha=.5,label="Uniform random pairs")
ax[1].hist(knn["cosines"][:,0],bins=80,density=True,alpha=.5,label="Nearest neighbours")
ax[1].axvline(cfg.get("dino_alone_cosine",cfg["strong_cosine"]),color="red",label="DINO-only strong cutoff")
ax[1].set(xlabel="DINOv2 cosine",ylabel="Density");ax[1].legend()
fig.tight_layout();fig.savefig(OUT/"random_vs_nearest.png",dpi=150);plt.close(fig)
def image_path(r):
    p=(ROOT/r["image"]).resolve()
    assert p.is_relative_to(ROOT)
    return p
def tile(indices,filename):
    columns=min(4,len(indices)); rows=(len(indices)+columns-1)//columns
    canvas=Image.new("RGB",(columns*240,rows*270),"white"); d=ImageDraw.Draw(canvas)
    for pos,i in enumerate(indices):
        x,y=(pos%columns)*240,(pos//columns)*270
        with Image.open(image_path(records[i])) as im:canvas.paste(ImageOps.contain(im.convert("RGB"),(240,240)),(x,y))
        d.text((x+4,y+245),f'{i} | {splits[i]}',fill="black")
    canvas.save(OUT/"gallery"/filename,quality=90)
page=['<!doctype html><meta charset="utf-8"><title>Allocation and remaining match review</title><style>body{font:16px sans-serif;max-width:1100px;margin:30px auto}img{max-width:100%}section{border:1px solid #ccc;padding:12px;margin:15px 0}</style>',
      '<h1>Allocation constraints and remaining cross-split matches</h1><p>These blocks are split co-location constraints, not claimed source videos. Compact pairwise-evidence groups remain distinct. A chain of strong edges can put unrelated scenes in the same split; this conservatively avoids separating strong matches.</p>',
      '<p>The following are sampled representatives, not exhaustive manual verification. Uncertain cross-split matches may still be correlated. Review thresholds and extend pair decisions before training.</p>']
metrics=[]
for block in sorted(blocks,key=lambda b:-b["size"])[:40]:
    members=block["members"]; z=e[members]; matrix=z@z.T; i,j=np.unravel_index(np.argmin(matrix),matrix.shape)
    indices=sorted(set([members[int(k)] for k in np.linspace(0,len(members)-1,6)]+[members[i],members[j]]))
    filename=block["block_id"]+"_allocation.jpg";tile(indices,filename)
    metrics.append(dict(block_id=block["block_id"],size=block["size"],minimum_pairwise_cosine=float(matrix[i,j]),
        split=splits[members[0]],farthest_a=members[i],farthest_b=members[j]))
    page.append(f'<section><h2>{block["block_id"]}: {block["size"]} images; {splits[members[0]]}</h2><p>Minimum pairwise cosine: {matrix[i,j]:.4f}. Representatives include a farthest pair; low cohesion warrants review.</p><img loading="lazy" src="gallery/{filename}"></section>')
page.append('<h1>Highest cosine matches remaining across splits</h1><p>Showing the top 40 retrieved cross-split candidates. These examples are deliberately difficult, not a random sample. Full list: remaining_cross_split_candidates.csv.</p>')
for k,p in enumerate(cross[:40]):
    a,b=int(p["a"]),int(p["b"]);filename=f"remaining_cross_{k:03d}.jpg";tile([a,b],filename)
    page.append(f'<section><p>indices {a}, {b}; pHash {p["phash_distance"]}/64; cosine {p["cosine"]}</p><img loading="lazy" src="gallery/{filename}"></section>')
(OUT/"allocation_review.html").write_text("\n".join(page),encoding="utf-8")
(OUT/"largest_block_cohesion.json").write_text(json.dumps(metrics,indent=2))
with open(OUT/"class_distribution.csv",newline="") as f: classes=list(csv.DictReader(f))
missing=[dict(name=r["name"],split=s) for r in classes for s in ("train","val","test") if int(r[s])==0]
risk=dict(remaining_cross_split_candidate_pairs=len(cross),
    dino_high_cross_pairs=sum(float(p["cosine"])>=cfg.get("dino_alone_cosine",cfg["strong_cosine"]) for p in cross),
    strong_joint_cross_pairs=summary["proposed_similarity_aware"]["provisional_strong_pairs_crossing"],
    classes_missing_from_splits=missing,
    minimum_allocation_blocks_per_class=min(int(r["allocation_blocks_with_class"]) for r in classes),
    random_pair_cosine_quantiles={str(q):float(np.quantile(cos,q)) for q in (0,.25,.5,.75,.95,.99,1)})
(OUT/"additional_diagnostics.json").write_text(json.dumps(risk,indent=2))
before=summary["illustrative_random"];after=summary["proposed_similarity_aware"]
text=["# Review summary","",
"PROVISIONAL: the exported dataset is a review copy. YOLO training has not started.","",
f'{summary["images"]:,} images; {summary["boxes"]:,} boxes; {len(classes)} classes.',
f'Byte-identical images: {summary["byte_identical_images"]:,}. Provisional strong-rule near-duplicate images: {summary["provisional_near_duplicate_images"]:,}.',
f'Candidate pairs: {summary["candidate_pairs"]:,}; compact non-singleton candidate groups: {summary["candidate_non_singleton_groups"]:,}.',
f'Allocation blocks including singletons: {len(blocks):,}; largest block: {max(b["size"] for b in blocks)} images.',
"Original split-spanning groups: unavailable; previous split manifests were not provided.","",
"| Split | Images | Percentage |","|---|---:|---:|"]
for s in ("train","val","test"):
    n=split_summary["images"][s];text.append(f'| {s} | {n:,} | {100*n/len(records):.2f}% |')
text+=["","| Cross-split measure | Illustrative random baseline | Proposed split |","|---|---:|---:|",
    f'| Strong configured-rule pairs | {before["provisional_strong_pairs_crossing"]:,} | {after["provisional_strong_pairs_crossing"]:,} |',
    f'| All retrieved candidate pairs | {before["candidate_pairs_crossing"]:,} | {after["candidate_pairs_crossing"]:,} |',
    f'| Median nearest cross-split cosine | {before["cross_nearest_cosine_quantiles"]["0.5"]:.4f} | {after["cross_nearest_cosine_quantiles"]["0.5"]:.4f} |',
    f'| Images with cross-split nearest cosine >= {cfg["strong_cosine"]} | {before["cross_nearest_cosine_above_strong"]:,} | {after["cross_nearest_cosine_above_strong"]:,} |',"",
    "The baseline is a new seeded random split, not your historical split. Cosine alone does not confirm common video origin.",
    f'{len(cross):,} retrieved weaker/uncertain candidate pairs still cross splits; {risk["dino_high_cross_pairs"]:,} meet the DINO-only cutoff.',
    "Zero configured strong-rule crossings is a threshold-specific result, not proof of no leakage.",
    "Compact groups use complete pairwise evidence to avoid weak-chain scene merging. Additional same-split constraints",
    "link strong matches between compact groups. These allocation blocks do not assert source-video identity.","",
    f'Classes absent from a split: {len(missing)}. Minimum class support: {risk["minimum_allocation_blocks_per_class"]} allocation blocks.',
    "See class_distribution.csv for per-class box counts, image counts and allocation-block support.",
    "The allocation optimizes class box proportions and image proportions; grouped scenes can prevent exact 70/15/15 class ratios.","",
    "Open [review.html](review.html) for stratified match examples and compact groups.",
    "Open [allocation_review.html](allocation_review.html) for large allocation blocks and remaining cross-split matches.",
    "Read [REPORT.md](REPORT.md) for method, threshold rationale, annotation conversion, provenance and limitations.",
    "Training and evaluation commands are in ../README.md. Freeze the reviewed split before training.",
    "New numeric class IDs are alphabetical because historical IDs are unavailable. YOLO labels preserve source class names through that mapping.",
    "The result is similarity-aware, NOT guaranteed video-independent."]
(OUT/"REVIEW_SUMMARY.md").write_text("\n".join(text)+"\n",encoding="utf-8")
p=OUT/"review.html";s=p.read_text(encoding="utf-8")
link='<p><a href="allocation_review.html">Review allocation blocks and remaining cross-split matches</a></p>'
if link not in s:p.write_text(s.replace("<h1>Similarity review: provisional evidence</h1>","<h1>Similarity review: provisional evidence</h1>"+link),encoding="utf-8")
print(json.dumps(risk,indent=2),flush=True)

