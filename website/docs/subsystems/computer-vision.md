---
title: Computer Vision Based Inspection and Safety System
outline: [2, 2]
prev: false
next: false
---

<script setup>
import { withBase } from 'vitepress'
import { data as integrationDemo } from '../cv-integration-demo.data'
</script>

<div class="cv-report">

<p class="chapter-kicker">FOD ARGUS / COMPUTER VISION &amp; SAFETY</p>

# Computer Vision Based Inspection and Safety System

<SubsystemLead class="cv-report-byline" name="Charansagar Ramanujam" matric="A0301658E" portrait="/team/Charan.png" />

## Executive Summary {#executive-summary}

The computer vision system was developed to enable the UAV to autonomously inspect runway surfaces for FOD (Foreign Object Debris), water puddles, surface cracks, and other common objects. A key challenge in this system is the impracticality of obtaining every possible object that can appear on the runway for the training dataset. Hence, it can identify classes within the training set, but it would not recognise unseen objects.

To address the limitation of detecting only objects seen in the training dataset, we adopted a multi-stage computer vision architecture. The RGB camera is used as the primary runway inspection system.

## System Overview & Requirements {#subsystem-overview}

### Requirements of This Subsystem

- Detect FOD as small as 1 cm.
- Detect visible surface cracks.
- Detect water puddles.
- Coordinate extraction.
- Design an integrated system.
- Suitable camera selection.
- Day and night operations.

No minimum crack size is specified; the aim is to detect visible surface cracks. The puddle size target, target detection performance and acceptable coordinate error still need to be defined.

### Software

These are some of the software tools used in this subsystem to train the model and generate and edit the dataset.

<CvFigure n="1" />

### ARGUS Camera View

<CvFigure n="2" />

The ARGUS drone has the RGB camera facing down and centred on the drone, rather than at an angle. The intended camera view covers a 2 m × 2 m area at a height of 5 m. A suitable lens is needed to achieve this coverage. A gimbal is planned for the RGB inspection camera, using attitude data from the flight controller to compensate for drone roll and pitch and keep the camera pointing straight down (nadir). Adding and testing this gimbal is future work. This setup makes it easier to collect training data and simplifies FOD coordinate extraction.

### RGB Cameras

<CvFigure n="3" />

The RGB camera proposed for the final drone is the e-con e-CAM56_CUONX as shown in the figure above. The camera is a global-shutter camera that runs at 79 fps. The selection is not final and may change once the RSAF budget is approved. It may be changed to an IDS camera which has a higher resolution and a global shutter as well. In the interim, we used the UGREEN-CM831 webcam for model testing and evaluation.

Manufacturer product page: [e-con Systems e-CAM56_CUONX - Sony IMX568 global-shutter camera](https://www.e-consystems.com/nvidia-cameras/jetson-orin-nx-cameras/5mp-imx568-global-shutter-camera.asp). See [CV-H01 in References](../references#cv-h01). IDS alternative: [U3-31L1ACP Rev.1.2](https://en.ids-imaging.com/store/u3-31l1acp-rev-1-2.html), [CV-H02 in References](../references#cv-h02).

### RGB Camera Calculation for 1 cm FOD

The requirement is to detect FOD as small as **1 cm at a flight height of 5 m**. The e-CAM56_CUONX has 2472 × 2064 active pixels. The supplied lens has a horizontal field of view of 85.64° and a vertical field of view of 72.25° ([CV-H01](../references#cv-h01)).

Assume the camera faces straight down over flat ground. Using an ideal pinhole approximation, the ground coverage is:

$$
W=2H\tan\left(\frac{\theta_H}{2}\right)
=2(5)\tan(85.64^\circ/2)\approx9.27\ \mathrm{m}
$$

$$
L=2H\tan\left(\frac{\theta_V}{2}\right)
=2(5)\tan(72.25^\circ/2)\approx7.30\ \mathrm{m}
$$

| Calculation | Horizontal | Vertical |
| --- | ---: | ---: |
| Ground sampling distance | 9266.6 / 2472 = 3.75 mm/pixel | 7298.8 / 2064 = 3.54 mm/pixel |
| Pixels across a 1 cm object | 10 / 3.75 ≈ 2.7 pixels | 10 / 3.54 ≈ 2.8 pixels |

A 1 cm object would span only about 3 pixels at full resolution, so reliable detection is not yet confirmed. Resizing the full frame before anomaly detection can reduce this further; enlarging a crop cannot recover lost detail.

#### Lens Needed for the Intended 2 m × 2 m View

The camera has a 2.74 µm pixel pitch and an M12 lens holder ([CV-H01](../references#cv-h01)). Its active sensor height is:

$$
S_y=2064\times0.00274=5.65536\ \mathrm{mm}
$$

For a 2 m vertical ground coverage at 5 m above the surface, the required focal length is approximately:

$$
f=\frac{H S_y}{L}
=\frac{5000\times5.65536}{2000}
=14.14\ \mathrm{mm}
$$

A **14 mm M12 lens** is therefore a candidate, provided it supports the camera's 1/1.8-inch sensor and can focus at 5 m. This is a calculated lens requirement; a specific lens model has not been confirmed.

With a 14 mm lens, the estimated full-frame coverage is:

$$
W=\frac{5000(2472\times0.00274)}{14}\approx2419\ \mathrm{mm},\qquad
L=\frac{5000(2064\times0.00274)}{14}\approx2020\ \mathrm{mm}
$$

The rectangular frame covers about **2.42 m × 2.02 m**. A centred 2064 × 2064 pixel crop gives approximately **2.02 m × 2.02 m**, close to the intended view, without stretching the image.

$$
\mathrm{GSD}=\frac{2020}{2064}\approx0.979\ \mathrm{mm/pixel},\qquad
n_{\mathrm{1\,cm}}=\frac{10}{0.979}\approx10.2\ \mathrm{pixels}
$$

A 1 cm object would span about **10 pixels before resizing**. This improves the sampling compared with the supplied wide-angle lens, but does not prove reliable detection. The anomaly stage must retain enough detail to identify the object before cropping.

The selected lens, distortion, focus, motion blur, lighting and model performance still need testing with real 1 cm FOD at 5 m. The coverage above is an estimate, not a calibrated measurement.

ARGUS is intended to fly at 15 km/h. Short exposure times will be needed to limit motion blur. Camera settings and processing performance will be tested on Jetson after the interim stage.

### Night Operation Lighting

A light source will be attached below the drone, near the RGB camera, and switched on during night operation to illuminate the inspection surface.

<CvFigure n="43" />

### Computer Vision System Architecture - Parallel

The RGB camera captures images continuously, which then pass through the system. The captured images first enter a PatchCore anomaly detection model. Each frame captured will keep triggering the navigation system to send the current drone position and orientation. The position gives the drone X and Y coordinates, while the quaternion gives its orientation. If there is no anomaly on the road, it continues the inspection. If an anomalous region is identified, the model produces a bounding box and crops it. The system then sends it to the second layer. The second layer consists of 2 models: a YOLO object detector and a U-Net segmentation model for runway cracks, which run in parallel. The cropped image is then resized to each model's input size and fed into that model. If any cracks are detected, the system sends them to the base. On the YOLO side, if it detects a FOD object, it performs more localised coordinate extraction and sends the coordinates to the UGV for extraction. If neither the crack detection model nor YOLO identifies it, the system sends it to the base station as it is an anomaly that neither model identifies. The models will be explained in more depth in the later sections. The drone position, quaternion heading and precise FOD coordinate calculations are explained in [FOD & Crack Coordinate Retrieval](#coordinate-retrieval).

<CvFigure n="4" />

### Computational Workload

| AI function | Model listed in the draft | Arithmetic complexity | Relative workload |
| --- | --- | ---: | ---: |
| Crack segmentation | U-Net | 62.512 GFLOPs | 100% |
| FOD detection | YOLO11s | 55.496 GFLOPs | 88.8% |
| Surface anomaly detection | PatchCore CNN | 23.998 GFLOPs | 38.4% |
| Thermal object detection | Thermal YOLO11s | 21.422 GFLOPs | 34.3% |

Computational workload was estimated across the AI models. Based on the GFLOPs calculated, FOD detection and Crack segmentation are the most computationally demanding tasks. In the parallel architecture above, these models are running in parallel. This is addressed in the next section.

GFLOPs describe the amount of computation. Measured laptop inference times are reported in [Section 8](#integration-evaluation).

### Computer Vision System Architecture - Sequential 1 (Fallback)

There would be cases when Jetson NX resources are scarce due to multiple subsystems running, such as navigation and communication systems. They would all be competing for GPU resources, memory bandwidth and power. Hence, a fallback architecture was designed for low-resource scenarios. This pipeline runs YOLO and Crack sequentially instead of in parallel, reducing resource consumption. Both models check every crop.

<CvFigure n="6" />

### Additional Tested Architecture - Sequential 2

Sequential 2 is an extra architecture that was tested where YOLO runs first. If FOD is detected, the coordinates are sent to the UGV and ARGUS continues inspection. Otherwise, the crop goes to U-Net for crack detection. This architecture bypasses the crack model whenever YOLO detects FOD. Nevertheless, it was rejected for the reasons explained after the next architecture comparison section.

<CvFigure n="42" />

### Architecture Comparison and Memory Use

All three architectures were tested on the same laptop. The setup and full timing results are in [Section 8](#integration-evaluation).

| Architecture | Average processing time (ms/frame) | Processing rate (frames/s) | Peak allocated GPU memory (MiB) |
| --- | ---: | ---: | ---: |
| Parallel | 87.34 | 11.45 | 532.44 |
| Sequential 1 | 99.19 | 10.08 | 391.66 |
| Sequential 2 | 72.87 | 13.72 | 391.66 |

<div class="cv-latency-result">
 <div class="cv-latency-label"><span>Mean latency reduction: Parallel vs Sequential 1</span><strong>11.9%</strong></div>
 <div class="cv-latency-track" role="meter" aria-label="Mean latency reduction with Parallel compared with Sequential 1" aria-valuemin="0" aria-valuemax="100" aria-valuenow="11.9"><span></span></div>
 <p>Parallel reduced mean processing time by 11.84 ms per frame compared with Sequential 1.</p>
</div>

<div class="cv-latency-result cv-memory-result">
 <div class="cv-latency-label"><span>Peak GPU memory reduction: Sequential 1 vs Parallel</span><strong>26.4%</strong></div>
 <div class="cv-latency-track" role="meter" aria-label="Peak allocated GPU memory reduction with Sequential 1 compared with Parallel" aria-valuemin="0" aria-valuemax="100" aria-valuenow="26.4"><span></span></div>
 <p>Sequential 1 used 140.78 MiB less peak allocated GPU memory than Parallel.</p>
</div>

Running YOLO and U-Net in Sequential 1 used about 26.4% less GPU memory, while running them in parallel reduced processing time by about 11.9%. This gives us a reason to keep the sequential fallback when less memory is available. We still need to test it on the Jetson alongside navigation and communication.

Memory figures show peak PyTorch allocation, not total GPU memory. Coordinates were simulated and messages were local JSON; camera, GPS, network and Jetson performance were not measured.

Source data: [CSV](/report-assets/computer-vision/architecture_comparison.csv) and <a :href="withBase('/report-assets/computer-vision/architecture_comparison.md')" download>benchmark notes</a>.

### Why Sequential 2 Is Not Selected

Sequential 2 was not selected even though it was faster. When YOLO detects FOD, it skips U-Net and can miss a crack in the same crop.

FAA guidance explains that concrete corner cracks can begin as hairline cracks and deteriorate until pieces come loose. Minor cracks may also need sealing to limit water entry ([CV-S02](../references#cv-s02), pp. 8-9). FAA research links crack-related spalling to loose pieces that can become FOD ([CV-S01](../references#cv-s01)).

This supports keeping the crack check for every anomalous crop in Parallel and Sequential 1. It does not mean every tiny crack is an immediate hazard. Small-crack detection at the intended 5 m flight height still needs testing.

<CvFigure n="7" />

### Explore the Inspection Pipeline

<PipelineDemo />

## PatchCore Anomaly Detection {#patchcore-anomaly-detection}

### What Is PatchCore?

PatchCore is used as the first stage because it identifies anomalies such as cracks and objects. We use it instead of running YOLO and the crack model continuously on each frame, which is computationally heavy. It allows these models to be skipped when no anomaly is found. The overall resource use still needs testing on Jetson.

PatchCore learns visual characteristics of a normal runway or road surface. It doesn't need to learn any specific FOD categories. During operation, if the obtained image region differs from the learned normal appearance, it generates high anomaly scores accordingly. The essential overview of this model is shown in the figure below.

<CvFigure n="8" />

### PatchCore in the Project

PatchCore produces an image-level anomaly score and a heatmap showing the unusual areas. Heatmap images are produced and stored in every run for visual inspection if necessary. A bounding box is then generated to identify the anomaly. The image is then cropped and resized to the normal model input size before passing it to YOLO and U-Net.

<div class="cv-figure-grid">
<CvFigure n="9" />

<CvFigure n="10" />

<CvFigure n="11" />
</div>

PatchCore also serves as a fallback mechanism for previously unseen objects. If PatchCore detects an anomaly that is unrecognised by either YOLO or U-Net (crack detector), the system can store it as an unknown anomaly and send it to the base station for further investigation.

### Dataset and Test Results

The dataset was collected at the NUS test ground outside Techno, at the roundabout.

<CvFigure n="12" />

At 1 m height, PatchCore detected anomalies in 10/10 tests. Testing at 5 m is pending. The system used the bounding boxes to crop the regions and send them to YOLO and the crack model.

<CvFigure n="13" />

## YOLO FOD Detection & Dataset Development {#yolo-fod-detection}

### FOD Classes and Dataset

The YOLO object detector is trained on 32 classes: 31 objects and a water puddle, as shown in the figure below. Data preparation is one of the most challenging parts of this system. We sourced the FOD dataset from Kaggle online. It included more than 31 classes, and we added the water puddle class to meet our requirements. The dataset has 33,793 images but lacks weather variations such as cloudy, rainy, or hazy conditions. The FOD background also appears to be a very light surface that doesn't resemble the dark road surface we require.

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

For this dataset, synthetic compositing helped with the background surface and automatic labelling after creating new artificial data to reduce time consumption.

| Challenge | Solution |
| --- | --- |
| Limited real FOD examples | Generate additional training samples |
| Small FOD objects (1 cm) | Adjust object scaling for different sizes |
| Limited variation in object orientation | Apply rotations |
| Model struggles on the actual test ground | Collect and use the target background |
| Manual labelling is time-consuming | Generate labels automatically from object placement |

### YOLO Detection Outputs

YOLO is responsible for identifying known FOD categories from the classes above. For each detected object, it returns the object class, confidence score and bounding-box coordinates. The cropped anomaly is resized so that small objects like nuts and nails are identified easily.

<div class="cv-figure-grid">
<CvFigure n="23" />

<CvFigure n="24" />
</div>

### YOLO Training Settings

Training was performed on HPC. The YOLO FOD models were trained using the following settings. The same settings were used for the thermal detection models.

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

### Ground Testing and Second Iteration

<CvFigure n="26" />

The model was performing very poorly, and the test object was detected inconsistently. In a 2nd iteration, instead of using different road surface images to generalise, I used only test-ground road surface for the synthetic compositing. The performance improved as shown below in the figure, but it was still not up to standard.

<CvFigure n="27" />

In ground testing, YOLO detected the battery in 3/10 tests and the plastic part in 7/10 tests.

### Dataset Investigation

The dataset was then investigated, and it was hypothesised that there was data leakage happening. Based on visual inspection, moving image by image, each FOD in the dataset was recorded as a video and sliced to generate the images. Hence, when a random split was performed above, the near-identical consecutive frames were placed across all the splits (training, testing and validation). This could explain the abnormally high YOLO results despite poor performance on the actual test ground.

I applied two similarity detection techniques to check for data leaks and reduce them. Perceptual hash identifies near-duplicate images by comparing their visual structure, while DINOv2 uses pretrained deep learning to identify similar features. Both techniques are combined to group strongly similar images and assign them to a single split.

Images are flagged as similar when either of the following conditions is met:

$$
(s_{\mathrm{DINOv2}} \geq 0.99)\quad\lor\quad
\left[(d_{\mathrm{pHash}} \leq 6)\land(s_{\mathrm{DINOv2}} \geq 0.97)\right]
$$

### Similarity-Aware Splitting

| Metric | Random split | Similarity-aware split |
| --- | ---: | ---: |
| Total images analysed | 33,793 | 33,793 |
| Strongly similar pairs crossing splits | 51,361 | 0 |
| Similarity groups crossing splits | 4,471 | 0 |
| Images involved in strong similarity relationships | 25,838 | 25,838 |
| Strong pair constraints identified | 110,605 | 110,605 |
| Related images kept in the same split | No | Yes |

### Dataset Variants

Three datasets were created: one was the random split, the second was the similarity split, and the third was the similarity split plus removal of redundant images.

| Dataset | Images | Main purpose |
| --- | ---: | --- |
| Random baseline | 33,793 | Baseline split; may contain similarity leakage and inflated performance |
| Strict | 33,793 | Keep all images while grouping strongly similar frames into the same split |
| Strict-reduced | 29,663 | Group similar frames and remove 4,130 redundant images |

### Results and Discussion

The lower mAP after similarity-aware splitting is consistent with the data leakage concern. However, removing similar images does not resolve the other dataset limitations. The images were taken at a low height, while we require images at 5 m. During synthetic compositing, precision and recall can be affected, as realistic lighting, scale, shadow and blur are hard to tune. Hence, the current FOD dataset will be replaced with a new dataset collected at the intended height and test ground. The results below document the earlier development work.

The earlier random-split model comparison reported mAP@50-95 values of 92.37% to 93.39% across six models. The strict-split results below are from separate runs; they are not a controlled comparison using a confirmed matching model and training setup.

| Dataset | Reported mAP@50-95 | Interpretation |
| --- | ---: | --- |
| Strict | 88.10% | All images retained with similarity-aware grouping |
| Strict-reduced | 88.93% | Similarity-aware grouping with redundant images removed |

## Crack Detection Using U-Net {#crack-detection}

### Crack Segmentation Approach

The crack dataset is obtained from [Mendeley Data: CrackAirport, version 1](https://data.mendeley.com/datasets/3v5r2fxf89/1). See [CV-D01 in References](../references#cv-d01) for the crack dataset citation.

Runway and road cracks are essentially different from the normal FOD objects. Cracks are usually thin, long and irregular, so segmentation is used to identify their shape at pixel level.

Therefore, we use a U-Net segmentation model. The cropped anomaly region is resized to 512 x 512 and fed into the U-Net, as this is the input size used in this implementation. The model then produces a pixel-level crack mask.

<div class="cv-figure-grid">
<CvFigure n="32" />

<CvFigure n="33" />

<CvFigure n="34" />
</div>

### On-the-Ground Results

<CvFigure n="35" />

On smooth roads, U-Net detected cracks in 10/10 tests. On the rough road, it made 2/10 correct crack/no-crack decisions. It often mistook the rough texture for cracks. Training data from similar rough surfaces is needed. A synthetic method may be used by adding artificial cracks to images of the test ground in the training dataset, but mimicking real-world cracks remains a challenge.

## FOD & Crack Coordinate Retrieval {#coordinate-retrieval}

### Drone Position and Quaternion Worked Example

A quaternion gives orientation, not position. The navigation system must provide both. ROS 2 stores them separately in a pose message ([CV-N01](../references#cv-n01)). The following values are an example, not measured flight data.

<div class="cv-supporting-evidence pose-worked-example">

#### Step 1: Given navigation data

Assume a level drone, a flat runway, and position already expressed in the shared map frame. The quaternion rotates the drone's body axes into that frame. ROS body axes are X forward, Y left and Z up ([CV-N02](../references#cv-n02)).

$$
\mathbf{p}_{\mathrm{UAV}}=(p_x,p_y,p_z)=(3,4,5)\ \mathrm{m}
$$

The quaternion uses ROS ordering $(q_x,q_y,q_z,q_w)$ and has unit length:

$$
q=\left(0,0,\frac{1}{\sqrt{2}},\frac{1}{\sqrt{2}}\right)
\approx(0,0,0.7071,0.7071)
$$

#### Step 2: Read the current drone X and Y

Take these from the position fields, not the quaternion:

$$
X_{\mathrm{UAV}}=p_x=3\ \mathrm{m},\qquad
Y_{\mathrm{UAV}}=p_y=4\ \mathrm{m}
$$

So the current drone position is **(3 m, 4 m)** in this map frame. A quaternion alone cannot provide these coordinates.

#### Step 3: Calculate heading from the quaternion

For a unit quaternion, away from the pitch singularity:

$$
\psi=\operatorname{atan2}\left(
2(q_wq_z+q_xq_y),\ 1-2(q_y^2+q_z^2)
\right)
$$

Substitute the exact quaternion values:

$$
\psi=\operatorname{atan2}(1,0)
=\frac{\pi}{2}\ \mathrm{rad}=90^\circ
$$

The drone is at **(3 m, 4 m)** with a heading of **90 degrees**. Changing its heading does not by itself change its position.

#### Step 4: Use heading when locating FOD

Suppose the image-to-ground calculation gives an offset of **0.20 m forward and 0.10 m left**, already converted into the drone's body axes. This is a separate illustrative offset, not a raw pixel measurement.

$$
\begin{bmatrix}\Delta X\\\Delta Y\end{bmatrix}
=
\begin{bmatrix}
\cos\psi&-\sin\psi\\
\sin\psi&\cos\psi
\end{bmatrix}
\begin{bmatrix}0.20\\0.10\end{bmatrix}
$$

At $\psi=90^\circ$:

$$
\begin{bmatrix}\Delta X\\\Delta Y\end{bmatrix}
=
\begin{bmatrix}0&-1\\1&0\end{bmatrix}
\begin{bmatrix}0.20\\0.10\end{bmatrix}
=
\begin{bmatrix}-0.10\\0.20\end{bmatrix}\ \mathrm{m}
$$

Add the drone's map position:

$$
\begin{aligned}
X_{\mathrm{FOD}}&=3+(-0.10)=2.90\ \mathrm{m}\\
Y_{\mathrm{FOD}}&=4+0.20=4.20\ \mathrm{m}
\end{aligned}
$$

**Drone position: (3.00 m, 4.00 m). FOD position: (2.90 m, 4.20 m).**

This yaw-only example assumes roll and pitch are zero. The planned gimbal will aim to keep the RGB camera pointing down as the drone tilts. With a tilted drone, coordinate retrieval must use the actual camera orientation from the drone attitude and gimbal angles; stabilisation alone does not make the drone body frame level. Full integration still needs camera calibration, camera-to-body axis mapping, matching timestamps and a common navigation frame. PX4 NED data must be converted to the chosen ROS frame before using these equations.

</div>

### Coordinate Retrieval Example

Suppose an original image size is 1280 x 720. The first PatchCore layer detects an anomalous region and bounds it. (x1,y1,x2,y2) = (400,200,700,500) is a bounded region in this case. Hence, the anomaly crop is 300 x 300. This crop will be resized before going to the other 2 models.

<CvFigure n="36" />

## ARGUS's Additional Vision Safety Feature {#thermal-safety}

Alongside runway inspection, ARGUS uses a separate thermal detection pipeline to monitor potential obstacles.

### Thermal Detection for Safety

The thermal detection layer was implemented as a safety layer in addition to obstacle avoidance. The LIDAR mounted can only detect obstacles at the height the drone is flying, leaving the road below outside its scanning plane. The thermal camera is used instead of a secondary RGB camera as it can operate in poor lighting.

<CvFigure n="37" />

Hence, the thermal camera is mounted along with the RGB camera below, pointed at an approximate angle of 45 degrees. This camera is positioned such that it will detect the area ahead on the road for potential obstacles such as people, birds and other heat emitters. If a thermal object is detected, the system is intended to stop and hold until the obstacle is cleared or gone, which reduces the risk of collision. This thermal sub-system operates independently from the RGB FOD detection pipeline. In the current prototype, it's simulated in software for testing, and some results are shown below.

<CvFigure n="38" />

### Thermal Datasets and Training Settings

The thermal detection models used the following datasets:

- [Thermal Bird, version 6, Roboflow Universe](https://universe.roboflow.com/arc-ejbpg/thermal-bird/dataset/6) - [CV-D03 in References](../references#cv-d03).
- [Thermal Images for Human Detection, Kaggle](https://www.kaggle.com/datasets/sikdermdsaiful/thermal-images-for-human-detection/data?select=dataset) - [CV-D04 in References](../references#cv-d04).

The thermal models used the [same training settings as the YOLO FOD models](#yolo-training-settings).

### Thermal Model Comparison

Different YOLO versions were tested as shown in the table below. The thermal model comparison shows greater variance across models. YOLO11m achieved the highest mAP@50-95, while YOLOv8s achieved the highest mAP@50 at 97.70%. YOLO11L achieved the highest recall at 95.38%, meaning it detected the largest proportion of thermal targets, even though it had the lowest precision. Since this detection serves as a safety layer for detecting people, birds, and potential obstacles, recall is important, as missing an obstacle is more critical than occasional false detections. Therefore, the final model should be chosen based on detection accuracy and reliable real-time performance onboard the UAV.

| Model | Precision | Recall | mAP@50 | mAP@50-95 |
| --- | ---: | ---: | ---: | ---: |
| YOLOv8s | 95.25% | 93.52% | 97.70% | 70.88% |
| YOLOv8m | 94.33% | 83.87% | 91.93% | 66.14% |
| YOLOv8L | 88.60% | 89.54% | 94.14% | 68.56% |
| YOLO11s | 95.46% | 93.69% | 96.80% | 70.88% |
| YOLO11m | 96.22% | 89.45% | 96.05% | 71.27% |
| YOLO11L | 88.00% | 95.38% | 95.46% | 69.36% |

### Thermal Camera Selection

This thermal camera provides the wide field of view needed for forward safety monitoring while remaining compact and lightweight. The camera uses a 256 x 196 thermal sensor with a 4 mm F/1.1 lens and a 45.5 degrees x 33.5 degrees field of view. This ensures a large area is monitored for people, birds and possibly other potential obstacles. The module operates at 25 Hz and supports interfaces such as MIPI and USB 2.0. It has a low power consumption, making it suitable for drone use.

<CvFigure n="40" />

## System Integration & Evaluation {#integration-evaluation}

### Overall Integrated System

The first integrated system used the sequential fallback architecture. It ran on the laptop but showed visible lag, as seen in the video below. All three architectures were later benchmarked. Further testing will be done on the Jetson NX.

These were preliminary functional checks using sample objects, including a battery. Formal testing against the subsystem requirements has not yet been conducted.

### Sequential Integration Demonstration

<figure class="cv-video-panel">
 <video v-if="integrationDemo.available" class="cv-integration-video" controls playsinline preload="none" :src="withBase(integrationDemo.src)" aria-label="Laptop demonstration of the sequential CV fallback architecture">
  Your browser does not support embedded video. <a :href="withBase(integrationDemo.src)">Open the demonstration video</a>.
 </video>
 <div v-else class="cv-video-pending" role="status"><span>INTEGRATION DEMO</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video CV-01</strong><span>Laptop demonstration of the integrated system running the sequential fallback architecture, showing visible processing lag.</span></figcaption>
</figure>

### Laptop Setup and Test Conditions

| Item | Test condition |
| --- | --- |
| Processor | AMD Ryzen 9 7845HX |
| GPU | NVIDIA GeForce RTX 4060 Laptop GPU; 8.00 GiB VRAM |
| System memory | 15.21 GiB RAM |
| Software | Python environment `fod_synthetic`; PyTorch 2.11.0+cu128; CUDA build 12.8 |
| RGB inputs | 30 images: 10 each at 300 x 300, 512 x 512 and 3024 x 4032 |
| Thermal inputs | 30 images: 15 each at 1280 x 1024 and 640 x 480 |
| Inference settings | Batch size 1; float32; models warmed up before measured processing |
| Repetitions | Three passes over the same RGB inputs: 90 frame observations per architecture; 84 YOLO calls; 84 U-Net calls for Parallel and Sequential 1, and 30 for Sequential 2 |
| Timing boundary | Already-loaded images; excludes model loading, live capture, GUI display and result-file writing |

All three used the same inputs, weights and settings. Sequential 1 was tested later; background activity and different message routing may affect the comparison.

### Measured Processing and Inference Results

The results below use the laptop setup and test conditions listed above. This table shows how long each model or complete pipeline takes to process an image or crop. Individual-model timings are from the earlier tests; the three pipeline timings are from the architecture comparison using 30 RGB images, each processed three times.

| Configuration | Mean processing time (ms) | P95 processing time (ms) | Mean forward inference time (ms) | Processing throughput | Unit |
| --- | ---: | ---: | ---: | ---: | --- |
| PatchCore | 33.03 | 48.95 | 21.52 | 30.28 frames/s | Full frame |
| YOLO FOD | 27.62 | 51.01 | 19.82 | 36.20 crops/s | Anomaly crop |
| Crack U-Net | 27.81 | 30.97 | 14.56 | 35.96 crops/s | Anomaly crop |
| Thermal YOLO11s | 36.39 | 48.35 | 30.96 | 27.48 frames/s | Full frame |
| Parallel RGB pipeline | 87.34 | 189.06 | Not measured separately | 11.45 frames/s | Full frame |
| Sequential 1 RGB pipeline | 99.19 | 234.20 | Not measured separately | 10.08 frames/s | Full frame |
| Sequential 2 RGB pipeline | 72.87 | 174.76 | Not measured separately | 13.72 frames/s | Full frame |

Processing time includes preparing the input, running the model and processing its output. Forward inference time covers the model alone. Each complete pipeline was timed directly. P95 means 95% of the measured processing times were at or below that value.

PatchCore produced 28 crops from 16 RGB images. The other 14 images had no valid crops, so YOLO and U-Net were skipped. Frames with more crops take longer to process. Thermal was tested separately and is not included in the RGB pipeline timings. All runs completed without processing failures.

### Architecture Workload and Result Routing

This table uses the same architecture comparison described above: 30 RGB images processed three times, giving 90 frame observations per architecture. The counts show how many times YOLO, U-Net and coordinate extraction ran, and how many simulated messages were generated for the UGV and base station. Median is the middle processing time; Max is the longest recorded time.

| Architecture | YOLO calls | U-Net calls | Coordinate calls / UGV messages | Base messages | Median (ms/frame) | Max (ms/frame) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Parallel | 84 | 84 | 54 / 54 | 72 | 72.36 | 236.97 |
| Sequential 1 | 84 | 84 | 54 / 54 | 84 | 80.43 | 306.70 |
| Sequential 2 | 84 | 30 | 54 / 54 | 30 | 59.34 | 222.85 |

Sequential 2 made 30 crack-model calls, compared with 84 for each of the other architectures. It is faster partly because it skips these checks.

These are laptop processing rates, not camera capture rates. Live capture, display and thermal integration may add delays. Detection accuracy under the intended operating conditions, night operation and performance on the Jetson still need to be tested.

### Overall Onboard Architecture

<CvFigure n="41" />

### Requirements and Test Status

| Requirement | Evidence so far | Still to test |
| --- | --- | --- |
| Detect FOD as small as 1 cm | YOLO: battery 3/10; plastic part 7/10. Detection of 1 cm FOD is not yet verified. | Verify 1 cm FOD detection at 5 m height |
| Detect visible surface cracks | Smooth road: 10/10 crack detections. Rough road: 2/10 correct decisions; texture mistaken for cracks. | Reduce rough-surface false detections and measure crack detection performance at 5 m |
| Detect water puddles | Water puddle class added to the FOD dataset | Define the puddle size target and test real puddles |
| Extract coordinates | Worked example and simulated coordinate calculations | Measure real position error using camera and navigation data |
| Run the integrated system | Laptop demonstration and three-architecture benchmarks | Test the full pipeline on Jetson NX |
| Select a suitable camera | RGB camera proposed; webcam used for interim testing | Confirm camera selection and test at the intended height |
| Day and night operation | Ground tests and proposed lighting | Test detection in daylight and at night with the light fitted |

## Semester 2 Development Plan {#semester-2-development-plan}

### CV System Future Works

- Replace the current FOD dataset with a new dataset taken 5 m above the test ground using the RGB camera. Keep training and test capture sessions separate.
- Add FOD items to the test ground and collect a dataset to increase YOLO robustness and reduce reliance on synthetic images.
- Test how often PatchCore misses FOD or cracks at 5 m, extending the current 1 m tests.
- Reduce U-Net false detections on rough surfaces using suitable training data, including crack-free test-ground images. Evaluate crack recall, Dice/IoU and false detections on separate test images.
- Verify 1 cm FOD detection through the full pipeline at 5 m and 15 km/h, during daylight and night operation. Test the selected lens, exposure settings and light.
- Define target detection performance, the puddle size target and acceptable coordinate error. Test real puddles and measure coordinate error using camera calibration, navigation data and gimbal angles.
- Complete system integration using Jetson NX following the pipeline.
- Test both RGB and thermal cameras with the models.
- Add and test a gimbal for the RGB inspection camera, using flight controller attitude data to compensate for tilt and maintain a nadir view. Include the gimbal angles in coordinate retrieval.
- Attach and test the light below the drone near the RGB camera for night operation.
- Implement the link between the cameras and the vision system in Jetson NX.
- Send current drone coordinates from ROS 2 navigation to the vision system.
- Link thermal detection to the flight controller for emergency stops.
- Set up a program to prevent repeated FOD coordinates from being sent (work with the UGV side).
- Test the latency for each model and the entire integrated system on Jetson alongside navigation and communication. Check that captured frames do not build up in a processing queue.

</div>
