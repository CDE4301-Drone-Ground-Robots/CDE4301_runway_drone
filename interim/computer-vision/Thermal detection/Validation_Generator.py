from pathlib import Path
import shutil


# ============================================================
# PATH
# ============================================================

TOTAL_DATASET = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CD4301_THERMAL\Total_Dataset"
)

TRAIN_IMAGES = TOTAL_DATASET / "train" / "images"
TRAIN_LABELS = TOTAL_DATASET / "train" / "labels"

VAL_IMAGES = TOTAL_DATASET / "val" / "images"
VAL_LABELS = TOTAL_DATASET / "val" / "labels"


# ============================================================
# CREATE VAL FOLDERS
# ============================================================

VAL_IMAGES.mkdir(parents=True, exist_ok=True)
VAL_LABELS.mkdir(parents=True, exist_ok=True)


# ============================================================
# GET BIRD AND HUMAN IMAGES
# ============================================================

extensions = [".jpg", ".jpeg", ".png"]

bird_images = sorted([
    f for f in TRAIN_IMAGES.iterdir()
    if f.suffix.lower() in extensions
    and f.name.startswith("bird_")
])

human_images = sorted([
    f for f in TRAIN_IMAGES.iterdir()
    if f.suffix.lower() in extensions
    and f.name.startswith("human_")
])


# ============================================================
# SELECT LAST 5 OF EACH
# ============================================================

selected_birds = bird_images[-25:]
selected_humans = human_images[-25:]

selected_images = selected_birds + selected_humans


# ============================================================
# MOVE IMAGE + MATCHING LABEL
# ============================================================

for image_path in selected_images:

    label_path = TRAIN_LABELS / f"{image_path.stem}.txt"

    if not label_path.exists():
        print("WARNING: Missing label:", label_path.name)
        continue

    # Move image
    shutil.move(
        str(image_path),
        str(VAL_IMAGES / image_path.name)
    )

    # Move corresponding YOLO label
    shutil.move(
        str(label_path),
        str(VAL_LABELS / label_path.name)
    )

    print("Moved:", image_path.name)


# ============================================================
# SUMMARY
# ============================================================

print("\nDone!")
print("Bird validation images:", len(selected_birds))
print("Human validation images:", len(selected_humans))
print("Total validation images:", len(selected_images))