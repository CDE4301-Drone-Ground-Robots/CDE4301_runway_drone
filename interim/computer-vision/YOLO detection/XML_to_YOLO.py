import os
import xml.etree.ElementTree as ET


# =========================================================
# PATH SETTINGS
# =========================================================

ANNOTATION_DIR = r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing\FODPascalVOCFormat-V.2.1\VOC2007\Annotations"

OUTPUT_DIR = r"C:\Users\Chara\OneDrive\Documents\YR4_SEM1\CDE4301\FOD_Detection\CDE4301_FOD_YOLO\Synthetic compositing"


LABEL_DIR = os.path.join(
    OUTPUT_DIR,
    "Yolo_labels"
)

CLASSES_FILE = os.path.join(
    OUTPUT_DIR,
    "classes.txt"
)

YAML_FILE = os.path.join(
    OUTPUT_DIR,
    "data.yaml"
)


os.makedirs(
    LABEL_DIR,
    exist_ok=True
)


# =========================================================
# STEP 1
# FIND ALL XML FILES
# =========================================================

xml_files = [
    f for f in os.listdir(ANNOTATION_DIR)
    if f.lower().endswith(".xml")
]


print(
    "XML files found:",
    len(xml_files)
)


# =========================================================
# STEP 2
# CREATE CLASS MAPPING
# =========================================================

class_names = set()


for xml_file in xml_files:

    xml_path = os.path.join(
        ANNOTATION_DIR,
        xml_file
    )

    tree = ET.parse(xml_path)

    root = tree.getroot()


    for obj in root.findall("object"):

        name = obj.find("name").text.strip()

        class_names.add(name)



# Sort alphabetically
class_names = sorted(class_names)


class_to_id = {
    name: idx
    for idx, name in enumerate(class_names)
}


print("\n======================")
print("CLASS MAPPING")
print("======================")


for idx, name in enumerate(class_names):

    print(
        f"{idx}: {name}"
    )


# =========================================================
# SAVE CLASSES.TXT
# =========================================================

with open(
    CLASSES_FILE,
    "w"
) as f:

    for name in class_names:

        f.write(
            name + "\n"
        )


# =========================================================
# STEP 3
# CONVERT XML TO YOLO
# =========================================================

converted = 0


for xml_file in xml_files:


    xml_path = os.path.join(
        ANNOTATION_DIR,
        xml_file
    )


    tree = ET.parse(xml_path)

    root = tree.getroot()


    # image size

    size = root.find("size")

    width = float(
        size.find("width").text
    )

    height = float(
        size.find("height").text
    )


    txt_name = (
        os.path.splitext(xml_file)[0]
        + ".txt"
    )


    output_txt = os.path.join(
        LABEL_DIR,
        txt_name
    )


    with open(
        output_txt,
        "w"
    ) as out:


        for obj in root.findall("object"):


            class_name = (
                obj.find("name")
                .text
                .strip()
            )


            class_id = class_to_id[class_name]


            bbox = obj.find("bndbox")


            xmin = float(
                bbox.find("xmin").text
            )

            ymin = float(
                bbox.find("ymin").text
            )

            xmax = float(
                bbox.find("xmax").text
            )

            ymax = float(
                bbox.find("ymax").text
            )


            # Pascal VOC → YOLO


            x_center = (
                (xmin + xmax) / 2
            ) / width


            y_center = (
                (ymin + ymax) / 2
            ) / height


            box_width = (
                xmax - xmin
            ) / width


            box_height = (
                ymax - ymin
            ) / height



            out.write(
                f"{class_id} "
                f"{x_center:.6f} "
                f"{y_center:.6f} "
                f"{box_width:.6f} "
                f"{box_height:.6f}\n"
            )


    converted += 1


    if converted % 500 == 0:

        print(
            f"Converted {converted}/{len(xml_files)}"
        )



print(
    "\nYOLO conversion complete"
)


# =========================================================
# STEP 4
# CREATE DATA.YAML
# =========================================================

dataset_path = OUTPUT_DIR.replace(
    "\\",
    "/"
)


with open(
    YAML_FILE,
    "w"
) as f:


    f.write(
        f"path: {dataset_path}\n\n"
    )


    f.write(
        "train: images/train\n"
    )

    f.write(
        "val: images/val\n"
    )

    f.write(
        "test: images/test\n\n"
    )


    f.write(
        "names:\n"
    )


    for idx, name in enumerate(class_names):

        f.write(
            f"  {idx}: {name}\n"
        )


print("\n======================")
print("FINISHED")
print("======================")

print(
    "Labels saved:",
    LABEL_DIR
)

print(
    "Classes saved:",
    CLASSES_FILE
)

print(
    "YAML saved:",
    YAML_FILE
)