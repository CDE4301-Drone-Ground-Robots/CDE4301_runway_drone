---
title: References
---

<p class="chapter-kicker">FOD ARGUS / PROJECT REPORT</p>

# References

## Computer Vision Dataset Sources

### CV-D01 - CrackAirport {#cv-d01}

Lyu, Zefeng; Yu, Andrew; Starr, Christopher (2026). **CrackAirport: A Dataset for Segmentation of Cracks in Airport Pavements**. Mendeley Data, version 1. Published 16 February 2026. DOI: [10.17632/3v5r2fxf89.1](https://doi.org/10.17632/3v5r2fxf89.1). Licence: CC BY 4.0.

[Open dataset](https://data.mendeley.com/datasets/3v5r2fxf89/1). Used for the U-Net crack-segmentation work.

### CV-D02 - Foreign Object Debris in Airports (FOD-A) {#cv-d02}

**Foreign Object Debris in Airports (FOD-A) Dataset**. Kaggle, dataset page under `kilogrand`.

[Open dataset page supplied by the author](https://www.kaggle.com/datasets/kilogrand/foreign-object-debris-in-airports-fod-a-dataset/code). Used as the source FOD dataset for YOLO development.

### CV-D03 - Thermal Bird, Version 6 {#cv-d03}

**Thermal Bird**, dataset version 6. Roboflow Universe, workspace `arc-ejbpg`.

[Open dataset](https://universe.roboflow.com/arc-ejbpg/thermal-bird/dataset/6). Used for thermal bird detection.

### CV-D04 - Thermal Images for Human Detection {#cv-d04}

**Thermal Images for Human Detection**. Kaggle, dataset page under `sikdermdsaiful`.

[Open dataset page supplied by the author](https://www.kaggle.com/datasets/sikdermdsaiful/thermal-images-for-human-detection/data?select=dataset). Used for thermal human detection.

## Computer Vision Hardware Sources

### CV-H01 - RGB Camera: e-CAM56_CUONX {#cv-h01}

e-con Systems. **5MP Sony Pregius S IMX568 Global Shutter Camera for NVIDIA Jetson Orin NX / Nano (e-CAM56_CUONX)**. Manufacturer product page.

[Open manufacturer specifications](https://www.e-consystems.com/nvidia-cameras/jetson-orin-nx-cameras/5mp-imx568-global-shutter-camera.asp). Referenced for the proposed RGB camera; final procurement remains subject to the project's hardware and budget decisions.

### CV-H02 - IDS RGB Camera Alternative: U3-31L1ACP Rev.1.2 {#cv-h02}

IDS Imaging Development Systems. **U3-31L1ACP Rev.1.2**. Manufacturer product page; accessed 8 November 2026.

[Manufacturer specifications](https://en.ids-imaging.com/store/u3-31l1acp-rev-1-2.html). Lists the Sony IMX545 sensor, 4128 x 3008 resolution (12.42 MP), global shutter, 32.4 fps at full resolution, USB 3 interface and 2.74 micrometre pixels. The camera remains an alternative under consideration.

## Mechanical Design Sources

The numbers below preserve the citations in Section 10 of the supplied *Interim Report.docx*. The supplied document contains no bibliography. Full bibliographic details must be completed manually; these entries do not identify verified sources.

### [1] - CAAS UA Pilot Licence requirement {#md-ref-1}

**Bibliographic details missing; manual completion required.** Referenced in the Mechanical Design report.

### [2] - Plus and cross quadcopter configuration comparison {#md-ref-2}

**Bibliographic details missing; manual completion required.** Referenced in the Mechanical Design report.

### [3] - Pusher and puller configuration CFD comparison {#md-ref-3}

**Bibliographic details missing; manual completion required.** Referenced in the Mechanical Design report.

### [4] - CFRP structural properties {#md-ref-4}

**Bibliographic details missing; manual completion required.** Referenced in the Mechanical Design report.

### [5] - CFRP structural properties {#md-ref-5}

**Bibliographic details missing; manual completion required.** Referenced in the Mechanical Design report.

### [7] - CFRP and aluminium-alloy motor-frame vibration experiment {#md-ref-7}

**Bibliographic details missing; manual completion required.** Referenced in the Mechanical Design report.

### [8] - CFRP structural properties {#md-ref-8}

**Bibliographic details missing; manual completion required.** Referenced in the Mechanical Design report.

### [9] - PETG CF compared with PETG and PLA {#md-ref-9}

**Bibliographic details missing; manual completion required.** Referenced in the Mechanical Design report.

### [10] - Vertical CG positioning and multicopter stability thesis {#md-ref-10}

**Bibliographic details missing; manual completion required.** Citation preserved from Sections 10.3?10.4 of the supplied *Interim Report.docx*.

### [11] - Direct georeferencing and sensor lever-arm transformation {#md-ref-11}

**Bibliographic details missing; manual completion required.** Citation preserved from Sections 10.3?10.4 of the supplied *Interim Report.docx*.

### [12] - PX4 flight controller mounting documentation {#md-ref-12}

**Bibliographic details missing; manual completion required.** Citation preserved from Sections 10.3?10.4 of the supplied *Interim Report.docx*.

### [13] - ArduPilot flight controller placement and IMU offsets {#md-ref-13}

**Bibliographic details missing; manual completion required.** Citation preserved from Sections 10.3?10.4 of the supplied *Interim Report.docx*.

## Computer Vision Safety Sources

### CV-S01 - Pavement Cracking and FOD Risk {#cv-s01}

Federal Aviation Administration. **Reflective Cracking Program**. Airport Technology Research and Development. Accessed 31 October 2026.

[Open FAA research overview](https://www.airporttech.tc.faa.gov/Airport-Pavement/Pavement-Design/Reflective-Cracking-Program). Explains that reflective cracks can lead to spalling and loose pavement pieces that become FOD. Used to support retaining crack inspection alongside FOD detection.

### CV-S02 - Hairline Cracks, Deterioration and Water Entry {#cv-s02}

Federal Aviation Administration. **AC 150/5320-17A, Appendix B: Concrete Airfield Pavement Surface Evaluation and Rating Manual**. 10 September 2014, pp. 8-9: Corner cracks and Meander cracks. Accessed 8 November 2026.

[Open FAA manual at the corner-crack discussion](https://www.faa.gov/documentlibrary/media/advisory_circular/150-5320-17a-appendix-b.pdf#page=10). Describes concrete corner cracks that may begin as hairline cracks and deteriorate until pieces come loose. The next page notes that minor cracks may benefit from sealing to limit water intrusion. These statements support inspection and assessment; they do not establish that every hairline crack is an immediate operational hazard.

### CV-N01 - ROS 2 Position, Orientation and Quaternion Heading {#cv-n01}

Open Robotics. **ROS 2 Jazzy common_interfaces and tf2**. Accessed 8 November 2026.

The [Pose message definition](https://github.com/ros2/common_interfaces/blob/jazzy/geometry_msgs/msg/Pose.msg) separates position from orientation. The [Quaternion message definition](https://github.com/ros2/common_interfaces/blob/jazzy/geometry_msgs/msg/Quaternion.msg) defines orientation using x, y, z and w. The [tf2 yaw implementation](https://github.com/ros2/geometry2/blob/jazzy/tf2/include/tf2/impl/utils.hpp) provides quaternion-to-heading calculation. These do not define a quaternion-to-position conversion.

### CV-N02 - ROS Coordinate Conventions {#cv-n02}

Foote, Tully and Purvis, Mike. **REP 103: Standard Units of Measure and Coordinate Conventions**. Open Robotics. Accessed 8 November 2026.

[Official REP 103 source](https://github.com/ros-infrastructure/rep/blob/master/rep-0103.rst). Defines right-handed frames, metre units, body axes, camera optical axes, ENU/NED conventions and positive yaw direction.

## Communication System Sources

### COM-H01 - Microhard pMDDL2450 {#com-h01}

Microhard. **pMDDL2450 - Wireless MIMO (2X2) OEM Digital Data Link**. Manufacturer product page; accessed 1 November 2026.

[Manufacturer specifications](https://www.microhardcorp.com/pMDDL2450.php). Identifies the candidate radio as a 2.4 GHz data link.

### COM-R01 - IMDA Short Range Devices Specification {#com-r01}

Infocomm Media Development Authority. **Technical Specification for Short Range Devices (IMDA TS SRD), September 2023**. Accessed 1 November 2026.

[Official technical specification](https://www.imda.gov.sg/-/media/imda/files/regulation-licensing-and-consultations/ict-standards/telecommunication-standards/radio-comms/imdatssrd.pdf). Lists band-specific device categories and operating conditions. A listed band alone does not establish approval for the proposed radio configuration.

### COM-R02 - IMDA Unmanned Aircraft Radio Guidance {#com-r02}

Infocomm Media Development Authority. **Operation of Unmanned Aircraft Systems (UAS)**. Accessed 1 November 2026.

[Official UAS guidance](https://www.imda.gov.sg/regulations-and-licensing-listing/spectrum-management/frequency-allocation-and-assignment/operation-of-unmanned-aircraft-systems-uas). Lists the commonly used 2.4000-2.4835 GHz UAV band with a maximum power of 100 mW EIRP under the published licence-exemption conditions.
