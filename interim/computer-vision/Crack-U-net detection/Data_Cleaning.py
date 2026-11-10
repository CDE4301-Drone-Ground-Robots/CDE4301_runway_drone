from pathlib import Path

# ============================================================
# FOLDERS
# ============================================================

IMAGE_DIR = Path(r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_CRACKS_DETECTION\Crack_Dataset\images")
MASK_DIR = Path(r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_CRACKS_DETECTION\Crack_Dataset\masks")


# ============================================================
# SETTINGS
# ============================================================

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]


# ============================================================
# GET ALL REMAINING IMAGE NAMES
# ============================================================

image_names = set()

for image_path in IMAGE_DIR.iterdir():

    if image_path.suffix.lower() in IMAGE_EXTENSIONS:

        # Example:
        # 001.jpg → "001"

        image_names.add(
            image_path.stem
        )


print("Remaining images:", len(image_names))


# ============================================================
# CHECK EVERY MASK
# ============================================================

removed = 0
kept = 0


for mask_path in MASK_DIR.iterdir():

    if mask_path.suffix.lower() not in IMAGE_EXTENSIONS:
        continue


    # --------------------------------------------------------
    # Convert mask filename to original image name
    #
    # Example:
    #
    # 001_mask.jpg
    #       ↓
    # 001
    # --------------------------------------------------------

    mask_name = mask_path.stem

    if mask_name.endswith("_mask"):

        original_name = mask_name[:-5]

    else:

        original_name = mask_name


    # --------------------------------------------------------
    # Check if corresponding image still exists
    # --------------------------------------------------------

    if original_name not in image_names:

        print(
            "Removing:",
            mask_path.name
        )

        mask_path.unlink()

        removed += 1

    else:

        kept += 1


# ============================================================
# SUMMARY
# ============================================================

print("\nFinished.")
print("Masks kept:", kept)
print("Masks removed:", removed)