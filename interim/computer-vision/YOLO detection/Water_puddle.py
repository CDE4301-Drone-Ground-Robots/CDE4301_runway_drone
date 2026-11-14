from pathlib import Path
import cv2
import numpy as np
import random


# ============================================================
# PATHS
# ============================================================

# YOUR EXISTING RUNWAY BACKGROUND FOLDER
INPUT_DIR = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Interim_background"
)

# TEST OUTPUT
OUTPUT_DIR = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Water_Puddle_Test_interim"
)

OUTPUT_IMAGE_DIR = OUTPUT_DIR / "Images"
OUTPUT_LABEL_DIR = OUTPUT_DIR / "Labels"

OUTPUT_IMAGE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_LABEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# DATASET SETTINGS
# ============================================================

# Generate 1000 synthetic puddle images
NUMBER_OF_SAMPLES = 1000

# Temporary / assumed class ID
# If your FOD classes are 0-12:
# 13 = water_puddle
WATER_PUDDLE_CLASS_ID = 31

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ============================================================
# CAMERA / PHYSICAL SIZE
# ============================================================
#
# Downward-facing RGB camera
#
# Ground FOV = 2 m x 2 m
#
# Minimum hazardous puddle dimension = 1 m
#
# Therefore:
#
# 1 / 2 = 0.50
#
# Minimum puddle dimension = 50% of image
#
# Maximum puddle dimension = 1.6 m
#
# 1.6 / 2 = 0.80
#
# ============================================================

MIN_DIMENSION = 0.50
MAX_DIMENSION = 0.80


# ============================================================
# CREATE LARGE IRREGULAR PUDDLE MASK
# ============================================================

def create_puddle_mask(height, width):

    # --------------------------------------------------------
    # Random puddle dimensions
    # --------------------------------------------------------

    puddle_w_ratio = random.uniform(
        MIN_DIMENSION,
        MAX_DIMENSION
    )

    puddle_h_ratio = random.uniform(
        MIN_DIMENSION,
        MAX_DIMENSION
    )

    puddle_w = int(width * puddle_w_ratio)
    puddle_h = int(height * puddle_h_ratio)

    # --------------------------------------------------------
    # Create local mask
    # --------------------------------------------------------

    local_mask = np.zeros(
        (puddle_h, puddle_w),
        dtype=np.uint8
    )

    # --------------------------------------------------------
    # Base puddle shape
    # --------------------------------------------------------

    cv2.ellipse(
        local_mask,
        (
            puddle_w // 2,
            puddle_h // 2
        ),
        (
            puddle_w // 2,
            puddle_h // 2
        ),
        0,
        0,
        360,
        255,
        -1
    )

    # --------------------------------------------------------
    # Mild irregularity
    # --------------------------------------------------------

    noise = np.random.rand(
        30,
        30
    ).astype(np.float32)

    noise = cv2.resize(
        noise,
        (puddle_w, puddle_h),
        interpolation=cv2.INTER_CUBIC
    )

    noise = cv2.GaussianBlur(
        noise,
        (0, 0),
        8
    )

    noise = cv2.normalize(
        noise,
        None,
        0,
        1,
        cv2.NORM_MINMAX
    )

    threshold = random.uniform(
        0.08,
        0.16
    )

    local_mask[
        noise < threshold
    ] = 0

    # --------------------------------------------------------
    # Smooth edge
    # --------------------------------------------------------

    local_mask = cv2.GaussianBlur(
        local_mask,
        (11, 11),
        0
    )

    # --------------------------------------------------------
    # Random rotation
    # --------------------------------------------------------

    angle = random.uniform(
        -30,
        30
    )

    center = (
        puddle_w // 2,
        puddle_h // 2
    )

    rotation_matrix = cv2.getRotationMatrix2D(
        center,
        angle,
        1.0
    )

    local_mask = cv2.warpAffine(
        local_mask,
        rotation_matrix,
        (puddle_w, puddle_h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0
    )

    # --------------------------------------------------------
    # FULL IMAGE MASK
    # --------------------------------------------------------

    mask = np.zeros(
        (height, width),
        dtype=np.uint8
    )

    # --------------------------------------------------------
    # IMPORTANT FIX:
    # Choose the TOP-LEFT corner directly.
    #
    # This guarantees the entire puddle fits inside
    # the image and prevents the 1-pixel mismatch.
    # --------------------------------------------------------

    x1 = random.randint(
        0,
        width - puddle_w
    )

    y1 = random.randint(
        0,
        height - puddle_h
    )

    x2 = x1 + puddle_w
    y2 = y1 + puddle_h

    # --------------------------------------------------------
    # Paste puddle
    # --------------------------------------------------------

    mask[
        y1:y2,
        x1:x2
    ] = local_mask

    return mask


# ============================================================
# APPLY WATER EFFECT
# ============================================================

def apply_water_effect(
    image,
    mask
):

    height, width = mask.shape

    # --------------------------------------------------------
    # Alpha mask
    # --------------------------------------------------------

    alpha = (
        mask.astype(
            np.float32
        )
        /
        255.0
    )

    alpha = alpha[:, :, None]

    # --------------------------------------------------------
    # Slightly smooth the asphalt
    #
    # Do NOT blur heavily.
    # We want to retain runway texture.
    # --------------------------------------------------------

    smooth = cv2.GaussianBlur(
        image,
        (0, 0),
        sigmaX=random.uniform(
            1.0,
            2.0
        )
    )

    # --------------------------------------------------------
    # Wet asphalt is slightly darker
    # --------------------------------------------------------

    darkness = random.uniform(
        0.80,
        0.92
    )

    water = (
        smooth.astype(
            np.float32
        )
        *
        darkness
    )

    # ========================================================
    # REFLECTION FROM EXISTING IMAGE
    # ========================================================

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # --------------------------------------------------------
    # Extract brighter areas
    # --------------------------------------------------------

    threshold = random.uniform(
        125,
        160
    )

    highlights = np.maximum(
        gray.astype(
            np.float32
        )
        -
        threshold,
        0
    )

    highlights /= (
        255.0 - threshold
    )

    highlights = np.clip(
        highlights,
        0,
        1
    )

    # --------------------------------------------------------
    # Blur reflection
    # --------------------------------------------------------

    highlights = cv2.GaussianBlur(
        highlights,
        (0, 0),
        sigmaX=random.uniform(
            4,
            8
        )
    )

    # --------------------------------------------------------
    # Horizontal reflection streak
    # --------------------------------------------------------

    kernel_width = random.randint(
        10,
        35
    )

    kernel = np.ones(
        (
            1,
            kernel_width
        ),
        dtype=np.float32
    )

    reflection = cv2.filter2D(
        highlights,
        -1,
        kernel
    )

    reflection = cv2.normalize(
        reflection,
        None,
        0,
        1,
        cv2.NORM_MINMAX
    )

    # --------------------------------------------------------
    # Random reflection strength
    # --------------------------------------------------------

    reflection_strength = random.uniform(
        0.08,
        0.25
    )

    reflection = (
        reflection
        *
        reflection_strength
        *
        255
    )

    water += (
        reflection[:, :, None]
    )

    # ========================================================
    # RANDOM LOCAL REFLECTION PATCHES
    # ========================================================

    # Not every puddle should have strong highlights.

    if random.random() < 0.70:

        number_of_highlights = random.randint(
            1,
            4
        )

        for _ in range(
            number_of_highlights
        ):

            highlight = np.zeros(
                (
                    height,
                    width
                ),
                dtype=np.float32
            )

            # Random position
            rx = random.randint(
                0,
                width - 1
            )

            ry = random.randint(
                0,
                height - 1
            )

            # Random elongated reflection
            rw = random.randint(
                max(20, width // 30),
                max(30, width // 8)
            )

            rh = random.randint(
                max(5, height // 80),
                max(10, height // 20)
            )

            cv2.ellipse(
                highlight,

                (
                    rx,
                    ry
                ),

                (
                    rw,
                    rh
                ),

                random.uniform(
                    -25,
                    25
                ),

                0,
                360,

                random.uniform(
                    0.10,
                    0.35
                ),

                -1
            )

            highlight = cv2.GaussianBlur(
                highlight,
                (0, 0),
                sigmaX=random.uniform(
                    5,
                    10
                )
            )

            water += (
                highlight[:, :, None]
                *
                255
            )

    # ========================================================
    # SURFACE VARIATION
    # ========================================================

    surface_noise = np.random.normal(
        0,
        random.uniform(
            1.0,
            2.0
        ),
        water.shape
    )

    water += surface_noise

    # --------------------------------------------------------
    # Slight colour variation
    # --------------------------------------------------------

    water[:, :, 0] *= random.uniform(
        1.00,
        1.03
    )

    water[:, :, 1] *= random.uniform(
        0.99,
        1.02
    )

    water[:, :, 2] *= random.uniform(
        0.98,
        1.01
    )

    water = np.clip(
        water,
        0,
        255
    )

    # ========================================================
    # BLEND WITH ORIGINAL RUNWAY
    # ========================================================

    result = (
        image.astype(
            np.float32
        )
        *
        (1 - alpha)
        +
        water
        *
        alpha
    )

    result = np.clip(
        result,
        0,
        255
    ).astype(
        np.uint8
    )

    return result


# ============================================================
# CREATE YOLO BOUNDING BOX
# ============================================================

def create_yolo_label(
    mask
):

    # --------------------------------------------------------
    # Threshold mask
    # --------------------------------------------------------

    binary = (
        mask > 80
    ).astype(
        np.uint8
    ) * 255

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:

        return None

    # Largest puddle region
    contour = max(
        contours,
        key=cv2.contourArea
    )

    x, y, w, h = cv2.boundingRect(
        contour
    )

    image_h, image_w = mask.shape

    # --------------------------------------------------------
    # YOLO normalized coordinates
    # --------------------------------------------------------

    x_center = (
        x + w / 2
    ) / image_w

    y_center = (
        y + h / 2
    ) / image_h

    box_width = (
        w / image_w
    )

    box_height = (
        h / image_h
    )

    return (
        f"{WATER_PUDDLE_CLASS_ID} "
        f"{x_center:.6f} "
        f"{y_center:.6f} "
        f"{box_width:.6f} "
        f"{box_height:.6f}"
    )


# ============================================================
# FIND BACKGROUNDS
# ============================================================

image_files = [
    f
    for f in INPUT_DIR.iterdir()
    if f.suffix.lower()
    in [
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp"
    ]
]


if len(image_files) == 0:

    raise RuntimeError(
        "No background images found."
    )


print(
    f"\nFound {len(image_files)} "
    "background images."
)

print(
    "These backgrounds will be randomly "
    "reused to create the dataset."
)


# ============================================================
# GENERATE 1000 IMAGES
# ============================================================

successful = 0


for index in range(
    1,
    NUMBER_OF_SAMPLES + 1
):

    # --------------------------------------------------------
    # Randomly select one of the 6 backgrounds
    # --------------------------------------------------------

    background_path = random.choice(
        image_files
    )

    image = cv2.imread(
        str(background_path)
    )

    if image is None:

        print(
            "Could not read:",
            background_path.name
        )

        continue

    height, width = image.shape[:2]

    # --------------------------------------------------------
    # Generate large puddle
    # --------------------------------------------------------

    mask = create_puddle_mask(
        height,
        width
    )

    # --------------------------------------------------------
    # Apply water appearance
    # --------------------------------------------------------

    result = apply_water_effect(
        image,
        mask
    )

    # --------------------------------------------------------
    # Generate YOLO annotation
    # --------------------------------------------------------

    label = create_yolo_label(
        mask
    )

    if label is None:

        print(
            "Could not generate label."
        )

        continue

    # --------------------------------------------------------
    # Output filename
    # --------------------------------------------------------

    image_name = (
        f"water_puddle_{index:05d}.jpg"
    )

    label_name = (
        f"water_puddle_{index:05d}.txt"
    )

    # --------------------------------------------------------
    # Save image
    # --------------------------------------------------------

    cv2.imwrite(
        str(
            OUTPUT_IMAGE_DIR
            /
            image_name
        ),
        result,
        [
            cv2.IMWRITE_JPEG_QUALITY,
            95
        ]
    )

    # --------------------------------------------------------
    # Save YOLO label
    # --------------------------------------------------------

    with open(
        OUTPUT_LABEL_DIR
        /
        label_name,
        "w"
    ) as f:

        f.write(
            label
            +
            "\n"
        )

    successful += 1

    # --------------------------------------------------------
    # Progress
    # --------------------------------------------------------

    if index % 100 == 0:

        print(
            f"Generated "
            f"{index}/"
            f"{NUMBER_OF_SAMPLES}"
        )


# ============================================================
# SUMMARY
# ============================================================

print("\n========================================")
print("WATER PUDDLE DATASET COMPLETE")
print("========================================")

print(
    f"Backgrounds used: "
    f"{len(image_files)}"
)

print(
    f"Samples requested: "
    f"{NUMBER_OF_SAMPLES}"
)

print(
    f"Samples generated: "
    f"{successful}"
)

print(
    "\nImages saved to:"
)

print(
    OUTPUT_IMAGE_DIR
)

print(
    "\nLabels saved to:"
)

print(
    OUTPUT_LABEL_DIR
)

print(
    "\nClass mapping:"
)

print(
    f"{WATER_PUDDLE_CLASS_ID}: water_puddle"
)

print(
    "\nCamera assumption:"
)

print(
    "Downward RGB"
)

print(
    "Ground FOV = 2 m x 2 m"
)

print(
    "Minimum puddle dimension = 1 m"
)