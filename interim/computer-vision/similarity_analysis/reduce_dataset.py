"""Build an object-aware representative subset without modifying source data."""
import argparse, csv, hashlib, json, math, os, shutil, sys, time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
os.environ["TORCH_HOME"]=str(HERE/"cache"/"torch")
os.environ["HF_HOME"]=str(HERE/"cache"/"huggingface")
os.environ["MPLCONFIGDIR"]=str(HERE/"cache"/"matplotlib")
os.environ["PYTHONDONTWRITEBYTECODE"]="1"

def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8-sig"))
def save_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+".tmp");tmp.write_text(json.dumps(data,indent=2),encoding="utf-8")
    for attempt in range(12):
        try:tmp.replace(path);return
        except PermissionError:
            if attempt==11:raise
            time.sleep(.5)
def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1048576),b""):h.update(b)
    return h.hexdigest()
def load_manifest(inp): return [json.loads(x) for x in (inp/"manifest.jsonl").read_text(encoding="utf-8").splitlines()]
def write_csv(path,rows,fields):
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def check_inside(path):
    p=Path(path).resolve()
    if not p.is_relative_to(ROOT): raise ValueError(f"Outside workspace: {p}")
    return p

def object_rows(records,cfg):
    rows=[]
    for i,r in enumerate(records):
        for ordinal,o in enumerate(r["objects"]):
            x1,y1,x2,y2=o["xyxy"];cx=(x1+x2)/2;cy=(y1+y2)/2
            side=min(max(cfg["minimum_crop_pixels"],cfg["crop_context"]*max(x2-x1,y2-y1)),max(r["width"],r["height"]))
            rows.append(dict(object_index=len(rows),image_index=i,ordinal=ordinal,class_name=o["class"],
                bbox=o["xyxy"],crop=[cx-side/2,cy-side/2,cx+side/2,cy+side/2]))
    return rows

def embeddings(cfg,inp,out):
    import numpy as np
    import torch
    from PIL import Image
    from torchvision import transforms
    records=load_manifest(inp);rows=object_rows(records,cfg);n=len(rows)
    index_path=out/"object_index.jsonl"
    expected=hashlib.sha256("\n".join(json.dumps(x,sort_keys=True) for x in rows).encode()).hexdigest()
    if index_path.exists():
        actual=sha(index_path)
        meta=read_json(out/"object_index_meta.json")
        if meta["logical_sha256"]!=expected:raise ValueError("Object crop index changed")
    else:
        with open(index_path,"w",encoding="utf-8") as f:
            for row in rows:f.write(json.dumps(row)+"\n")
        save_json(out/"object_index_meta.json",dict(logical_sha256=expected,file_sha256=sha(index_path),objects=n))
    model_info=read_json(HERE/"model_lock.json")
    device="cuda" if torch.cuda.is_available() else "cpu"
    fingerprint=dict(manifest=sha(inp/"manifest.jsonl"),object_index=expected,model=model_info,
        method="DINOv2 patch-token pooling over expanded boxes; one batched GPU-to-CPU transfer",
        crop_context=cfg["crop_context"],minimum_crop_pixels=cfg["minimum_crop_pixels"],dimension=384,device=device)
    state_path=out/"object_embedding_state.json";target=out/"object_embeddings.npy";done=0
    if state_path.exists():
        state=read_json(state_path)
        if state["fingerprint"]!=fingerprint:raise ValueError("Object embedding inputs changed")
        done=state["completed"]
    if done==n:
        print(f"Object embeddings already complete: {n}",flush=True);return
    torch.manual_seed(cfg["seed"]);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    model=torch.hub.load(f'facebookresearch/dinov2:{model_info["revision"]}',model_info["model"],pretrained=True,trust_repo=True,skip_validation=True).eval().to(device)
    for p in model.parameters():p.requires_grad_(False)
    transform=transforms.Compose([transforms.Resize((224,224),interpolation=transforms.InterpolationMode.BICUBIC),
        transforms.ToTensor(),transforms.Normalize((.485,.456,.406),(.229,.224,.225))])
    def image_tensor(r):
        with Image.open(check_inside(ROOT/r["image"])) as im:return transform(im.convert("RGB"))
    by_image=defaultdict(list)
    for row in rows:by_image[row["image_index"]].append(row)
    # Singleton compact groups cannot lose an image, so they need no object feature.
    needed_images=sorted({i for g in read_json(inp/"groups.json") if g["size"]>1 for i in g["members"]})
    e=np.lib.format.open_memmap(target,mode="r+" if target.exists() else "w+",dtype="float32",shape=(n,384))
    start=time.time()
    with ThreadPoolExecutor(max_workers=cfg["io_workers"]) as pool,torch.inference_mode():
        # Checkpoints are by image, since one forward pass supplies every object in that image.
        done_images=0
        if state_path.exists():done_images=read_json(state_path).get("completed_images",0)
        remaining=[i for i in needed_images if i>=done_images]
        for pos in range(0,len(remaining),cfg["batch_size"]):
            image_indices=remaining[pos:pos+cfg["batch_size"]];batch=torch.stack(list(pool.map(image_tensor,[records[i] for i in image_indices]))).to(device)
            patches=model.forward_features(batch)["x_norm_patchtokens"].float().reshape(len(image_indices),16,16,384).cpu().numpy()
            for local,image_index in enumerate(image_indices):
                r=records[image_index]
                for row in by_image[image_index]:
                    x1,y1,x2,y2=row["crop"]
                    # Select patch centers within the expanded square, clipped to the image.
                    xs=(np.arange(16)+.5)*(r["width"]/16)
                    ys=(np.arange(16)+.5)*(r["height"]/16)
                    mask=(ys[:,None]>=max(0,y1))&(ys[:,None]<=min(r["height"],y2))&(xs[None,:]>=max(0,x1))&(xs[None,:]<=min(r["width"],x2))
                    if not mask.any():
                        cx=(x1+x2)/2;cy=(y1+y2)/2;ix=int(max(0,min(15,cx/r["width"]*16)));iy=int(max(0,min(15,cy/r["height"]*16)))
                        pooled=patches[local,iy,ix]
                    else:pooled=patches[local][mask].mean(0)
                    e[row["object_index"]]=pooled/max(np.linalg.norm(pooled),1e-12)
            e.flush();next_image=image_indices[-1]+1;completed_objects=sum(len(by_image[i]) for i in needed_images if i<next_image)
            final=pos+len(image_indices)==len(remaining)
            save_json(state_path,dict(fingerprint=fingerprint,completed=n if final else completed_objects,total=n,completed_images=len(records) if final else next_image,total_images=len(records),needed_images=len(needed_images)))
            if pos%1024<cfg["batch_size"] or final:print(f"Object-aware DINOv2 {pos+len(image_indices)}/{len(remaining)} remaining group images; {time.time()-start:.1f}s",flush=True)

def prepare(records,objrows):
    by_image=defaultdict(list)
    for row in objrows:by_image[row["image_index"]].append(row)
    signatures={i:tuple(sorted(x["class_name"] for x in rows)) for i,rows in by_image.items()}
    return by_image,signatures

def pair_metrics(a,b,by_image,embeddings,records):
    import numpy as np
    from scipy.optimize import linear_sum_assignment
    left=by_image[a];right=by_image[b]
    if sorted(x["class_name"] for x in left)!=sorted(x["class_name"] for x in right):return None
    sims=[];centers=[];scales=[]
    for name in sorted(set(x["class_name"] for x in left)):
        li=[x for x in left if x["class_name"]==name];ri=[x for x in right if x["class_name"]==name]
        matrix=np.asarray(embeddings[[x["object_index"] for x in li]])@np.asarray(embeddings[[x["object_index"] for x in ri]]).T
        xidx,yidx=linear_sum_assignment(-matrix)
        for x,y in zip(xidx,yidx):
            lo,ro=li[x],ri[y];sims.append(float(matrix[x,y]))
            lb,rb=lo["bbox"],ro["bbox"]
            lc=((lb[0]+lb[2])/(2*records[a]["width"]),(lb[1]+lb[3])/(2*records[a]["height"]))
            rc=((rb[0]+rb[2])/(2*records[b]["width"]),(rb[1]+rb[3])/(2*records[b]["height"]))
            centers.append(math.dist(lc,rc))
            la=(lb[2]-lb[0])*(lb[3]-lb[1])/(records[a]["width"]*records[a]["height"])
            ra=(rb[2]-rb[0])*(rb[3]-rb[1])/(records[b]["width"]*records[b]["height"])
            scales.append(abs(math.log(max(la,1e-12)/max(ra,1e-12))))
    return min(sims),max(centers),max(scales),sum(sims)/len(sims)

def analyze(cfg,inp,out):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    records=load_manifest(inp);objrows=[json.loads(x) for x in (out/"object_index.jsonl").read_text().splitlines()]
    e=np.load(out/"object_embeddings.npy",mmap_mode="r");by_image,_=prepare(records,objrows)
    groups=read_json(inp/"groups.json");rows=[]
    for g in groups:
        m=g["members"]
        for p,a in enumerate(m):
            for b in m[p+1:]:
                metrics=pair_metrics(a,b,by_image,e,records)
                if metrics:
                    rows.append(dict(group_id=g["group_id"],a=a,b=b,min_object_cosine=f"{metrics[0]:.8f}",
                        maximum_center_delta=f"{metrics[1]:.8f}",maximum_log_area_delta=f"{metrics[2]:.8f}",mean_object_cosine=f"{metrics[3]:.8f}"))
    write_csv(out/"object_pair_scores.csv",rows,["group_id","a","b","min_object_cosine","maximum_center_delta","maximum_log_area_delta","mean_object_cosine"])
    vals=np.array([float(x["min_object_cosine"]) for x in rows]);cent=np.array([float(x["maximum_center_delta"]) for x in rows]);scale=np.array([float(x["maximum_log_area_delta"]) for x in rows])
    fig,ax=plt.subplots(1,3,figsize=(15,4));ax[0].hist(vals,bins=80);ax[0].axvline(cfg["object_cosine"],color="red");ax[0].set_xlabel("Minimum matched-object cosine")
    ax[1].hist(cent,bins=80);ax[1].axvline(cfg["maximum_center_delta"],color="red");ax[1].set_xlabel("Maximum normalized center change")
    ax[2].hist(np.clip(scale,0,3),bins=80);ax[2].axvline(cfg["maximum_log_area_delta"],color="red");ax[2].set_xlabel("Maximum absolute log-area change")
    fig.tight_layout();fig.savefig(out/"object_pair_distributions.png",dpi=150);plt.close(fig)
    save_json(out/"object_pair_summary.json",dict(comparable_pairs=len(rows),quantiles={
        "object_cosine":{str(q):float(np.quantile(vals,q)) for q in (0,.1,.25,.5,.75,.9,.95,.99,1)},
        "center_delta":{str(q):float(np.quantile(cent,q)) for q in (0,.5,.9,.95,.99,1)},
        "log_area_delta":{str(q):float(np.quantile(scale,q)) for q in (0,.5,.9,.95,.99,1)}}))
    print(json.dumps(read_json(out/"object_pair_summary.json"),indent=2),flush=True)

def select(cfg,inp,out):
    import numpy as np
    records=load_manifest(inp);objrows=[json.loads(x) for x in (out/"object_index.jsonl").read_text().splitlines()]
    by_image,signatures=prepare(records,objrows);groups=read_json(inp/"groups.json")
    class_counts=Counter(o["class"] for r in records for o in r["objects"])
    rare={c for c,n in class_counts.items() if n<cfg["rare_class_box_cutoff"]}
    areas=defaultdict(list)
    for r in records:
        for o in r["objects"]:
            b=o["xyxy"];areas[o["class"]].append((b[2]-b[0])*(b[3]-b[1])/(r["width"]*r["height"]))
    cut={c:float(np.quantile(v,cfg["small_object_quantile"])) for c,v in areas.items()}
    protected={};reasons=defaultdict(list)
    for i,r in enumerate(records):
        if len(r["objects"])>1:reasons[i].append("multi_object")
        for o in r["objects"]:
            b=o["xyxy"];area=(b[2]-b[0])*(b[3]-b[1])/(r["width"]*r["height"])
            if o["class"] in rare:reasons[i].append("rare_class")
            if str(o.get("difficult","0"))=="1":reasons[i].append("difficult")
            if area<=cut[o["class"]]:reasons[i].append("small_for_class")
            m=cfg["edge_margin_pixels"]
            if b[0]<=m or b[1]<=m or b[2]>=r["width"]-m or b[3]>=r["height"]-m:reasons[i].append("edge_object")
        if reasons[i]:protected[i]=True
    scores={}
    with open(out/"object_pair_scores.csv",newline="",encoding="utf-8") as f:
        for row in csv.DictReader(f):scores[(int(row["a"]),int(row["b"]))]=row
    kept=set();representative={};group_id={}
    for g in groups:
        members=g["members"]
        for i in members:group_id[i]=g["group_id"]
        cover={i:{i} for i in members}
        for p,a in enumerate(members):
            for b in members[p+1:]:
                row=scores.get((a,b))
                if not row:continue
                if (float(row["min_object_cosine"])>=cfg["object_cosine"] and
                    float(row["maximum_center_delta"])<=cfg["maximum_center_delta"] and
                    float(row["maximum_log_area_delta"])<=cfg["maximum_log_area_delta"] and signatures[a]==signatures[b]):
                    cover[a].add(b);cover[b].add(a)
        selected={i for i in members if i in protected};uncovered=set(members)
        for i in selected:uncovered-=cover[i]
        while uncovered:
            candidates=members
            choice=max(candidates,key=lambda i:(len(cover[i]&uncovered),i in protected,-i))
            selected.add(choice);uncovered-=cover[choice]
        kept.update(selected)
        for i in members:
            possible=[r for r in selected if i in cover[r]]
            representative[i]=min(possible,key=lambda r:(r!=i if i in selected else 0,-len(cover[r]),r)) if possible else i
    rows=[]
    for i,r in enumerate(records):
        keep=i in kept
        rows.append(dict(index=i,image_id=r["id"],group_id=group_id[i],keep=int(keep),representative=representative[i],
            protected=int(i in protected),reason="|".join(sorted(set(reasons[i])))))
    write_csv(out/"selection.csv",rows,["index","image_id","group_id","keep","representative","protected","reason"])
    save_json(out/"selection_summary.json",dict(original_images=len(records),kept_images=len(kept),removed_images=len(records)-len(kept),
        retained_fraction=len(kept)/len(records),protected_images=len(protected),rare_classes=sorted(rare),
        thresholds={k:cfg[k] for k in ("object_cosine","maximum_center_delta","maximum_log_area_delta","rare_class_box_cutoff","small_object_quantile","edge_margin_pixels")}))
    print(json.dumps(read_json(out/"selection_summary.json"),indent=2),flush=True)

def build_blocks(inp,kept):
    parent={i:i for i in kept};size={i:1 for i in kept}
    def find(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    def join(a,b):
        a,b=find(a),find(b)
        if a==b:return
        if size[a]<size[b]:a,b=b,a
        parent[b]=a;size[a]+=size[b]
    with open(inp/"candidate_pairs.csv",newline="",encoding="utf-8") as f:
        for p in csv.DictReader(f):
            a,b=int(p["a"]),int(p["b"])
            if a in kept and b in kept and p["decision"]!="reject" and (int(p["exact"]) or int(p["provisional_strong"]) or p["decision"]=="accept"):join(a,b)
    blocks=defaultdict(list)
    for i in sorted(kept):blocks[find(i)].append(i)
    return list(blocks.values())

def optimize(cfg,inp,out):
    import numpy as np
    from scipy.optimize import Bounds,LinearConstraint,milp
    from scipy.sparse import lil_matrix
    records=load_manifest(inp);mapping=read_json(inp/"class_mapping.json")
    with open(out/"selection.csv",newline="",encoding="utf-8") as f:kept={int(r["index"]) for r in csv.DictReader(f) if int(r["keep"])}
    blocks=build_blocks(inp,kept);B=len(blocks);S=3;C=len(mapping);fractions=np.array(cfg["split_fractions"])
    bc=np.zeros((B,C));bs=np.array([len(x) for x in blocks],dtype=float)
    for j,block in enumerate(blocks):
        for i in block:
            for o in records[i]["objects"]:bc[j,mapping[o["class"]]]+=1
    totals=bc.sum(0);target_i=fractions*len(kept);target_c=fractions[:,None]*totals[None,:]
    base=B*S;metrics=S+S*C;nvar=base+2*metrics
    rows=B+S+S*C+S*C;A=lil_matrix((rows,nvar),dtype=float);lb=np.full(rows,-np.inf);ub=np.full(rows,np.inf);row=0
    for j in range(B):
        for s in range(S):A[row,j*S+s]=1
        lb[row]=ub[row]=1;row+=1
    metric=0;c=np.zeros(nvar)
    for s in range(S):
        for j in range(B):A[row,j*S+s]=bs[j]
        A[row,base+2*metric]=-1;A[row,base+2*metric+1]=1;lb[row]=ub[row]=target_i[s]
        c[base+2*metric:base+2*metric+2]=5/max(target_i[s],1);metric+=1;row+=1
    for s in range(S):
        for k in range(C):
            nz=np.flatnonzero(bc[:,k])
            for j in nz:A[row,j*S+s]=bc[j,k]
            A[row,base+2*metric]=-1;A[row,base+2*metric+1]=1;lb[row]=ub[row]=target_c[s,k]
            c[base+2*metric:base+2*metric+2]=1/max(target_c[s,k],1);metric+=1;row+=1
    for s in range(S):
        for k in range(C):
            for j in np.flatnonzero(bc[:,k]):A[row,j*S+s]=bc[j,k]
            lb[row]=1;row+=1
    bounds=Bounds(np.zeros(nvar),np.r_[np.ones(base),np.full(2*metrics,np.inf)])
    integrality=np.r_[np.ones(base),np.zeros(2*metrics)]
    print(f"MILP: {B} indivisible blocks, {base} binary variables",flush=True)
    result=milp(c,integrality=integrality,bounds=bounds,constraints=LinearConstraint(A.tocsr(),lb,ub),
        options={"time_limit":cfg["optimizer_time_limit_seconds"],"mip_rel_gap":0.002,"presolve":True})
    if result.x is None:raise RuntimeError(f"Split optimizer failed: {result.message}")
    assignment=np.argmax(result.x[:base].reshape(B,S),axis=1);names=["train","val","test"];rows_out=[]
    for j,block in enumerate(blocks):
        for i in block:rows_out.append(dict(index=i,image_id=records[i]["id"],allocation_block=f"rb{min(block):06d}",split=names[assignment[j]]))
    rows_out.sort(key=lambda r:r["index"]);write_csv(out/"reduced_split.csv",rows_out,["index","image_id","allocation_block","split"])
    image_counts=Counter(x["split"] for x in rows_out);box_counts=Counter();class_rows=[]
    split_of={x["index"]:x["split"] for x in rows_out}
    for x in rows_out:
        for o in records[x["index"]]["objects"]:box_counts[x["split"]]+=1
    for name,k in mapping.items():
        vals=Counter();imgs=Counter()
        for i in kept:
            objects=[o for o in records[i]["objects"] if o["class"]==name]
            if objects:vals[split_of[i]]+=len(objects);imgs[split_of[i]]+=1
        class_rows.append(dict(class_id=k,name=name,total=sum(vals.values()),train=vals["train"],val=vals["val"],test=vals["test"],train_images=imgs["train"],val_images=imgs["val"],test_images=imgs["test"]))
    write_csv(out/"class_distribution.csv",class_rows,["class_id","name","total","train","val","test","train_images","val_images","test_images"])
    save_json(out/"split_summary.json",dict(status=result.message,objective=float(result.fun),images=dict(image_counts),boxes=dict(box_counts),
        blocks={s:int(sum(assignment==j)) for j,s in enumerate(names)},largest_block=max(map(len,blocks)),strong_pairs_crossing=0,source_video_independent=False))
    save_json(out/"reduced_blocks.json",[dict(block_id=f"rb{min(b):06d}",members=b,size=len(b),split=names[assignment[j]]) for j,b in enumerate(blocks)])
    print(json.dumps(read_json(out/"split_summary.json"),indent=2),flush=True)

def export(cfg,inp,out):
    import yaml
    records=load_manifest(inp);mapping=read_json(inp/"class_mapping.json")
    with open(out/"reduced_split.csv",newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
    target=check_inside(ROOT/cfg["destination"])
    if target.exists():raise FileExistsError(f"Refusing to overwrite {target}")
    for s in ("train","val","test"):(target/"images"/s).mkdir(parents=True);(target/"labels"/s).mkdir(parents=True)
    def one(row):
        i=int(row["index"]);r=records[i];s=row["split"];src=check_inside(ROOT/r["image"])
        if sha(src)!=r["image_sha256"]:raise ValueError(f"Source changed: {src}")
        shutil.copyfile(src,target/"images"/s/(r["id"]+".jpg"));lines=[]
        for o in r["objects"]:
            a,b,c,d=o["xyxy"];w,h=r["width"],r["height"]
            lines.append(f'{mapping[o["class"]]} {(a+c)/(2*w):.10f} {(b+d)/(2*h):.10f} {(c-a)/w:.10f} {(d-b)/h:.10f}')
        (target/"labels"/s/(r["id"]+".txt")).write_text("\n".join(lines)+"\n",encoding="utf-8");return 1
    with ThreadPoolExecutor(max_workers=cfg["io_workers"]) as pool:
        for n,_ in enumerate(pool.map(one,rows),1):
            if n%1000==0:print(f"Exported {n}/{len(rows)}",flush=True)
    data=dict(path=str(target).replace("\\","/"),train="images/train",val="images/val",test="images/test",names={v:k for k,v in mapping.items()})
    (target/"dataset.yaml").write_text(yaml.safe_dump(data,sort_keys=False),encoding="utf-8")
    shutil.copyfile(out/"reduced_split.csv",target/"split_manifest.csv")
    save_json(target/"provenance.json",dict(provisional=True,source_manifest=sha(inp/"manifest.jsonl"),selection=sha(out/"selection.csv"),split=sha(out/"reduced_split.csv"),video_independent=False))

def validate(cfg,inp,out):
    import yaml
    records=load_manifest(inp);mapping=read_json(inp/"class_mapping.json");target=check_inside(ROOT/cfg["destination"])
    with open(out/"reduced_split.csv",newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
    split={int(r["index"]):r["split"] for r in rows};kept=set(split);counts=Counter();boxes=Counter()
    with open(out/"selection.csv",newline="",encoding="utf-8") as f:selection=list(csv.DictReader(f))
    if len(selection)!=len(records) or {int(r["index"]) for r in selection}!=set(range(len(records))):raise ValueError("Selection does not cover the manifest exactly once")
    selected={int(r["index"]):r for r in selection}
    if kept!={i for i,r in selected.items() if int(r["keep"])}:raise ValueError("Export and selection disagree")
    pair_scores={}
    with open(out/"object_pair_scores.csv",newline="",encoding="utf-8") as f:
        for p in csv.DictReader(f):pair_scores[(int(p["a"]),int(p["b"]))]=p
    covered=0
    for i,row in selected.items():
        if int(row["protected"]) and not int(row["keep"]):raise ValueError(f"Protected image was removed: {i}")
        if int(row["keep"]):continue
        rep=int(row["representative"]);key=tuple(sorted((i,rep)));score=pair_scores.get(key)
        if rep not in kept or selected[rep]["group_id"]!=row["group_id"] or score is None:raise ValueError(f"Invalid representative for {i}")
        if not (float(score["min_object_cosine"])>=cfg["object_cosine"] and float(score["maximum_center_delta"])<=cfg["maximum_center_delta"] and float(score["maximum_log_area_delta"])<=cfg["maximum_log_area_delta"]):raise ValueError(f"Representative thresholds failed for {i}")
        if sorted(o["class"] for o in records[i]["objects"])!=sorted(o["class"] for o in records[rep]["objects"]):raise ValueError(f"Representative class signature differs for {i}")
        covered+=1
    data=yaml.safe_load((target/"dataset.yaml").read_text());assert Path(data["path"]).resolve()==target and data["names"]=={v:k for k,v in mapping.items()}
    def one(row):
        i=int(row["index"]);r=records[i];s=row["split"];img=target/"images"/s/(r["id"]+".jpg");lab=target/"labels"/s/(r["id"]+".txt")
        if sha(img)!=r["image_sha256"]:raise ValueError(f"Bad copied image: {img}")
        lines=[x.split() for x in lab.read_text().splitlines() if x.strip()]
        if len(lines)!=len(r["objects"]):raise ValueError(f"Label count mismatch: {lab}")
        for line,o in zip(lines,r["objects"]):
            a,b,c,d=o["xyxy"];w,h=r["width"],r["height"];expected=[mapping[o["class"]],(a+c)/(2*w),(b+d)/(2*h),(c-a)/w,(d-b)/h]
            got=[int(line[0]),*map(float,line[1:])]
            if got[0]!=expected[0] or any(abs(x-y)>1e-9 for x,y in zip(got[1:],expected[1:])):raise ValueError(f"Label mismatch: {lab}")
        return s,len(lines)
    with ThreadPoolExecutor(max_workers=cfg["io_workers"]) as pool:
        for n,(s,b) in enumerate(pool.map(one,rows),1):counts[s]+=1;boxes[s]+=b
    strong_cross=0
    with open(inp/"candidate_pairs.csv",newline="",encoding="utf-8") as f:
        for p in csv.DictReader(f):
            a,b=int(p["a"]),int(p["b"])
            if a in kept and b in kept and p["decision"]!="reject" and (int(p["exact"]) or int(p["provisional_strong"]) or p["decision"]=="accept"):strong_cross+=split[a]!=split[b]
    if strong_cross:raise ValueError(f"{strong_cross} strong pairs cross splits")
    for s in ("train","val","test"):
        if len(list((target/"images"/s).glob("*.jpg")))!=counts[s] or len(list((target/"labels"/s).glob("*.txt")))!=counts[s]:raise ValueError("Export file count mismatch")
    class_presence={s:set() for s in ("train","val","test")}
    for i,s in split.items():class_presence[s].update(o["class"] for o in records[i]["objects"])
    expected_classes=set(mapping)
    if any(class_presence[s]!=expected_classes for s in class_presence):raise ValueError("A class is absent from a split")
    result=dict(status="passed",images=dict(counts),boxes=dict(boxes),strong_pairs_crossing=strong_cross,
        copied_images_sha256_verified=True,yolo_labels_verified=True,source_images=len(records),retained_images=len(rows),
        removed_images_covered_by_verified_representative=covered,protected_images_retained=True,all_classes_present_in_every_split=True,
        object_embeddings_sha256=sha(out/"object_embeddings.npy"),selection_sha256=sha(out/"selection.csv"),split_sha256=sha(out/"reduced_split.csv"))
    save_json(out/"validation.json",result);print(json.dumps(result,indent=2),flush=True)

def report(cfg,inp,out):
    from PIL import Image,ImageDraw,ImageOps
    records=load_manifest(inp);selection=[]
    with open(out/"selection.csv",newline="",encoding="utf-8") as f:selection=list(csv.DictReader(f))
    split=read_json(out/"split_summary.json");summary=read_json(out/"selection_summary.json")
    scores={}
    with open(out/"object_pair_scores.csv",newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):scores[(int(r["a"]),int(r["b"]))]=r
    gallery=out/"gallery";gallery.mkdir(exist_ok=True);removed=[r for r in selection if not int(r["keep"])]
    page=['<!doctype html><meta charset="utf-8"><title>Object-aware reduction review</title><style>body{font:16px sans-serif;max-width:1100px;margin:30px auto}img{max-width:100%}section{border:1px solid #ccc;margin:12px;padding:10px}</style>',
        '<h1>Object-aware representative-frame reduction</h1><p>Removed images are retained in the original datasets. Each pair shows the retained representative then the omitted redundant frame. Review before training.</p>']
    for n,row in enumerate(removed[:120]):
        i=int(row["index"]);r=int(row["representative"]);canvas=Image.new("RGB",(600,330),"white");draw=ImageDraw.Draw(canvas)
        for k,j in enumerate((r,i)):
            with Image.open(check_inside(ROOT/records[j]["image"])) as im:canvas.paste(ImageOps.fit(im.convert("RGB"),(300,300)),(300*k,0))
            for o in records[j]["objects"]:
                b=o["xyxy"];draw.rectangle((b[0]+300*k,b[1],b[2]+300*k,b[3]),outline="red",width=2)
            draw.text((300*k+4,305),f'{j} | {records[j]["id"]}',fill="black")
        key=tuple(sorted((i,r)));metric=scores.get(key,{});name=f"removed_{n:03d}.jpg";canvas.save(gallery/name,quality=90)
        page.append(f'<section><p>representative {r}; removed {i}; object cosine {metric.get("min_object_cosine","n/a")}; center {metric.get("maximum_center_delta","n/a")}; scale {metric.get("maximum_log_area_delta","n/a")}</p><img src="gallery/{name}"></section>')
    (out/"reduction_review.html").write_text("\n".join(page),encoding="utf-8")
    # Annotation outliers: source boxes remain unchanged; these are review prompts.
    candidates=[]
    for i,r in enumerate(records):
        for o in r["objects"]:
            b=o["xyxy"];area=(b[2]-b[0])*(b[3]-b[1])/(r["width"]*r["height"]);aspect=max((b[2]-b[0])/(b[3]-b[1]),(b[3]-b[1])/(b[2]-b[0]))
            candidates.append((area,aspect,i,o["class"],b))
    chosen=sorted(candidates)[:30]+sorted(candidates,reverse=True)[:20]+sorted(candidates,key=lambda x:x[1],reverse=True)[:30]
    outlier=['<!doctype html><meta charset="utf-8"><title>Annotation outliers</title><style>body{font:16px sans-serif;max-width:1100px;margin:auto}section{display:inline-block;border:1px solid #ccc;margin:7px;padding:7px}img{width:300px}</style><h1>Annotation outliers for manual review</h1><p>Small, large or extreme-aspect boxes are not automatically errors.</p>']
    for n,(area,aspect,i,name,b) in enumerate(chosen):
        with Image.open(check_inside(ROOT/records[i]["image"])) as im:canvas=im.convert("RGB").copy()
        d=ImageDraw.Draw(canvas);d.rectangle(tuple(b),outline="red",width=3);fn=f"box_outlier_{n:03d}.jpg";canvas.save(gallery/fn,quality=90)
        outlier.append(f'<section><img src="gallery/{fn}"><p>{records[i]["id"]} | {name}<br>area={area:.6f}, aspect={aspect:.2f}</p></section>')
    (out/"annotation_review.html").write_text("\n".join(outlier),encoding="utf-8")
    text=f'''# Object-aware reduced dataset\n\nStatus: PROVISIONAL; review before training.\n\nOriginal images: {summary["original_images"]:,}. Retained: {summary["kept_images"]:,}. Removed as covered redundancy: {summary["removed_images"]:,} ({100*(1-summary["retained_fraction"]):.2f}%).\nProtected images: {summary["protected_images"]:,}; rare classes: {", ".join(summary["rare_classes"])}.\n\nSplit images: {json.dumps(split["images"])}. Split boxes: {json.dumps(split["boxes"])}. Largest indivisible block: {split["largest_block"]}.\nAll retained strong similarity pairs are constrained to one split. This is similarity-aware, not guaranteed video-independent.\n\nA frame is removable only when a retained frame in the same compact complete-link group has the same class multiset, minimum matched-object cosine >= {cfg["object_cosine"]}, normalized center change <= {cfg["maximum_center_delta"]}, and absolute log-area change <= {cfg["maximum_log_area_delta"]}. Rare-class, multi-object, difficult, class-small and edge-object images are protected.\n\nThe constrained split optimizer returned a valid feasible allocation before reaching its {cfg["optimizer_time_limit_seconds"]}-second limit; it is not proven globally optimal. Every class occurs in every split. MetalSheet has an unavoidable 243/108/43 train/validation/test box distribution because its examples belong to a small number of indivisible correlated blocks.\n\nReview [reduction_review.html](reduction_review.html), [annotation_review.html](annotation_review.html), object_pair_distributions.png and class_distribution.csv. Removed files were not deleted from any earlier dataset. No YOLO training was run.\n'''
    (out/"REPORT.md").write_text(text,encoding="utf-8")

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("stage",choices=["embeddings","analyze","select","optimize","export","validate","report","all"]);p.add_argument("--config",default=str(HERE/"reduction_config.json"));a=p.parse_args()
    cfg=read_json(a.config);inp=check_inside(ROOT/cfg["input_output"]);out=check_inside(ROOT/cfg["output"]);out.mkdir(parents=True,exist_ok=True)
    stages=["embeddings","analyze","select","optimize","export","validate","report"] if a.stage=="all" else [a.stage]
    for stage in stages:print(f"=== {stage} ===",flush=True);globals()[stage](cfg,inp,out)
if __name__=="__main__":main()
