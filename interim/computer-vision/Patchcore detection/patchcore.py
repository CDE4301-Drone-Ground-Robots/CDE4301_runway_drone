from pathlib import Path

from anomalib.data import Folder
from anomalib.models import Patchcore
from anomalib.engine import Engine


# ============================================================
# PATHS
# ============================================================

PROJECT_DIR = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_ANOMALY"
)

NORMAL_DIR = PROJECT_DIR / "Anomaly_dataset" / "Anomaly"


# ============================================================
# DATASET
# ============================================================

datamodule = Folder(
    name="runway_anomaly",
    root=PROJECT_DIR / "dataset",

    normal_dir="normal",

    # No labelled anomaly images yet
    abnormal_dir=None,

    train_batch_size=8,
    eval_batch_size=8,

    num_workers=0,
)


# ============================================================
# PATCHCORE MODEL
# ============================================================

model = Patchcore(
    backbone="wide_resnet50_2",
    layers=["layer2", "layer3"],
    coreset_sampling_ratio=0.1,
)


# ============================================================
# TRAINING ENGINE
# ============================================================

engine = Engine(
    default_root_dir=PROJECT_DIR / "results"
)


# ============================================================
# TRAIN
# ============================================================

engine.fit(
    model=model,
    datamodule=datamodule
)


print("\nPatchCore training complete!")