# Seeded random-split baseline

This dataset contains all 33,793 original images and 34,472 boxes. It uses the previously measured seed-4301 image-level random assignment: 23,655 train, 5,069 validation and 5,069 test images.

This baseline deliberately ignores pHash/DINOv2 similarity groups. The similarity audit measured 51,361 strong candidate pairs and 4,471 compact similarity groups crossing its splits. Its scores may therefore be optimistic and should be presented as the random-frame baseline, not as the main generalization result.

All source and copied image checksums and all generated YOLO labels were verified. Every class appears in every split. The original VOC dataset and all similarity-aware datasets were left unchanged. Historical Kaggle split assignments were unavailable, so this is a newly generated reproducible baseline rather than a reconstruction of the prior split.
