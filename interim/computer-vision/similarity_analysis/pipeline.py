"""Reproducible similarity-aware VOC -> YOLO audit. Never trains a model."""
import os, sys, json, csv, hashlib, argparse, time, random, shutil, platform
from pathlib import Path
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
os.environ["TORCH_HOME"] = str(HERE / "cache" / "torch")
os.environ["HF_HOME"] = str(HERE / "cache" / "huggingface")
os.environ["MPLCONFIGDIR"] = str(HERE / "cache" / "matplotlib")
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

def confined(path):
    p = Path(path).resolve()
    if not p.is_relative_to(ROOT): raise ValueError(f"Outside workspace: {p}")
    return p

def digest(path):
    h = hashlib.sha256()
    with open(confined(path), "rb") as f:
        for b in iter(lambda: f.read(1048576), b""): h.update(b)
    return h.hexdigest()

def save_json(path, data):
    path = confined(path); path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2), encoding="utf-8"); temp.replace(path)

def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8-sig"))

def is_strong_pair(cfg, phash_distance, cosine):
    """Return the configured split co-location decision for one image pair."""
    rule = cfg.get("strong_rule", "joint")
    if rule == "joint":
        return phash_distance <= cfg["strong_phash"] and cosine >= cfg["strong_cosine"]
    if rule == "strict_union":
        return (cosine >= cfg["dino_alone_cosine"] or
                (phash_distance <= cfg["strong_phash"] and cosine >= cfg["strong_cosine"]))
    raise ValueError(f"Unknown strong_rule: {rule}")

def strong_rule_description(cfg):
    if cfg.get("strong_rule", "joint") == "joint":
        return (f'pHash <= {cfg["strong_phash"]} AND '
                f'DINO cosine >= {cfg["strong_cosine"]}')
    return (f'DINO cosine >= {cfg["dino_alone_cosine"]} OR '
            f'(pHash <= {cfg["strong_phash"]} AND '
            f'DINO cosine >= {cfg["strong_cosine"]})')
def write_csv(path, rows, fields):
    with open(confined(path), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

def load_manifest(out):
    return [json.loads(x) for x in (out/"manifest.jsonl").read_text(encoding="utf-8").splitlines()]

def audit_one(item):
    import numpy as np
    from PIL import Image
    from scipy.fft import dctn
    idx, image, annotation = item
    x = ET.parse(annotation).getroot()
    with Image.open(image) as im:
        im.load(); width, height = im.size
        if im.size != (int(x.findtext("size/width")), int(x.findtext("size/height"))):
            raise ValueError(f"Image/XML dimensions disagree: {image.name}")
        pixels = np.asarray(im.convert("L").resize((32,32), Image.Resampling.LANCZOS), dtype=float)
    coeff = dctn(pixels, type=2, norm="ortho")[:8,:8].flatten()
    # Exclude DC from the threshold; force the DC hash bit off.
    bits = coeff > np.median(coeff[1:]); bits[0] = False
    phash = sum(int(b) << i for i,b in enumerate(bits))
    objects = []
    for o in x.findall("object"):
        box = [float(o.findtext("bndbox/"+k)) for k in ("xmin","ymin","xmax","ymax")]
        if not (0 <= box[0] < box[2] <= width and 0 <= box[1] < box[3] <= height):
            raise ValueError(f"Invalid box: {annotation.name}: {box}")
        objects.append({"class":o.findtext("name"),"xyxy":box,"difficult":o.findtext("difficult","0")})
    if x.findtext("filename") != image.name: raise ValueError("XML filename mismatch")
    return dict(index=idx,id=image.stem,image=str(image.relative_to(ROOT)).replace("\\","/"),
        annotation=str(annotation.relative_to(ROOT)).replace("\\","/"),
        image_sha256=digest(image),annotation_sha256=digest(annotation),
        width=width,height=height,phash=f"{phash:016x}",objects=objects,original_split=None)

def inventory(cfg, out):
    base = confined(ROOT/cfg["source"])
    images = sorted((base/"JPEGImages").glob("*.jpg"))
    anns = {p.stem:p for p in (base/"Annotations").glob("*.xml")}
    if {p.stem for p in images} != set(anns): raise ValueError("Unpaired images/annotations")
    signature = hashlib.sha256("\n".join(str(p.relative_to(ROOT)) for p in images).encode()).hexdigest()
    stamp = out/"inventory_inputs.json"
    if stamp.exists() and read_json(stamp)["path_signature"] != signature:
        raise ValueError("Source paths changed; use a new output directory")
    save_json(stamp,dict(path_signature=signature,count=len(images),config=cfg))
    manifest = out/"manifest.jsonl"
    previous = load_manifest(out) if manifest.exists() else []
    for i,row in enumerate(previous):
        if row["index"]!=i or row["id"]!=images[i].stem: raise ValueError("Invalid resume order")
    tasks = [(i,p,anns[p.stem]) for i,p in enumerate(images) if i>=len(previous)]
    print(f"Inventory/pHash: {len(previous)}/{len(images)} already complete",flush=True)
    with open(manifest,"a",encoding="utf-8") as f, ThreadPoolExecutor(max_workers=cfg["io_workers"]) as pool:
        for row in pool.map(audit_one,tasks):
            f.write(json.dumps(row)+"\n"); f.flush(); previous.append(row)
            if len(previous)%500==0: print(f"Inventory/pHash {len(previous)}/{len(images)}",flush=True)
    classes = Counter(o["class"] for r in previous for o in r["objects"])
    mapping = {name:i for i,name in enumerate(sorted(classes))}
    save_json(out/"class_mapping.json",mapping)
    stats = dict(images=len(previous),annotation_files=len(previous),bounding_boxes=sum(classes.values()),
        classes=dict(sorted(classes.items())),mapping_policy="Alphabetical new IDs; historical IDs unavailable",
        original_splits_available=False,synthetic_images=False,verified_pairs=len(previous),
        image_sizes=dict(Counter(f'{r["width"]}x{r["height"]}' for r in previous)))
    save_json(out/"inventory.json",stats)
    save_json(out/"manifest_identity.json",dict(sha256=digest(manifest)))
    print(json.dumps(stats,indent=2),flush=True)

def embeddings(cfg,out):
    import numpy as np
    import torch
    from torchvision import transforms
    from PIL import Image
    import urllib.request
    records=load_manifest(out); n=len(records)
    lock=HERE/"model_lock.json"
    if not lock.exists():
        request=urllib.request.Request("https://api.github.com/repos/facebookresearch/dinov2/commits/main",
                                     headers={"User-Agent":"FOD-similarity-audit"})
        with urllib.request.urlopen(request,timeout=60) as response: revision=json.load(response)["sha"]
        save_json(lock,dict(repository="facebookresearch/dinov2",revision=revision,model="dinov2_vits14"))
    model_info=read_json(lock)
    fingerprint=dict(manifest=digest(out/"manifest.jsonl"),model=model_info,
        transform="RGB resize 224x224 bicubic ImageNet normalization; L2-normalized CLS",dimension=384)
    statepath=out/"embedding_state.json"; target=out/"embeddings.npy"
    done=0
    if statepath.exists():
        state=read_json(statepath)
        if state["fingerprint"]!=fingerprint: raise ValueError("Embedding inputs changed")
        done=state["completed"]
    device="cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(cfg["seed"]); torch.set_num_threads(cfg["cpu_threads"])
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False
    torch.backends.cudnn.benchmark=False
    print(f"DINOv2 {model_info['revision']} {device}, resume {done}/{n}",flush=True)
    if done==n: return
    model=torch.hub.load(f"facebookresearch/dinov2:{model_info['revision']}",
                         model_info["model"],pretrained=True,trust_repo=True,skip_validation=True)
    model=model.eval().to(device)
    for p in model.parameters(): p.requires_grad_(False)
    transform=transforms.Compose([transforms.Resize((224,224),interpolation=transforms.InterpolationMode.BICUBIC),
        transforms.ToTensor(),transforms.Normalize((.485,.456,.406),(.229,.224,.225))])
    def read_image(r):
        with Image.open(confined(ROOT/r["image"])) as im: return transform(im.convert("RGB"))
    e=np.lib.format.open_memmap(target,mode="r+" if target.exists() else "w+",dtype="float32",shape=(n,384))
    started=time.time()
    with ThreadPoolExecutor(max_workers=cfg["io_workers"]) as pool,torch.inference_mode():
        for a in range(done,n,cfg["batch_size"]):
            b=min(a+cfg["batch_size"],n)
            batch=torch.stack(list(pool.map(read_image,records[a:b]))).to(device)
            z=model(batch); z=torch.nn.functional.normalize(z.float(),dim=1)
            e[a:b]=z.cpu().numpy(); e.flush()
            save_json(statepath,dict(fingerprint=fingerprint,completed=b,total=n))
            print(f"DINOv2 {b}/{n}; session {time.time()-started:.1f}s",flush=True)
    save_json(out/"environment.json",dict(python=sys.version,platform=platform.platform(),
        torch=torch.__version__,numpy=np.__version__,device=device,
        gpu=torch.cuda.get_device_name(0) if device=="cuda" else None,
        model=model_info,weight_files={str(p.relative_to(HERE)):digest(p) for p in (HERE/"cache/torch/hub/checkpoints").glob("*") if p.is_file()}))

class BKTree:
    def __init__(self): self.nodes=[]
    def add(self,value,index):
        if not self.nodes: self.nodes.append([value,[index],{}]); return
        node=0
        while True:
            v,indices,children=self.nodes[node]; d=(value^v).bit_count()
            if d==0: indices.append(index); return
            if d not in children:
                children[d]=len(self.nodes); self.nodes.append([value,[index],{}]); return
            node=children[d]
    def query(self,value,radius):
        if not self.nodes: return
        stack=[0]
        while stack:
            v,indices,children=self.nodes[stack.pop()]; d=(value^v).bit_count()
            if d<=radius:
                for i in indices: yield i,d
            stack.extend(j for distance,j in children.items() if d-radius<=distance<=d+radius)

def cosine_knn(e,k,block,allowed=None):
    # Exact search: float32 GPU/CPU matrix multiply in blocks, bounded memory.
    import torch
    import numpy as np
    device="cuda" if torch.cuda.is_available() else "cpu"
    torch.set_num_threads(4)
    torch.backends.cuda.matmul.allow_tf32=False
    t=torch.tensor(np.asarray(e),device=device)
    n=len(e); ids=np.empty((n,k),dtype=np.int32); scores=np.empty((n,k),dtype=np.float32)
    with torch.inference_mode():
        for a in range(0,n,block):
            b=min(n,a+block); sim=t[a:b]@t.T
            sim[torch.arange(b-a,device=device),torch.arange(a,b,device=device)]=-float("inf")
            if allowed is not None:
                # Cross-split only: nearest image in any other split.
                mask=torch.tensor(allowed[a:b,None]!=allowed[None,:],device=device)
                sim.masked_fill_(~mask,-float("inf"))
            val,ix=sim.topk(k,dim=1)
            scores[a:b]=val.cpu().numpy(); ids[a:b]=ix.cpu().numpy()
            if a%(block*16)==0: print(f"Exact cosine search {b}/{n}",flush=True)
    return ids,scores

def neighbours(cfg,out):
    import numpy as np
    records=load_manifest(out); hashes=[int(r["phash"],16) for r in records]
    e=np.load(out/"embeddings.npy",mmap_mode="r")
    state=read_json(out/"embedding_state.json")
    if state["completed"]!=len(records): raise ValueError("Incomplete embeddings")
    if state["fingerprint"]["manifest"]!=digest(out/"manifest.jsonl"): raise ValueError("Stale embeddings")
    pairs={}; tree=BKTree()
    for i,h in enumerate(hashes):
        for j,d in tree.query(h,cfg["phash_radius"]): pairs[(j,i)]=d
        tree.add(h,i)
        if i%2000==0: print(f"pHash search {i}/{len(records)}; {len(pairs)} pairs",flush=True)
    ix,sc=cosine_knn(e,min(cfg["knn_k"],len(e)-1),cfg["search_block"])
    np.savez_compressed(out/"knn.npz",indices=ix,cosines=sc)
    for i in range(len(e)):
        for j in ix[i]:
            a,b=sorted((i,int(j))); pairs[(a,b)]=(hashes[a]^hashes[b]).bit_count()
    # Include all byte-identical pairs even if hash search settings change.
    exact=defaultdict(list)
    for i,r in enumerate(records): exact[r["image_sha256"]].append(i)
    for group in exact.values():
        for p,i in enumerate(group):
            for j in group[p+1:]: pairs[(i,j)]=0
    review=out/"pair_decisions.csv"
    if not review.exists(): write_csv(review,[],["a","b","decision","note"])
    decisions={}
    with open(review,encoding="utf-8-sig",newline="") as f:
        for row in csv.DictReader(f):
            if row["decision"] not in ("accept","reject",""): raise ValueError("Decision must be accept/reject/blank")
            if row["decision"]: decisions[tuple(sorted((int(row["a"]),int(row["b"]))))]=row["decision"]
    for a,b in decisions:
        if not (0<=a<b<len(e)): raise ValueError("Invalid review indices")
        pairs[(a,b)]=(hashes[a]^hashes[b]).bit_count()
    rows=[]
    for (a,b),h in sorted(pairs.items()):
        c=float(np.clip(e[a]@e[b],-1,1)); exact_match=records[a]["image_sha256"]==records[b]["image_sha256"]
        strong=is_strong_pair(cfg,h,c)
        candidate=h<=cfg["phash_radius"] or c>=cfg["review_cosine"]
        if exact_match or candidate or (a,b) in decisions:
            rows.append(dict(a=a,b=b,id_a=records[a]["id"],id_b=records[b]["id"],phash_distance=h,
                cosine=f"{c:.8f}",exact=int(exact_match),provisional_strong=int(strong),
                decision=decisions.get((a,b),"")))
    write_csv(out/"candidate_pairs.csv",rows,
        ["a","b","id_a","id_b","phash_distance","cosine","exact","provisional_strong","decision"])
    save_json(out/"neighbour_config.json",dict(config=cfg,manifest=digest(out/"manifest.jsonl")))
    print(f"Saved {len(rows)} candidate pairs",flush=True)

def read_pairs(out):
    with open(out/"candidate_pairs.csv",encoding="utf-8",newline="") as f: return list(csv.DictReader(f))

def groups(cfg,out):
    records=load_manifest(out); pairs=read_pairs(out); n=len(records)
    adjacency=[set() for _ in records]; edges=[]; rejected=set()
    for p in pairs:
        a,b=int(p["a"]),int(p["b"])
        if p["decision"]=="reject":
            if int(p["exact"]): raise ValueError("Byte-identical images cannot be separated; review conflict")
            rejected.add((a,b)); continue
        if int(p["exact"]) or int(p["provisional_strong"]) or p["decision"]=="accept":
            adjacency[a].add(b); adjacency[b].add(a)
            edges.append((int(p["exact"]),p["decision"]=="accept",float(p["cosine"]),-int(p["phash_distance"]),a,b))
    membership=list(range(n)); clusters={i:{i} for i in range(n)}; blocked=[]
    # Every pair in a proposed cluster must carry strong/explicitly accepted evidence.
    for _,_,_,_,a,b in sorted(edges,reverse=True):
        ga,gb=membership[a],membership[b]
        if ga==gb: continue
        left,right=clusters[ga],clusters[gb]
        if not all(right.issubset(adjacency[x]) for x in left):
            blocked.append(dict(a=a,b=b,reason="complete-link constraint prevents weak chaining")); continue
        if len(left)<len(right): ga,gb=gb,ga; left,right=right,left
        for x in right: membership[x]=ga
        left.update(right); del clusters[gb]
    result=[]
    for members in sorted(clusters.values(),key=lambda s:min(s)):
        ordered=sorted(members); sha={records[i]["image_sha256"] for i in ordered}
        result.append(dict(group_id=f"g{ordered[0]:06d}",members=ordered,size=len(ordered),
            status="byte_identical" if len(sha)==1 and len(ordered)>1 else
                   ("provisional_needs_review" if len(ordered)>1 else "singleton")))
    save_json(out/"groups.json",result); save_json(out/"blocked_merges.json",blocked)
    write_csv(out/"group_members.csv",
        [dict(group_id=g["group_id"],index=i,image_id=records[i]["id"],status=g["status"]) for g in result for i in g["members"]],
        ["group_id","index","image_id","status"])
    print(f"Groups: {len(result)} including {sum(g['size']>1 for g in result)} non-singleton; blocked edges {len(blocked)}",flush=True)

def allocation_blocks(out,records):
    # Co-location constraints, NOT scene/video identity groups. No weak edges.
    parent=list(range(len(records)))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def join(a,b):
        a,b=find(a),find(b)
        if a!=b: parent[max(a,b)]=min(a,b)
    for g in read_json(out/"groups.json"):
        for i in g["members"][1:]: join(g["members"][0],i)
    for p in read_pairs(out):
        if p["decision"]!="reject" and (int(p["exact"]) or int(p["provisional_strong"]) or p["decision"]=="accept"):
            join(int(p["a"]),int(p["b"]))
    components=defaultdict(list)
    for i in range(len(records)): components[find(i)].append(i)
    return [dict(block_id=f"b{min(v):06d}",members=v,size=len(v))
            for v in sorted(components.values(),key=min)]

def propose(cfg,out):
    import numpy as np
    records=load_manifest(out); compact=read_json(out/"groups.json")
    names=read_json(out/"class_mapping.json"); blocks=allocation_blocks(out,records)
    save_json(out/"allocation_blocks.json",blocks)
    group_lookup={i:g["group_id"] for g in compact for i in g["members"]}
    c=len(names); n=len(records); vectors=[]
    for block in blocks:
        v=np.zeros(c)
        for i in block["members"]:
            for o in records[i]["objects"]: v[names[o["class"]]]+=1
        vectors.append(v)
    vectors=np.asarray(vectors); totals=vectors.sum(0)
    fractions=np.array(cfg["split_fractions"]); target_n=fractions*n; target_c=fractions[:,None]*totals[None,:]
    best=None
    for attempt in range(cfg["split_restarts"]):
        rng=random.Random(cfg["seed"]+attempt); jitter=[rng.random() for _ in blocks]
        order=sorted(range(len(blocks)),key=lambda j:(-blocks[j]["size"],-float((vectors[j]/np.maximum(totals,1)).max()),jitter[j]))
        counts=np.zeros(3); class_counts=np.zeros((3,c)); assignment={}
        for j in order:
            costs=[]
            for s in range(3):
                a=counts.copy(); b=class_counts.copy(); a[s]+=blocks[j]["size"]; b[s]+=vectors[j]
                cost=float(np.square((a-target_n)/np.maximum(target_n,1)).mean()
                    +np.square((b-target_c)/np.maximum(target_c,1)).mean())
                costs.append(cost)
            s=min(range(3),key=lambda z:costs[z]); assignment[j]=s
            counts[s]+=blocks[j]["size"]; class_counts[s]+=vectors[j]
        score=float(np.square((counts-target_n)/target_n).mean()+np.square((class_counts-target_c)/np.maximum(target_c,1)).mean())
        if best is None or score<best[0]: best=(score,assignment,counts,class_counts)
    _,assignment,counts,class_counts=best
    def objective(a,b):
        return float(np.square((a-target_n)/target_n).mean()
            +np.square((b-target_c)/np.maximum(target_c,1)).mean())
    current=objective(counts,class_counts)
    # Local block moves repair avoidable class imbalance left by greedy placement.
    moves=0
    for sweep in range(12):
        order=list(range(len(blocks))); random.Random(cfg["seed"]+1000+sweep).shuffle(order)
        changed=False
        for j in order:
            src=assignment[j]; chosen=src; chosen_cost=current
            for dst in range(3):
                if dst==src: continue
                a=counts.copy(); b=class_counts.copy()
                a[src]-=blocks[j]["size"]; a[dst]+=blocks[j]["size"]
                b[src]-=vectors[j]; b[dst]+=vectors[j]
                cost=objective(a,b)
                if cost<chosen_cost-1e-12: chosen=dst; chosen_cost=cost
            if chosen!=src:
                counts[src]-=blocks[j]["size"]; counts[chosen]+=blocks[j]["size"]
                class_counts[src]-=vectors[j]; class_counts[chosen]+=vectors[j]
                assignment[j]=chosen; current=chosen_cost; changed=True; moves+=1
        if not changed: break
    print(f"Class-balance refinement: {moves} block moves; objective {best[0]:.6f} -> {current:.6f}",flush=True)
    split_names=["train","val","test"]; rows=[]
    for j,block in enumerate(blocks):
        for i in block["members"]:
            rows.append(dict(index=i,image_id=records[i]["id"],group_id=group_lookup[i],
                allocation_block=block["block_id"],split=split_names[assignment[j]]))
    rows.sort(key=lambda r:r["index"])
    write_csv(out/"proposed_split.csv",rows,["index","image_id","group_id","allocation_block","split"])
    class_rows=[]
    for name,k in names.items():
        image_counts=Counter()
        for row in rows:
            if any(o["class"]==name for o in records[row["index"]]["objects"]): image_counts[row["split"]]+=1
        class_rows.append(dict(class_id=k,name=name,total=int(totals[k]),
            allocation_blocks_with_class=int((vectors[:,k]>0).sum()),
            **{s:int(class_counts[j,k]) for j,s in enumerate(split_names)},
            **{s+"_images":image_counts[s] for s in split_names}))
    write_csv(out/"class_distribution.csv",class_rows,
        ["class_id","name","total","allocation_blocks_with_class","train","val","test","train_images","val_images","test_images"])
    split_by_index={r["index"]:r["split"] for r in rows}
    save_json(out/"split_summary.json",dict(seed=cfg["seed"],images={s:int(counts[i]) for i,s in enumerate(split_names)},
        groups={s:sum(split_by_index[g["members"][0]]==s for g in compact) for s in split_names},
        allocation_blocks={s:sum(assignment[j]==i for j in assignment) for i,s in enumerate(split_names)},
        total_allocation_blocks=len(blocks),largest_allocation_block=max(b["size"] for b in blocks),
        allocation_policy="Compact groups remain distinct. Strong/accepted pair components are only split co-location constraints; not inferred videos.",
        status="PROVISIONAL: inspect candidate groups, thresholds and remaining weaker cross-split matches",
        original_split_overlap=None,source_video_independence=False))
    baseline=np.random.default_rng(cfg["seed"]).permutation(np.repeat(np.arange(3),
        [round(n*.70),round(n*.15),n-round(n*.70)-round(n*.15)]))
    np.save(out/"illustrative_random_baseline.npy",baseline)
    print(json.dumps(read_json(out/"split_summary.json"),indent=2),flush=True)


def gallery(cfg,out):
    from PIL import Image,ImageOps,ImageDraw
    import html
    records=load_manifest(out); pairs=read_pairs(out)
    sections={}
    sections["byte_identical"]=[p for p in pairs if int(p["exact"])]
    sections["strong_provisional"]=[p for p in pairs if int(p["provisional_strong"]) and not int(p["exact"])]
    sections["hash_only"]=[p for p in pairs if int(p["phash_distance"])<=cfg["phash_radius"] and not int(p["provisional_strong"]) and not int(p["exact"])]
    sections["dino_only"]=[p for p in pairs if float(p["cosine"])>=cfg["review_cosine"] and int(p["phash_distance"])>cfg["phash_radius"]]
    sections["threshold_boundary"]=sorted(pairs,key=lambda p:abs(float(p["cosine"])-cfg["strong_cosine"])+abs(int(p["phash_distance"])-cfg["strong_phash"])*.005)
    rng=random.Random(cfg["seed"]); folder=out/"gallery"; folder.mkdir(exist_ok=True)
    page=['<!doctype html><meta charset="utf-8"><title>FOD similarity review</title><style>body{font:16px sans-serif;max-width:1200px;margin:30px auto}img{width:600px;max-width:100%}article{display:inline-block;border:1px solid #ccc;margin:8px;padding:8px}code{background:#eee}</style>',
          '<h1>Similarity review: provisional evidence</h1><p>Similar runway backgrounds do not establish shared video identity. All displays are from the clean source dataset.</p><p>Edit pair_decisions.csv with zero-based a,b,accept/reject,note, then rerun neighbours, groups, propose, report. Blank means unreviewed. Review galleries are samples; candidate_pairs.csv contains all retrieved pairs.</p>']
    for category,ps in sections.items():
        if category!="threshold_boundary": rng.shuffle(ps)
        selected=ps[:cfg["gallery_pairs_per_category"]]
        page.append(f'<h2>{category}: {len(ps)} candidate pairs; showing {len(selected)}</h2>')
        for j,p in enumerate(selected):
            canvas=Image.new("RGB",(600,340),"white"); draw=ImageDraw.Draw(canvas)
            for k,field in enumerate(("a","b")):
                r=records[int(p[field])]
                with Image.open(confined(ROOT/r["image"])) as im:
                    tile=ImageOps.contain(im.convert("RGB"),(300,300)); canvas.paste(tile,(k*300,0))
                draw.text((k*300+5,305),f'index {p[field]} | {r["id"]}',fill="black")
            draw.text((5,322),f'pHash={p["phash_distance"]}/64, DINO cosine={p["cosine"]}',fill="black")
            name=f"{category}_{j:03d}.jpg"; canvas.save(folder/name,quality=90)
            page.append(f'<article><img loading="lazy" src="gallery/{name}" alt="{html.escape(category)}"><p>CSV: <code>{p["a"]},{p["b"]},accept or reject,note</code></p></article>')
    gs=read_json(out/"groups.json")
    page.append('<h2>Largest proposed groups: representative images</h2>')
    for g in sorted((g for g in gs if g["size"]>1),key=lambda g:-g["size"])[:30]:
        members=g["members"]; reps=sorted(set(members[i] for i in (0,len(members)//2,len(members)-1)))
        canvas=Image.new("RGB",(300*len(reps),330),"white"); draw=ImageDraw.Draw(canvas)
        for k,i in enumerate(reps):
            with Image.open(confined(ROOT/records[i]["image"])) as im: canvas.paste(im.convert("RGB").resize((300,300)),(300*k,0))
            draw.text((300*k+5,307),str(i),fill="black")
        name=g["group_id"]+".jpg"; canvas.save(folder/name,quality=90)
        page.append(f'<article><p>{g["group_id"]}: {g["size"]} images ({g["status"]})</p><img loading="lazy" src="gallery/{name}"></article>')
    (out/"review.html").write_text("\n".join(page),encoding="utf-8")

def report(cfg,out):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    records=load_manifest(out); pairs=read_pairs(out); gs=read_json(out/"groups.json")
    with open(out/"proposed_split.csv",newline="",encoding="utf-8") as f: assignments=list(csv.DictReader(f))
    labels={"train":0,"val":1,"test":2}
    corrected=np.array([labels[r["split"]] for r in assignments]); baseline=np.load(out/"illustrative_random_baseline.npy")
    knn=np.load(out/"knn.npz"); e=np.load(out/"embeddings.npy",mmap_mode="r")
    summary={}
    for label,split in (("illustrative_random",baseline),("proposed_similarity_aware",corrected)):
        cross=[p for p in pairs if split[int(p["a"])]!=split[int(p["b"])]]
        ids,scores=cosine_knn(e,1,cfg["search_block"],split)
        np.savez_compressed(out/f"{label}_cross_nearest.npz",indices=ids,cosines=scores)
        vals=scores[:,0]; nearest_hash=[(int(records[i]["phash"],16)^int(records[int(j)]["phash"],16)).bit_count() for i,j in enumerate(ids[:,0])]
        summary[label]=dict(candidate_pairs_crossing=len(cross),byte_identical_pairs_crossing=sum(int(p["exact"]) for p in cross),
            provisional_strong_pairs_crossing=sum(int(p["provisional_strong"]) for p in cross),
            phash_radius_pairs_crossing=sum(int(p["phash_distance"])<=cfg["phash_radius"] for p in cross),
            cross_nearest_cosine_quantiles={str(q):float(np.quantile(vals,q)) for q in (0,.25,.5,.75,.9,.95,.99,1)},
            cross_nearest_cosine_above_strong=int((vals>=cfg["strong_cosine"]).sum()),
            groups_crossing=sum(len(set(split[g["members"]]))>1 for g in gs))
        plt.hist(vals,bins=80,alpha=.5,label=label)
        write_csv(out/f"{label}_cross_nearest.csv",
            [dict(index=i,other_index=int(ids[i,0]),cosine=float(vals[i]),phash_distance=nearest_hash[i]) for i in range(len(e))],
            ["index","other_index","cosine","phash_distance"])
    plt.xlabel("Cosine similarity to nearest image in a different split"); plt.ylabel("Images")
    plt.legend(); plt.tight_layout(); plt.savefig(out/"cross_split_similarity.png",dpi=150); plt.close()
    fig,ax=plt.subplots(1,2,figsize=(12,4))
    ax[0].hist([int(p["phash_distance"]) for p in pairs],bins=np.arange(66)-.5)
    ax[0].set(xlabel="pHash Hamming distance",ylabel="Retrieved candidate pairs")
    ax[1].hist(knn["cosines"][:,0],bins=80); ax[1].set(xlabel="Nearest-neighbour DINO cosine",ylabel="Images")
    fig.tight_layout(); fig.savefig(out/"similarity_distributions.png",dpi=150); plt.close(fig)
    exact_ids={int(p[k]) for p in pairs if int(p["exact"]) for k in ("a","b")}
    strong_ids={int(p[k]) for p in pairs if int(p["provisional_strong"]) for k in ("a","b")}
    summary.update(images=len(records),annotations=len(records),boxes=sum(len(r["objects"]) for r in records),
        byte_identical_images=len(exact_ids),provisional_near_duplicate_images=len(strong_ids),
        candidate_pairs=len(pairs),candidate_non_singleton_groups=sum(g["size"]>1 for g in gs),
        all_groups_including_singletons=len(gs),original_split_spanning_groups=None,
        unreviewed_candidate_pairs=sum(not p["decision"] and not int(p["exact"]) for p in pairs))
    save_json(out/"analysis_summary.json",summary)
    gallery(cfg,out)
    inventory_stats=read_json(out/"inventory.json"); split_stats=read_json(out/"split_summary.json")
    text=f"""# FOD similarity-aware dataset audit
Status: PROVISIONAL; review similarity evidence and proposed split before YOLO training.

Images: {len(records)}; annotation files: {len(records)}; bounding boxes: {summary['boxes']}; classes: {len(inventory_stats['classes'])}.
Byte-identical images (all members, not redundant-copy count): {len(exact_ids)}.
Provisional near-duplicate images (pHash + DINO rule, NOT human-confirmed): {len(strong_ids)}.
Candidate pairs: {len(pairs)}. Non-singleton candidate groups: {summary['candidate_non_singleton_groups']}.
Groups including singletons: {len(gs)}.
Original split-spanning groups: unavailable, because historical split assignments are missing.

## Method and thresholds
pHash: RGB decoded to grayscale, LANCZOS 32x32, orthonormal type-II DCT, 8x8 low-frequency block;
DC is excluded from the median and its bit is forced off. This custom 64-bit convention is versioned in the script.
Radius <= {cfg['phash_radius']} is exhaustively searched with a BK-tree. It is a candidate retrieval threshold.
DINOv2: pinned official pretrained ViT-S/14, no fine-tuning, float32 L2-normalized CLS embeddings.
RGB images resize directly to 224x224 with bicubic interpolation, without cropping the runway edges.
Exact float32 batched cosine top-{cfg['knn_k']} search; no approximate-neighbour recall loss.
However, top-k retrieval does NOT enumerate every pair above a cosine threshold.
Review cosine >= {cfg['review_cosine']}.
Configured strong co-location rule: {strong_rule_description(cfg)}.
These are review heuristics, NOT calibrated probabilities or established video-identity boundaries.
Inspect review.html, especially hash-only, DINO-only and boundary examples, before accepting them.
pHash distances reflect global low-frequency appearance and can miss small FOD differences.
DINO semantic similarity can confuse unrelated runway scenes.
Class labels do not determine similarity grouping.
Byte-identical files are kept together. All pairs inside each proposed group must have strong or explicitly
accepted evidence (complete-link constraint); transitive weak chains cannot create a group.
This conservative rule can leave strong edges between distinct compact groups. Split co-location blocks
keep every such un-rejected strong edge in the same split without declaring those groups to be one scene.

## Split
Seed: {cfg['seed']}. Targets: 70/15/15. Actual images: {json.dumps(split_stats['images'])}.
Multiple seeded greedy allocations optimize image counts and per-class BOX counts.
Compact pairwise-verified candidate groups remain separate for interpretation.
For split allocation ONLY, all strong/explicitly accepted pairs impose same-split constraints.
Transitive closure of those constraints defines allocation blocks, not inferred videos or similarity groups.
Weak candidate edges never impose these constraints. A block can contain unrelated scenes linked through
strong matches; co-location is conservative for evaluation and does not assert shared video provenance.
See allocation_blocks.json. The largest block size and block counts are in split_summary.json.
See class_distribution.csv for class IDs, counts and unavoidable imbalance. Class coverage is not guaranteed
where a class occurs in very few independent groups. No source annotations are edited.
New class IDs are alphabetical because historical YOLO IDs were not supplied.
VOC fractional xyxy coordinates are interpreted as zero-origin continuous coordinates, matching this export's
decimal box style; they are normalized without a one-pixel offset. Validate overlays if the source convention differs.
Difficult objects are retained; their flags remain in the manifest but YOLO detection labels do not encode them.

## Before and after
There is NO measured historical baseline. illustrative_random is a newly generated, seeded image-level random
split of this clean download, supplied solely to demonstrate sensitivity to splitting methodology.
proposed_similarity_aware uses the proposed groups. Both are compared using all retrieved candidate pairs
and exact per-image nearest cosine matches in other splits.
See analysis_summary.json and cross_split_similarity.png.
Cross-split candidate matches are evidence to review, not confirmed leakage. Accepted/proposed groups never cross splits.
All retrieved un-rejected strong pairs are constrained to one split; weaker uncertain matches can still cross.
Do not treat the split as final
while concerning cross-split matches remain unresolved. Consider broader manually verified scene groups,
quarantining uncertain scenes, or a genuinely independent acquisition.

## Review workflow
Open review.html; inspect candidate_pairs.csv and blocked_merges.json.
Add pair decisions to pair_decisions.csv (a,b,decision,note; accept/reject/blank), then rerun:
neighbours, groups, propose, report. Decisions bind to immutable manifest indices.
An accepted edge may be blocked if the resulting group lacks complete pairwise evidence; inspect blocked_merges.json.
Do not force a video identity from background semantics or numerical filenames.
Export a review copy with --provisional, or a reviewed copy with --reviewed. No script invokes model training.

## Limitations
This is similarity-aware, NOT guaranteed video-independent. Videos/timestamps/camera session IDs are unavailable.
XML track IDs 0 and 1 are reused across files; no reliable video identity can be inferred from them.
The clean dataset contains no synthetic images, as confirmed by the user.
Embeddings/global hashes may miss spatially transformed, illuminated, occluded, or temporally distant related frames.
Near-identical backgrounds with changing tiny debris need careful manual review.
No negative/background-only annotations were found in the initial audit; deployment false-positive performance
needs independent real runway background samples.
Repeated use of validation/test images to tune model decisions biases evaluation; freeze the reviewed split
before training and reserve test model evaluation for the final run.
Sources: https://github.com/facebookresearch/dinov2
https://docs.ultralytics.com/modes/train/
https://docs.ultralytics.com/modes/val/
"""
    (out/"REPORT.md").write_text(text,encoding="utf-8")
    print(json.dumps(summary,indent=2),flush=True)

def export(cfg,out,reviewed,provisional=False):
    if not reviewed and not provisional: raise ValueError("Use --provisional for a review copy, or --reviewed after review")
    records=load_manifest(out); names=read_json(out/"class_mapping.json")
    with open(out/"proposed_split.csv",newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
    if len(rows)!=len(records) or [int(r["index"]) for r in rows]!=list(range(len(records))):
        raise ValueError("Split does not contain every index exactly once")
    gs=read_json(out/"groups.json"); split_by_index={int(r["index"]):r["split"] for r in rows}
    if any(len({split_by_index[i] for i in g["members"]})!=1 for g in gs):
        raise ValueError("Group crosses splits")
    blocks=read_json(out/"allocation_blocks.json")
    if any(len({split_by_index[i] for i in b["members"]})!=1 for b in blocks):
        raise ValueError("Strong-pair allocation block crosses splits")
    target=confined(ROOT/cfg["corrected_destination"])
    if target.exists(): raise FileExistsError("Refusing to overwrite corrected destination")
    target.mkdir()
    for s in ("train","val","test"):
        (target/"images"/s).mkdir(parents=True); (target/"labels"/s).mkdir(parents=True)
    def export_one(row):
        i=int(row["index"]); r=records[i]; s=row["split"]
        image=confined(ROOT/r["image"]); ann=confined(ROOT/r["annotation"])
        if digest(image)!=r["image_sha256"] or digest(ann)!=r["annotation_sha256"]:
            raise ValueError(f"Source changed: {r['id']}")
        shutil.copyfile(image,target/"images"/s/(r["id"]+".jpg"))
        labels=[]
        for o in r["objects"]:
            a,b,c,d=o["xyxy"]; w,h=r["width"],r["height"]
            labels.append(f'{names[o["class"]]} {(a+c)/(2*w):.10f} {(b+d)/(2*h):.10f} {(c-a)/w:.10f} {(d-b)/h:.10f}')
        (target/"labels"/s/(r["id"]+".txt")).write_text("\n".join(labels)+"\n",encoding="utf-8")
        return 1
    with ThreadPoolExecutor(max_workers=cfg["io_workers"]) as pool:
        for completed,_ in enumerate(pool.map(export_one,rows),1):
            if completed%1000==0: print(f"Exported {completed}/{len(rows)}",flush=True)
    import yaml
    config=dict(path=str(target).replace("\\","/"),train="images/train",val="images/val",test="images/test",
                names={v:k for k,v in names.items()})
    (target/"dataset.yaml").write_text(yaml.safe_dump(config,sort_keys=False),encoding="utf-8")
    shutil.copyfile(out/"proposed_split.csv",target/"split_manifest.csv")
    save_json(target/"provenance.json",dict(manifest=digest(out/"manifest.jsonl"),
        split=digest(out/"proposed_split.csv"),config=cfg,reviewed=reviewed,provisional=not reviewed,video_independent=False))
    print(f"Exported {len(rows)} images to {target}",flush=True)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("stage",choices=["inventory","embeddings","neighbours","groups","propose","report","export","all"])
    p.add_argument("--config",default=str(HERE/"config.json"))
    p.add_argument("--reviewed",action="store_true")
    p.add_argument("--provisional",action="store_true")
    args=p.parse_args(); cfg=read_json(confined(args.config)); out=confined(ROOT/cfg["output"]); out.mkdir(parents=True,exist_ok=True)
    stages=["inventory","embeddings","neighbours","groups","propose","report"] if args.stage=="all" else [args.stage]
    for stage in stages:
        print(f"=== {stage} ===",flush=True)
        if stage=="export": export(cfg,out,args.reviewed,args.provisional)
        else: globals()[stage](cfg,out)
if __name__=="__main__": main()

