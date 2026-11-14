# Review summary

PROVISIONAL: the exported dataset is a review copy. YOLO training has not started.

33,793 images; 34,472 boxes; 31 classes.
Byte-identical images: 0. Provisional strong-rule near-duplicate images: 25,838.
Candidate pairs: 494,447; compact non-singleton candidate groups: 7,318.
Allocation blocks including singletons: 10,409; largest block: 1096 images.
Original split-spanning groups: unavailable; previous split manifests were not provided.

| Split | Images | Percentage |
|---|---:|---:|
| train | 23,106 | 68.38% |
| val | 5,301 | 15.69% |
| test | 5,386 | 15.94% |

| Cross-split measure | Illustrative random baseline | Proposed split |
|---|---:|---:|
| Strong configured-rule pairs | 51,361 | 0 |
| All retrieved candidate pairs | 230,386 | 74,753 |
| Median nearest cross-split cosine | 0.9805 | 0.9536 |
| Images with cross-split nearest cosine >= 0.97 | 25,275 | 7,905 |

The baseline is a new seeded random split, not your historical split. Cosine alone does not confirm common video origin.
74,753 retrieved weaker/uncertain candidate pairs still cross splits; 0 meet the DINO-only cutoff.
Zero configured strong-rule crossings is a threshold-specific result, not proof of no leakage.
Compact groups use complete pairwise evidence to avoid weak-chain scene merging. Additional same-split constraints
link strong matches between compact groups. These allocation blocks do not assert source-video identity.

Classes absent from a split: 0. Minimum class support: 6 allocation blocks.
See class_distribution.csv for per-class box counts, image counts and allocation-block support.
The allocation optimizes class box proportions and image proportions; grouped scenes can prevent exact 70/15/15 class ratios.

The stricter constraints cause material class imbalance in some splits. For example, Bolt boxes are
1,930/408/962 and MetalSheet boxes are 243/43/108 across train/val/test. This is an unavoidable
tradeoff under the current constraints and allocation: splitting those blocks would reintroduce
strong cross-split matches. Use per-class metrics when evaluating the strict dataset.

Open [review.html](review.html) for stratified match examples and compact groups.
Open [allocation_review.html](allocation_review.html) for large allocation blocks and remaining cross-split matches.
Read [REPORT.md](REPORT.md) for method, threshold rationale, annotation conversion, provenance and limitations.
Training and evaluation commands are in ../README.md. Freeze the reviewed split before training.
New numeric class IDs are alphabetical because historical IDs are unavailable. YOLO labels preserve source class names through that mapping.
The result is similarity-aware, NOT guaranteed video-independent.
