from pathlib import Path
import shutil


# ============================================================
# PATH
# ============================================================

TOTAL_DATASET = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CD4301_THERMAL\Total_Dataset"
)


# ============================================================
# BIRD SEGMENTATION -> BOUNDING BOX
# ============================================================

def bird_seg_to_box(line):

    parts = line.strip().split()

    # Need class + at least 2 coordinate pairs
    if len(parts) < 5:
        return None

    # Ignore original bird species class
    # Final bird class = 1
    class_id = 1

    coords = list(map(float, parts[1:]))

    xs = coords[0::2]
    ys = coords[1::2]

    # Find outer limits of polygon
    x_min = min(xs)
    x_max = max(xs)

    y_min = min(ys)
    y_max = max(ys)

    # Convert to YOLO box
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2

    width = x_max - x_min
    height = y_max - y_min

    return (
        f"{class_id} "
        f"{x_center:.6f} "
        f"{y_center:.6f} "
        f"{width:.6f} "
        f"{height:.6f}"
    )


# ============================================================
# PROCESS TRAIN / TEST
# ============================================================

for split in ["train", "test"]:

    original_labels = TOTAL_DATASET / split / "labels"

    yolo_labels = TOTAL_DATASET / split / "yolo_label"

    yolo_labels.mkdir(
        parents=True,
        exist_ok=True
    )


    bird_count = 0
    human_count = 0


    for label_path in original_labels.glob("*.txt"):


        # ====================================================
        # BIRD
        # ====================================================

        if label_path.name.startswith("bird_"):

            new_lines = []

            with open(label_path, "r") as file:

                for line in file:

                    converted = bird_seg_to_box(line)

                    if converted is not None:
                        new_lines.append(converted)


            output_path = (
                yolo_labels /
                label_path.name
            )


            with open(output_path, "w") as file:

                file.write(
                    "\n".join(new_lines)
                )


            bird_count += 1


        # ====================================================
        # HUMAN
        # ====================================================

        elif label_path.name.startswith("human_"):

            # Human labels are already YOLO detection format
            # Class 0 = person

            shutil.copy2(
                label_path,
                yolo_labels / label_path.name
            )


            human_count += 1


    print(f"\n{split.upper()}")
    print("Bird labels converted:", bird_count)
    print("Human labels copied:", human_count)


print("\nDONE")