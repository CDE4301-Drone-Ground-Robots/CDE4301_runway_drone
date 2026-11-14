# Runway FOD similarity-aware evaluation

All paths, downloaded model weights, source code caches, generated reports and corrected images stay in this workspace.
The original FODPascalVOCFormat-V.2.1 folder is read-only to this pipeline.
This is similarity-aware, not guaranteed video-independent. No historical split or YOLO class mapping is available.
The user confirmed the clean source dataset contains no synthetic images.

## Run (PowerShell, from workspace root)
python -B similarity_analysis/pipeline.py all
python -B similarity_analysis/supplement_report.py
python -B similarity_analysis/pipeline.py export --provisional
python -B similarity_analysis/validate_export.py
python -B similarity_analysis/verify_algorithms.py

Stages can be run separately: inventory, embeddings, neighbours, groups, propose, report.
Inventory and embeddings resume from flushed checkpoints. Do not alter source files while running.
Changing source data, model, preprocessing or config requires a NEW output directory.
The inventory validates every image, parses every XML and hashes both source files.
A failed/incomplete line at the end of manifest.jsonl must be repaired by removing ONLY that incomplete generated line before resuming.
The model's official Git commit is resolved once and saved in model_lock.json; downloaded weight checksums are recorded.
No dependencies are installed globally. Current environment uses torch, torchvision, numpy, scipy, Pillow, matplotlib and PyYAML.
See environment.json for actual runtime versions. CUDA is optional; CPU runs are much slower.

## Review
Open outputs/review.html in your browser.
Read outputs/REPORT.md, analysis_summary.json, blocked_merges.json and class_distribution.csv.
The full candidates are in candidate_pairs.csv; the gallery is a stratified sample, not exhaustive validation.
Use pair_decisions.csv to enter a,b,decision,note, with accept/reject/blank.
Rerun neighbours, groups, propose, report after changing decisions.
Complete-link grouping can block accepted edges if other pairwise evidence is absent; those need further review.
A proposed split can still have strong cross-split matches between different groups. Inspect before accepting.
To rerun an export, use a new corrected_destination. Existing corrected outputs are never overwritten.
Do not set --reviewed until the similarity groups, remaining cross-split risks and split have been reviewed.

## Threshold policy
64-bit pHash (DC bit forced zero): retrieve all pairs within Hamming distance <=6.
DINOv2 normalized CLS cosine: retrieve top-30 neighbours per image; retain cosine >=0.95.
Provisional strong pair: pHash <=4 AND DINO cosine >=0.98; byte-identical images are always grouped.
These are starting heuristics requiring dataset-specific human calibration, not proof of common video identity.
Boundary, hash-only and DINO-only examples are deliberately included for calibration.
Thresholds are pre-model evaluation choices; do not tune them using YOLO test performance.
Exact batched cosine search avoids ANN recall loss, but top-k is not a full threshold-radius DINO search.
The before/after audit also computes exact nearest cross-split cosine for every image.
Compact similarity groups require complete pairwise evidence.
Split allocation additionally co-locates all un-rejected strong/accepted matches, using transitive constraint blocks.
These blocks do NOT assert common video identity; their only role is preventing strong matches crossing splits.
Weak candidate edges impose no allocation constraints.
A local block-move refinement improves avoidable class imbalance after greedy allocation.
Exact GPU search is memory bounded but has quadratic compute cost; a million-image collection would need an ANN backend.

## YOLO commands: FOR USER REVIEW; NOT EXECUTED
Use the same architecture, initialization, epochs and image size as your earlier experiment for a fair comparison.
The example uses YOLOv8n; replace it with your earlier model if different.
Run only after reviewing and freezing the dataset. Match the image size to the intended deployment.
The test split should be evaluated once after selecting model/hyperparameters on validation.

yolo detect train model=yolov8n.pt data=corrected_yolo_proposed/dataset.yaml epochs=100 imgsz=640 seed=4301 deterministic=True project=similarity_analysis/yolo_runs name=fod_similarity_aware
yolo detect val model=similarity_analysis/yolo_runs/fod_similarity_aware/weights/best.pt data=corrected_yolo_proposed/dataset.yaml split=val imgsz=640 project=similarity_analysis/yolo_runs name=validation
yolo detect val model=similarity_analysis/yolo_runs/fod_similarity_aware/weights/best.pt data=corrected_yolo_proposed/dataset.yaml split=test imgsz=640 project=similarity_analysis/yolo_runs name=final_test

The analysis script never imports Ultralytics or starts YOLO training.
dataset.yaml is generated on export with absolute workspace path and alphabetical class IDs 0..30.
Historical YOLO class IDs cannot be recovered from these VOC XML files.
All fractional Pascal VOC boxes retain their class identity and continuous pixel coordinates when normalized.
Before training, verify representative box overlays against the source coordinate convention.

Official references:
- https://github.com/facebookresearch/dinov2
- https://docs.ultralytics.com/modes/train/
- https://docs.ultralytics.com/modes/val/



## Generated artifacts
- outputs/REVIEW_SUMMARY.md: start here for measured results.
- outputs/review.html: stratified near-duplicate and uncertain match examples.
- outputs/allocation_review.html: large allocation blocks and strongest remaining cross-split candidates.
- outputs/REPORT.md: methodology, thresholds, conversion and limitations.
- outputs/class_distribution.csv: per-class boxes, images and block support.
- outputs/remaining_cross_split_candidates.csv: prioritized unresolved matches.
- outputs/manifest.jsonl: original file checksums, source boxes, image metadata and pHashes.
- outputs/embeddings.npy: L2-normalized pretrained DINOv2 features.
- outputs/export_validation.json: copied-image, label and group-constraint validation.
- ../corrected_yolo_proposed/dataset.yaml: current provisional YOLO dataset.
- ../corrected_yolo_proposed_initial/: preserved first export; superseded by the balanced proposal.
- outputs/iterations/: snapshots of superseded proposals; not the original dataset splits.

The result is a PROVISIONAL review copy. High DINO cosine matches outside the strict joint cutoff
remain; some inspected examples look like correlated frames. This is not yet a claim of leakage-free evaluation.
Review and resolve concerning matches before training. No training has been run.
Do not use the historical 90%+ result as evidence of performance on this new split.

## Stricter proposal

`corrected_yolo_strict` uses this stronger co-location rule:

```
DINOv2 cosine >= 0.99
OR
(pHash distance <= 6 AND DINOv2 cosine >= 0.97)
```

The stricter proposal keeps all 33,793 images. Its large indivisible allocation blocks make the
split 68.38/15.69/15.94 rather than exactly 70/15/15, and produce larger unavoidable class-count
deviations. Review `strict_outputs/REVIEW_SUMMARY.md`, `strict_outputs/review.html`, and
`strict_outputs/allocation_review.html`. Reproduce or validate it with:

```
python -B similarity_analysis/pipeline.py neighbours --config similarity_analysis/strict_config.json
python -B similarity_analysis/pipeline.py groups --config similarity_analysis/strict_config.json
python -B similarity_analysis/pipeline.py propose --config similarity_analysis/strict_config.json
python -B similarity_analysis/pipeline.py report --config similarity_analysis/strict_config.json
python -B similarity_analysis/supplement_report.py --config similarity_analysis/strict_config.json
python -B similarity_analysis/pipeline.py export --provisional --config similarity_analysis/strict_config.json
python -B similarity_analysis/validate_export.py --config similarity_analysis/strict_config.json
```

After reviewing and freezing the strict split, substitute
`corrected_yolo_strict/dataset.yaml` in the YOLO commands above. The scripts do not train YOLO.

## Object-aware reduced proposal

`corrected_yolo_strict_reduced` is derived from the strict dataset without deleting or changing any
earlier files. Pretrained DINOv2 patch tokens are pooled over expanded bounding-box regions. Within
each compact complete-link group, a frame can be omitted only when a retained representative has
the same class multiset, object cosine >= 0.99, normalized center change <= 0.08, and absolute
log-area change <= 0.30. Rare-class, multi-object, difficult, class-small and edge-object images are
protected. Whole remaining strong-similarity blocks are assigned with a constrained MILP split.

Use `reduced_outputs/REPORT.md`, `reduced_outputs/reduction_review.html`, and
`reduced_outputs/annotation_review.html` for review. Reproduce it with:

```
python -B similarity_analysis/reduce_dataset.py embeddings
python -B similarity_analysis/reduce_dataset.py analyze
python -B similarity_analysis/reduce_dataset.py select
python -B similarity_analysis/reduce_dataset.py optimize
python -B similarity_analysis/reduce_dataset.py export
python -B similarity_analysis/reduce_dataset.py validate
python -B similarity_analysis/reduce_dataset.py report
```

The export is provisional until the representative pairs and annotation outliers are reviewed.
No script in this workflow starts YOLO training.

## Random-split baseline

`original_yolo_random_split` exports the previously measured seed-4301 image-level random baseline.
It contains all original images and intentionally ignores similarity groups, allowing the effect of
random-frame leakage to be compared with the strict datasets. Reproduce it once with:

```
python -B similarity_analysis/create_random_baseline.py
```

The exporter refuses to overwrite an existing destination and verifies source/copy checksums and
generated YOLO labels. This is a new reproducible random baseline because the historical Kaggle
split assignments were unavailable.

After review, train the reduced proposal with the same model, initialization, image size and epochs
used in the earlier experiment:

```
yolo detect train model=yolov8n.pt data=corrected_yolo_strict_reduced/dataset.yaml epochs=100 imgsz=640 seed=4301 deterministic=True project=similarity_analysis/yolo_runs name=fod_strict_reduced
yolo detect val model=similarity_analysis/yolo_runs/fod_strict_reduced/weights/best.pt data=corrected_yolo_strict_reduced/dataset.yaml split=val imgsz=640 project=similarity_analysis/yolo_runs name=fod_strict_reduced_validation
yolo detect val model=similarity_analysis/yolo_runs/fod_strict_reduced/weights/best.pt data=corrected_yolo_strict_reduced/dataset.yaml split=test imgsz=640 project=similarity_analysis/yolo_runs name=fod_strict_reduced_final_test
```

Use validation while choosing the model and hyperparameters. Run the test command once after those
choices are frozen. These commands are documentation only and have not been executed.
