from pathlib import Path
import random
import shutil

# ============================================================
# PATHS
# ============================================================

# Original human dataset
SOURCE_IMAGES = Path(r"C:\Users\Chara\Downloads\archive(2)\dataset\train\images")
SOURCE_LABELS = Path(r"C:\Users\Chara\Downloads\archive(2)\dataset\train\labels")

# New smaller dataset
OUTPUT = Path(r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CD4301_THERMAL\Human_Dataset")


# ============================================================
# SETTINGS
# ============================================================

TOTAL_IMAGES = 700
TRAIN_RATIO = 0.8
SEED = 42

random.seed(SEED)


# ============================================================
# CREATE OUTPUT FOLDERS
# ============================================================

train_images = OUTPUT / "images" / "train"
test_images = OUTPUT / "images" / "test"

train_labels = OUTPUT / "labels" / "train"
test_labels = OUTPUT / "labels" / "test"

for folder in [
    train_images,
    test_images,
    train_labels,
    test_labels
]:
    folder.mkdir(parents=True, exist_ok=True)


# ============================================================
# FIND VALID IMAGE + LABEL PAIRS
# ============================================================

image_extensions = [".jpg", ".jpeg", ".png"]

valid_pairs = []

for image_path in SOURCE_IMAGES.iterdir():

    if image_path.suffix.lower() not in image_extensions:
        continue

    # YOLO label has same filename, but .txt
    label_path = SOURCE_LABELS / f"{image_path.stem}.txt"

    if label_path.exists():
        valid_pairs.append((image_path, label_path))


print("Valid image-label pairs found:", len(valid_pairs))


# ============================================================
# CHECK ENOUGH IMAGES EXIST
# ============================================================

if len(valid_pairs) < TOTAL_IMAGES:
    raise ValueError(
        f"Only {len(valid_pairs)} valid pairs found. "
        f"Cannot select {TOTAL_IMAGES}."
    )


# ============================================================
# RANDOMLY SELECT 700
# ============================================================

selected = random.sample(
    valid_pairs,
    TOTAL_IMAGES
)

random.shuffle(selected)


# ============================================================
# 80 / 20 SPLIT
# ============================================================

train_count = int(TOTAL_IMAGES * TRAIN_RATIO)

train_data = selected[:train_count]
test_data = selected[train_count:]


# ============================================================
# COPY FUNCTION
# ============================================================

def copy_data(data, image_output, label_output):

    for image_path, label_path in data:

        shutil.copy2(
            image_path,
            image_output / image_path.name
        )

        shutil.copy2(
            label_path,
            label_output / label_path.name
        )


# ============================================================
# COPY TRAIN DATA
# ============================================================

copy_data(
    train_data,
    train_images,
    train_labels
)


# ============================================================
# COPY TEST DATA
# ============================================================

copy_data(
    test_data,
    test_images,
    test_labels
)


# ============================================================
# SUMMARY
# ============================================================

print("\nDone!")
print("Total selected:", len(selected))
print("Training:", len(train_data))
print("Testing:", len(test_data))

print("\nDataset saved to:")
print(OUTPUT)