import os
import random
import shutil
from collections import defaultdict, Counter


# =========================================================
# PATHS
# =========================================================

IMAGE_DIR = r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Output_interim\Combined_Dataset\images"

LABEL_DIR = r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Output_interim\Combined_Dataset\labels"

OUTPUT_DIR = r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Output_interim\Final_Combined_Dataset"


# =========================================================
# SETTINGS
# =========================================================

TRAIN_RATIO = 0.80
VAL_RATIO = 0.10
TEST_RATIO = 0.10

SEED = 42

random.seed(SEED)

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp"
)


# =========================================================
# CREATE OUTPUT FOLDERS
# =========================================================

for split in ["train", "val", "test"]:

    os.makedirs(
        os.path.join(
            OUTPUT_DIR,
            "images",
            split
        ),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(
            OUTPUT_DIR,
            "labels",
            split
        ),
        exist_ok=True
    )


# =========================================================
# READ CLASSES FROM LABEL
# =========================================================

def get_classes(label_path):

    classes = set()

    with open(label_path, "r") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            parts = line.split()

            classes.add(int(parts[0]))

    return classes


# =========================================================
# DETERMINE GROUP NAME
#
# These:
#
# 000003.jpg
# 000003_rain.jpg
# 000003_fog.jpg
#
# become ONE group:
#
# 000003
#
# Water puddle images remain independent.
# =========================================================

def get_group_name(stem):

    if stem.endswith("_rain"):
        return stem[:-5]

    if stem.endswith("_fog"):
        return stem[:-4]

    return stem


# =========================================================
# FIND ALL IMAGE-LABEL PAIRS
# =========================================================

image_files = []

for file in os.listdir(IMAGE_DIR):

    if file.lower().endswith(IMAGE_EXTENSIONS):

        image_files.append(file)


print(
    f"Images found: {len(image_files)}"
)


# =========================================================
# CREATE GROUPS
# =========================================================

groups = defaultdict(list)

missing_labels = []


for image in image_files:

    stem = os.path.splitext(image)[0]

    label_name = stem + ".txt"

    label_path = os.path.join(
        LABEL_DIR,
        label_name
    )

    if not os.path.exists(label_path):

        missing_labels.append(image)

        continue

    group_name = get_group_name(stem)

    groups[group_name].append(image)


if missing_labels:

    print("\nWARNING: Images without labels:")

    for image in missing_labels:

        print(" ", image)


print(
    f"\nValid image groups: {len(groups)}"
)


# =========================================================
# GET CLASSES FOR EACH GROUP
# =========================================================

group_classes = {}

class_groups = defaultdict(list)


for group_name, images in groups.items():

    classes = set()

    for image in images:

        stem = os.path.splitext(image)[0]

        label_path = os.path.join(
            LABEL_DIR,
            stem + ".txt"
        )

        classes.update(
            get_classes(label_path)
        )

    group_classes[group_name] = classes

    for class_id in classes:

        class_groups[class_id].append(
            group_name
        )


# =========================================================
# SHOW CLASS DISTRIBUTION
# =========================================================

print("\n======================================")
print("CLASS DISTRIBUTION")
print("======================================")

for class_id in sorted(class_groups):

    print(
        f"Class {class_id}: "
        f"{len(class_groups[class_id])} groups"
    )


# =========================================================
# TARGET NUMBER OF GROUPS
# =========================================================

total_groups = len(groups)

target_train = round(
    total_groups * TRAIN_RATIO
)

target_val = round(
    total_groups * VAL_RATIO
)

target_test = (
    total_groups
    - target_train
    - target_val
)


print("\n======================================")
print("TARGET SPLIT")
print("======================================")

print("Train:", target_train)
print("Val:  ", target_val)
print("Test: ", target_test)


# =========================================================
# SPLITS
# =========================================================

train = set()
val = set()
test = set()


split_sets = {
    "train": train,
    "val": val,
    "test": test
}

split_targets = {
    "train": target_train,
    "val": target_val,
    "test": target_test
}


# =========================================================
# PROCESS RARE CLASSES FIRST
# =========================================================

classes_sorted = sorted(
    class_groups.keys(),
    key=lambda c: len(class_groups[c])
)


# =========================================================
# ASSIGN GROUPS
# =========================================================

unassigned = set(groups.keys())


for class_id in classes_sorted:

    candidates = [
        g for g in class_groups[class_id]
        if g in unassigned
    ]

    random.shuffle(candidates)


    for group in candidates:

        # ---------------------------------------------
        # Calculate current class counts
        # ---------------------------------------------

        scores = []

        for split_name in [
            "train",
            "val",
            "test"
        ]:

            split = split_sets[split_name]

            target = split_targets[split_name]

            # Don't exceed target
            if len(split) >= target:
                continue


            # Number of groups containing this class
            class_count = sum(
                class_id in group_classes[g]
                for g in split
            )


            # Prefer split with fewer examples
            # of this class
            class_ratio = (
                class_count / target
            )


            # Also consider overall split size
            size_ratio = (
                len(split) / target
            )


            score = (
                class_ratio * 10
                +
                size_ratio
            )


            scores.append(
                (
                    score,
                    split_name
                )
            )


        if not scores:
            continue


        scores.sort(
            key=lambda x: x[0]
        )


        selected_split = scores[0][1]


        split_sets[
            selected_split
        ].add(group)


        unassigned.remove(group)


# =========================================================
# ASSIGN REMAINING GROUPS
# =========================================================

remaining = list(unassigned)

random.shuffle(remaining)


for group in remaining:

    available = [
        split_name
        for split_name in [
            "train",
            "val",
            "test"
        ]
        if len(
            split_sets[split_name]
        ) < split_targets[split_name]
    ]


    if not available:

        # Should normally never happen
        # because targets add to 100%
        break


    # Choose split furthest below target
    selected_split = min(
        available,
        key=lambda s:
        len(split_sets[s])
        /
        split_targets[s]
    )


    split_sets[
        selected_split
    ].add(group)


# =========================================================
# CHECK FOR DUPLICATES
# =========================================================

assert (
    len(train & val) == 0
)

assert (
    len(train & test) == 0
)

assert (
    len(val & test) == 0
)


assert (
    len(train | val | test)
    ==
    total_groups
)


# =========================================================
# COPY DATA
# =========================================================

def copy_groups(
    group_set,
    split_name
):

    image_count = 0


    for group_name in group_set:

        for image in groups[group_name]:

            stem = os.path.splitext(image)[0]

            label = stem + ".txt"


            source_image = os.path.join(
                IMAGE_DIR,
                image
            )

            source_label = os.path.join(
                LABEL_DIR,
                label
            )


            destination_image = os.path.join(
                OUTPUT_DIR,
                "images",
                split_name,
                image
            )

            destination_label = os.path.join(
                OUTPUT_DIR,
                "labels",
                split_name,
                label
            )


            shutil.copy2(
                source_image,
                destination_image
            )

            shutil.copy2(
                source_label,
                destination_label
            )


            image_count += 1


    return image_count


# =========================================================
# COPY EACH SPLIT
# =========================================================

train_images = copy_groups(
    train,
    "train"
)

val_images = copy_groups(
    val,
    "val"
)

test_images = copy_groups(
    test,
    "test"
)


# =========================================================
# FINAL CLASS DISTRIBUTION
# =========================================================

def count_split_classes(
    group_set
):

    counter = Counter()

    for group in group_set:

        for class_id in group_classes[group]:

            counter[class_id] += 1

    return counter


train_counts = count_split_classes(train)
val_counts = count_split_classes(val)
test_counts = count_split_classes(test)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n======================================")
print("FINAL DATASET")
print("======================================")

print(
    f"Train groups: {len(train)}"
)

print(
    f"Val groups:   {len(val)}"
)

print(
    f"Test groups:  {len(test)}"
)

print()

print(
    f"Train images: {train_images}"
)

print(
    f"Val images:   {val_images}"
)

print(
    f"Test images:  {test_images}"
)


# =========================================================
# CLASS COVERAGE
# =========================================================

print("\n======================================")
print("CLASS COVERAGE")
print("======================================")

for class_id in sorted(class_groups):

    print(
        f"Class {class_id:2d} | "
        f"Train: {train_counts[class_id]:4d} | "
        f"Val: {val_counts[class_id]:4d} | "
        f"Test: {test_counts[class_id]:4d}"
    )


# =========================================================
# CHECK WEATHER GROUPS
# =========================================================

print("\n======================================")
print("WEATHER GROUP CHECK")
print("======================================")


weather_groups = [
    group
    for group in groups
    if any(
        "_rain" in image
        or "_fog" in image
        for image in groups[group]
    )
]


weather_errors = []


for group in weather_groups:

    locations = []

    if group in train:
        locations.append("train")

    if group in val:
        locations.append("val")

    if group in test:
        locations.append("test")


    if len(locations) != 1:

        weather_errors.append(
            (
                group,
                locations
            )
        )


if weather_errors:

    print(
        "WARNING: Weather groups split incorrectly!"
    )

    for group, locations in weather_errors:

        print(
            group,
            locations
        )

else:

    print(
        "✓ All rain/fog variants stay "
        "with their original image group."
    )


# =========================================================
# FINISHED
# =========================================================

print("\n======================================")
print("SPLIT COMPLETE")
print("======================================")

print(
    "Dataset saved to:"
)

print(
    OUTPUT_DIR
)