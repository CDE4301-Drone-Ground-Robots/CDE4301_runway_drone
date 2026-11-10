"""Export the measured seeded image-level random baseline as a YOLO dataset."""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import yaml


ROOT = Path(__file__).resolve().parent.parent
ANALYSIS = ROOT / "similarity_analysis" / "strict_outputs"
OUTPUT = ROOT / "similarity_analysis" / "random_baseline_outputs"
DESTINATION = ROOT / "original_yolo_random_split"
BUILDING = DESTINATION
SPLIT_NAMES = ("train", "val", "test")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def label_text(record: dict, mapping: dict[str, int]) -> str:
    labels = []
    width, height = record["width"], record["height"]
    for obj in record["objects"]:
        xmin, ymin, xmax, ymax = obj["xyxy"]
        labels.append(
            f'{mapping[obj["class"]]} {(xmin+xmax)/(2*width):.10f} '
            f'{(ymin+ymax)/(2*height):.10f} {(xmax-xmin)/width:.10f} '
            f'{(ymax-ymin)/height:.10f}'
        )
    return "\n".join(labels) + "\n"


def main() -> None:
    if DESTINATION.exists():
        raise FileExistsError("Refusing to overwrite the existing random-baseline destination")

    manifest_path = ANALYSIS / "manifest.jsonl"
    records = [json.loads(line) for line in manifest_path.read_text(encoding="utf-8").splitlines()]
    mapping = load_json(ANALYSIS / "class_mapping.json")
    allocation_path = ANALYSIS / "illustrative_random_baseline.npy"
    allocation = np.load(allocation_path)
    if len(allocation) != len(records) or set(np.unique(allocation)) != {0, 1, 2}:
        raise ValueError("Invalid illustrative random allocation")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    for split in SPLIT_NAMES:
        (BUILDING / "images" / split).mkdir(parents=True, exist_ok=False)
        (BUILDING / "labels" / split).mkdir(parents=True, exist_ok=False)

    manifest_rows = []
    for index, record in enumerate(records):
        manifest_rows.append(
            {"index": index, "image_id": record["id"], "split": SPLIT_NAMES[int(allocation[index])]}
        )

    def export_one(row: dict) -> tuple[int, int]:
        record = records[row["index"]]
        source_image = ROOT / record["image"]
        source_annotation = ROOT / record["annotation"]
        if sha256(source_image) != record["image_sha256"]:
            raise ValueError(f'Source image changed: {record["id"]}')
        if sha256(source_annotation) != record["annotation_sha256"]:
            raise ValueError(f'Source annotation changed: {record["id"]}')
        split = row["split"]
        target_image = BUILDING / "images" / split / f'{record["id"]}.jpg'
        target_label = BUILDING / "labels" / split / f'{record["id"]}.txt'
        shutil.copyfile(source_image, target_image)
        expected_label = label_text(record, mapping)
        target_label.write_text(expected_label, encoding="utf-8")
        if sha256(target_image) != record["image_sha256"]:
            raise ValueError(f'Copied image checksum failed: {record["id"]}')
        if target_label.read_text(encoding="utf-8") != expected_label:
            raise ValueError(f'YOLO label verification failed: {record["id"]}')
        return row["index"], len(record["objects"])

    with ThreadPoolExecutor(max_workers=16) as pool:
        for completed, _ in enumerate(pool.map(export_one, manifest_rows), 1):
            if completed % 1000 == 0:
                print(f"Exported and verified {completed}/{len(records)}", flush=True)

    with (BUILDING / "split_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("index", "image_id", "split"))
        writer.writeheader()
        writer.writerows(manifest_rows)

    dataset_yaml = {
        "path": str(DESTINATION).replace("\\", "/"),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "names": {class_id: name for name, class_id in mapping.items()},
    }
    (BUILDING / "dataset.yaml").write_text(
        yaml.safe_dump(dataset_yaml, sort_keys=False), encoding="utf-8"
    )

    image_counts = Counter(row["split"] for row in manifest_rows)
    box_counts = Counter()
    class_rows = []
    for row in manifest_rows:
        box_counts[row["split"]] += len(records[row["index"]]["objects"])
    for name, class_id in sorted(mapping.items(), key=lambda item: item[1]):
        boxes = Counter()
        images = Counter()
        for row in manifest_rows:
            count = sum(obj["class"] == name for obj in records[row["index"]]["objects"])
            if count:
                boxes[row["split"]] += count
                images[row["split"]] += 1
        class_rows.append(
            {
                "class_id": class_id,
                "name": name,
                "total": sum(boxes.values()),
                **{split: boxes[split] for split in SPLIT_NAMES},
                **{f"{split}_images": images[split] for split in SPLIT_NAMES},
            }
        )
    fields = ("class_id", "name", "total", "train", "val", "test", "train_images", "val_images", "test_images")
    with (OUTPUT / "class_distribution.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(class_rows)

    measured = load_json(ANALYSIS / "analysis_summary.json")["illustrative_random"]
    validation = {
        "status": "passed",
        "seed": 4301,
        "images": {split: image_counts[split] for split in SPLIT_NAMES},
        "boxes": {split: box_counts[split] for split in SPLIT_NAMES},
        "total_images": len(records),
        "total_boxes": sum(box_counts.values()),
        "all_source_and_copied_image_sha256_verified": True,
        "all_yolo_labels_verified": True,
        "all_classes_present_in_every_split": all(
            all(row[split] > 0 for split in SPLIT_NAMES) for row in class_rows
        ),
        "measured_strong_similarity_pairs_crossing_splits": measured["provisional_strong_pairs_crossing"],
        "measured_similarity_groups_crossing_splits": measured["groups_crossing"],
    }
    save_json(OUTPUT / "validation.json", validation)
    save_json(
        BUILDING / "provenance.json",
        {
            "purpose": "seeded image-level random-split baseline",
            "seed": 4301,
            "source_manifest_sha256": sha256(manifest_path),
            "allocation_sha256": sha256(allocation_path),
            "video_independent": False,
            "similarity_aware": False,
            "warning": "Strongly similar frames may cross splits by design in this baseline.",
        },
    )
    report = f'''# Seeded random-split baseline

This dataset contains all {len(records):,} original images and {sum(box_counts.values()):,} boxes. It uses the previously measured seed-4301 image-level random assignment: {image_counts["train"]:,} train, {image_counts["val"]:,} validation and {image_counts["test"]:,} test images.

This baseline deliberately ignores pHash/DINOv2 similarity groups. The similarity audit measured {measured["provisional_strong_pairs_crossing"]:,} strong candidate pairs and {measured["groups_crossing"]:,} compact similarity groups crossing its splits. Its scores may therefore be optimistic and should be presented as the random-frame baseline, not as the main generalization result.

All source and copied image checksums and all generated YOLO labels were verified. Every class appears in every split. The original VOC dataset and all similarity-aware datasets were left unchanged. Historical Kaggle split assignments were unavailable, so this is a newly generated reproducible baseline rather than a reconstruction of the prior split.
'''
    (OUTPUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(validation, indent=2), flush=True)
    print(f"Created {DESTINATION}", flush=True)


if __name__ == "__main__":
    main()
