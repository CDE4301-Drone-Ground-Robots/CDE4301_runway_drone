"""Small algorithm checks: no source files read or modified."""
import importlib.util
import random
from pathlib import Path
import numpy as np

spec=importlib.util.spec_from_file_location("audit",Path(__file__).with_name("pipeline.py"))
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rng=random.Random(4301)
values=[rng.getrandbits(64) for _ in range(400)]
values += [values[0]^((1<<j)-1) for j in range(1,8)]+[values[0]]
tree=m.BKTree()
for i,v in enumerate(values): tree.add(v,i)
for v in values[::7]:
    actual=set(tree.query(v,6))
    expected={(i,(v^w).bit_count()) for i,w in enumerate(values) if (v^w).bit_count()<=6}
    assert actual==expected,"BK-tree radius recall failed"
print("PASS: BK-tree matches exhaustive Hamming search, including repeated hashes")

captured={}
m.load_manifest=lambda out:[{"image_sha256":str(i),"id":str(i)} for i in range(3)]
chain=[dict(a="0",b="1",decision="",exact="0",provisional_strong="1",cosine=".99",phash_distance="2"),
       dict(a="1",b="2",decision="",exact="0",provisional_strong="1",cosine=".99",phash_distance="2")]
m.read_pairs=lambda out:chain
m.save_json=lambda p,data:captured.update({p.name:data})
m.write_csv=lambda *args:None
m.groups({},m.HERE)
assert max(g["size"] for g in captured["groups.json"])==2
assert len(captured["blocked_merges.json"])==1
print("PASS: A-B and B-C cannot merge A,B,C without A-C evidence")

chain.append(dict(a="0",b="2",decision="",exact="0",provisional_strong="1",cosine=".99",phash_distance="2"))
m.groups({},m.HERE)
assert max(g["size"] for g in captured["groups.json"])==3
print("PASS: complete pairwise evidence permits a three-image group")

chain[2]["decision"]="reject"
m.groups({},m.HERE)
assert max(g["size"] for g in captured["groups.json"])==2
print("PASS: explicit rejection blocks a proposed merge")

try:
    m.confined(m.ROOT.parent/"outside")
    raise AssertionError("Workspace boundary failed")
except ValueError:
    pass
print("PASS: workspace path boundary")

# The exact cosine backend must match a NumPy all-pairs reference.
e=np.random.default_rng(4301).normal(size=(24,16)).astype(np.float32)
e/=np.linalg.norm(e,axis=1,keepdims=True)
ids,scores=m.cosine_knn(e,3,7)
reference=e@e.T; np.fill_diagonal(reference,-np.inf)
expected=np.argsort(reference,axis=1)[:,-3:][:,::-1]
assert np.array_equal(ids,expected)
assert np.allclose(scores,np.take_along_axis(reference,expected,axis=1),atol=1e-5)
splits=np.arange(24)%3
ids,scores=m.cosine_knn(e,1,7,splits)
reference[splits[:,None]==splits[None,:]]=-np.inf
assert np.array_equal(ids[:,0],np.argmax(reference,axis=1))
print("PASS: exact batched cosine and cross-split search match exhaustive reference")


# A-B/B-C remain separate compact groups but must be co-located during splitting.
m.read_json=lambda path:[dict(group_id="one",members=[0,1]),dict(group_id="two",members=[2])]
m.read_pairs=lambda out:chain[:2]
blocks=m.allocation_blocks(m.HERE,[{}, {}, {}])
assert len(blocks)==1 and blocks[0]["members"]==[0,1,2]
print("PASS: strong edges between distinct compact groups impose same-split constraints")

strict={"strong_rule":"strict_union","strong_phash":6,"strong_cosine":.97,"dino_alone_cosine":.99}
assert m.is_strong_pair(strict,18,.991)
assert m.is_strong_pair(strict,6,.971)
assert not m.is_strong_pair(strict,7,.989)
assert not m.is_strong_pair(strict,6,.969)
print("PASS: strict union thresholds include DINO-only and joint pHash/DINO matches")
