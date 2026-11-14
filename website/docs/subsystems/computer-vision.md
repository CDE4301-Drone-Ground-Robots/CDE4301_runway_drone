---
title: Computer Vision Based Inspection and Safety System
outline: [2, 2]
prev: false
next: false
aside: false
pageClass: subsystem-report-page
---

<script setup>
import { withBase } from 'vitepress'
import { data as integrationDemo } from '../cv-integration-demo.data'
</script>

<div class="cv-report rubric-report" style="--report-chapter: '4'">

<p class="chapter-kicker">FOD ARGUS / COMPUTER VISION &amp; SAFETY</p>

# 4. Computer Vision Based Inspection and Safety System {#computer-vision-based-inspection-and-safety-system}

<SubsystemLead class="cv-report-byline" name="Charansagar Ramanujam" matric="A0301658E" portrait="/team/Charan.png" />

## 4.1 Objective and Requirements {#a1-objective-scope-context}

<span id="executive-summary" class="report-anchor" aria-hidden="true"></span>

The computer vision system was developed to enable the UAV to autonomously inspect runway surfaces for FOD (Foreign Object Debris), water puddles, surface cracks, and other common objects. A key challenge in this system is the impracticality of obtaining every possible object that can appear on the runway for the training dataset. A supervised object detector can identify its trained classes, but may not recognise unseen objects.

To address the limitation of detecting only objects seen in the training dataset, we adopted a multi-stage computer vision architecture. The RGB camera is used for primary runway inspection. Interim testing used the UGREEN webcam and a laptop. The final cameras, 5 m setup, Jetson deployment and live navigation link are proposed work.

<span id="subsystem-overview" class="report-anchor" aria-hidden="true"></span>

### 4.1.1 Requirements of This Subsystem {#requirements-of-this-subsystem}

- Detect FOD as small as 1 cm.
- Detect visible surface cracks.
- Detect water puddles.
- Coordinate extraction.
- Design an integrated system.
- Suitable camera selection.
- Day and night operations.

Although the earlier research mentioned a 3 cm FOD target, I set a stricter requirement of detecting objects as small as 1 cm. This provides a safety margin when detecting 3 cm FOD. Since missed FOD can endanger aircraft and people, I chose this requirement to reduce the risk of missed detections. Detection at both sizes will need to be verified under the intended operating conditions.

## 4.2 Vision Methodology and Architecture Development {#a2-methodology-concept-development}

### 4.2.1 ARGUS Camera View {#argus-camera-view}

<CvFigure number="81" n="2" />

In the proposed setup, the RGB camera will face down and be centred on ARGUS. The intended camera view covers a 2 m × 2 m area at a height of 5 m. A suitable lens is needed to achieve this coverage. A gimbal is planned for the RGB inspection camera, using attitude data from the flight controller to compensate for drone roll and pitch and keep the camera pointing straight down (nadir). Adding and testing this gimbal is future work. This setup is intended to simplify training-data collection and FOD coordinate extraction.

### 4.2.2 RGB Cameras {#rgb-cameras}

<CvFigure number="82" n="3" />

The RGB camera proposed for the final drone is the e-con e-CAM56_CUONX as shown in the figure above. The camera is a global-shutter camera that runs at 79 fps. The selection is not final and may change once the RSAF budget is approved. It may be changed to an IDS camera which has a higher resolution and a global shutter as well. In the interim, we used the UGREEN-CM831 webcam for model testing and evaluation.

Manufacturer product page: [e-con Systems e-CAM56_CUONX - Sony IMX568 global-shutter camera](https://www.e-consystems.com/nvidia-cameras/jetson-orin-nx-cameras/5mp-imx568-global-shutter-camera.asp). See [\[57\]](../references#cv-h01). IDS alternative: [U3-31L1ACP Rev.1.2](https://en.ids-imaging.com/store/u3-31l1acp-rev-1-2.html), [\[58\]](../references#cv-h02).

### 4.2.3 RGB Camera Calculation for 1 cm FOD {#rgb-camera-calculation-for-1-cm-fod}

::: details 4.2.3.1 UGREEN CM831 Calculation at 1 m Height (Interim)

The UGREEN CM831 was used for interim testing at **1 m height** ([\[59\]](../references#cv-h03)). The integration script requests **1280 x 720 pixels**. Using the stated whole-image coverage of **0.5 m x 0.5 m**:

$$
W=L=500\ \mathrm{mm}
$$

$$
\mathrm{GSD}_x=\frac{500}{1280}=0.390625\ \mathrm{mm/pixel},\qquad
\mathrm{GSD}_y=\frac{500}{720}\approx0.694444\ \mathrm{mm/pixel}
$$

For a **1 cm x 1 cm object**:

$$
n_x=\frac{10}{0.390625}=25.6\ \mathrm{pixels},\qquad
n_y=\frac{10}{0.694444}=14.4\ \mathrm{pixels}
$$

The object would span about **26 x 14 pixels before resizing**. This calculation uses the stated ground coverage, with separate horizontal and vertical scales. The coverage and image mapping need checking against a measured ground target.

:::

::: details 4.2.3.2 e-CAM56_CUONX Calculation at 5 m Height (Proposed Final Setup)

The requirement is to detect FOD as small as **1 cm at a flight height of 5 m**. The e-CAM56_CUONX has 2472 × 2064 active pixels. The supplied lens has a horizontal field of view of 85.64° and a vertical field of view of 72.25° ([\[57\]](../references#cv-h01)).

Assume the camera faces straight down over flat ground. Using an ideal pinhole approximation, the ground coverage is:

$$
W=2H\tan\left(\frac{\theta_H}{2}\right)
=2(5)\tan(85.64^\circ/2)\approx9.27\ \mathrm{m}
$$

$$
L=2H\tan\left(\frac{\theta_V}{2}\right)
=2(5)\tan(72.25^\circ/2)\approx7.30\ \mathrm{m}
$$

<p class="report-table-caption" id="table-47"><strong>Table 47.</strong> e-CAM56_CUONX Calculation at 5 m Height (Proposed Final Setup)</p>

| Calculation | Horizontal | Vertical |
| --- | ---: | ---: |
| Ground sampling distance | 9266.6 / 2472 = 3.75 mm/pixel | 7298.8 / 2064 = 3.54 mm/pixel |
| Pixels across a 1 cm object | 10 / 3.75 ≈ 2.7 pixels | 10 / 3.54 ≈ 2.8 pixels |

A 1 cm object would span only about 3 pixels at full resolution, so reliable detection is not yet confirmed. Resizing the full frame before anomaly detection can reduce this further. Enlarging a crop cannot recover lost detail.

<span id="lens-needed-for-the-intended-2-m-×-2-m-view" class="report-anchor" aria-hidden="true"></span>

**Lens Needed for the Intended 2 m × 2 m View**

The camera has a 2.74 µm pixel pitch and an M12 lens holder ([\[57\]](../references#cv-h01)). Its active sensor height is:

$$
S_y=2064\times0.00274=5.65536\ \mathrm{mm}
$$

For a 2 m vertical ground coverage at 5 m above the surface, the required focal length is approximately:

$$
f=\frac{H S_y}{L}
=\frac{5000\times5.65536}{2000}
=14.14\ \mathrm{mm}
$$

A **14 mm M12 lens** is therefore a candidate, provided it supports the camera's 1/1.8-inch sensor and can focus at 5 m. The lens requirement is calculated, but the lens model is not confirmed.

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

The selected lens, distortion, focus, motion blur, lighting and model performance still need testing with real 1 cm FOD at 5 m. The coverage above is an estimate, not a calibrated measurement.

ARGUS is intended to fly at 15 km/h. Short exposure times will be needed to limit motion blur. Camera settings and processing performance will be tested on Jetson after the interim stage.

At 5 m, a 1 cm x 1 cm object spans about **10 x 10 pixels** with this camera and the proposed lens. This may be too small for the current PatchCore setup to detect reliably after resizing the full image. The proposed PatchCore modification uses overlapping tiles, as explained in [Section 4.6.1.2](#patchcore-5m-plan) under Future Works.

:::

::: details 4.2.3.3 IDS U3-31L1ACP Calculation at 5 m Height (Proposed Final Setup)

The IDS U3-31L1ACP has **4128 x 3008 pixels**, a **2.74 micrometre pixel pitch** and a **1/1.1-inch sensor** ([\[58\]](../references#cv-h02)). Use the same requirement: **1 cm FOD, 5 m height and a 2 m x 2 m view**. Assume a level camera pointing down at flat ground.

**1. Calculate the sensor size**

$$
S_x=4128(0.00274)=11.31072\ \mathrm{mm},\qquad
S_y=3008(0.00274)=8.24192\ \mathrm{mm}
$$

**2. Find the lens needed for 2 m vertical coverage**

$$
f=\frac{H S_y}{L}
=\frac{5000(8.24192)}{2000}
=20.6048\ \mathrm{mm}
$$

With this focal length, a centred **3008 x 3008 pixel crop** covers **2 m x 2 m** without stretching the image.

$$
\mathrm{GSD}=\frac{2000}{3008}=0.6649\ \mathrm{mm/pixel},\qquad
n_{\mathrm{1\,cm}}=\frac{10}{0.6649}\approx15.04\ \mathrm{pixels}
$$

**3. Check a 20 mm lens**

A 20 mm lens is close to the calculated focal length. The lens must cover the 1/1.1-inch sensor, fit the camera's lens mount and focus at 5 m. A lens model has not been selected.

$$
W=\frac{5000(11.31072)}{20}=2827.68\ \mathrm{mm},\qquad
L=\frac{5000(8.24192)}{20}=2060.48\ \mathrm{mm}
$$

The full frame covers **2.83 m x 2.06 m**. A centred **3008 x 3008 pixel crop** covers **2.06 m x 2.06 m**.

$$
\mathrm{GSD}=\frac{2060.48}{3008}=0.685\ \mathrm{mm/pixel},\qquad
n_{\mathrm{1\,cm}}=\frac{10}{0.685}\approx14.60\ \mathrm{pixels}
$$

At 5 m, a 1 cm x 1 cm object spans about **15 x 15 pixels** with this camera and the proposed lens. This may be too small for the current PatchCore setup to detect reliably after resizing the full image. The proposed PatchCore modification uses overlapping tiles, as explained in [Section 4.6.1.2](#patchcore-5m-plan) under Future Works. Actual 1 cm detection still needs testing.

:::

### 4.2.4 Proposed Night Operation Lighting {#night-operation-lighting}

The proposed setup includes a light below the drone, near the RGB camera, that will turn on automatically during night operation to illuminate the inspection surface.

<CvFigure number="83" n="43" />

### 4.2.5 Computer Vision System Architecture - Parallel {#computer-vision-system-architecture-parallel}

The following describes the proposed onboard flow. The model pipeline was tested on a laptop using simulated navigation coordinates and local messages. Live navigation and communication links are pending.

The RGB camera captures images continuously, which then pass through the system. The captured images first enter a PatchCore anomaly detection model. For each captured frame, the system requests the drone's X and Y coordinates and orientation (quaternion) from navigation. Coordinate extraction finds the object's ground offset from the image. Heading from the quaternion aligns this offset with the map before adding the drone's X and Y. If there is no anomaly on the road, it continues the inspection. If an anomalous region is identified, the model produces a bounding box and crops it. The system then sends it to the second layer. The second layer consists of 2 models: a YOLO object detector and a U-Net segmentation model for runway cracks. Both run in parallel. The cropped image is then resized to each model's input size and fed into that model. If any cracks are detected, the system sends them to the base. On the YOLO side, if it detects a FOD object, it performs more localised coordinate extraction and sends the coordinates to the UGV for extraction. If neither the crack detection model nor YOLO identifies it, the system sends it to the base station as it is an anomaly that neither model identifies. The models will be explained in more depth in the later sections. The quaternion-to-heading conversion, 2D rotation and precise FOD coordinate calculations are explained in [FOD & Crack Coordinate Retrieval](#coordinate-retrieval).

The base station is the control room where operators can receive updates from ARGUS or HUNTER and take the necessary actions if required. In the proposed vision system, crack detections and unknown anomalies will be sent there for operator review. The base-station communication link is planned for the final setup.

<CvFigure number="84" n="4" />

### 4.2.6 Computational Workload {#computational-workload}

<p class="report-table-caption" id="table-48"><strong>Table 48.</strong> Computational Workload</p>

| AI function | Model listed in the draft | Arithmetic complexity | Relative workload |
| --- | --- | ---: | ---: |
| Crack segmentation | U-Net | 62.512 GFLOPs | 100% |
| FOD detection | YOLO11s | 55.496 GFLOPs | 88.8% |
| Surface anomaly detection | PatchCore CNN | 23.998 GFLOPs | 38.4% |
| Thermal object detection | Thermal YOLO11s | 21.422 GFLOPs | 34.3% |

Computational workload was estimated across the AI models. Based on the GFLOPs calculated, FOD detection and Crack segmentation are the most computationally demanding tasks. In the parallel architecture above, these models are running in parallel. This is addressed in the next section.

GFLOPs describe the amount of computation. Measured laptop inference times are reported in [Section 4.5: Analysis](#a5-analysis).

### 4.2.7 Computer Vision System Architecture - Sequential 1 (Fallback) {#computer-vision-system-architecture-sequential-1-fallback}

Jetson NX resources may be limited when vision, navigation and communication run together. They would all be competing for GPU resources, memory bandwidth and power. Hence, a fallback architecture was designed for low-resource scenarios. This pipeline runs YOLO and Crack sequentially instead of in parallel, reducing resource consumption. Both models check every crop. This fallback was tested on the laptop and still needs testing on Jetson.

<CvFigure number="85" n="6" />

### 4.2.8 Additional Tested Architecture - Sequential 2 {#additional-tested-architecture-sequential-2}

Sequential 2 is an extra architecture that was tested where YOLO runs first. If FOD is detected, the coordinates are sent to the UGV and ARGUS continues inspection. Otherwise, the crop goes to U-Net for crack detection. This architecture bypasses the crack model whenever YOLO detects FOD. The reason for rejecting it is explained in [Section 4.5: Analysis](#a5-analysis).

<CvFigure number="86" n="42" />

### 4.2.9 PatchCore Anomaly Detection {#patchcore-anomaly-detection}

#### 4.2.9.1 What Is PatchCore? {#what-is-patchcore}

PatchCore is used as the first stage because it identifies anomalies such as cracks and objects. We use it instead of running YOLO and the crack model continuously on each frame, which is computationally heavy. It allows these models to be skipped when no anomaly is found. The overall resource use still needs testing on Jetson.

PatchCore learns visual characteristics of a normal runway or road surface. It doesn't need to learn any specific FOD categories. During operation, if the obtained image region differs from the learned normal appearance, it generates high anomaly scores accordingly. The essential overview of this model is shown in the figure below.

<CvFigure number="87" n="8" />

### 4.2.10 Crack Detection Using U-Net {#crack-detection}

#### 4.2.10.1 Crack Segmentation Approach {#crack-segmentation-approach}

The crack dataset is obtained from [Mendeley Data: CrackAirport, version 1](https://data.mendeley.com/datasets/3v5r2fxf89/1). See [\[60\]](../references#cv-d01) for the crack dataset citation.

Runway and road cracks are essentially different from the normal FOD objects. Cracks are usually thin, long and irregular, so segmentation is used to identify their shape at pixel level.

Therefore, we use a U-Net segmentation model with a ResNet34 encoder. The cropped anomaly region is resized to 512 x 512 and fed into the U-Net, as this is the input size used in this implementation. The model then produces a pixel-level crack mask.

::: details 4.2.10.1.1 How U-Net Uses ResNet34

- **ResNet34 encoder:** Extracts features from the RGB crop at different scales. It uses residual shortcuts that add a block's input to its output, helping deeper networks train ([\[61\]](../references#cv-m02)).
- **U-Net decoder:** Upsamples these features to produce the crack mask. U-Net also passes encoder features to the decoder through skip connections to retain spatial detail. These are separate from the residual shortcuts inside ResNet34 ([\[62\]](../references#cv-m01)).
- **Training:** The training script loads ImageNet-pretrained encoder weights and freezes the encoder parameters. The decoder and segmentation head are trained on the crack dataset using combined Dice and binary cross-entropy losses.
- **Input and output:** A 512 x 512 RGB crop produces a single-channel output. During inference, sigmoid converts this output to pixel probabilities. Values above the default threshold of 0.5 are marked as cracks. The binary mask is resized back to the original crop size.

:::


<div class="cv-figure-grid">
<CvFigure number="88" n="32" />

<CvFigure number="89" n="33" />

<CvFigure number="90" n="34" />

</div>

### 4.2.11 FOD & Crack Coordinate Retrieval {#coordinate-retrieval}

<CvFigure number="91" n="45" />

#### 4.2.11.1 Navigation Data: Drone Position and Heading {#drone-position-and-quaternion-worked-example}

For the proposed navigation link, the vision system will receive the drone's X and Y position and a quaternion describing its orientation ([\[63\]](../references#cv-n01)). The position gives the starting coordinates. Heading from the quaternion is used to rotate the ground offset into map directions.

The example below assumes a level camera pointing down at flat ground. These are example values, not flight measurements.

<div class="cv-supporting-evidence pose-worked-example">

##### 4.2.11.1.1 Step 1: Get the drone position from navigation {#step-1-given-navigation-data}

Assume navigation provides this position in the shared map frame:

$$
\mathbf{p}_{\mathrm{UAV}}=(p_x,p_y,p_z)=(3,4,5)\ \mathrm{m}
$$

<span id="step-2-read-the-current-drone-x-and-y" class="report-anchor" aria-hidden="true"></span>

The drone's starting coordinates are therefore **X = 3 m and Y = 4 m**, at a height of 5 m above the flat ground in this example.

##### 4.2.11.1.2 Step 2: Convert the quaternion to heading {#step-3-calculate-heading-from-the-quaternion}

Using ROS quaternion ordering $(q_x,q_y,q_z,q_w)$, assume:

$$
q=\left(0,0,\frac{1}{\sqrt{2}},\frac{1}{\sqrt{2}}\right)
\approx(0,0,0.7071,0.7071)
$$

For a unit quaternion, away from the pitch singularity:

$$
\psi=\operatorname{atan2}\left(
2(q_wq_z+q_xq_y),\ 1-2(q_y^2+q_z^2)
\right)
=\operatorname{atan2}(1,0)=90^\circ
$$

This gives the drone's heading. Its position remains **(3 m, 4 m)**.

</div>

#### 4.2.11.2 Image-Based Coordinate Extraction {#coordinate-retrieval-example}

##### 4.2.11.2.1 Step 3: Use the bounding box and crop to find the ground offset {#image-to-ground-offset}

Suppose an original image size is 1280 x 720. The first PatchCore layer detects an anomalous region and bounds it. (x1,y1,x2,y2) = (400,200,700,500) is a bounded region in this case. Hence, the anomaly crop is 300 x 300. This crop will be resized before going to the other 2 models.

The calculation below maps the bounding box back to the original image, finds its centre and converts the pixel offset into metres. The quaternion is used after this calculation to correct the direction of the ground offset.

<CvFigure number="92" n="36" />

Use Steps 1-5 in the image to obtain the ground offset: approximately **-0.172 m along image-right and -0.056 m along image-down**. For the rotated-camera example here, replace Step 6 in the image with Steps 4 and 5 below. These apply the heading correction before adding the drone position.

<div class="cv-supporting-evidence pose-worked-example">

##### 4.2.11.2.2 Step 4: Align the ground offset with the map {#step-4-use-heading-when-locating-fod}

For this example, assume the camera is mounted so that image-top points forward and image-right points to the drone's right. ROS body axes are X forward, Y left and Z up ([\[64\]](../references#cv-n02)). The offset from Step 3 becomes:

$$
\begin{aligned}
\Delta x_{\mathrm{body}}&=-\Delta y_{\mathrm{image}}=+0.05556\ \mathrm{m}\\
\Delta y_{\mathrm{body}}&=-\Delta x_{\mathrm{image}}=+0.171875\ \mathrm{m}
\end{aligned}
$$

Use the heading from Step 2 to rotate this offset into the map axes:

$$
\begin{bmatrix}\Delta X\\\Delta Y\end{bmatrix}
=
\begin{bmatrix}
\cos\psi&-\sin\psi\\
\sin\psi&\cos\psi
\end{bmatrix}
\begin{bmatrix}0.05556\\0.171875\end{bmatrix}
$$

At $\psi=90^\circ$:

$$
\begin{bmatrix}\Delta X\\\Delta Y\end{bmatrix}
=
\begin{bmatrix}0&-1\\1&0\end{bmatrix}
\begin{bmatrix}0.05556\\0.171875\end{bmatrix}
=
\begin{bmatrix}-0.171875\\0.05556\end{bmatrix}\ \mathrm{m}
$$

##### 4.2.11.2.3 Step 5: Add the drone position to get the FOD coordinates {#add-drone-position-to-fod-offset}

$$
\begin{aligned}
X_{\mathrm{FOD}}&=3-0.171875\approx2.828\ \mathrm{m}\\
Y_{\mathrm{FOD}}&=4+0.05556\approx4.056\ \mathrm{m}
\end{aligned}
$$

**Drone position: (3.000 m, 4.000 m). FOD position after heading correction: (2.828 m, 4.056 m).**

This combines the image-based extraction with navigation data in one calculation. Full integration is pending. It requires camera calibration, the actual camera-to-body mounting alignment, matching timestamps and a common navigation frame. The planned gimbal will aim to keep the camera pointing down. If the camera is tilted, its full orientation, including the gimbal angles, must be used rather than heading alone. PX4 NED data must be converted to the chosen ROS frame before using these equations.

</div>

### 4.2.12 ARGUS's Additional Vision Safety Feature {#thermal-safety}

A separate thermal detection pipeline is proposed to monitor potential obstacles. YOLO11s with the `Thermal_yolo11s.pt` weights was tested separately on thermal images of people and birds. Live thermal integration is pending.

#### 4.2.12.1 Thermal Detection for Safety {#thermal-detection-for-safety}

The thermal detection layer is proposed as an additional safety feature alongside obstacle avoidance. The LIDAR mounted can only detect obstacles at the height the drone is flying, leaving the road below outside its scanning plane. The thermal camera is used instead of a secondary RGB camera as it can operate in poor lighting.

<CvFigure number="93" n="37" />

The thermal camera is planned to be mounted below the drone at about 45 degrees to view the road ahead. It will be used to detect people and birds. If a target is detected, the proposed response is to stop and hold until the obstacle clears. The thermal pipeline is intended to run separately from RGB inspection. The stop-and-hold response is simulated in the current prototype. Linking it to the flight controller is future work.

The thermal camera is also planned to provide a live feed for manual override. The 1080p live-video requirement applies to the RGB feed. The thermal feed will use the camera’s native resolution. If the drone encounters a problem at night, the operator can use this view to guide ARGUS back. Live-feed integration and testing are future work.

<CvFigure number="94" n="38" />

#### 4.2.12.2 Thermal Camera Selection {#thermal-camera-selection}

The proposed thermal camera has a wide field of view for forward safety monitoring and is compact and lightweight. The camera uses a 256 x 196 thermal sensor with a 4 mm F/1.1 lens and a 45.5 degrees x 33.5 degrees field of view. Its coverage and detection performance still need testing on the drone. The module operates at 25 Hz and supports interfaces such as MIPI and USB 2.0. It has a low power consumption, making it suitable for drone use.

<CvFigure number="95" n="40" />

### 4.2.13 Proposed Overall Onboard Architecture {#overall-onboard-architecture}

This is the overall proposed architecture for the Jetson NX. It may change after the hardware is obtained and the appropriate benchmarks are tested. If the Jetson cannot handle all the systems, a Raspberry Pi will also be used to share the workload.

<CvFigure number="96" n="41" />

## 4.3 Vision Model and Pipeline Implementation {#a3-prototype-development}

### 4.3.1 Software {#software}

These are some of the software tools used in this subsystem to train the model and generate and edit the dataset.

<CvFigure number="97" n="1" />

### 4.3.2 PatchCore in the Project {#patchcore-in-the-project}

For the interim implementation, PatchCore was developed using the Anomalib framework with a WideResNet50-2 backbone to extract features. The model was trained using normal runway surface images, with a coreset sampling ratio of 10% to build a representative memory bank of normal features. During inference, input images were resized to 256 × 256 pixels before being processed by PatchCore. The model generates an anomaly score and an anomaly heatmap. The heatmap is resized and overlaid on the original image for visualisation, as shown in Figs. 98-100. Bounding-box generation and cropping are handled by the integration code for all three architectures.

<div class="cv-figure-grid">
<CvFigure number="98" n="9" />

<CvFigure number="99" n="10" />

<CvFigure number="100" n="11" />
</div>

PatchCore also flags previously unseen objects. If neither YOLO nor U-Net identifies a detected anomaly, it is stored as an unknown anomaly. In the proposed onboard system, it will be sent to the base station for inspection. Current transmission is simulated using local messages.

### 4.3.3 YOLO FOD Detection & Dataset Development {#yolo-fod-detection}

#### 4.3.3.1 FOD Classes and Dataset {#fod-classes-and-dataset}

The YOLO object detector is trained on 32 classes: 31 objects and a water puddle, as shown in the figure below. Data preparation is one of the most challenging parts of this system. We sourced the FOD dataset from Kaggle online. It included more than 31 classes, and we added the water puddle class to meet our requirements. The dataset has 33,793 images but lacks weather variations such as cloudy, rainy, or hazy conditions. The FOD background also appears to be a very light surface that doesn't resemble the dark road surface we require.

Dataset source: [Foreign Object Debris in Airports (FOD-A), Kaggle](https://www.kaggle.com/datasets/kilogrand/foreign-object-debris-in-airports-fod-a-dataset/code). See [\[65\]](../references#cv-d02).

<CvFigure number="101" n="14" />

<CvFigure number="102" n="15" />

#### 4.3.3.2 Synthetic Compositing Method {#synthetic-compositing-method}

Therefore, we implemented synthetic compositing to address the issues above. This method can place FODs artificially on any surface. We synthetically added the FODs to different road surfaces to create a new dataset. We also synthetically generated rain and fog with corresponding YOLO bounding-box annotations. I made them look as realistic as possible by tuning them, as shown in the figure below. This reduces the need to collect many real-world samples.

<div class="cv-figure-grid">
<CvFigure number="103" n="16" />

<CvFigure number="104" n="17" />

<CvFigure number="105" n="18" />

<CvFigure number="106" n="19" />

<CvFigure number="107" n="20" />

<CvFigure number="108" n="21" />
</div>

For this dataset, synthetic compositing helped with the background surface and automatic labelling after creating new artificial data to reduce time consumption. The table below shows the different challenges that the synthetic compositing method can solve.

<p class="report-table-caption" id="table-49"><strong>Table 49.</strong> Synthetic Compositing Method</p>

| Challenge | Solution |
| --- | --- |
| Limited real FOD examples | Generate additional training samples |
| Small FOD objects (1 cm) | Adjust object scaling for different sizes |
| Limited variation in object orientation | Apply rotations |
| Model struggles on the actual test ground | Collect and use the target background |
| Manual labelling is time-consuming | Generate labels automatically from object placement |

#### 4.3.3.3 YOLO Detection Outputs {#yolo-detection-outputs}

YOLO is responsible for identifying known FOD categories from the classes above. For each detected object, it returns the object class, confidence score and bounding-box coordinates. The cropped anomaly is resized so that small objects like nuts and nails are identified easily.

<div class="cv-figure-grid">
<CvFigure number="109" n="23" />

<CvFigure number="110" n="24" />
</div>

#### 4.3.3.4 YOLO Training Settings {#yolo-training-settings}

Training was performed on HPC. The YOLO FOD models were trained using the following settings. The same settings were used for the thermal detection models.

<p class="report-table-caption" id="table-50"><strong>Table 50.</strong> YOLO Training Settings</p>

| Setting | Value |
| --- | ---: |
| Epochs | 100 |
| Batch size | 16 |
| Training split | 80% |
| Validation split | 10% |
| Testing split | 10% |

### 4.3.4 Thermal Datasets and Training Settings {#thermal-datasets-and-training-settings}

The thermal detection models used the following datasets:

- [Thermal Bird, version 6, Roboflow Universe](https://universe.roboflow.com/arc-ejbpg/thermal-bird/dataset/6) - [\[66\]](../references#cv-d03).
- [Thermal Images for Human Detection, Kaggle](https://www.kaggle.com/datasets/sikdermdsaiful/thermal-images-for-human-detection/data?select=dataset) - [\[67\]](../references#cv-d04).

The thermal models used the [same training settings as the YOLO FOD models](#yolo-training-settings).

### 4.3.5 Explore the Inspection Pipeline {#explore-the-inspection-pipeline}

<PipelineDemo />

## 4.4 Vision Model and Integration Testing {#a4-testing}

### 4.4.1 System Integration & Evaluation {#integration-evaluation}

#### 4.4.1.1 Overall Integrated System {#overall-integrated-system}

The first integrated system used the sequential fallback architecture. It ran on the laptop but showed visible lag, as seen in the video below. All three architectures were later benchmarked. Further testing will be done on the Jetson NX.

These were preliminary functional checks using sample objects, including a battery. Formal testing against the subsystem requirements has not yet been conducted.

#### 4.4.1.2 Sequential Integration Demonstration {#sequential-integration-demonstration}

<figure class="cv-video-panel">
 <video v-if="integrationDemo.available" class="cv-integration-video" controls playsinline preload="none" :src="withBase(integrationDemo.src)" aria-label="Laptop demonstration of the sequential CV fallback architecture">
  Your browser does not support embedded video. <a :href="withBase(integrationDemo.src)">Open the demonstration video</a>.
 </video>
 <div v-else class="cv-video-pending" role="status"><span>INTEGRATION DEMO</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video CV-01</strong><span>Laptop demonstration of the integrated system running the sequential fallback architecture, showing visible processing lag.</span></figcaption>
</figure>

### 4.4.2 PatchCore Dataset and Test Results {#dataset-and-test-results}

The dataset was collected at the NUS test ground outside Techno, at the roundabout.

<CvFigure number="111" n="12" />

At 1 m height, PatchCore detected anomalies in 10/10 tests. Testing at 5 m is pending. The system used the bounding boxes to crop the regions and send them to YOLO and the crack model.

<CvFigure number="112" n="13" />

### 4.4.3 YOLO Model Comparison {#model-comparison}

We tested different YOLO versions, as shown in the table below. All achieved very high detection performance, with only small differences. These results were suspiciously high, so we also tested them on the ground.

<p class="report-table-caption" id="table-51"><strong>Table 51.</strong> YOLO Model Comparison</p>

| Model | Precision | Recall | mAP@50 | mAP@50-95 |
| --- | ---: | ---: | ---: | ---: |
| YOLOv8s | 99.69% | 99.20% | 99.15% | 92.37% |
| YOLOv8m | 99.54% | 99.28% | 99.12% | 92.95% |
| YOLOv8L | 99.72% | 99.34% | 99.18% | 93.39% |
| YOLO11s | 99.67% | 99.33% | 99.19% | 92.57% |
| YOLO11m | 99.70% | 99.35% | 99.23% | 92.88% |
| YOLO11L | 99.68% | 99.39% | 99.26% | 93.25% |

### 4.4.4 YOLO Ground Testing and Second Iteration {#ground-testing-and-second-iteration}

<CvFigure number="113" n="26" />

The model was performing very poorly, and the test object was detected inconsistently. In a 2nd iteration, instead of using different road surface images to generalise, I used only test-ground road surface for the synthetic compositing. The performance improved as shown below in the figure, but it was still not up to standard.

<CvFigure number="114" n="27" />

The ground tests used a plastic part, a battery and a pen. The 10 tests used different object placements at different locations along the test ground. YOLO detected the battery in 3/10 tests and the plastic part in 7/10 tests. Further investigation of the dataset was conducted, as discussed in [Section 4.5.4](#dataset-investigation).

### 4.4.5 U-Net On-the-Ground Results {#on-the-ground-results}

<CvFigure number="115" n="35" />

On smooth roads, U-Net detected cracks in 10/10 tests. On the rough road, it made 2/10 correct crack/no-crack decisions. It often mistook the rough texture for cracks. Training data from similar rough surfaces is needed. A synthetic method may be used by adding artificial cracks to images of the test ground in the training dataset, but mimicking real-world cracks remains a challenge.

### 4.4.6 Thermal Model Comparison {#thermal-model-comparison}

YOLO11s is the current thermal model for detecting people and birds. It was also used for the standalone laptop benchmark. The table below compares the tested models. YOLO11m had the highest mAP@50-95, YOLOv8s had the highest mAP@50 at 97.70%, and YOLO11L had the highest recall at 95.38%. Recall matters for this safety system because missed obstacles can cause collisions. The final onboard model will be confirmed after Jetson testing.

<p class="report-table-caption" id="table-52"><strong>Table 52.</strong> Thermal Model Comparison</p>

| Model | Precision | Recall | mAP@50 | mAP@50-95 |
| --- | ---: | ---: | ---: | ---: |
| YOLOv8s | 95.25% | 93.52% | 97.70% | 70.88% |
| YOLOv8m | 94.33% | 83.87% | 91.93% | 66.14% |
| YOLOv8L | 88.60% | 89.54% | 94.14% | 68.56% |
| YOLO11s | 95.46% | 93.69% | 96.80% | 70.88% |
| YOLO11m | 96.22% | 89.45% | 96.05% | 71.27% |
| YOLO11L | 88.00% | 95.38% | 95.46% | 69.36% |

## 4.5 Vision Performance and Dataset Analysis {#a5-analysis}

### 4.5.1 Laptop Benchmark Setup and Test Conditions {#laptop-setup-and-test-conditions}

This is the setup used for the laptop benchmarks below. Ground-detection tests are in Section 4.4.

<p class="report-table-caption" id="table-53"><strong>Table 53.</strong> Laptop Benchmark Setup and Test Conditions</p>

| Item | Test condition |
| --- | --- |
| Processor | AMD Ryzen 9 7845HX |
| GPU | NVIDIA GeForce RTX 4060 Laptop GPU, 8.00 GiB VRAM |
| System memory | 15.21 GiB RAM |
| Software | Python environment `fod_synthetic`, PyTorch 2.11.0+cu128, CUDA build 12.8 |
| RGB inputs | 30 images: 10 each at 300 x 300, 512 x 512 and 3024 x 4032 |
| Thermal inputs | 30 images: 15 each at 1280 x 1024 and 640 x 480 |
| Inference settings | Batch size 1, float32, models warmed up before measured processing |
| Repetitions | Three passes over the same RGB inputs: 90 frame observations per architecture, 84 YOLO calls, 84 U-Net calls for Parallel and Sequential 1, and 30 for Sequential 2 |
| Timing boundary | Already-loaded images, excludes model loading, live capture, GUI display and result-file writing |

All three used the same inputs, weights and settings. Sequential 1 was tested later. Background activity and different message routing may affect the comparison.

### 4.5.2 Architecture Comparison and Memory Use {#architecture-comparison-and-memory-use}

All three architectures used the [laptop setup above](#laptop-setup-and-test-conditions). Full timings are under [Measured Processing and Inference Results](#measured-processing-and-inference-results) in Section 4.5.

<p class="report-table-caption" id="table-54"><strong>Table 54.</strong> Architecture Comparison and Memory Use</p>

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

Memory figures show peak PyTorch allocation, not total GPU memory. Coordinates were simulated and messages were local JSON. Camera, GPS, network and Jetson performance were not measured.

Source data: [CSV](/report-assets/computer-vision/architecture_comparison.csv) and <a :href="withBase('/report-assets/computer-vision/architecture_comparison.md')" download>benchmark notes</a>.

### 4.5.3 Why Sequential 2 Is Not Selected {#why-sequential-2-is-not-selected}

Sequential 2 was the fastest of the three architectures in the laptop benchmark, averaging 72.87 ms per frame (13.72 frames/s). It was not selected because it skips U-Net when YOLO detects FOD and can miss a crack in the same crop.

FAA guidance explains that concrete corner cracks can begin as hairline cracks and deteriorate until pieces come loose. Minor cracks may also need sealing to limit water entry ([\[68\]](../references#cv-s02), pp. 8-9). FAA research links crack-related spalling to loose pieces that can become FOD ([\[69\]](../references#cv-s01)).

This supports keeping the crack check for every anomalous crop in Parallel and Sequential 1. It does not mean every tiny crack is an immediate hazard. Small-crack detection at the intended 5 m flight height still needs testing.

<CvFigure number="116" n="7" />

### 4.5.4 YOLO Dataset Investigation {#dataset-investigation}

Since the YOLO models that gave very high results performed poorly on the test ground, a dataset investigation was conducted.

Data leakage was suspected. Based on visual inspection, moving image by image, each FOD in the dataset was recorded as a video and sliced to generate the images. Hence, when a random split was performed above, the near-identical consecutive frames were placed across all the splits (training, testing and validation). This could explain the abnormally high YOLO results despite poor performance on the actual test ground.

I applied two similarity detection techniques to check for data leaks and reduce them. Perceptual hash identifies near-duplicate images by comparing their visual structure, while DINOv2 uses pretrained deep learning to identify similar features. Both techniques are combined to group strongly similar images and assign them to a single split.

Images are flagged as similar when either of the following conditions is met:

$$
(s_{\mathrm{DINOv2}} \geq 0.99)\quad\lor\quad
\left[(d_{\mathrm{pHash}} \leq 6)\land(s_{\mathrm{DINOv2}} \geq 0.97)\right]
$$

### 4.5.5 YOLO Similarity-Aware Splitting {#similarity-aware-splitting}

<p class="report-table-caption" id="table-55"><strong>Table 55.</strong> YOLO Similarity-Aware Splitting</p>

| Metric | Random split | Strict |
| --- | ---: | ---: |
| Total images analysed | 33,793 | 33,793 |
| Strongly similar pairs crossing splits | 51,361 | 0 |
| Similarity groups crossing splits | 4,471 | 0 |
| Images involved in strong similarity relationships | 25,838 | 25,838 |
| Strong pair constraints identified | 110,605 | 110,605 |
| Related images kept in the same split | No | Yes |

The original splits contained 51,361 strongly similar image pairs across the training, validation and test sets. The dataset was re-split so that similar images stayed in the same set. This split was named Strict to reduce data leakage and give a fairer test of the model.

### 4.5.6 YOLO Results and Discussion {#results-and-discussion}

Both Kaggle dataset results below used YOLOv8L: the original random split and the Strict similarity-aware split.

<p class="report-table-caption" id="table-56"><strong>Table 56.</strong> YOLO Results and Discussion</p>

| Dataset | Reported mAP@50-95 | Interpretation |
| --- | ---: | --- |
| Original Kaggle dataset (random split) | 93.39% | Best result from the six YOLO models tested (YOLOv8L) |
| Strict (Original Kaggle dataset) | 88.10% | All images retained, with similar images kept in the same split |

The lower mAP after Strict splitting supports the concern about data leakage. However, re-splitting does not fix the other dataset limitations. The images were taken at a low height, while we require images at 5 m. Synthetic images can also differ from real images in lighting, scale, shadows and blur. The current FOD dataset will therefore be replaced with a new dataset collected at the intended height and test ground.

### 4.5.7 Measured Processing and Inference Results {#measured-processing-and-inference-results}

The results below use the [laptop benchmark setup and test conditions](#laptop-setup-and-test-conditions) listed above. This table shows how long each model or complete pipeline takes to process an image or crop. Individual-model timings are from the earlier tests. The three pipeline timings are from the architecture comparison using 30 RGB images, each processed three times.

<p class="report-table-caption" id="table-57"><strong>Table 57.</strong> Measured Processing and Inference Results</p>

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

### 4.5.8 Architecture Workload and Result Routing {#architecture-workload-and-result-routing}

Each architecture processed the same 30 RGB images three times, giving 90 frame observations. The table counts the YOLO, U-Net and coordinate extraction calls, along with simulated messages to the UGV and base station. Median is the middle processing time. Max is the longest recorded time.

<p class="report-table-caption" id="table-58"><strong>Table 58.</strong> Architecture Workload and Result Routing</p>

| Architecture | YOLO calls | U-Net calls | Coordinate calls / UGV messages | Base messages | Median (ms/frame) | Max (ms/frame) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Parallel | 84 | 84 | 54 / 54 | 72 | 72.36 | 236.97 |
| Sequential 1 | 84 | 84 | 54 / 54 | 84 | 80.43 | 306.70 |
| Sequential 2 | 84 | 30 | 54 / 54 | 30 | 59.34 | 222.85 |

Sequential 2 made 30 crack-model calls, compared with 84 for each of the other architectures. Skipping these checks partly explains why it was the fastest in this benchmark.

These are laptop processing rates, not camera capture rates. Live capture, display and thermal integration may add delays. Detection accuracy under the intended operating conditions, night operation and performance on the Jetson still need to be tested.

### 4.5.9 Requirements and Test Status {#requirements-and-test-status}

<p class="report-table-caption" id="table-59"><strong>Table 59.</strong> Requirements and Test Status</p>

| Requirement | Evidence so far | Still to test |
| --- | --- | --- |
| Detect FOD as small as 1 cm | YOLO: battery 3/10, plastic part 7/10. Detection of 1 cm FOD is not yet verified. | Verify 1 cm FOD detection at 5 m height |
| Detect visible surface cracks | Smooth road: 10/10 crack detections. Rough road: 2/10 correct decisions. Texture was mistaken for cracks. | Reduce rough-surface false detections and measure crack detection performance at 5 m |
| Detect water puddles | Water puddle class added to the FOD dataset | Define the puddle size target and test real puddles |
| Extract coordinates | Worked example and simulated coordinate calculations | Measure real position error using camera and navigation data |
| Run the integrated system | Laptop demonstration and three-architecture benchmarks | Test the full pipeline on Jetson NX |
| Select a suitable camera | RGB camera proposed. Webcam used for interim testing | Confirm camera selection and test at the intended height |
| Day and night operation | Ground tests and proposed lighting | Test detection in daylight and at night with the light fitted |

## 4.6 Discussion of Future Works {#a6-problems-project-plan}

### 4.6.1 Semester 2 Development Plan {#semester-2-development-plan}

<span id="cv-system-future-works" class="report-anchor" aria-hidden="true"></span>

::: details 4.6.1.1 FOD Dataset and Crack Model Training

- **Collect a new dataset:** Replace the current FOD dataset with a new dataset taken 5 m above the test ground using the RGB camera. Keep training and test capture sessions separate.
- **Capture real FOD objects:** Add FOD items to the test ground and collect a dataset to increase YOLO robustness and reduce reliance on synthetic images.
- **Train for rough surfaces:** Reduce U-Net false detections on rough surfaces using suitable training data, including crack-free test-ground images. Evaluate crack recall, Dice/IoU and false detections on separate test images.

:::

<span id="patchcore-5m-plan" class="report-anchor" aria-hidden="true"></span>

::: details 4.6.1.2 PatchCore for 1 cm FOD at 5 m (Proposed)

The workflow below is planned for PatchCore inspection at **5 m height** using the IDS camera. The 3008 x 3008 image is a square crop from the full 4128 x 3008 frame. Each tile keeps the original pixel scale.

<CvFigure number="117" n="46" />

For the proposed final setup at 5 m, a 1 cm object spans only about 10 or 15 pixels with the e-CAM or IDS camera and lens setups. The proposed change is to divide the inspection image into overlapping 512 x 512 pixel tiles, each processed individually by PatchCore for anomaly detection. Each tile's anomaly heatmap will then be mapped back to the inspection image using its tile coordinate offsets. The heatmaps will be combined to identify anomalous regions. These regions will be marked and cropped directly from the original camera image, accounting for any inspection-crop offset, before continuing through the remaining stages of the selected architecture.

Compare the current model with a dual-branch model using different feature layers. Measure 1 cm FOD detection, false alarms, processing time and GPU memory before selecting the final setup. This is a proposed configuration and has not been tested.

:::

::: details 4.6.1.3 Detection and Coordinate Testing

- **Check PatchCore misses:** Test how often PatchCore misses FOD or cracks at 5 m, extending the current 1 m tests.
- **Test detection during flight:** Verify 1 cm FOD detection through the full pipeline at 5 m and 15 km/h, during daylight and night operation. Test the selected lens, exposure settings and light.
- **Set targets and check coordinate error:** Define the target detection performance and puddle size target. Test real puddles and measure coordinate error using camera calibration, navigation data and gimbal angles.

:::

::: details 4.6.1.4 Camera Setup, Gimbal and Night Lighting

- **Test the cameras:** Test both RGB and thermal cameras with the models.
- **Add the gimbal:** Add and test a gimbal for the RGB inspection camera, using flight controller attitude data to compensate for tilt and maintain a nadir view. Include the gimbal angles in coordinate retrieval.
- **Test night lighting:** Attach and test the light below the drone near the RGB camera for night operation.

:::

::: details 4.6.1.5 Jetson Integration and Processing Tests

- **Integrate the pipeline:** Complete system integration using Jetson NX following the pipeline.
- **Connect the cameras:** Implement the link between the cameras and the vision system in Jetson NX.
- **Measure processing time:** Test the latency for each model and the entire integrated system on Jetson alongside navigation and communication. Check that captured frames do not build up in a processing queue.

:::

::: details 4.6.1.6 Thermal Safety and Live Feed

- **Connect emergency stops:** Link thermal detection to the flight controller for emergency stops.
- **Test the thermal live feed:** Integrate and test the thermal live feed for manual override and guiding ARGUS back at night. Check image clarity and video delay.

:::

::: details 4.6.1.7 Navigation and FOD Coordinate Transmission

- **Link navigation data:** Send current drone coordinates from ROS 2 navigation to the vision system.
- **Prevent repeated coordinates:** Set up a program to prevent repeated FOD coordinates from being sent (work with the UGV side).

:::

</div>
