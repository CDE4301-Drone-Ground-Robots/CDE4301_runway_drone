# Local model profiling

Run from this folder (the profiling environment has been prepared here):

    .\.profile_venv\Scripts\python.exe profile_models.py

Output: model_flops_summary.csv. All original checkpoint files are read only.
No training/inference source files were present in this folder.

For another Python environment, install:

    python -m pip install torch torchvision ultralytics ultralytics-thop==2.1.6 segmentation-models-pytorch==0.5.0 timm==1.0.30

Only load trusted checkpoints: the Ultralytics files contain pickled Python models.
Anomalib is not required. Its saved precision enum is read as inert metadata; the
actual timm feature extractor is reconstructed and its complete weights loaded
with strict=True. No pretrained downloads are used.

## Deployment inputs and YOLO evidence

User-confirmed deployment: original RGB frame 2472x2064 (W x H).
PatchCore receives a 256x256 resize of the FULL frame. Detected ROIs are mapped back
to the original frame and cropped there. U-Net receives a 512x512 resize of that
original-resolution ROI. These are the script's defaults; no webcam dimensions
are used.

No inference/training source or separate config exists in this folder. In the
installed Ultralytics 8.4.126:
- Generic DEFAULT_CFG_DICT["imgsz"] is 640.
- Loading FOD_yolo11s.pt retains imgsz=1024 in YOLO(...).overrides.
- Loading Thermal_yolo11s.pt retains imgsz=640.
- Model.predict() merges these overrides; without an explicit imgsz argument,
  it retains 1024 for this FOD checkpoint and 640 for thermal. This was verified
  by inspecting the loaded objects and installed Model.predict/_reset_ckpt_args.
- The CSV reports generic-default 640-square costs separately.
- predict defaults to rect=True, allowing smaller stride-padded tensors than the
  square target. No YOLO ROI or thermal source dimensions are available, so the
  default square profiles are upper bounds, not certified actual pipeline costs.

For actual single-image rectangular letterbox shapes, supply source H W dimensions:

    .\.profile_venv\Scripts\python.exe profile_models.py --fod-source-size H W --thermal-source-size H W

Replace H and W with integer dimensions. The script runs Ultralytics LetterBox
(auto=True, stride=model stride) to determine the model tensor size. This assumes
single-image PyTorch inference with rect=True. It does not change inference code.
Explicit --fod-size H W and --thermal-size H W override configured imgsz targets.
Without source-size arguments they profile the supplied tensor dimensions directly
as square/rectangular target bounds.

U-Net/PatchCore can be overridden using --unet-size H W / --patchcore-size H W.
--roi-size H W records a known original-resolution RGB ROI in preprocessing rows.
All dimensions on command-line arguments are H W.

## Preprocessing, reported separately

The same CSV contains category=preprocessing rows. Network MAC fields are blank
for these rows. The full-frame resize is 2472x2064 -> 256x256, and the original-frame
ROI resize is dynamic ROI -> 512x512. At three channels, a conditional bilinear
model uses 7*Hout*Wout*3 FLOPs (four multiplies plus three adds per output sample):
1,376,256 FLOPs for PatchCore resize; 5,505,024 for U-Net resize. These are separate
estimates, not measured operations or claims about the unknown interpolation.
Coordinate/coefficient generation, antialiasing, conversions and normalization
are excluded. The ROI map uses x scale 2472/256 and y scale 2064/256; four bounding
coordinates require four multiplications, with rounding/clamping separately.
Crop cost depends on ROI dimensions and whether the implementation returns a view
or makes a copy. YOLO letterbox cost depends on source aspect ratio and cannot
be assigned a defensible numeric total without source dimensions/backend.
U-Net/FOD branch cost per camera frame also depends on anomaly frequency and ROI
count; the script reports per-invocation model costs, not an invented frame total.

## Counts and limitations

Batch 1, float32, eval, full-size forward; CPU by default, optional --device cuda.
1 MAC = 2 FLOPs; GFLOPs = FLOPs / 1e9. THOP counts convolution/linear MACs with
explicit rules. YOLO attention's two matrix products are included separately.
Normalization, activations, pooling, interpolation, elementwise/residual arithmetic,
preprocessing, NMS, and output processing are excluded. Counts therefore describe
the dominant dense arithmetic, not every operation or measured latency.
THOP is pinned because its hook traversal and functional-matmul support affect
custom counting rules. No spatial scaling from a smaller profile is used.

Parameters are counted independently using model.parameters(), including unused
parameters but excluding buffers. YOLO requires_grad flags are those of its loaded
inference model (often all zero). U-Net's original freezing cannot be recovered
from a state_dict; its trainable count uses constructor defaults. PatchCore is
frozen. U-Net and timm backbone weights must load strictly before counts are reported.

PatchCore CNN: Wide-ResNet50-2 only through layer3, feature taps layer2 and layer3.
It does not include the unused classifier or layer4. Memory bank: 5734 x 1536,
float32, 8,807,424 elements, 35,229,696 bytes (~33.60 MiB), a buffer rather than
trainable weights. Runtime includes BOTH CNN extraction and nearest-neighbour
memory search, plus feature/map processing.

With Q observed layer2 patch locations, M bank vectors and D feature dimensions,
exact dense search evaluates Q*M distances and has Q*M*D dot-product MACs.
The CSV also reports uncached norm/combine overhead:
(Q+M)*(2D-1) + 3*Q*M scalar FLOPs, Q*M sqrt evaluations, and Q*(M-1) minimum
comparisons. Caching norms or using squared distances changes this overhead.
For num_neighbors=9, optional support-neighbour reweighting is reported separately
as M*D + 9*D extra dot-product MACs, excluding its norms, top-k and softmax.
Actual search index/backend is unknown: no ANN speedup is assumed. The combined
CNN+search GFLOPs field is a partial total of CNN and main dot products only.
No giant pairwise distance matrix is allocated during profiling.

References:
- https://github.com/ultralytics/thop
- https://smp.readthedocs.io/en/docs/models.html
- https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/models/image/patchcore.html

Ultralytics preprocessing reference: https://docs.ultralytics.com/modes/predict/

## HTML report

Open model_flops_report.html for the offline dark-mode dashboard. To refresh it after generating a new CSV, run:

    python build_model_report.py

The renderer uses only Python standard-library modules, validates source arithmetic, and writes only the HTML file. Unicode symbols are emitted as UTF-8 rather than passed through a legacy terminal encoding.
