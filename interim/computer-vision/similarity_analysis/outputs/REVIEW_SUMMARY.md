# Review summary

PROVISIONAL: the exported dataset is a review copy. YOLO training has not started.

33,793 images; 34,472 boxes; 31 classes.
Byte-identical images: 0. Provisional joint-rule near-duplicate images: 18,984.
Candidate pairs: 494,446; compact non-singleton candidate groups: 6,150.
Allocation blocks including singletons: 17,671; largest block: 260 images.
Original split-spanning groups: unavailable; previous split manifests were not provided.

| Split | Images | Percentage |
|---|---:|---:|
| train | 23,682 | 70.08% |
| val | 5,055 | 14.96% |
| test | 5,056 | 14.96% |

| Cross-split measure | Illustrative random baseline | Proposed split |
|---|---:|---:|
| Strong joint-rule pairs | 22,347 | 0 |
| All retrieved candidate pairs | 230,384 | 137,401 |
| Median nearest cross-split cosine | 0.9805 | 0.9657 |
| Images with cross-split nearest cosine >= .98 | 17,424 | 5,406 |

The baseline is a new seeded random split, not your historical split. Cosine alone does not confirm common video origin.
137,401 retrieved weaker/uncertain candidate pairs still cross splits; 14,402 have cosine >= .98.
Zero strong joint-rule crossings is a threshold-specific result, not proof of no leakage.
Compact groups use complete pairwise evidence to avoid weak-chain scene merging. Additional same-split constraints
link strong matches between compact groups. These allocation blocks do not assert source-video identity.

Classes absent from a split: 0. Minimum class support: 26 allocation blocks.
See class_distribution.csv for per-class box counts, image counts and allocation-block support.
The allocation optimizes class box proportions and image proportions; grouped scenes can prevent exact 70/15/15 class ratios.

Open [review.html](review.html) for stratified match examples and compact groups.
Open [allocation_review.html](allocation_review.html) for large allocation blocks and remaining cross-split matches.
Read [REPORT.md](REPORT.md) for method, threshold rationale, annotation conversion, provenance and limitations.
Training and evaluation commands are in ../README.md. Freeze the reviewed split before training.
New numeric class IDs are alphabetical because historical IDs are unavailable. YOLO labels preserve source class names through that mapping.
The result is similarity-aware, NOT guaranteed video-independent.
