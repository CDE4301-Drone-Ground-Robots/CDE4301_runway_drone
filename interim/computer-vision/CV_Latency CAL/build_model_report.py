# -*- coding: utf-8 -*-
"""Build the offline HTML report from model_flops_summary.csv.
Run after profiling: python build_model_report.py
Only the HTML output is written; checkpoint and profiling source files are untouched.
"""

import csv, html, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
# Resolve every input/output beside this renderer, never from another project.

with (ROOT / 'model_flops_summary.csv').open(encoding='utf-8-sig',newline='') as f:
    data=list(csv.DictReader(f))
models=[r for r in data if r['category']=='model']
pre=[r for r in data if r['category']=='preprocessing']
e=lambda s:html.escape(str(s))
n=lambda x,d=0:f'{float(x):,.{d}f}'
p=models[2]

# Validate source arithmetic before making a readable report. Do not invent missing values.
assert len(models) == 4 and len(pre) == 5, "Expected four models and five preprocessing rows"
for r in models:
    assert not r['status'].startswith('FAILED'), r['model'] + ": profiling failed"
    assert int(r['FLOPs']) == 2 * int(r['MACs']), r['model'] + ": inconsistent FLOPs"
    assert abs(float(r['GMACs']) - int(r['MACs'])/1e9) < 1e-8
    assert abs(float(r['GFLOPs']) - int(r['FLOPs'])/1e9) < 1e-8
    assert 0 <= int(r['trainable_parameters']) <= int(r['total_parameters'])
assert int(p['memory_bank_elements']) == int(p['memory_bank_vectors'])*int(p['memory_bank_dimension'])
assert int(p['memory_bank_bytes']) == int(p['memory_bank_elements'])*4
assert int(p['distance_comparisons']) == int(p['query_patches'])*int(p['memory_bank_vectors'])
assert int(p['search_dot_product_MACs']) == int(p['distance_comparisons'])*int(p['memory_bank_dimension'])
assert int(p['search_dot_product_FLOPs']) == 2*int(p['search_dot_product_MACs'])
assert abs(float(p['backbone_plus_search_dot_GFLOPs']) -
           (int(p['FLOPs'])+int(p['search_dot_product_FLOPs']))/1e9) < 1e-8

css="""
:root{--ink:#173a30;--muted:#64776f;--line:#dce5dc;--green:#2f7456;--paper:#f6f8f4;--mono:Consolas,monospace}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 "Segoe UI",Arial,sans-serif}a{color:var(--green)}button{font:inherit;cursor:pointer}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #c78b24;outline-offset:4px}.wrap{max-width:1200px;margin:auto;padding:0 32px}.top{background:white;border-bottom:1px solid var(--line)}.top .wrap{display:flex;justify-content:space-between;align-items:center;min-height:74px}.brand{font-size:19px;font-weight:750;letter-spacing:-.5px}.logo{background:var(--ink);color:#d7eeac;display:inline-grid;place-items:center;width:33px;height:33px;border-radius:8px;margin-right:10px}nav{display:flex;gap:25px}nav a{font-size:12px;text-decoration:none;color:var(--muted)}.hero{display:flex;justify-content:space-between;align-items:end;gap:24px;padding:50px 0 30px}.eyebrow{text-transform:uppercase;letter-spacing:2px;font:11px/1.5 var(--mono);font-weight:700}h1{font-size:clamp(34px,4.5vw,54px);line-height:1.12;letter-spacing:-1.8px;margin:14px 0 18px;font-weight:650}h2{font-size:25px;letter-spacing:-.6px;margin:0 0 6px}h3{font-size:17px;margin:0}.lead{max-width:670px;color:var(--muted);font-size:16px}.actions{display:flex;flex-wrap:wrap;gap:9px}.button{font-size:12px;font-weight:650;background:white;border:1px solid var(--line);padding:10px 15px;border-radius:6px;text-decoration:none;color:var(--ink);white-space:nowrap}.primary{background:var(--ink);color:white;border-color:var(--ink)}.pills{display:flex;gap:8px;flex-wrap:wrap}.pill{font-size:11px;border:1px solid var(--line);background:white;padding:4px 10px;border-radius:20px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin:8px 0 25px}.stat{padding:20px;background:white;border:1px solid var(--line);border-radius:10px}.stat small{display:block;color:var(--muted);font-size:10px;letter-spacing:.8px}.stat strong{display:block;font-size:26px;letter-spacing:-.8px;font-weight:650;margin:7px 0}.stat span{font-size:12px;color:var(--muted)}.notice{background:#f4eddd;border:1px solid #e8dcbd;border-radius:8px;padding:15px 19px;color:#73571e;font-size:13px}.section{margin:34px 0}.section-head{margin-bottom:18px;display:flex;justify-content:space-between;align-items:end;gap:20px}.sub{margin:0;color:var(--muted);font-size:13px}.panel{background:white;border:1px solid var(--line);border-radius:11px;overflow:hidden}.scroll{overflow-x:auto}table{width:100%;border-collapse:collapse;text-align:left;font-size:13px;white-space:nowrap}th{padding:13px 18px;background:#eef3eb;color:var(--muted);font-size:10px;letter-spacing:.9px;text-transform:uppercase}td{padding:18px;border-top:1px solid #edf1e9;vertical-align:top}td small{display:block;font-size:11px;color:var(--muted);margin-top:5px}.num{font-family:var(--mono);font-size:12px}.name{font-weight:650}.badge{display:inline-block;font-size:10px;background:#e9f3e5;color:#3e6537;padding:3px 7px;border-radius:4px;line-height:1.4}.bound{background:#f8efda;color:#89651e}.table-note{font-size:12px;color:var(--muted);padding:13px 18px;border-top:1px solid var(--line);background:#fbfcfa}.two{display:grid;grid-template-columns:1.05fr 1fr;gap:22px}.pad{padding:25px}.seg{display:flex;border:1px solid var(--line);border-radius:5px;overflow:hidden}.seg button{border:0;background:white;color:var(--muted);font-size:11px;padding:6px 9px}.seg button[aria-pressed=true]{background:var(--ink);color:white}.chart-row{margin:21px 0}.chart-label{display:flex;justify-content:space-between;gap:12px;font-size:12px;margin-bottom:7px}.track{background:#eef2e9;border-radius:3px;height:13px;overflow:hidden}.bar{height:100%;border-radius:3px;background:var(--green);transition:width .25s}.chart-row:nth-child(2) .bar{background:#6b936b}.chart-row:nth-child(3) .bar{background:#99ae72}.chart-row:nth-child(4) .bar{background:#bbc996}.inline{font-size:12px;color:var(--muted);margin:16px 0 0}.dark{background:var(--ink);border-color:var(--ink);color:white}.dark .sub,.dark .inline{color:#bdcfc4}.formula{background:#284c3c;border:1px solid #557463;border-radius:7px;padding:14px;font:12px/1.9 var(--mono);margin:20px 0}.breakdown{display:grid;grid-template-columns:1fr 1fr;gap:18px}.breakdown strong{display:block;color:#d7eeac;font:26px/1.3 var(--mono)}.breakdown small{color:#c3d4c8;font-size:11px}.workflow{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}.step{padding:18px;border:1px solid var(--line);border-radius:8px;background:white}.step .n{font:10px var(--mono);color:var(--green);margin-bottom:13px}.step strong{display:block;font-size:13px}.step span{font-size:12px;color:var(--muted)}.pre{white-space:normal;min-width:680px}.pre td{font-size:12px}.pre .num{white-space:nowrap}.details{display:grid;grid-template-columns:1fr 1fr;gap:12px}details{background:white;border:1px solid var(--line);padding:17px 20px;border-radius:8px}summary{font-weight:650;font-size:13px;cursor:pointer}details p{font-size:12px;color:var(--muted);overflow-wrap:anywhere}code{font-family:var(--mono);font-size:12px}pre{background:#edf2e8;padding:16px;border-radius:7px;overflow:auto;font:12px var(--mono)}footer{margin-top:40px;border-top:1px solid var(--line);padding:22px 0 30px;color:var(--muted);font-size:12px}.foot{display:flex;justify-content:space-between;gap:20px}
@media(max-width:900px){.hero{align-items:start;flex-direction:column}.stats{grid-template-columns:1fr 1fr}.two{grid-template-columns:1fr}.workflow{grid-template-columns:1fr 1fr}.wrap{padding:0 22px}.section-head{flex-wrap:wrap}}
@media(max-width:550px){nav{display:none}.wrap{padding:0 16px}.hero{padding-top:32px}.stat{padding:15px}.stat strong{font-size:22px}.details{grid-template-columns:1fr}.pad{padding:20px}.foot{display:block}}

/* Dark appearance uses the same palette for every panel and control. */
:root{color-scheme:dark;--ink:#e8f2ed;--muted:#adc0b7;--line:#34493f;--green:#94dfb6;--paper:#0b1410;--surface:#15221b;--raised:#1d3025}
.top,.button,.pill,.stat,.panel,.step,details{background:var(--surface)}
.top{background:#101d16}
.logo{background:#94dfb6;color:#10251a}
.primary{background:#94dfb6;border-color:#94dfb6;color:#10251a}
.button:hover{background:#233c2c;color:#e8f2ed}.primary:hover{background:#b2efcc;color:#10251a}
nav a:hover{color:#94dfb6}
th{background:#1b2d22;color:#c0d2c7}
td{border-color:#293c30}
.badge{background:#203e2b;color:#b1eac4}
.bound{background:#40351d;color:#f3d48b}
.notice{background:#2b2517;border-color:#65522b;color:#f3d493}
.table-note{background:#111f17;color:#b3c6b9}
.seg button{background:#15221b;color:#b7cabe}.seg button[aria-pressed=true]{background:#94dfb6;color:#10251a}
.track{background:#293d2f}.bar{background:#94dfb6}
.chart-row:nth-child(2) .bar{background:#a4d788}.chart-row:nth-child(3) .bar{background:#79bfc0}.chart-row:nth-child(4) .bar{background:#c8c88b}
.dark{background:#173b28;border-color:#3b674a;color:#ecf8ee}
.dark .sub,.dark .inline{color:#c3d9c8}
.formula{background:#102a1b;border-color:#487253;color:#dcefe0}
.breakdown strong{color:#c7f5b0}.breakdown small{color:#d0e5d4}
pre{background:#0d1911;color:#d2e9d9;border:1px solid #354d3c}
.stat strong.input-pair{font-size:21px;line-height:1.5}
.glossary{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0}
.term{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:15px}
.term strong{display:block;color:#b8efce;font-size:13px}
.term p{font-size:12px;color:var(--muted);margin:5px 0 0}
.audit-note{margin:18px 0;padding:16px 18px;border:1px solid #4b7256;border-radius:8px;background:#162c1d;font-size:13px;color:#c9e6cf}
code{overflow-wrap:anywhere}
@media(max-width:900px){.glossary{grid-template-columns:1fr 1fr}}
@media(max-width:550px){.workflow,.glossary{grid-template-columns:1fr}.chart-label{flex-wrap:wrap}.stat strong.input-pair{font-size:16px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.bar{transition:none}}

@media print{:root{color-scheme:light;--ink:#173a30;--muted:#506257;--line:#b8c6bc;--green:#245b3c;--paper:#fff;--surface:#fff;--raised:#f2f5f0}body{background:white;color:#173a30}.top,.button,.pill,.stat,.panel,.step,details,.term,.audit-note{background:white;color:#173a30}.badge{background:#edf5e9;color:#245b3c}.bound,.notice{background:#faf4e4;color:#6d4d12}.table-note{background:white;color:#506257}th{background:#eef3eb;color:#506257}.term strong{color:#245b3c}pre{background:#eef3eb;color:#173a30}.wrap{max-width:none;padding:0}.top,.actions,.seg{display:none}.hero{padding:8px 0}h1{font-size:32px}.section{margin:20px 0}.panel,.stat,.step,details{break-inside:avoid}.scroll{overflow:visible}th,td{padding:10px 8px}.dark{background:white;color:var(--ink)}.dark .sub,.dark .inline,.breakdown small{color:#555}.breakdown strong{color:var(--green)}.formula{color:#222;background:#eee}.two{grid-template-columns:1fr 1fr}footer{margin-top:15px}}
"""
parts=['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>Vision models | Compute report</title><style>'+css+'</style></head><body>']
parts.append("""
<header class="top"><div class="wrap"><div class="brand"><span class="logo" aria-hidden="true">CV</span>Vision / Compute</div><nav aria-label="Report sections"><a href="#models">Models</a><a href="#patchcore">PatchCore</a><a href="#preprocessing">Preprocessing</a><a href="#method">Method</a></nav></div></header>
<main class="wrap"><section class="hero"><div><div class="eyebrow">CDE4301 \u00b7 Local profiling report</div><h1>Your vision pipeline,<br>by the numbers.</h1><p class="lead">Model complexity at deployment resolutions, with memory search and image preprocessing shown separately.</p><div class="pills"><span class="pill">1 MAC = 2 FLOPs</span><span class="pill">Batch size 1</span><span class="pill">CPU \u00b7 float32 \u00b7 eval</span><span class="pill">Offline report</span></div></div><div class="actions"><a class="button primary" href="model_flops_summary.csv" download>Download CSV</a><button class="button" id="print">Print / save PDF</button></div></section>
<div class="stats"><div class="stat"><small>CHECKPOINTS PROFILED</small><strong>04 / 04</strong><span>Original models preserved</span></div><div class="stat"><small>RGB SOURCE \u00b7 W \u00d7 H</small><strong>2472 \u00d7 2064</strong><span>Resize copies; crop original ROIs</span></div><div class="stat"><small>PATCHCORE MEMORY BANK</small><strong>33.60 MiB</strong><span>Stored features, not trainable weights</span></div><div class="stat"><small>MODEL INPUTS \u00b7 H \u00d7 W</small><strong class="input-pair">256 &times; 256<br>512 &times; 512</strong><span>PatchCore full frame / crack ROI</span></div></div>
<div class="notice"><strong>YOLO values are square-target bounds.</strong> No inference source or config was available here. The checkpoints retain <code>imgsz=1024</code> for FOD and <code>640</code> for thermal. Rectangular letterboxing may produce a smaller tensor; incoming ROI dimensions alone are not the network input.</div>
<section class="section" id="models"><div class="section-head"><div><div class="eyebrow">01 / Model comparison</div><h2>Compute per inference</h2><p class="sub">One invocation per model. PatchCore figures in this table cover its CNN only.</p></div><span class="badge">Strict weight checks + arithmetic audit</span></div><div class="panel"><div class="scroll"><table aria-label="Model parameters and arithmetic complexity"><thead><tr><th>Model / scope</th><th>Input N\u00d7C\u00d7H\u00d7W</th><th>Total params</th><th title="Number of parameters with requires_grad=True in the loaded or reconstructed model">Trainable flags*</th><th>GMACs</th><th>GFLOPs</th></tr></thead><tbody>
""")
for i,r in enumerate(models):
    bound='upper bound' in r['status']
    badge='Square-target bound' if bound else ('CNN only \u00b7 search separate' if i==2 else 'Deployment input')
    parts.append(f'<tr><td class="name">{e(r["model"])}<small><span class="badge {"bound" if bound else ""}">{badge}</span></small></td><td class="num">{e(r["input_size_NCHW"].replace("x", " " + chr(215) + " "))}</td>')
    for k in ['total_parameters','trainable_parameters','GMACs','GFLOPs']:
        parts.append(f'<td class="num">{n(r[k],3 if k in ["GMACs","GFLOPs"] else 0)}</td>')
    parts.append('</tr>')
parts.append("""
</tbody></table></div><div class="table-note">* These are parameter flags, not a measure of model capability. YOLO is loaded for inference with gradients disabled. The U-Net count assumes all parameters are trainable; its original freezing configuration is unknown. PatchCore uses a frozen feature extractor. N = batch, C = channels, H = height, W = width.</div></div></section>
<div class="two"><section class="panel pad"><div class="section-head"><div><h3 id="chart-title">Model arithmetic per inference</h3><p class="sub" id="chart-description">Same scopes as the table above; PatchCore CNN only.</p></div><div class="seg" aria-label="Chart metric"><button data-metric="GFLOPs" aria-pressed="true">GFLOPs</button><button data-metric="GMACs" aria-pressed="false">GMACs</button><button data-metric="params" aria-pressed="false">Params</button></div></div><div id="chart" aria-live="polite">
""")
short=['FOD YOLO11s','Crack U-Net','PatchCore CNN','Thermal YOLO11s']
maximum=max(float(r['GFLOPs']) for r in models)
for i,r in enumerate(models):
    vals={k:float(r[k]) for k in ['GFLOPs','GMACs']}
    vals['params']=float(r['total_parameters'])/1e6
    attrs=' '.join(f'data-{k.lower()}="{v}"' for k,v in vals.items())
    parts.append(f'<div class="chart-row" {attrs}><div class="chart-label"><span>{short[i]}</span><span class="value num">{n(r["GFLOPs"],3)} GFLOPs</span></div><div class="track"><div class="bar" style="width:{float(r["GFLOPs"])/maximum*100:.5f}%"></div></div></div>')
parts.append('<p class="inline">Arithmetic complexity does not directly predict latency. Hardware, memory traffic, kernel efficiency and preprocessing also matter.</p></div></section>')
parts.append(f"""
<section class="panel dark pad" id="patchcore"><div class="eyebrow">02 / Beyond the backbone</div><h2>PatchCore includes a search.</h2><p class="sub">Each query patch is compared with the saved memory bank. A CNN-only number understates the full pipeline cost.</p><div class="formula">{n(p['query_patches'])} query patches \u00d7 {n(p['memory_bank_vectors'])} bank vectors<br>\u00d7 {n(p['memory_bank_dimension'])} dimensions = {n(float(p['search_dot_product_MACs'])/1e9,3)} GMACs</div><div class="breakdown"><div><strong>{n(p['GFLOPs'],2)}</strong><small>CNN GFLOPs</small></div><div><strong>{n(float(p['search_dot_product_FLOPs'])/1e9,2)}</strong><small>Main search dot-product GFLOPs</small></div><div><strong>{n(p['backbone_plus_search_dot_GFLOPs'],2)}</strong><small>Partial combined GFLOPs</small></div><div><strong>{n(float(p['distance_comparisons'])/1e6,2)}M</strong><small>Distance comparisons per image</small></div></div><p class="inline">Dense exact search estimate. The partial combined value is only CNN + main search dot products. Norms, square roots, min/top-k, support reweighting and anomaly-map processing are additional. An approximate index could change search work; the actual backend was not recorded.</p></section></div>
<section class="section"><div class="section-head"><div><h3>YOLO: framework default vs. checkpoint setting</h3><p class="sub">Installed Ultralytics retains checkpoint image-size overrides when calling predict().</p></div></div><div class="panel"><div class="scroll"><table><thead><tr><th>Detector</th><th>Loaded imgsz</th><th>Framework default</th><th>Default 640\u00b2 GFLOPs</th><th>Exact padded tensor</th></tr></thead><tbody>
""")
for r in models:
    if r['configured_imgsz']:
        parts.append(f'<tr><td class="name">{e(r["model"])}</td><td class="num">{e(r["configured_imgsz"])}</td><td class="num">{e(r["framework_default_imgsz"])}</td><td class="num">{n(r["framework_default_square_GFLOPs"],3)}</td><td><span class="badge bound">Source dimensions needed</span></td></tr>')
parts.append("""
</tbody></table></div><div class="table-note">Use --fod-source-size H W and --thermal-source-size H W to resolve single-image rect=True letterboxing for known source dimensions.</div></div></section>
<section class="section" id="preprocessing"><div class="section-head"><div><div class="eyebrow">03 / Image preparation</div><h2>Keep preprocessing separate.</h2><p class="sub">The camera controls the source resolution. Each model receives its own prepared tensor.</p></div></div><div class="workflow"><div class="step"><div class="n">01 \u00b7 CAPTURE</div><strong>2472 \u00d7 2064 RGB</strong><span>Original frame, W \u00d7 H</span></div><div class="step"><div class="n">02 \u00b7 SCREEN</div><strong>256 \u00d7 256 PatchCore</strong><span>Resized copy of the full frame</span></div><div class="step"><div class="n">03 \u00b7 MAP + CROP</div><strong>Original-resolution ROI</strong><span>When an anomaly triggers</span></div><div class="step"><div class="n">04 \u00b7 SEGMENT</div><strong>512 \u00d7 512 U-Net</strong><span>Resized ROI, per crop</span></div></div><div class="panel"><div class="scroll"><table class="pre"><thead><tr><th>Operation</th><th>Source \u2192 destination \u00b7 W \u00d7 H</th><th>Conditional resize FLOPs</th><th>Interpretation</th></tr></thead><tbody>
""")
for r in pre:
    cost=n(r['preprocessing_bilinear_estimated_FLOPs']) if r['preprocessing_bilinear_estimated_FLOPs'] else 'Not determined'
    parts.append(f'<tr><td class="name">{e(r["model"])}</td><td>{e(r["preprocessing_source_WH"])} \u2192 {e(r["preprocessing_target_WH"] or "depends on source")}</td><td class="num">{cost}</td><td>{e(r["notes"])}</td></tr>')
parts.append("""
</tbody></table></div><div class="table-note">Conditional bilinear model: 4 multiplications + 3 additions per output channel sample, three channels. Excludes coordinate/weight generation, antialiasing, conversion and normalization. Actual interpolation was unavailable. These estimates are separate from model GFLOPs.</div></div></section>
<section class="section" id="method"><div class="section-head"><div><div class="eyebrow">04 / Reproducibility</div><h2>What these numbers mean</h2><p class="sub">Definitions first, then the exact counts and model assumptions.</p></div></div>
<div class="glossary">
<div class="term"><strong>MACs / GMACs</strong><p>A multiply-accumulate combines multiplication and addition. One GMAC means one billion MACs.</p></div>
<div class="term"><strong>FLOPs / GFLOPs</strong><p>Floating-point arithmetic operations. One GFLOP means one billion operations. Here, 1 MAC = 2 FLOPs.</p></div>
<div class="term"><strong>Parameters</strong><p>Weight and bias values stored in the model. Parameter count is independent of image resolution and excludes feature buffers.</p></div>
<div class="term"><strong>ROI / letterbox</strong><p>ROI means a cropped region of interest. Letterboxing resizes while preserving aspect ratio, then pads to the required shape.</p></div></div>
<div class="audit-note"><strong>Arithmetic checked independently.</strong> PyTorch operator-level convolution and matrix-product counts matched the four model profiles at the listed resolutions. Weight totals also matched. This validates the stated arithmetic scope; unknown YOLO source shapes and search-backend behavior remain explicit assumptions.</div>
<div class="details">
<details><summary>Counting convention and exclusions</summary><p>1 MAC = 2 FLOPs; G = 10\u2079; M = 10\u2076; MiB = 2\u00b2\u2070 bytes. Convolution, linear layers and YOLO attention matrix products are included. Normalization, activations, pooling, interpolation, residual/scalar arithmetic, preprocessing, NMS and output processing are excluded. Counts describe dominant dense arithmetic, not every operation. FLOPs here is an operation count per invocation, not FLOPs per second (FLOP/s). Parameters are counted independently from model.parameters(); buffers are excluded. No whole-pipeline latency or FPS is claimed.</p></details>
<details><summary>Construction and profiling method</summary><p>Actual local Ultralytics checkpoints are loaded. Crack weights strictly match segmentation_models_pytorch.Unet with ResNet34, decoder channels (256, 128, 64, 32, 16), three input channels and one output class. PatchCore strictly loads a timm Wide-ResNet50-2 feature extractor with layer2/layer3 outputs; unused layer4 and the classification head are absent. THOP 2.1.6 uses explicit convolution/linear rules plus separate functional-attention counting. All models are forwarded at full input size.</p></details>
""")
for r in models:
    # The checkpoint itself omits preprocessing; the user separately confirmed it.
    note=r['notes'].replace('Input resize/crop/tiling configuration is absent; workload is per supplied model tensor, before tiling.','The checkpoint omits preprocessing configuration; this report uses the user-confirmed 256x256 full-frame deployment input.')
    exact=f'Checkpoint: {r["checkpoint"]}. MACs: {n(r["MACs"])}. FLOPs: {n(r["FLOPs"])}. Parameter scope: {r["parameter_scope"]}. Input evidence: {r["input_size_source"]}.'
    parts.append(f'<details><summary>{e(r["model"])} \u00b7 full profile notes</summary><p>{e(exact)}</p><p>{e(note)}</p>')
    if r is p:
        extra=f'Bank: {n(r["memory_bank_elements"])} float32 elements / {n(r["memory_bank_bytes"])} bytes. Estimated norm/combine overhead: {n(r["search_norm_and_combine_FLOPs"])} scalar FLOPs; {n(r["search_sqrt_evaluations"])} square-root evaluations; {n(r["search_minimum_comparisons"])} minimum comparisons. Optional support reweighting: {n(r["extra_reweight_dot_product_MACs"])} additional dot-product MACs, excluding other operations.'
        parts.append('<p>'+e(extra)+'</p>')
    parts.append('</details>')
parts.append("""
</div><div class="panel pad" style="margin-top:18px"><h3>Run the profiler again</h3><p class="sub">From this folder, using the prepared Python environment:</p><pre>.\\.profile_venv\\Scripts\\python.exe profile_models.py</pre><p class="inline">This HTML displays the saved CSV. After re-profiling, regenerate this report with <code>python build_model_report.py</code>. Model parameters and network code are unchanged. For package installation and input overrides, see <a href="PROFILING_README.md">PROFILING_README.md</a> or <a href="profile_models.py">profile_models.py</a>.</p></div></section></main><footer><div class="wrap foot"><span>VISION / COMPUTE \u00b7 CDE4301 \u00b7 Local results</span><span>Per invocation \u00b7 Original model files unchanged</span></div></footer>
<script>
"use strict";
document.getElementById("print").addEventListener("click",()=>window.print());
document.querySelectorAll("[data-metric]").forEach(button=>button.addEventListener("click",()=>{
 const metric=button.dataset.metric, key=metric.toLowerCase();
 document.getElementById("chart-title").textContent=metric==="params"?"Model parameter counts":"Model arithmetic per inference";
 document.getElementById("chart-description").textContent=metric==="params"?"Millions of weight values; memory-bank features are excluded.":"Same scopes as the table above; PatchCore CNN only.";
 const rows=[...document.querySelectorAll(".chart-row")];
 const max=Math.max(...rows.map(row=>Number(row.dataset[key])));
 rows.forEach(row=>{
  const value=Number(row.dataset[key]);
  row.querySelector(".bar").style.width=(value/max*100)+"%";
  row.querySelector(".value").textContent=value.toLocaleString("en-US",{minimumFractionDigits:3,maximumFractionDigits:3})+" "+(metric==="params"?"M params":metric);
 });
 document.querySelectorAll("[data-metric]").forEach(b=>b.setAttribute("aria-pressed",String(b===button)));
}));
</script></body></html>
""")
output=ROOT / 'model_flops_report.html'
report = ''.join(parts)
audited_profiles = [(9440176, 55496278016), (24436369, 62511906816),
                    (24862528, 23997710336), (9428566, 21422028800)]
current_profiles = [(int(r['total_parameters']), int(r['FLOPs'])) for r in models]
if current_profiles != audited_profiles:
    report = report.replace('Strict weight checks + arithmetic audit', 'Source arithmetic checked')
    start = report.index('<div class="audit-note">')
    end = report.index('</div>', start) + len('</div>')
    report = report[:start] + '<div class="audit-note"><strong>Source arithmetic checked.</strong> MAC/FLOP conversion, parameter flags, memory-bank size and main search arithmetic are consistent with the CSV. These updated profiles have not been independently rechecked with PyTorch operator profiling.</div>' + report[end:]
output.write_text(report, encoding='utf-8')
print(f'Created {output.name}: {output.stat().st_size:,} bytes; four model rows and five preprocessing rows.')
