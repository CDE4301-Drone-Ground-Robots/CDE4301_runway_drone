# CV.docx import notes - original wording preserved

The author requested that the original wording be retained, with only small corrections. The nine Computer Vision chapters have therefore been rebuilt directly from the extracted CV.docx paragraphs. Their order is now tailored to the actual CV pipeline, rather than the generic subsystem headings. The earlier extensive rewrite, generated interface and acceptance tables, additional interpretations, and newly written development plan have been removed.

## Formatting retained

- Original prose is organised beneath the nine report chapter titles.
- Original headings are formatted for website navigation.
- The short executive summary uses the source introduction and two existing architecture sentences; it is not a new rewritten summary.
- All 41 supplied images remain, with captions and full-size viewing.
- Dark figure panels, responsive galleries, and readable transcriptions of the original numerical tables remain.
- The coordinate calculation remains in the original supplied figure; added explanatory calculations and assumptions have been removed.
- The Semester 2 plan uses the original list verbatim.
- Ground-test iterations, lessons, and results now stay together within the YOLO chapter. No new lessons or test outcomes are invented.

## Small corrections applied

- Source paragraph 5: `detect runway surfaces for FOD (Field of Debris)` -> `inspect runway surfaces for FOD (Foreign Object Debris)`
- Source paragraph 35: `Latency calculation was done across the AI models.` -> `Computational workload was estimated across the AI models.`
- Source paragraph 135: `as it can operate regardless of poor lighting or bad weather conditions.` -> `as it can operate in poor lighting.`
- Source paragraph 71: `PatchCore worked very well, detecting all anomalies regardless of size, shape, or texture.` -> `PatchCore worked very well in the examples tested, detecting anomalies of different sizes, shapes, and textures.`
- Source paragraph 118: `more than 51000 images were similar to one another across the random split` -> `more than 51,000 similar image pairs crossed the random split`

Whitespace around paragraphs was trimmed. Caption text and navigation labels are website formatting, not replacements for the author's prose.

## Source details for the author to check

These points are recorded here without rewriting the report: provisional camera specifications and purchase status; the exact combined perceptual-hash/DINOv2 similarity rule; complete dataset references and third-party figure attributions; and validation evidence for the stated requirements. Numerical benchmark results are transcribed from the source figures, not independently re-tested.

The original DOCX was not modified. Other members' chapters and the Communication System report were not modified. Changes have not been committed or pushed.

## Current scrolling report layout

All nine CV sections now live together in website/docs/subsystems/computer-vision.md. Sidebar links jump to explicit section anchors; no previous/next navigation is required. The original paragraphs and all 41 figures remain. Old chapter URLs redirect to the appropriate position in this report. The other four subsystem reports are empty below their title and lead details until their authors provide content.

## Author additions - 29 October 2026

- Added the four dataset URLs supplied by the author to the CV report and shared references. Mendeley publisher metadata was verified; the Kaggle and Roboflow links were retained as supplied where automated access was limited.
- YOLO FOD and thermal detection training: 100 epochs; batch size 16; 80% train, 10% validation, 10% test, confirmed by the author after correcting the initial 80/20/20 entry. No settings were inferred for PatchCore or U-Net.
- Transcribed the two similarity conditions from CV-28, using the original prose's either-condition logic: DINOv2 >= 0.99 OR (pHash <= 6 AND DINOv2 >= 0.97).
- Added the planned underside light near the RGB camera, switched on for night operation, and its future test task.
- Retained the distinction between GFLOPs and elapsed inference latency. The existing workload table does not provide measured milliseconds per frame.

These are targeted additions and source links; the author's original paragraphs remain otherwise unchanged.

## Flow and repetition review

At the author's request, repeated architecture opening sentences, repeated thermal training numbers, redundant split-count prose, the duplicate audit-table image, and a repeated thermal future-work sentence were removed. The original dataset-variant sentence was moved beside its figure. The crack dataset citation now precedes the approach/results. The model-rationale heading distinguishes using both models from concurrent scheduling; a small grammar error was corrected. RGB camera wording now consistently describes a provisional selection. The integration section explicitly records the author's clarification that object trials were functional checks, not formal requirement validation. HPC training location was added from the author's statement. Original wording is otherwise retained; no results or timing measurements were invented.
