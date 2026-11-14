from pathlib import Path

import cv2
import numpy as np
import torch
import matplotlib.pyplot as plt

from anomalib.data import PredictDataset
from anomalib.engine import Engine
from anomalib.models import Patchcore


# ============================================================
# PATHS
# ============================================================

TEST_DIR = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_ANOMALY\test_images"
)

CHECKPOINT = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_ANOMALY\results\Patchcore\runway_anomaly\latest\weights\lightning\model.ckpt"
)

OUTPUT_DIR = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_ANOMALY\heatmap_results"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# SETTINGS
# ============================================================

IMAGE_SIZE = (256, 256)


# ============================================================
# LOAD PATCHCORE
# ============================================================

model = Patchcore()


# ============================================================
# ENGINE
# ============================================================

engine = Engine()


# ============================================================
# TEST DATASET
# ============================================================

dataset = PredictDataset(
    path=TEST_DIR,
    image_size=IMAGE_SIZE,
)


# ============================================================
# RUN PATCHCORE
# ============================================================

predictions = engine.predict(
    model=model,
    dataset=dataset,
    ckpt_path=CHECKPOINT,
)


# ============================================================
# PROCESS RESULTS
# ============================================================

if predictions is not None:

    print("\n======================================")
    print("PATCHCORE TEST RESULTS")
    print("======================================")


    for prediction in predictions:

        # ----------------------------------------------------
        # IMAGE PATH
        # ----------------------------------------------------

        image_path = Path(
            prediction.image_path[0]
            if isinstance(prediction.image_path, list)
            else prediction.image_path
        )


        # ----------------------------------------------------
        # ANOMALY SCORE
        # ----------------------------------------------------

        anomaly_score = float(
            prediction.pred_score
        )


        # ----------------------------------------------------
        # ANOMALY MAP
        # ----------------------------------------------------

        anomaly_map = prediction.anomaly_map


        # Convert tensor → NumPy

        if torch.is_tensor(anomaly_map):

            anomaly_map = (
                anomaly_map
                .detach()
                .cpu()
                .numpy()
            )


        # Remove unnecessary dimensions

        anomaly_map = np.squeeze(
            anomaly_map
        )


        # ----------------------------------------------------
        # LOAD ORIGINAL IMAGE
        # ----------------------------------------------------

        original = cv2.imread(
            str(image_path)
        )

        original = cv2.cvtColor(
            original,
            cv2.COLOR_BGR2RGB
        )


        # ----------------------------------------------------
        # RESIZE HEATMAP
        # ----------------------------------------------------

        anomaly_map = cv2.resize(
            anomaly_map,
            (
                original.shape[1],
                original.shape[0]
            )
        )


        # ----------------------------------------------------
        # NORMALIZE HEATMAP
        # ----------------------------------------------------

        heatmap = cv2.normalize(
            anomaly_map,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        ).astype(np.uint8)


        # ----------------------------------------------------
        # APPLY COLOUR MAP
        # ----------------------------------------------------

        heatmap_color = cv2.applyColorMap(
            heatmap,
            cv2.COLORMAP_JET
        )

        heatmap_color = cv2.cvtColor(
            heatmap_color,
            cv2.COLOR_BGR2RGB
        )


        # ----------------------------------------------------
        # CREATE OVERLAY
        # ----------------------------------------------------

        overlay = cv2.addWeighted(
            original,
            0.6,
            heatmap_color,
            0.4,
            0
        )


        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        output_name = (
            image_path.stem
            + "_heatmap.jpg"
        )

        output_path = (
            OUTPUT_DIR /
            output_name
        )


        # ----------------------------------------------------
        # DISPLAY 3 IMAGES
        # ----------------------------------------------------

        plt.figure(
            figsize=(15, 5)
        )


        # Original

        plt.subplot(
            1,
            3,
            1
        )

        plt.imshow(
            original
        )

        plt.title(
            "Original"
        )

        plt.axis(
            "off"
        )


        # Heatmap

        plt.subplot(
            1,
            3,
            2
        )

        plt.imshow(
            heatmap_color
        )

        plt.title(
            f"Anomaly Heatmap\nScore: {anomaly_score:.4f}"
        )

        plt.axis(
            "off"
        )


        # Overlay

        plt.subplot(
            1,
            3,
            3
        )

        plt.imshow(
            overlay
        )

        plt.title(
            "PatchCore Overlay"
        )

        plt.axis(
            "off"
        )


        plt.tight_layout()


        plt.savefig(
            output_path,
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()


        # ----------------------------------------------------
        # PRINT RESULT
        # ----------------------------------------------------

        print("\nImage:")
        print(image_path)

        print(
            "Anomaly score:",
            anomaly_score
        )

        print(
            "Prediction:",
            "ANOMALY"
            if int(prediction.pred_label) == 1
            else "NORMAL"
        )

        print(
            "Saved heatmap:",
            output_path
        )

        print("--------------------------------------")


print("\nTesting complete.")