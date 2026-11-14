"""Correctness checks only: fake detector outputs are never used as performance samples."""
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import core

class Stub:
    def __init__(self,result):self.result=result;self.calls=0
    def detect(self,frame):self.calls+=1;return self.result

def check(fod,crack,parallel,anomaly=True):
    det=dict(object="test",confidence=.9,bbox=(0,0,1280,720))
    models=dict(patchcore=Stub(dict(boxes=[(0,0,8,8)] if anomaly else [])),
                fod=Stub([det] if fod else []),
                crack=Stub(dict(bbox=(0,0,1280,720)) if crack else None))
    frame=np.zeros((8,8,3),dtype=np.uint8)
    with ThreadPoolExecutor(max_workers=2) as pool:
        records,details=core.pipeline(frame,models,parallel,pool if parallel else None)
    expected_crack=int(anomaly and (parallel or not fod))
    assert models["crack"].calls==expected_crack
    assert models["fod"].calls==int(anomaly)
    assert details["coordinate_count"]==int(anomaly and fod)
    expected_base=int(anomaly and ((crack and expected_crack) or not fod))
    assert details["base_message_count"]==expected_base
    assert details["ugv_message_count"]==int(anomaly and fod)
    assert np.count_nonzero(frame)==0
    return dict(fod=fod,crack=crack,parallel=parallel,anomaly=anomaly,status="passed",routing=details)

if __name__=="__main__":
    checks=[check(f,c,p) for p in (False,True) for f,c in ((True,True),(True,False),(False,True),(False,False))]
    checks += [check(False,False,p,anomaly=False) for p in (False,True)]
    core.write_json(core.OUT/"routing_checks.json",dict(status="passed",checks=checks,
        meaning="logic checks, not model accuracy or timing measurements"))
    core.write_json(core.OUT/"coordinate_math_test.json",core.self_test(core.SIMULATION))
    print("Passed 10 routing checks and 4 coordinate math checks",flush=True)

