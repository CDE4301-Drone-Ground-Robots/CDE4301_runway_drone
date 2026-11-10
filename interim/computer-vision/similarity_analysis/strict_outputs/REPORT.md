# FOD similarity-aware dataset audit
Status: PROVISIONAL; review similarity evidence and proposed split before YOLO training.

Images: 33793; annotation files: 33793; bounding boxes: 34472; classes: 31.
Byte-identical images (all members, not redundant-copy count): 0.
Provisional near-duplicate images (pHash + DINO rule, NOT human-confirmed): 25838.
Candidate pairs: 494447. Non-singleton candidate groups: 7318.
Groups including singletons: 17366.
Original split-spanning groups: unavailable, because historical split assignments are missing.

## Method and thresholds
pHash: RGB decoded to grayscale, LANCZOS 32x32, orthonormal type-II DCT, 8x8 low-frequency block;
DC is excluded from the median and its bit is forced off. This custom 64-bit convention is versioned in the script.
Radius <= 6 is exhaustively searched with a BK-tree. It is a candidate retrieval threshold.
DINOv2: pinned official pretrained ViT-S/14, no fine-tuning, float32 L2-normalized CLS embeddings.
RGB images resize directly to 224x224 with bicubic interpolation, without cropping the runway edges.
Exact float32 batched cosine top-30 search; no approximate-neighbour recall loss.
However, top-k retrieval does NOT enumerate every pair above a cosine threshold.
Review cosine >= 0.95.
Configured strong co-location rule: DINO cosine >= 0.99 OR (pHash <= 6 AND DINO cosine >= 0.97).
These are review heuristics, NOT calibrated probabilities or established video-identity boundaries.
Inspect review.html, especially hash-only, DINO-only and boundary examples, before accepting them.
pHash distances reflect global low-frequency appearance and can miss small FOD differences.
DINO semantic similarity can confuse unrelated runway scenes.
Class labels do not determine similarity grouping.
Byte-identical files are kept together. All pairs inside each proposed group must have strong or explicitly
accepted evidence (complete-link constraint); transitive weak chains cannot create a group.
This conservative rule can leave strong edges between distinct compact groups. Split co-location blocks
keep every such un-rejected strong edge in the same split without declaring those groups to be one scene.

## Split
Seed: 4301. Targets: 70/15/15. Actual images: {"train": 23106, "val": 5301, "test": 5386}.
Multiple seeded greedy allocations optimize image counts and per-class BOX counts.
Compact pairwise-verified candidate groups remain separate for interpretation.
For split allocation ONLY, all strong/explicitly accepted pairs impose same-split constraints.
Transitive closure of those constraints defines allocation blocks, not inferred videos or similarity groups.
Weak candidate edges never impose these constraints. A block can contain unrelated scenes linked through
strong matches; co-location is conservative for evaluation and does not assert shared video provenance.
See allocation_blocks.json. The largest block size and block counts are in split_summary.json.
See class_distribution.csv for class IDs, counts and unavoidable imbalance. Class coverage is not guaranteed
where a class occurs in very few independent groups. No source annotations are edited.
New class IDs are alphabetical because historical YOLO IDs were not supplied.
VOC fractional xyxy coordinates are interpreted as zero-origin continuous coordinates, matching this export's
decimal box style; they are normalized without a one-pixel offset. Validate overlays if the source convention differs.
Difficult objects are retained; their flags remain in the manifest but YOLO detection labels do not encode them.

## Before and after
There is NO measured historical baseline. illustrative_random is a newly generated, seeded image-level random
split of this clean download, supplied solely to demonstrate sensitivity to splitting methodology.
proposed_similarity_aware uses the proposed groups. Both are compared using all retrieved candidate pairs
and exact per-image nearest cosine matches in other splits.
See analysis_summary.json and cross_split_similarity.png.
Cross-split candidate matches are evidence to review, not confirmed leakage. Accepted/proposed groups never cross splits.
All retrieved un-rejected strong pairs are constrained to one split; weaker uncertain matches can still cross.
Do not treat the split as final
while concerning cross-split matches remain unresolved. Consider broader manually verified scene groups,
quarantining uncertain scenes, or a genuinely independent acquisition.

## Review workflow
Open review.html; inspect candidate_pairs.csv and blocked_merges.json.
Add pair decisions to pair_decisions.csv (a,b,decision,note; accept/reject/blank), then rerun:
neighbours, groups, propose, report. Decisions bind to immutable manifest indices.
An accepted edge may be blocked if the resulting group lacks complete pairwise evidence; inspect blocked_merges.json.
Do not force a video identity from background semantics or numerical filenames.
Export a review copy with --provisional, or a reviewed copy with --reviewed. No script invokes model training.

## Limitations
This is similarity-aware, NOT guaranteed video-independent. Videos/timestamps/camera session IDs are unavailable.
XML track IDs 0 and 1 are reused across files; no reliable video identity can be inferred from them.
The clean dataset contains no synthetic images, as confirmed by the user.
Embeddings/global hashes may miss spatially transformed, illuminated, occluded, or temporally distant related frames.
Near-identical backgrounds with changing tiny debris need careful manual review.
No negative/background-only annotations were found in the initial audit; deployment false-positive performance
needs independent real runway background samples.
Repeated use of validation/test images to tune model decisions biases evaluation; freeze the reviewed split
before training and reserve test model evaluation for the final run.
Sources: https://github.com/facebookresearch/dinov2
https://docs.ultralytics.com/modes/train/
https://docs.ultralytics.com/modes/val/
