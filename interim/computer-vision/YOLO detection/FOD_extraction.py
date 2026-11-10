import cv2
import numpy as np
from pathlib import Path
import random
import shutil

import torch

from sam2.sam2_image_predictor import SAM2ImagePredictor
# ============================================================
# SETTINGS
# ============================================================

IMAGE_DIR = Path(r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\FODPascalVOCFormat-V.2.1\VOC2007\Images")
LABEL_DIR = Path(r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Yolo_labels")

BACKGROUND_DIR = Path(r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Interim_background")

OUTPUT_IMAGE_DIR = Path(r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Output_interim\Synthetic_Images")
OUTPUT_LABEL_DIR = Path(r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Output_interim\Yolo_labels")
OUTPUT_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_LABEL_DIR.mkdir(parents=True, exist_ok=True)

# Controls blending around FOD edges
FEATHER_SIZE = 1


# ============================================================
# LOAD SAM2
# ============================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Using device:", device)

predictor = SAM2ImagePredictor.from_pretrained(
    "facebook/sam2-hiera-small"
)

predictor.model.to(device)


# ============================================================
# READ YOLO LABELS
# ============================================================

def read_yolo_labels(label_path):

    labels = []

    with open(label_path, "r") as f:

        for line in f:

            parts = line.strip().split()

            if len(parts) != 5:
                continue

            class_id = int(parts[0])
            xc = float(parts[1])
            yc = float(parts[2])
            bw = float(parts[3])
            bh = float(parts[4])

            labels.append(
                (class_id, xc, yc, bw, bh)
            )

    return labels


# ============================================================
# YOLO → PIXEL BOX
# ============================================================

def yolo_to_bbox(xc, yc, bw, bh, image_width, image_height):

    x1 = int((xc - bw / 2) * image_width)
    y1 = int((yc - bh / 2) * image_height)

    x2 = int((xc + bw / 2) * image_width)
    y2 = int((yc + bh / 2) * image_height)

    x1 = max(0, x1)
    y1 = max(0, y1)

    x2 = min(image_width - 1, x2)
    y2 = min(image_height - 1, y2)

    return x1, y1, x2, y2


# ============================================================
# SAM2 SEGMENTATION
# ============================================================

def segment_with_sam2(image, labels):

    h, w = image.shape[:2]

    # Convert BGR → RGB because SAM2 expects RGB
    image_rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    predictor.set_image(image_rgb)

    final_mask = np.zeros(
        (h, w),
        dtype=np.uint8
    )

    for label in labels:

        class_id, xc, yc, bw, bh = label

        x1, y1, x2, y2 = yolo_to_bbox(
            xc,
            yc,
            bw,
            bh,
            w,
            h
        )

        # Box format:
        # [x1, y1, x2, y2]
        box = np.array(
            [x1, y1, x2, y2],
            dtype=np.float32
        )

        with torch.inference_mode():

            masks, scores, _ = predictor.predict(
                box=box,
                multimask_output=True
            )

        # Choose mask with highest SAM2 confidence
        best_index = np.argmax(scores)

        mask = masks[best_index]

        mask = (
            mask.astype(np.uint8) * 255
        )

        final_mask = cv2.bitwise_or(
            final_mask,
            mask
        )

    return final_mask


# ============================================================
# OPTIONAL MASK CLEAN-UP
# ============================================================

def clean_mask(mask):

    kernel = np.ones(
        (3, 3),
        np.uint8
    )

    # Remove tiny isolated pixels
    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    # Slightly shrink mask edge
    # This helps remove remaining original-background halo
    mask = cv2.erode(
        mask,
        kernel,
        iterations=1
    )

    return mask


# ============================================================
# FEATHER
# ============================================================

def feather_mask(mask):

    if FEATHER_SIZE <= 0:

        return (
            mask.astype(np.float32) / 255.0
        )

    kernel_size = (
        FEATHER_SIZE * 2 + 1
    )

    blurred = cv2.GaussianBlur(
        mask,
        (kernel_size, kernel_size),
        0
    )

    return (
        blurred.astype(np.float32) / 255.0
    )


# ============================================================
# PREPARE BACKGROUND
# ============================================================

def prepare_background(
    background,
    target_width,
    target_height
):

    bg_h, bg_w = background.shape[:2]

    scale = max(
        target_width / bg_w,
        target_height / bg_h
    )

    new_w = int(bg_w * scale)
    new_h = int(bg_h * scale)

    background = cv2.resize(
        background,
        (new_w, new_h),
        interpolation=cv2.INTER_AREA
    )

    max_x = new_w - target_width
    max_y = new_h - target_height

    crop_x = (
        random.randint(0, max_x)
        if max_x > 0
        else 0
    )

    crop_y = (
        random.randint(0, max_y)
        if max_y > 0
        else 0
    )

    background = background[
        crop_y:crop_y + target_height,
        crop_x:crop_x + target_width
    ]

    return background


# ============================================================
# BACKGROUND REPLACEMENT
# ============================================================

def replace_background(
    original,
    background,
    object_mask
):

    height, width = original.shape[:2]

    background = prepare_background(
        background,
        width,
        height
    )

    alpha = feather_mask(
        object_mask
    )

    alpha = alpha[:, :, None]

    result = (
        original.astype(np.float32) * alpha
        +
        background.astype(np.float32) * (1 - alpha)
    )

    result = np.clip(
        result,
        0,
        255
    ).astype(np.uint8)

    return result


# ============================================================
# BACKGROUNDS
# ============================================================

background_files = [
    f
    for f in BACKGROUND_DIR.glob("*")
    if f.suffix.lower()
    in [".jpg", ".jpeg", ".png"]
]

if not background_files:

    raise RuntimeError(
        "No background images found."
    )


# ============================================================
# SOURCE IMAGES
# ============================================================

image_files = [
    f
    for f in IMAGE_DIR.glob("*")
    if f.suffix.lower()
    in [".jpg", ".jpeg", ".png"]
]

print("FOD images:", len(image_files))
print("Backgrounds:", len(background_files))


# ============================================================
# MAIN LOOP
# ============================================================

for index, image_path in enumerate(image_files):

    label_path = (
        LABEL_DIR /
        f"{image_path.stem}.txt"
    )

    if not label_path.exists():

        print(
            "Skipping:",
            image_path.name
        )

        continue


    original = cv2.imread(
        str(image_path)
    )

    if original is None:
        continue


    labels = read_yolo_labels(
        label_path
    )

    if len(labels) == 0:
        continue


    # --------------------------------------------------------
    # SAM2 segmentation
    # --------------------------------------------------------

    object_mask = segment_with_sam2(
        original,
        labels
    )


    # --------------------------------------------------------
    # Clean mask
    # --------------------------------------------------------

    object_mask = clean_mask(
        object_mask
    )


    # --------------------------------------------------------
    # Random road background
    # --------------------------------------------------------

    background_path = random.choice(
        background_files
    )

    background = cv2.imread(
        str(background_path)
    )

    if background is None:
        continue


    # --------------------------------------------------------
    # Replace background
    # --------------------------------------------------------

    synthetic = replace_background(
        original,
        background,
        object_mask
    )


    # --------------------------------------------------------
    # Save image
    # --------------------------------------------------------

    output_image_path = (
        OUTPUT_IMAGE_DIR /
        image_path.name
    )

    cv2.imwrite(
        str(output_image_path),
        synthetic
    )


    # --------------------------------------------------------
    # Keep ORIGINAL YOLO label
    #
    # Object is not resized or moved.
    # --------------------------------------------------------

    output_label_path = (
        OUTPUT_LABEL_DIR /
        label_path.name
    )

    shutil.copy(
        label_path,
        output_label_path
    )


    # --------------------------------------------------------
    # OPTIONAL: save masks for checking
    # --------------------------------------------------------

    mask_dir = Path("output/masks")

    mask_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    cv2.imwrite(
        str(
            mask_dir /
            f"{image_path.stem}_mask.png"
        ),
        object_mask
    )


    print(
        f"[{index + 1}/{len(image_files)}]",
        image_path.name,
        "→",
        background_path.name
    )


print("\nFinished.")