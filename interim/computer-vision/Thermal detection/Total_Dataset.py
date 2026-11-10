from pathlib import Path
import cv2
import shutil


# ============================================================
# PATHS
# ============================================================

BIRD_DATASET = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CD4301_THERMAL\Birds_Dataset"
)

HUMAN_DATASET = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CD4301_THERMAL\Human_Dataset"
)

TOTAL_DATASET = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CD4301_THERMAL\Total_Dataset"
)

# ============================================================
# CREATE OUTPUT FOLDERS
# ============================================================

for split in ["train", "test"]:

    (TOTAL_DATASET / split / "images").mkdir(
        parents=True,
        exist_ok=True
    )

    (TOTAL_DATASET / split / "labels").mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# PROCESS BIRDS
# ============================================================

def process_birds(split):

    image_folder = BIRD_DATASET / split / "images"
    label_folder = BIRD_DATASET / split / "labels"

    output_images = TOTAL_DATASET / split / "images"
    output_labels = TOTAL_DATASET / split / "labels"

    count = 0

    for image_path in image_folder.iterdir():

        if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
            continue

        # ----------------------------------------------------
        # READ BIRD IMAGE
        # ----------------------------------------------------

        image = cv2.imread(str(image_path))

        if image is None:
            print("Cannot read:", image_path)
            continue


        # ----------------------------------------------------
        # CONVERT TO GRAYSCALE
        # ----------------------------------------------------

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )


        # ----------------------------------------------------
        # SAVE IMAGE WITH bird_ PREFIX
        # ----------------------------------------------------

        new_image_name = (
            "bird_" + image_path.name
        )

        cv2.imwrite(
            str(output_images / new_image_name),
            gray
        )


        # ----------------------------------------------------
        # ORIGINAL LABEL
        # ----------------------------------------------------

        label_path = (
            label_folder /
            f"{image_path.stem}.txt"
        )


        if label_path.exists():

            new_label_path = (
                output_labels /
                f"bird_{image_path.stem}.txt"
            )


            # ------------------------------------------------
            # CHANGE ALL BIRD CLASS IDs TO 1
            # ------------------------------------------------

            new_lines = []

            with open(label_path, "r") as file:

                for line in file:

                    parts = line.strip().split()

                    if len(parts) >= 5:

                        # Force bird class = 1
                        parts[0] = "1"

                        new_lines.append(
                            " ".join(parts)
                        )


            with open(
                new_label_path,
                "w"
            ) as file:

                file.write(
                    "\n".join(new_lines)
                )


        else:

            print(
                "No bird label:",
                image_path.name
            )


        count += 1


    print(
        f"Bird {split}: {count}"
    )


# ============================================================
# PROCESS HUMANS
# ============================================================

def process_humans(split):

    

    image_folder = HUMAN_DATASET / "images" / split
    label_folder = HUMAN_DATASET / "labels" / split

    output_images = TOTAL_DATASET / split / "images"
    output_labels = TOTAL_DATASET / split / "labels"

    count = 0


    for image_path in image_folder.iterdir():

        if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
            continue


        # ----------------------------------------------------
        # HUMAN IMAGE ALREADY GRAYSCALE
        # ----------------------------------------------------

        new_image_name = (
            "human_" + image_path.name
        )


        shutil.copy2(
            image_path,
            output_images / new_image_name
        )


        # ----------------------------------------------------
        # COPY HUMAN LABEL
        #
        # Human class is already 0
        # ----------------------------------------------------

        label_path = (
            label_folder /
            f"{image_path.stem}.txt"
        )


        if label_path.exists():

            new_label_name = (
                f"human_{image_path.stem}.txt"
            )


            shutil.copy2(
                label_path,
                output_labels / new_label_name
            )


        else:

            print(
                "No human label:",
                image_path.name
            )


        count += 1


    print(
        f"Human {split}: {count}"
    )


# ============================================================
# RUN
# ============================================================

print("\nProcessing TRAIN...")

process_birds("train")
process_humans("train")


print("\nProcessing TEST...")

process_birds("test")
process_humans("test")


print("\nDONE")
print("Dataset saved to:")
print(TOTAL_DATASET)