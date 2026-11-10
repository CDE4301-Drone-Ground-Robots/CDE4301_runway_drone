"""Profile only the checkpoints beside this script; never import pipeline code.

Run: .\.profile_venv\Scripts\python.exe profile_models.py
Deployment defaults: U-Net 512x512 ROI; PatchCore 256x256 full RGB frame.
Override sizes: --unet-size H W --patchcore-size H W
YOLO overrides: --fod-size H W --thermal-size H W
One image, CPU/float32 by default. No pretrained weights are downloaded.
"""
import argparse
import csv
import gc
import importlib.metadata
import os
import pickle
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# Keep library settings/cache writes in this project, including on subsequent runs.
sys.dont_write_bytecode = True
for key, folder in {
    "YOLO_CONFIG_DIR": ".profile_config", "TORCH_HOME": ".profile_cache/torch",
    "HF_HOME": ".profile_cache/huggingface", "MPLCONFIGDIR": ".profile_cache/matplotlib",
}.items():
    os.environ[key] = str(ROOT / folder)

import torch
from torch import nn
from thop import profile

CONVENTION = (
    "1 MAC = 2 FLOPs; batch=1; convolution/linear and YOLO attention matrix products only. "
    "Excluded: normalization, activation, pooling, interpolation, residual/scalar arithmetic, "
    "preprocessing, NMS and output processing. Arithmetic estimates, not latency."
)
FIELDS = [
    "category", "model", "checkpoint", "status", "input_size_NCHW", "input_size_source",
    "configured_imgsz", "framework_default_imgsz", "framework_default_square_MACs",
    "framework_default_square_GFLOPs", "preprocessing_operations",
    "preprocessing_source_WH", "preprocessing_target_WH", "preprocessing_output_pixels",
    "preprocessing_bilinear_estimated_FLOPs",
    "total_parameters", "trainable_parameters", "parameter_scope",
    "MACs", "GMACs", "FLOPs", "GFLOPs", "convention",
    "memory_bank_vectors", "memory_bank_dimension", "memory_bank_elements",
    "memory_bank_bytes", "memory_bank_MiB", "query_patches",
    "distance_comparisons", "search_dot_product_MACs",
    "search_dot_product_FLOPs", "search_norm_and_combine_FLOPs",
    "search_sqrt_evaluations", "search_minimum_comparisons",
    "extra_reweight_dot_product_MACs", "backbone_plus_search_dot_GFLOPs",
    "notes",
]


class PrecisionMetadata:
    """Preserve an Anomalib enum value without installing its training stack."""
    def __init__(self, *values):
        self.values = values


class MetadataUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # This checkpoint's ONLY unavailable global is a precision enum.
        # Never substitute model/transform classes or silently guess their behavior.
        if module == "anomalib" and name == "PrecisionType":
            return PrecisionMetadata
        return super().find_class(module, name)


def load_checkpoint(filename, patchcore=False):
    """Load user-supplied local checkpoints; pickle files must be trusted."""
    path = ROOT / filename
    if not path.is_file():
        raise FileNotFoundError(path.name)
    kwargs = {}
    if patchcore:
        kwargs["pickle_module"] = types.SimpleNamespace(
            __name__="profiling_metadata", Unpickler=MetadataUnpickler, load=pickle.load
        )
    return torch.load(path, map_location="cpu", weights_only=False, **kwargs)


def get_size(override, saved=None, reference=256):
    """Never describe a saved training size or reference size as verified inference."""
    if override:
        return tuple(override), "user supplied deployment tensor size", False
    if saved is not None:
        size = (saved, saved) if isinstance(saved, int) else tuple(saved)
        if len(size) != 2:
            raise ValueError(f"Invalid saved image size: {saved}")
        return size, "checkpoint train_args.imgsz; inference size unverified", True
    return (reference, reference), "REFERENCE ONLY: actual pipeline resolution unavailable", True


def zero_ops(module, inputs, output):
    # This explicit policy makes MAC and FLOP units consistent across all models.
    pass


def count_conv(module, inputs, output):
    k = 1
    for dim in module.kernel_size:
        k *= dim
    module.total_ops += output.numel() * (module.in_channels // module.groups) * k


def count_linear(module, inputs, output):
    module.total_ops += output.numel() * module.in_features


def arithmetic_profile(model, shape, device):
    """THOP counts Conv/Linear. Count YOLO's functional attention products explicitly.

    THOP 2.1.6 visits child modules even when a parent has a custom rule.
    Pin this version so functional matmul support in later versions cannot double count.
    All sizes are forwarded in full: no spatial extrapolation.
    """
    version = importlib.metadata.version("ultralytics-thop")
    if version != "2.1.6":
        raise RuntimeError("Use ultralytics-thop==2.1.6 for this script's counting policy.")
    model = model.float().to(device).eval()
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    custom = {}
    for module in model.modules():
        rule = zero_ops
        if isinstance(module, (nn.Conv1d, nn.Conv2d, nn.Conv3d)):
            rule = count_conv
        elif isinstance(module, nn.Linear):
            rule = count_linear
        custom[type(module)] = rule

    # YOLO11 C2PSA contains functional Q^T K and V A products invisible to
    # this THOP version's module hooks. Include both without counting them twice.
    attention_macs = [0]
    handles = []
    from ultralytics.nn.modules.block import Attention

    def count_attention(module, inputs, output):
        batch, _, height, width = inputs[0].shape
        tokens = height * width
        attention_macs[0] += (
            batch * module.num_heads * tokens * tokens
            * (module.key_dim + module.head_dim)
        )

    for module in model.modules():
        if isinstance(module, Attention):
            handles.append(module.register_forward_hook(count_attention))
    try:
        x = torch.zeros(shape, device=device)
        with torch.inference_mode():
            macs, _ = profile(model, inputs=(x,), custom_ops=custom, verbose=False)
        return total, trainable, int(macs) + attention_macs[0]
    finally:
        for handle in handles:
            handle.remove()


def fill_profile(row, model, channels, size, device):
    shape = (1, channels, *size)
    row["input_size_NCHW"] = "x".join(map(str, shape))
    total, trainable, macs = arithmetic_profile(model, shape, device)
    row.update(total_parameters=total, trainable_parameters=trainable,
               MACs=macs, GMACs=macs / 1e9, FLOPs=2 * macs, GFLOPs=2 * macs / 1e9)


def profile_yolo(row, filename, override, device, source_size=None):
    # Inspect actual checkpoint-loading behavior as well as the generic default.
    from ultralytics import YOLO
    from ultralytics.cfg import DEFAULT_CFG_DICT
    from ultralytics.data.augment import LetterBox
    import numpy as np

    yolo = YOLO(str(ROOT / filename))
    model = yolo.model
    framework_size = DEFAULT_CFG_DICT["imgsz"]
    configured = override or yolo.overrides.get("imgsz", framework_size)
    size = (configured, configured) if isinstance(configured, int) else tuple(configured)
    row.update(configured_imgsz=str(configured), framework_default_imgsz=str(framework_size))
    row["input_size_source"] = (
        "explicit --size override" if override else
        "YOLO(checkpoint).overrides.imgsz inherited by predict(); no pipeline config available"
    )
    channels = next(m.in_channels for m in model.modules() if isinstance(m, nn.Conv2d))
    stride = int(model.stride.max().item())
    if any(s % stride for s in size):
        raise ValueError(f"YOLO target dimensions must be multiples of stride {stride}.")
    if source_size:
        # Match single-image PyTorch predict(rect=True): use the REAL Ultralytics
        # preprocessing class to determine the network tensor, not the raw ROI size.
        source_h, source_w = source_size
        transformed = LetterBox(size, auto=True, stride=stride)(
            image=np.zeros((source_h, source_w, 3), dtype=np.uint8))
        size = transformed.shape[:2]
        row["status"] = "rectangular profile; assuming predict(rect=True), batch=1"
        row["preprocessing_source_WH"] = f"{source_w}x{source_h}"
    else:
        row["status"] = "square-target upper bound; exact rect tensor unknown"
    row["parameter_scope"] = "actual loaded Ultralytics model; requires_grad flags as loaded"
    fill_profile(row, model, channels, size, device)
    # Report generic framework-default square cost separately; it can differ from
    # the effective no-argument predict setting retained by a loaded checkpoint.
    default_shape = (framework_size, framework_size)
    if tuple(size) == default_shape:
        default_macs = row["MACs"]
    else:
        _, _, default_macs = arithmetic_profile(model, (1, channels, *default_shape), device)
    row.update(framework_default_square_MACs=default_macs,
               framework_default_square_GFLOPs=2 * default_macs / 1e9,
               preprocessing_operations="Ultralytics aspect-preserving resize + stride letterbox; channel conversion/normalization")
    row["notes"] = (
        f"Actual classes: {yolo.names}. Unfused eval forward; no NMS. "
        "The installed Ultralytics predict() inherits checkpoint imgsz unless overridden; "
        "its generic default is reported separately. No inference source/config exists "
        "in this folder. Without source dimensions/rect setting, exact tensor shape "
        "and true pipeline FLOPs cannot be certified: square-target values are upper "
        "bounds for ordinary single-image rect=True letterboxing at this imgsz. "
        "Use --fod-source-size H W / --thermal-source-size H W to profile that path. "
        "Loaded YOLO inference requires_grad flags may all be false. Attention matrix "
        "products included explicitly. Source/target resize arithmetic is separate."
    )


def profile_unet(row, override, device):
    import segmentation_models_pytorch as smp
    checkpoint = load_checkpoint("best_crack_model.pth")
    sd = checkpoint.get("state_dict", checkpoint.get("model_state_dict", checkpoint))
    # Infer dimensions from saved tensors rather than assuming RGB/single-class output.
    channels = sd["encoder.conv1.weight"].shape[1]
    classes = sd["segmentation_head.0.weight"].shape[0]
    decoder_channels = tuple(sd[f"decoder.blocks.{i}.conv2.0.weight"].shape[0]
                             for i in range(5))
    model = smp.Unet(encoder_name="resnet34", encoder_weights=None,
                     in_channels=channels, classes=classes,
                     decoder_channels=decoder_channels, activation=None)
    # A strict match is required before reporting a profile for the actual weights.
    model.load_state_dict(sd, strict=True)
    size, source, provisional = get_size(override)
    if any(s % 32 for s in size):
        raise ValueError("U-Net input dimensions must be multiples of 32.")
    row.update(input_size_source=source,
               status="reference-size estimate" if provisional else "profiled",
               parameter_scope="strictly loaded SMP Unet; default all-trainable reconstruction")
    fill_profile(row, model, channels, size, device)
    row["notes"] = (
        "SMP Unet(resnet34), decoder_channels=" + str(decoder_channels) +
        f", classes={classes}; strict state_dict match. A state_dict does not preserve "
        "input resolution, requires_grad flags, or output activation. Trainable count "
        "uses SMP constructor defaults; original encoder freezing is unknown. "
        "Output activation is excluded by the arithmetic convention."
    )


def profile_patchcore(row, override, device):
    import timm
    checkpoint = load_checkpoint("Anomaly_model.ckpt", patchcore=True)
    sd = checkpoint["state_dict"]
    hp = checkpoint["hyper_parameters"]
    backbone, layers = hp["backbone"], hp["layers"]
    if backbone != "wide_resnet50_2" or layers != ["layer2", "layer3"]:
        raise ValueError(f"Unsupported checkpoint configuration: {backbone}, {layers}")
    # Recreate the SAME timm feature extractor, not a complete classification ResNet.
    # features_only prunes layer4 and fc; they are absent from this checkpoint too.
    model = timm.create_model(backbone, pretrained=False, features_only=True,
                              out_indices=(2, 3))
    prefix = "model.feature_extractor.feature_extractor."
    feature_sd = {k[len(prefix):]: v for k, v in sd.items() if k.startswith(prefix)}
    model.load_state_dict(feature_sd, strict=True)
    model.requires_grad_(False)  # PatchCore's feature backbone is frozen.
    bank = sd["model.memory_bank"]
    if bank.ndim != 2:
        raise ValueError(f"Expected a matrix memory bank, got {tuple(bank.shape)}")
    vectors, dimension = bank.shape
    row.update(memory_bank_vectors=vectors, memory_bank_dimension=dimension,
               memory_bank_elements=bank.numel(),
               memory_bank_bytes=bank.numel() * bank.element_size(),
               memory_bank_MiB=bank.numel() * bank.element_size() / 2**20)
    size, source, provisional = get_size(override)
    row.update(input_size_source=source,
               status="reference-size estimate" if provisional else "backbone profiled; search estimated",
               parameter_scope="strictly loaded, frozen timm feature extractor; bank is a buffer")

    # Capture actual feature-grid dimensions during the profiled forward pass.
    observed = {}
    def capture(module, inputs, outputs):
        observed["shapes"] = [tuple(t.shape) for t in outputs]
    handle = model.register_forward_hook(capture)
    try:
        fill_profile(row, model, feature_sd["conv1.weight"].shape[1], size, device)
    finally:
        handle.remove()
    shapes = observed["shapes"]
    if sum(s[1] for s in shapes) != dimension:
        raise ValueError("Backbone feature channels do not match memory-bank dimension.")
    queries = shapes[0][0] * shapes[0][2] * shapes[0][3]
    pairs = queries * vectors
    dot_macs = pairs * dimension
    # Dense exact Euclidean search: ||x||² + ||y||² - 2 x.y.
    # These are arithmetic estimates; no large Q-by-M distance tensor is allocated.
    # Norms may be cached, so report their overhead separately from dot products.
    overhead = (queries + vectors) * (2 * dimension - 1) + 3 * pairs
    row.update(query_patches=queries, distance_comparisons=pairs,
               search_dot_product_MACs=dot_macs,
               search_dot_product_FLOPs=2 * dot_macs,
               search_norm_and_combine_FLOPs=overhead,
               search_sqrt_evaluations=pairs,
               search_minimum_comparisons=queries * (vectors - 1),
               backbone_plus_search_dot_GFLOPs=(row["FLOPs"] + 2 * dot_macs) / 1e9)
    # Anomalib additionally searches the bank for support neighbours of the most
    # anomalous patch's nearest bank vector (num_neighbors > 1), once per image.
    neighbours = hp.get("num_neighbors", 1)
    extra = (vectors * dimension + neighbours * dimension) if neighbours > 1 else 0
    row["extra_reweight_dot_product_MACs"] = extra
    row["notes"] = (
        f"{backbone}, layers={layers}, observed feature shapes={shapes}; "
        f"num_neighbors={neighbours}. MACs/FLOPs columns cover CNN ONLY. Search fields "
        "estimate dense exact exhaustive Euclidean search; actual index/backend is "
        "not recorded. Combined GFLOPs is a partial arithmetic total (CNN+main search "
        "dot products), excluding norms, sqrt, min/top-k comparisons, optional support "
        "search/reweighting, feature pooling/alignment, and anomaly-map blur/resize. "
        "Memory bank storage is not a trainable parameter. Input resize/crop/tiling "
        "configuration is absent; workload is per supplied model tensor, before tiling."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("fod", "thermal", "unet", "patchcore"):
        default = {"unet": [512, 512], "patchcore": [256, 256]}.get(name)
        parser.add_argument(f"--{name}-size", nargs=2, type=int, default=default, metavar=("H", "W"))
    parser.add_argument("--fod-source-size", nargs=2, type=int, metavar=("H", "W"))
    parser.add_argument("--thermal-source-size", nargs=2, type=int, metavar=("H", "W"))
    parser.add_argument("--roi-size", nargs=2, type=int, metavar=("H", "W"),
                        help="Actual RGB crop dimensions, if known (for preprocessing report).")
    parser.add_argument("--device", default="cpu", help="cpu or cuda")
    args = parser.parse_args()
    for name in ("fod", "thermal", "unet", "patchcore", "fod_source", "thermal_source", "roi"):
        size = getattr(args, name + "_size")
        if size and min(size) < 1:
            parser.error(f"--{name}-size dimensions must be positive")
    torch.set_num_threads(min(4, os.cpu_count() or 1))
    print(CONVENTION)
    print("Deployment: RGB 2472x2064 (W x H); PatchCore 256x256; U-Net 512x512 ROI.")
    print("YOLO square-target bounds and generic framework defaults are labelled separately.")
    print("Packages:", ", ".join(
        f"{p}={importlib.metadata.version(p)}"
        for p in ("torch", "ultralytics", "ultralytics-thop",
                  "segmentation-models-pytorch", "timm")))
    jobs = [
        ("FOD YOLO11s", "FOD_yolo11s.pt", profile_yolo, args.fod_size),
        ("Crack U-Net ResNet34", "best_crack_model.pth", profile_unet, args.unet_size),
        ("PatchCore CNN backbone", "Anomaly_model.ckpt", profile_patchcore, args.patchcore_size),
        ("Thermal YOLO11s", "Thermal_yolo11s.pt", profile_yolo, args.thermal_size),
    ]
    rows = []
    for name, filename, function, size in jobs:
        row = dict.fromkeys(FIELDS, "")
        row.update(category="model", model=name, checkpoint=filename, convention=CONVENTION)
        print(f"\n{name} ({filename})", flush=True)
        try:
            if function is profile_yolo:
                function(row, filename, size, args.device,
                         args.fod_source_size if filename.startswith("FOD") else args.thermal_source_size)
            else:
                function(row, size, args.device)
        except Exception as error:
            row.update(status="FAILED: no invented estimate", notes=f"{type(error).__name__}: {error}")
        rows.append(row)
        for key in ("status", "input_size_NCHW", "input_size_source", "configured_imgsz", "framework_default_imgsz",
                    "framework_default_square_GFLOPs", "total_parameters",
                    "trainable_parameters", "MACs", "FLOPs", "GFLOPs", "memory_bank_MiB",
                    "distance_comparisons", "search_dot_product_MACs",
                    "backbone_plus_search_dot_GFLOPs", "notes"):
            if row[key] != "":
                print(f"  {key}: {row[key]}", flush=True)
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    # Preprocessing is reported independently of network MACs. The actual pipeline
    # interpolation/backend is unavailable, so provide a conditional bilinear model:
    # four multiplications plus three additions per output channel sample. This
    # excludes coefficient/coordinate calculation, antialiasing, casts and transfers.
    def preprocessing(name, operation, source, target="", pixels="", bilinear="", notes=""):
        row = dict.fromkeys(FIELDS, "")
        row.update(category="preprocessing", model=name, status="operation workload; not timed",
                   preprocessing_operations=operation, preprocessing_source_WH=source,
                   preprocessing_target_WH=target, preprocessing_output_pixels=pixels,
                   preprocessing_bilinear_estimated_FLOPs=bilinear, notes=notes)
        rows.append(row)
        print(f"\nPreprocessing: {name}: {operation}; {source} -> {target or 'dynamic'}")
        if bilinear != "":
            print(f"  Conditional bilinear interpolation FLOPs: {bilinear}")
        print(f"  {notes}")
    ph, pw = args.patchcore_size
    uh, uw = args.unet_size
    preprocessing("PatchCore full-frame resize", "resize full RGB frame", "2472x2064",
                  f"{pw}x{ph}", ph * pw, 7 * 3 * ph * pw,
                  "3 channels; conditional 4-multiply+3-add bilinear estimate only. "
                  "Actual interpolation/normalization is unavailable.")
    roi = f"{args.roi_size[1]}x{args.roi_size[0]}" if args.roi_size else "dynamic ROI in original RGB frame"
    preprocessing("ROI mapping and crop", "map anomaly coordinates to original frame, clamp, crop",
                  f"{pw}x{ph} anomaly coordinates / 2472x2064 RGB", roi,
                  notes=f"Direct-resize mapping scales x by {2472/pw}, y by {2064/ph}; "
                  "bounding box uses four coordinate multiplications, then rounding/clamping. "
                  "ROI dimensions/detection frequency unknown. Crop may be a view or copy; "
                  "copy traffic is proportional to ROI area, not CNN MACs. "
                  "Mapping assumes no prior padding/crop.")
    preprocessing("Crack ROI resize", "resize original-resolution RGB crop", roi,
                  f"{uw}x{uh}", uh * uw, 7 * 3 * uh * uw,
                  "3 channels; conditional bilinear interpolation estimate. Per ROI, invoked "
                  "only when an anomaly triggers this branch; no per-frame frequency assumed.")
    for name, source in (("FOD letterbox", args.fod_source_size),
                         ("Thermal letterbox", args.thermal_source_size)):
        preprocessing(name, "Ultralytics resize and stride padding; channel conversion/normalization",
                      f"{source[1]}x{source[0]}" if source else "source/ROI dimensions unavailable",
                      notes="Configured imgsz and square bounds are in the model row. "
                      "Resized content dimensions, interpolation cost and padding bytes depend "
                      "on source aspect ratio; incoming ROI size is not the network input.")
    output = ROOT / "model_flops_summary.csv"
    with output.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved {output.name}")
    if any(row["status"].startswith("FAILED") for row in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
