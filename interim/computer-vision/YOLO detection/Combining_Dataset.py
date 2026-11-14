from pathlib import Path
import shutil


# ============================================================
# PATHS
# ============================================================

# ------------------------------------------------------------
# WEATHER AUGMENTATION DATASET
# ------------------------------------------------------------

WEATHER_DIR = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Output_interim\Weather_Augumented_Dataset"
)

WEATHER_IMAGES = WEATHER_DIR / "Final_Images"
WEATHER_LABELS = WEATHER_DIR / "Final_Labels"


# ------------------------------------------------------------
# WATER PUDDLE DATASET
# ------------------------------------------------------------

PUDDLE_DIR = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Water_Puddle_Test_interim"
)

PUDDLE_IMAGES = PUDDLE_DIR / "Images"
PUDDLE_LABELS = PUDDLE_DIR / "Labels"


# ------------------------------------------------------------
# FINAL COMBINED DATASET
# ------------------------------------------------------------

OUTPUT_DIR = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Output_interim\Combined_Dataset"
)

OUTPUT_IMAGES = OUTPUT_DIR / "images"
OUTPUT_LABELS = OUTPUT_DIR / "labels"


# ============================================================
# SETTINGS
# ============================================================

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp"
}


# ============================================================
# CREATE OUTPUT FOLDERS
# ============================================================

OUTPUT_IMAGES.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_LABELS.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# GET DATASET FILES
# ============================================================

def get_images(folder):

    return {
        file.stem: file
        for file in folder.iterdir()
        if file.is_file()
        and file.suffix.lower()
        in IMAGE_EXTENSIONS
    }


def get_labels(folder):

    return {
        file.stem: file
        for file in folder.iterdir()
        if file.is_file()
        and file.suffix.lower() == ".txt"
    }


# ============================================================
# VALIDATE DATASET
# ============================================================

def validate_dataset(
    dataset_name,
    image_folder,
    label_folder
):

    print("\n========================================")
    print(f"CHECKING {dataset_name}")
    print("========================================")

    images = get_images(
        image_folder
    )

    labels = get_labels(
        label_folder
    )

    print(
        f"Images found: {len(images)}"
    )

    print(
        f"Labels found: {len(labels)}"
    )

    # --------------------------------------------------------
    # Images without labels
    # --------------------------------------------------------

    images_without_labels = (
        set(images.keys())
        -
        set(labels.keys())
    )

    # --------------------------------------------------------
    # Labels without images
    # --------------------------------------------------------

    labels_without_images = (
        set(labels.keys())
        -
        set(images.keys())
    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    if images_without_labels:

        print(
            "\nWARNING: Images without labels:"
        )

        for name in sorted(
            images_without_labels
        ):

            print(
                f"  {name}"
            )

    if labels_without_images:

        print(
            "\nWARNING: Labels without images:"
        )

        for name in sorted(
            labels_without_images
        ):

            print(
                f"  {name}"
            )

    if not images_without_labels and not labels_without_images:

        print(
            "✓ Every image has a matching label."
        )

    return images, labels


# ============================================================
# CHECK INPUT DATASETS EXIST
# ============================================================

required_folders = [
    WEATHER_IMAGES,
    WEATHER_LABELS,
    PUDDLE_IMAGES,
    PUDDLE_LABELS
]

for folder in required_folders:

    if not folder.exists():

        raise FileNotFoundError(
            f"\nFolder not found:\n{folder}"
        )


# ============================================================
# VALIDATE WEATHER DATASET
# ============================================================

weather_images, weather_labels = validate_dataset(
    "WEATHER DATASET",
    WEATHER_IMAGES,
    WEATHER_LABELS
)


# ============================================================
# VALIDATE PUDDLE DATASET
# ============================================================

puddle_images, puddle_labels = validate_dataset(
    "PUDDLE DATASET",
    PUDDLE_IMAGES,
    PUDDLE_LABELS
)


# ============================================================
# CHECK FOR FILENAME COLLISIONS
# ============================================================

weather_names = set(
    weather_images.keys()
)

puddle_names = set(
    puddle_images.keys()
)

collisions = (
    weather_names
    &
    puddle_names
)


print("\n========================================")
print("CHECKING FILENAME COLLISIONS")
print("========================================")


if collisions:

    print(
        f"WARNING: "
        f"{len(collisions)} filename collisions found."
    )

    for name in sorted(
        collisions
    ):

        print(
            f"  {name}"
        )

    raise RuntimeError(
        "\nDuplicate filenames detected. "
        "Nothing was merged."
    )

else:

    print(
        "✓ No filename collisions."
    )


# ============================================================
# COPY FUNCTION
# ============================================================

def copy_dataset(
    dataset_name,
    images,
    labels
):

    print("\n========================================")
    print(
        f"COPYING {dataset_name}"
    )
    print("========================================")

    copied_images = 0
    copied_labels = 0

    # --------------------------------------------------------
    # Copy images
    # --------------------------------------------------------

    for stem, image_path in images.items():

        destination = (
            OUTPUT_IMAGES
            /
            image_path.name
        )

        if destination.exists():

            raise RuntimeError(
                f"\nFile already exists:\n"
                f"{destination}\n"
                f"Merge stopped to prevent overwrite."
            )

        shutil.copy2(
            image_path,
            destination
        )

        copied_images += 1

    # --------------------------------------------------------
    # Copy labels
    # --------------------------------------------------------

    for stem, label_path in labels.items():

        destination = (
            OUTPUT_LABELS
            /
            label_path.name
        )

        if destination.exists():

            raise RuntimeError(
                f"\nFile already exists:\n"
                f"{destination}\n"
                f"Merge stopped to prevent overwrite."
            )

        shutil.copy2(
            label_path,
            destination
        )

        copied_labels += 1

    print(
        f"Images copied: {copied_images}"
    )

    print(
        f"Labels copied: {copied_labels}"
    )


# ============================================================
# COPY WEATHER DATA
# ============================================================

copy_dataset(
    "WEATHER DATASET",
    weather_images,
    weather_labels
)


# ============================================================
# COPY PUDDLE DATA
# ============================================================

copy_dataset(
    "WATER PUDDLE DATASET",
    puddle_images,
    puddle_labels
)


# ============================================================
# FINAL VALIDATION
# ============================================================

print("\n========================================")
print("FINAL DATASET CHECK")
print("========================================")


final_images = get_images(
    OUTPUT_IMAGES
)

final_labels = get_labels(
    OUTPUT_LABELS
)


print(
    f"Total images: {len(final_images)}"
)

print(
    f"Total labels: {len(final_labels)}"
)


# ------------------------------------------------------------
# Check matching files
# ------------------------------------------------------------

missing_labels = (
    set(final_images.keys())
    -
    set(final_labels.keys())
)

missing_images = (
    set(final_labels.keys())
    -
    set(final_images.keys())
)


if missing_labels:

    print(
        "\nERROR: Images without labels:"
    )

    for name in sorted(
        missing_labels
    ):

        print(
            name
        )

    raise RuntimeError(
        "Final dataset contains images without labels."
    )


if missing_images:

    print(
        "\nERROR: Labels without images:"
    )

    for name in sorted(
        missing_images
    ):

        print(
            name
        )

    raise RuntimeError(
        "Final dataset contains labels without images."
    )


# ============================================================
# FINAL RESULT
# ============================================================

print("\n========================================")
print("MERGE COMPLETE")
print("========================================")

print(
    f"Weather images: "
    f"{len(weather_images)}"
)

print(
    f"Puddle images: "
    f"{len(puddle_images)}"
)

print(
    f"Combined images: "
    f"{len(final_images)}"
)

print(
    f"Combined labels: "
    f"{len(final_labels)}"
)

print(
    "\nFinal dataset:"
)

print(
    OUTPUT_DIR
)

print(
    "\n✓ No filename collisions"
)

print(
    "✓ All images have matching labels"
)

print(
    "✓ All labels have matching images"
)

print(
    "✓ Original datasets were not modified"
)