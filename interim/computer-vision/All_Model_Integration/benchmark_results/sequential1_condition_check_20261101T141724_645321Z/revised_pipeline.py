def pipeline(frame, models, parallel=False, executor=None, streams=None, sequential2=False):
    patch=detect(models["patchcore"],frame)
    details=dict(crop_count=0,stages=["patchcore"],crop_resize_host_ms=0.,
        output_merge_host_ms=0.,coordinate_extraction_ms=0.,coordinate_count=0,
        message_preparation_ms=0.,fod_calls=0,crack_calls=0,fod_positive_crops=0,
        crack_positive_crops=0,neither_detected_crops=0,no_crack_base_crops=0)
    records=[]
    frame_size=(frame.shape[1],frame.shape[0])
    for roi in patch["boxes"]:
        t=time.perf_counter()
        xa,ya,xb,yb=roi
        crop=frame[ya:yb,xa:xb]
        if not crop.size: continue
        zoom=cv2.resize(crop,(1280,720))
        details["crop_resize_host_ms"]+=(time.perf_counter()-t)*1000
        details["crop_count"]+=1
        details["fod_calls"]+=1
        cr=None
        if parallel:
            def task(name):
                if streams:
                    with torch.cuda.stream(streams[name]):
                        return fod_branch(zoom,roi,frame_size,models[name]) if name=="fod" else detect(models[name],zoom)
                return fod_branch(zoom,roi,frame_size,models[name]) if name=="fod" else detect(models[name],zoom)
            f=executor.submit(task,"fod"); c=executor.submit(task,"crack")
            fod_records,coordinate_ms,message_ms=f.result()
            cr=c.result()
            details["crack_calls"]+=1
        else:
            fod_records,coordinate_ms,message_ms=fod_branch(zoom,roi,frame_size,models["fod"])
            # Corrected sequential fallback: run U-Net ONLY if YOLO detects no FOD.
            if sequential2 or not fod_records:
                cr=detect(models["crack"],zoom)
                details["crack_calls"]+=1
        details["coordinate_extraction_ms"]+=coordinate_ms
        details["coordinate_count"]+=len(fod_records)
        details["message_preparation_ms"]+=message_ms
        details["fod_positive_crops"]+=int(bool(fod_records))
        t=time.perf_counter()
        records.extend(fod_records)
        details["output_merge_host_ms"]+=(time.perf_counter()-t)*1000
        # Base receives positive cracks, and residual anomalies when neither detects.
        t=time.perf_counter()
        if cr is not None:
            details["crack_positive_crops"]+=1
            records.append(pack_message("CRACK","BASE",
                dict(bbox_original_px=remap_box(cr["bbox"],roi),roi=roi)))
        elif sequential2 and not fod_records:
            details["no_crack_base_crops"]+=1
            details["neither_detected_crops"]+=1
            records.append(pack_message("UNCLASSIFIED_ANOMALY","BASE",dict(roi=roi)))
        elif not fod_records:
            details["neither_detected_crops"]+=1
            records.append(pack_message("UNCLASSIFIED_ANOMALY","BASE",dict(roi=roi)))
        details["message_preparation_ms"]+=(time.perf_counter()-t)*1000
    if details["fod_calls"]:details["stages"].append("fod")
    if details["crack_calls"]:details["stages"].append("crack")
    if details["coordinate_count"]:details["stages"].append("simulated_coordinate_extraction")
    details["message_count"]=len(records)
    details["ugv_message_count"]=sum(r["destination"]=="UGV" for r in records)
    details["base_message_count"]=sum(r["destination"]=="BASE" for r in records)
    return records,details
