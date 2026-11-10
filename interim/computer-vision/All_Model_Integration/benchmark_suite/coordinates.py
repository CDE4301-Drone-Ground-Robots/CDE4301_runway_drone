"""Simulated planar pixel-to-world coordinates, following the supplied worked example.
No GPS, camera calibration, attitude estimation or network operations.
"""
import math

def remap_box(box, roi, detector_size=(1280,720)):
    rx1,ry1,rx2,ry2=map(float,roi)
    sw,sh=map(float,detector_size)
    if sw<=0 or sh<=0 or rx2<=rx1 or ry2<=ry1:
        raise ValueError("Invalid detector size or ROI")
    x1,y1,x2,y2=map(float,box)
    sx,sy=(rx2-rx1)/sw,(ry2-ry1)/sh
    return (round(rx1+x1*sx),round(ry1+y1*sy),
            round(rx1+x2*sx),round(ry1+y2*sy))

def extract(box, roi, frame_size, simulation, detector_size=(1280,720)):
    w,h=map(float,frame_size)
    gw,gh=map(float,simulation["ground_coverage_m"])
    ux,uy=map(float,simulation["uav_world_m"])
    if not all(math.isfinite(v) for v in (w,h,gw,gh,ux,uy)) or min(w,h,gw,gh)<=0:
        raise ValueError("Invalid simulated geometry")
    mapped=remap_box(box,roi,detector_size)
    x1,y1,x2,y2=mapped
    cx,cy=(x1+x2)/2.,(y1+y2)/2.
    dx,dy=cx-w/2.,cy-h/2.
    gx,gy=dx*gw/w,dy*gh/h
    return dict(simulated=True,bbox_original_px=mapped,center_px=(cx,cy),
                offset_px=(dx,dy),ground_offset_m=(gx,gy),world_xy_m=(ux+gx,uy+gy))

def self_test(simulation):
    example=extract((171,137,273,341),(400,200,700,500),(1280,720),
                    simulation,detector_size=(512,512))
    assert example["bbox_original_px"]==(500,280,560,400)
    assert example["center_px"]==(530.,340.)
    assert math.isclose(example["world_xy_m"][0],2.828125,abs_tol=1e-12)
    assert math.isclose(example["world_xy_m"][1],3.9444444444444446,abs_tol=1e-12)
    center=extract((0,0,1280,720),(0,0,1280,720),(1280,720),simulation)
    assert center["world_xy_m"]==(3.,4.)
    # Non-square source frame and ROI: exercise independent x/y scale.
    nonsquare=extract((0,0,1280,720),(100,200,300,600),(800,1000),simulation)
    assert nonsquare["center_px"]==(200.,400.)
    assert nonsquare["world_xy_m"]==(2.5,3.8)
    # Wrapper boxes already refer to the zoomed 1280x720 image, not raw 512x512.
    restored=extract((0,0,1280,720),(400,200,700,500),(1280,720),simulation)
    assert restored["bbox_original_px"]==(400,200,700,500)
    return dict(status="passed",checks=4,example=example,
                meaning="math test only; not measured localisation accuracy")

