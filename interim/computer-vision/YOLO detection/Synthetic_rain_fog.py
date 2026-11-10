import cv2
import shutil
import random
from pathlib import Path

import albumentations as A


# =========================================================
# PATHS
# =========================================================

INPUT_IMAGE_DIR = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Output_interim\Synthetic_Images"
)

INPUT_LABEL_DIR = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Output_interim\Yolo_labels"
)


OUTPUT_IMAGE_DIR = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Output_interim\Weather_Augumented_Dataset\Final_Images"
)

OUTPUT_LABEL_DIR = Path(
    r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\Output_interim\Weather_Augumented_Dataset\Final_Labels"
)

OUTPUT_IMAGE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_LABEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

## ============================================================
# WEATHER EFFECTS
# ============================================================

rain_transform = A.Compose(
    [
        A.RandomRain(
            slant_lower=-10,
            slant_upper=10,
            drop_length=15,
            drop_width=1,
            brightness_coefficient=0.85,
            p=1.0
        )
    ]
)


fog_transform = A.Compose(
    [
        A.RandomFog(
         fog_coef_lower=0.03,
         fog_coef_upper=0.10,
         alpha_coef=0.03,
         p=1.0)
        
    ]
)



# ============================================================
# IMAGE LIST
# ============================================================

image_files = list(
    INPUT_IMAGE_DIR.glob("*")
)


print(
    "Synthetic images found:",
    len(image_files)
)



normal_count = 0
rain_count = 0
fog_count = 0



# ============================================================
# PROCESS DATASET
# ============================================================

for index, image_path in enumerate(image_files):


    label_path = (
        INPUT_LABEL_DIR /
        f"{image_path.stem}.txt"
    )


    if not label_path.exists():

        print(
            "Missing label:",
            image_path.name
        )

        continue



    image = cv2.imread(
        str(image_path)
    )


    if image is None:
        continue



    # ========================================================
    # ALWAYS KEEP ORIGINAL
    # ========================================================

    shutil.copy2(
        image_path,
        OUTPUT_IMAGE_DIR /
        image_path.name
    )


    shutil.copy2(
        label_path,
        OUTPUT_LABEL_DIR /
        label_path.name
    )


    normal_count += 1



    # ========================================================
    # RANDOMLY ADD WEATHER
    #
    # 20% Rain
    # 20% Fog
    # 60% Nothing
    # ========================================================

    probability = random.random()



    # --------------------------
    # Rain
    # --------------------------

    if probability < 0.20:


        rain_image = rain_transform(
            image=image
        )["image"]


        new_image_name = (
            image_path.stem
            +
            "_rain.jpg"
        )


        new_label_name = (
            image_path.stem
            +
            "_rain.txt"
        )


        cv2.imwrite(
            str(
                OUTPUT_IMAGE_DIR /
                new_image_name
            ),
            rain_image
        )


        shutil.copy2(
            label_path,
            OUTPUT_LABEL_DIR /
            new_label_name
        )


        rain_count += 1



    # --------------------------
    # Fog
    # --------------------------

    elif probability < 0.40:


        fog_image = fog_transform(
            image=image
        )["image"]


        new_image_name = (
            image_path.stem
            +
            "_fog.jpg"
        )


        new_label_name = (
            image_path.stem
            +
            "_fog.txt"
        )


        cv2.imwrite(
            str(
                OUTPUT_IMAGE_DIR /
                new_image_name
            ),
            fog_image
        )


        shutil.copy2(
            label_path,
            OUTPUT_LABEL_DIR /
            new_label_name
        )


        fog_count += 1



    if (index + 1) % 500 == 0:

        print(
            f"Processed {index+1}/{len(image_files)}"
        )



# ============================================================
# SUMMARY
# ============================================================

total = (
    normal_count
    +
    rain_count
    +
    fog_count
)


print("\n==============================")
print("WEATHER AUGMENTATION COMPLETE")
print("==============================")

print(
    "Normal:",
    normal_count
)

print(
    "Rain:",
    rain_count
)

print(
    "Fog:",
    fog_count
)

print(
    "Total dataset:",
    total
)