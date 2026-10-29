---
title: Computer Vision Based Inspection and Safety System
outline: [2, 2]
prev: false
next: false
---

<div class="cv-report">

<p class="chapter-kicker">FOD ARGUS / COMPUTER VISION &amp; SAFETY</p>

# Computer Vision Based Inspection and Safety System

<div class="cv-report-byline"><span>Charansagar Ramanujam</span><span>A0301658E</span></div>

## Executive Summary {#executive-summary}

The computer vision system was developed to enable the UAV to autonomously inspect runway surfaces for FOD (Foreign Object Debris), water puddles, surface cracks, and other common objects. A key challenge in this system is the impracticality of obtaining every possible object that can appear on the runway for the training dataset. Hence, it can identify classes within the training set, but it would not recognise unseen objects. The next section addresses the solution.

To address the limitations of an unseen training dataset, we adopted a multi-stage computer vision architecture. The RGB camera is used as the primary runway inspection system.

## System Overview & Requirements {#subsystem-overview}

### Requirements of This Subsystem

- Detect FOD as small as 5mm.
- Detect Huge cracks.
- Detect huge water puddles.
- Coordinate extraction.
- Design an integrated system.
- Suitable camera selection.
- Day and Night operations.

### Software

These are some of the software tools used in this subsystem to train the model and generate and edit the dataset.

<CvFigure n="1" />

### ARGUS Camera View

<CvFigure n="2" />

The ARGUS drone has the RGB camera facing down and centred on the drone, rather than at an angle. This setup makes it easier to collect training data and simplifies FOD coordinate extraction.

### RGB Cameras

<CvFigure n="3" />

The RGB camera selected for the final drone is the e-con e-CAM56_CUONX as shown in the figure above. The camera is a global-shutter camera that runs at 79 fps. This is not the final camera and may change once the RSAF budget is approved. In the interim, we used the UGREEN-CM831 webcam for model testing and evaluation.

### Night Operation Lighting

A light will be attached below the drone, near the RGB camera, and switched on during night operation to illuminate the inspection surface.

### Computer Vision System Architecture

To address the limitations of an unseen training dataset, we adopted a multi-stage computer vision architecture. The RGB camera is used as the primary runway inspection system. The RGB camera captures images continuously, which then pass through the system. The captured images first enter a PatchCore anomaly detection model. The system then crops regions identified as anomalous and sends them to the second layer. The crop is done to make the unknown anomaly occupy a larger proportion, avoiding the loss of important feature details. It also stores them separately as heatmap images for visual inspection, if needed. The second layer consists of 2 models. YOLO object detector and a U-Net segmentation model for runway cracks run simultaneously. The cropped image is then resized to the model's input size and fed into the model. If any cracks are detected, the system sends them to the base. On the YOLO side, if it detects a FOD object, it sends the coordinates to the UGV for extraction. If neither the crack detection model nor YOLO identifies it, the system sends it to the base station for inspection.

<CvFigure n="4" />

### Computational Workload

| AI function | Model listed in the draft | Arithmetic complexity | Relative workload |
| --- | --- | ---: | ---: |
| Crack segmentation | U-Net | 62.512 GFLOPs | 100% |
| FOD detection | YOLO11s | 55.496 GFLOPs | 88.8% |
| Surface anomaly detection | PatchCore CNN | 23.998 GFLOPs | 38.4% |
| Thermal object detection | Thermal YOLO11s | 21.422 GFLOPs | 34.3% |

Computational workload was estimated across the AI models. Based on the GFLOPS calculated, FOD detection and Crack segmentation are the most computationally demanding tasks. In Architecture prototype 1 above, these models are running simultaneously. This is addressed in the next section.

The table reports computational workload in GFLOPs, rather than measured inference time in milliseconds. Runtime latency will be measured during the model and integrated-system tests listed in the future work.

### Computer Vision System Architecture (Fallback)

There would be cases when Jetson Nx resources are scarce due to multiple subsystems running, such as navigation and communication systems. They would all be competing for GPU resources, memory bandwidth and power. Hence, we designed a fallback architecture for low-resource scenarios. This pipeline runs Crack and YOLO sequentially instead of simultaneously, reducing resource consumption.

<CvFigure n="6" />

### Why Do Crack U-Net and YOLO Run Together?

Based on the architecture, I run both models independently, not conditionally, to ensure I don't miss one type of anomaly for the other. As illustrated below, if a system, for example, detected a water puddle using YOLO and the skip crack model, we would miss the underlying large crack. Although this approach adds computational requirements, it prioritises detection requirements over computational efficiency, which is important for runway safety applications.

<CvFigure n="7" />

## PatchCore Anomaly Detection {#patchcore-anomaly-detection}

### What Is PatchCore?

PatchCore is used as the first stage because it identifies anomalies such as cracks and objects. We use it instead of running YOLO and Crack continuously on each frame, which is computationally heavy. Hence, running a single model saves computational resources on Jetson.

PatchCore learns visual characteristics of a normal runway or road surface. It doesn't need to learn any specific FOD categories. During operation, if the obtained image region differs from the learned normal appearance, it generates high anomaly scores accordingly. The essential overview of this model is shown in the figure below.

<CvFigure n="8" />

### PatchCore in the Project

Patchcore produces an image-level anomaly score and a heatmap showing the unusual areas. Heatmap images are produced and stored in every run for visual inspection if necessary. A bounding box is then generated to identify the anomaly. The image is then cropped and resized to the normal model input size before passing it to YOLO and U-Net.

<div class="cv-figure-grid">
<CvFigure n="9" />

<CvFigure n="10" />

<CvFigure n="11" />
</div>

PatchCore also serves as a fallback mechanism for previously unseen objects. If PatchCore detects an anomaly that is unrecognised by either YOLO or U-Net (crack detector), the system can store it as an unknown anomaly and send it to the base station for further investigation.

### Dataset and Test Results

The dataset was collected at the NUS test ground outside Techno, at the roundabout.

<CvFigure n="12" />

PatchCore worked very well in the examples tested, detecting anomalies of different sizes, shapes, and textures. The system used the bounding boxes to crop the regions and send them to YOLO and the crack model.

<CvFigure n="13" />

## YOLO FOD Detection & Dataset Development {#yolo-fod-detection}

### FOD Classes and Dataset

The anomaly region processed by Patchcore is then cropped and passed to the YOLO FOD detector. The YOLO object detector is trained on 32 classes: 31 objects and a water puddle, as shown in the figure below. Data preparation is one of the most challenging parts of this system. We sourced the FOD dataset from Kaggle online.  It included more than 31 classes, and we added the water puddle class to meet our requirements. The dataset has 33793 images but lacks weather variations such as cloudy, rainy, or hazy conditions. The FOD background also appears to be a very light surface that doesn't resemble the dark road surface we require.

Dataset source: [Foreign Object Debris in Airports (FOD-A), Kaggle](https://www.kaggle.com/datasets/kilogrand/foreign-object-debris-in-airports-fod-a-dataset/code). See [CV-D02 in References](../references#cv-d02).

<CvFigure n="14" />

<CvFigure n="15" />

### Synthetic Compositing Method

Therefore, we implemented synthetic compositing to address the issues above. This method can place FODs artificially on any surface. We synthetically added the FODs to different road surfaces to create a new dataset. We also synthetically generated rain and fog with corresponding YOLO bounding-box annotations. I made them look as realistic as possible by tuning them, as shown in the figure below. This reduces the need to collect many real-world samples.

<div class="cv-figure-grid">
<CvFigure n="16" />

<CvFigure n="17" />

<CvFigure n="18" />

<CvFigure n="19" />

<CvFigure n="20" />

<CvFigure n="21" />
</div>

These are some of the challenges this method can help to solve. Specifically, for this dataset, it helped to solve the 2 issues highlighted above. The background surface issue and automatic labelling after creating new artificial data to reduce time consumption.

<CvFigure n="22" />

### YOLO Detection Outputs

YOLO is responsible for identifying known FOD categories from the classes above. For each detected object, it returns the object class, confidence score and bounding-box coordinates. The cropped anomaly is resized so that small objects like nuts and nails are identified easily.

<div class="cv-figure-grid">
<CvFigure n="23" />

<CvFigure n="24" />
</div>

### YOLO Training Settings

The YOLO FOD models were trained using the following settings. The same settings were used for the thermal detection models.

| Setting | Value |
| --- | ---: |
| Epochs | 100 |
| Batch size | 16 |
| Training split | 80% |
| Validation split | 10% |
| Testing split | 10% |

### Model Comparison

We tested different YOLO versions, as shown in the table below. All achieved very high detection performance, with only small differences. These results were suspiciously high, so we also tested them on the ground.

| Model | Precision | Recall | mAP@50 | mAP@50-95 |
| --- | ---: | ---: | ---: | ---: |
| YOLOv8s | 99.69% | 99.20% | 99.15% | 92.37% |
| YOLOv8m | 99.54% | 99.28% | 99.12% | 92.95% |
| YOLOv8L | 99.72% | 99.34% | 99.18% | 93.39% |
| YOLO11s | 99.67% | 99.33% | 99.19% | 92.57% |
| YOLO11m | 99.70% | 99.35% | 99.23% | 92.88% |
| YOLO11L | 99.68% | 99.39% | 99.26% | 93.25% |

<CvFigure n="25" />

### Ground Testing and Second Iteration

<CvFigure n="26" />

The model was performing very poorly, and the test object was detected inconsistently. In a 2nd iteration, instead of using different road surface images to generalise, I used only test-ground road surface for the synthetic compositing. The performance improved as shown below in the figure, but it was still not up to standard.

<CvFigure n="27" />

### Dataset Investigation

The dataset was then investigated, and it was hypothesised that there was data leakage happening. Based on visual inspection, moving image by image, each FOD in the dataset was recorded as a video and sliced to generate the images. Hence, when a random split was performed above, the near-identical consecutive frames were placed across all the splits (training, testing and validation). This resulted in abnormally high results from YOLO but underperformed on the actual ground.

I applied two similarity detection techniques to check for data leaks and reduce them. Perceptual hash identifies near-duplicate images by comparing their visual structure, while DINOv2 uses pretrained deep learning to identify similar features. Both techniques are combined to group strongly similar images and assign them to a single split. A constraint was added where, if either one is true, the images are flagged as similar.

As shown in Figure CV-28, images are flagged as similar when either of the following conditions is met:

- DINOv2 similarity is at least 0.99.
- Perceptual-hash distance is at most 6 **and** DINOv2 similarity is at least 0.97.

$$
(s_{\mathrm{DINOv2}} \geq 0.99)\quad\lor\quad
\left[(d_{\mathrm{pHash}} \leq 6)\land(s_{\mathrm{DINOv2}} \geq 0.97)\right]
$$

<CvFigure n="28" />

### Similarity-Aware Splitting

| Metric | Random split | Similarity-aware split |
| --- | ---: | ---: |
| Total images analysed | 33,793 | 33,793 |
| Strongly similar pairs crossing splits | 51,361 | 0 |
| Similarity groups crossing splits | 4,471 | 0 |
| Images involved in strong similarity relationships | 25,838 | 25,838 |
| Strong pair constraints identified | 110,605 | 110,605 |
| Related images kept in the same split | No | Yes |

<CvFigure n="29" />

### Dataset Variants

<CvFigure n="30" />

### Results and Discussion

I ran the similarity test on the original Kaggle dataset, where more than 51,000 similar image pairs crossed the random split. After applying these techniques, we re-ran the split, which minimised similarity leakage, as shown in the figure. Three datasets were created: one was the random split, the second was the similarity split, and the third was the similarity split plus removal of redundant images. The results below confirm the hypothesis that data leakage occurs, as mAP decreases. This shows that if further fine-tuning were done, better accuracy of the model could be obtained. Nevertheless, this dataset has many limitations. The images in the dataset were all taken at a low height, while we require images at 5m. Too many classes also reduce the model's accuracy. During synthetic compositing, precision and recall get affected, as realistic lighting, scale, shadow and blur are hard to tune.

| Dataset | Reported mAP@50-95 | Interpretation |
| --- | ---: | --- |
| Random baseline | Approximately 95% | Approximate reference result; potentially inflated by leakage |
| Strict | 88.10% | All images retained with similarity-aware grouping |
| Strict-reduced | 88.93% | Similarity-aware grouping with redundant images removed |

<CvFigure n="31" />

## Crack Detection Using U-Net {#crack-detection}

### Crack Segmentation Approach

Runway and road cracks are essentially different from the normal FOD objects. Cracks are usually thin, long and irregular, so a normal object detector is not feasible.

Therefore, we use a U-Net segmentation model. The cropped anomaly region is resized to 512 x 512 and fed into the U-Net, as this is the required input size. The model then produces a pixel-level crack mask.

<div class="cv-figure-grid">
<CvFigure n="32" />

<CvFigure n="33" />

<CvFigure n="34" />
</div>

### On-the-Ground Results

<CvFigure n="35" />

The crack dataset is obtained from [Mendeley Data: CrackAirport, version 1](https://data.mendeley.com/datasets/3v5r2fxf89/1), where the model worked well for surfaces like concrete but doesn't perform well on the test ground surface due to its roughness. Hence, either cracks from the original test ground or an artificial method is required to obtain the dataset.

See [CV-D01 in References](../references#cv-d01) for the crack dataset citation.

## FOD & Crack Coordinate Retrieval {#coordinate-retrieval}

### Coordinate Retrieval Example

Suppose an original image size is 1280 x 720. The first PatchCore layer detects an anomalous region and bounds it. (x1,y1,x2,y2) = (400,200,700,500) is a bounded region in this case. Hence, the anomaly crop is 300 x 300. This crop will be resized before going to the other 2 models.

<CvFigure n="36" />

## Thermal Safety & Camera Selection {#thermal-safety}

### Thermal Detection for Safety

The thermal detection layer was implemented as a safety layer in addition to obstacle avoidance. The LIDAR mounted can only detect obstacles at the height the drone is flying, leaving the road below completely clueless to the UAV. The thermal camera is used instead of a secondary RGB camera as it can operate in poor lighting.

<CvFigure n="37" />

Hence, the thermal camera is mounted along with the RGB camera below, pointed at an approximate angle of 45 degrees. This camera is positioned such that it will detect the area ahead on the road for potential obstacles such as people, birds and other heat emitters. If a thermal object is detected, the system is intended to stop and hold till the obstacle is cleared or gone, which reduces the risk of collision. This thermal sub-system operates independently from the RGB FOD detection pipeline. In the current prototype, it's simulated in software for testing, and some results are shown below. Future work includes integrating the thermal detector directly to the flight controller for an automatic safety response.

<CvFigure n="38" />

### Thermal Datasets and Training Settings

The thermal detection models used the following datasets:

- [Thermal Bird, version 6, Roboflow Universe](https://universe.roboflow.com/arc-ejbpg/thermal-bird/dataset/6) - [CV-D03 in References](../references#cv-d03).
- [Thermal Images for Human Detection, Kaggle](https://www.kaggle.com/datasets/sikdermdsaiful/thermal-images-for-human-detection/data?select=dataset) - [CV-D04 in References](../references#cv-d04).

The thermal models were trained for **100 epochs** with a **batch size of 16** and an **80% training / 10% validation / 10% testing split**, matching the [YOLO training settings](#yolo-training-settings).

### Thermal Model Comparison

Different YOLO versions were tested as shown below in the table.  The thermal model comparison shows greater variance across models. YOLO11m achieved the highest mAP@50-95, while YOLOv8s achieved the highest mAP@50 at 97.70%. YOLO11L achieved the highest recall at 95.38%, meaning it detected the largest proportion of thermal targets, even though it had the lowest precision. Since this detection serves as a safety layer for detecting people, birds, and potential obstacles, recall is important, as missing an obstacle is more critical than occasional false detections. Therefore, the final model should be chosen based on detection accuracy and reliable real-time performance onboard the UAV.

| Model | Precision | Recall | mAP@50 | mAP@50-95 |
| --- | ---: | ---: | ---: | ---: |
| YOLOv8s | 95.25% | 93.52% | 97.70% | 70.88% |
| YOLOv8m | 94.33% | 83.87% | 91.93% | 66.14% |
| YOLOv8L | 88.60% | 89.54% | 94.14% | 68.56% |
| YOLO11s | 95.46% | 93.69% | 96.80% | 70.88% |
| YOLO11m | 96.22% | 89.45% | 96.05% | 71.27% |
| YOLO11L | 88.00% | 95.38% | 95.46% | 69.36% |

<CvFigure n="39" />

### Cameras Selected for RGB and Thermal

This thermal camera provides the wide field of view needed for forward safety monitoring while remaining compact and lightweight. The camera uses a 256 x 196 thermal sensor with a 4mm F/1.1 lens and a 45.5 degrees x 33.5 degrees field of view. This ensures a large area is monitored for people, birds and possibly other potential obstacles. The module operates at 25Hz and supports interfaces such as MIPI and USB 2.0. It has a low power consumption, making it suitable for drone use.

<CvFigure n="40" />

For the current prototype, we used a standard USB webcam for full vision system testing. The intended final RGB camera is the Sony IMX568 global-shutter camera; however, it has not been purchased and is not used in the interim till the specifications are confirmed and meet the system and project requirements.

## System Integration & Evaluation {#integration-evaluation}

### Overall Integrated System

The first integration demonstrated a collaborative system where all models run together using a fallback architecture in which the models run sequentially. The first prototype architecture was not implemented due to hardware limitations in running two models at the same time. Testing was done on the laptop, but it slowed the laptop, resulting in visual latency. Hence, I will conduct more thorough testing and evaluation once I receive the Jetson NX.

<CvFigure n="41" />

## Semester 2 Development Plan {#semester-2-development-plan}

### CV System Future Works

- Obtain a new dataset with pictures taken 5m above the test ground using the RGB camera.
- Add FOD items to the test ground and collect a dataset to increase YOLO robustness and reduce reliance on synthetic images.
- Do proper system integration using Jetson NX following the Pipeline.
- Test both RGB and Thermal cameras with the models.
- Attach and test the light below the drone near the RGB camera for night operation.
- Implement the link between the cameras and the vision system in Jetson NX.
- Extract current drone coordinates from ROS2 Navigation to the Vision system.
- Link Thermal detection to the flight controller for emergency stops.
- Set up a program to prevent repeated FOD coordinates from being sent (Work with the UGV side).
- Test the Latency for each model and the entire integrated system.

</div>
