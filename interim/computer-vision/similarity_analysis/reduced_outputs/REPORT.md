# Object-aware reduced dataset

Status: PROVISIONAL; review before training.

Original images: 33,793. Retained: 29,663. Removed as covered redundancy: 4,130 (12.22%).
Protected images: 10,756; rare classes: AdjustableWrench, Hose, MetalSheet, Pen, Screw, Tape, Wood.

Split images: {"train": 20716, "test": 4451, "val": 4496}. Split boxes: {"train": 21211, "test": 4535, "val": 4596}. Largest indivisible block: 802.
All retained strong similarity pairs are constrained to one split. This is similarity-aware, not guaranteed video-independent.

A frame is removable only when a retained frame in the same compact complete-link group has the same class multiset, minimum matched-object cosine >= 0.99, normalized center change <= 0.08, and absolute log-area change <= 0.3. Rare-class, multi-object, difficult, class-small and edge-object images are protected.

The constrained split optimizer returned a valid feasible allocation before reaching its 180-second limit; it is not proven globally optimal. Every class occurs in every split. MetalSheet has an unavoidable 243/108/43 train/validation/test box distribution because its examples belong to a small number of indivisible correlated blocks.

Review [reduction_review.html](reduction_review.html), [annotation_review.html](annotation_review.html), object_pair_distributions.png and class_distribution.csv. Removed files were not deleted from any earlier dataset. No YOLO training was run.
