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

## Computer Vision Model Sources

### CV-M01 - U-Net Encoder and Decoder {#cv-m01}

Segmentation Models PyTorch. **Unet model documentation**.

[Official documentation](https://smp.readthedocs.io/en/latest/models.html#unet). Describes the encoder, decoder, encoder-to-decoder skip connections, pretrained encoder options and segmentation outputs. Implementation settings in the report were checked against the project's crack training and inference scripts.

### CV-M02 - ResNet Residual Learning {#cv-m02}

He, Kaiming; Zhang, Xiangyu; Ren, Shaoqing; Sun, Jian (2015). **Deep Residual Learning for Image Recognition**. arXiv:1512.03385.

[Original paper](https://arxiv.org/abs/1512.03385). Explains residual learning and shortcut connections used in the ResNet family.

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

### [14] - Singapore annual mean wind speed {#md-ref-14}

The Straits Times. **ST Explains: Why is February the windiest month in Singapore?** Accessed 10 November 2026.

[Open the Straits Times article](https://www.straitstimes.com/singapore/st-explains-why-is-february-the-windiest-month-in-singapore). Supports the approximately 2 m/s annual mean used for preliminary headwind sizing. The source report supplied the publisher and citation number but no article title or URL; this matching article was located during integration. The [Meteorological Service Singapore climate overview](https://www.weather.gov.sg/climate-climate-of-singapore) independently reports mean surface winds of around 2 m/s. This mean does not define a maximum operating wind or gust limit.

### [15] - Beaufort Wind Scale {#md-ref-15}

**Bibliographic details missing; manual completion required.** Citation preserved from “Results across Different Flight Scenarios” in the supplied interim report.

### [16] - DJI Matrice 350 RTK maximum pitch angle {#md-ref-16}

**Bibliographic details missing; manual completion required.** Citation and reference figure preserved from “Setting Conservative Thrust Estimate” in the supplied interim report.

### [17] - T-Motor MN501-S KV360 performance data {#md-ref-17}

**Bibliographic details missing; manual completion required.** Manufacturer performance data citation preserved from “T-Motor MN501-S KV360 with 17-inch Propellers” in the supplied interim report.

### [18] - MAD 5005 IPE KV440 performance data {#md-ref-18}

**Bibliographic details missing; manual completion required.** Manufacturer performance data citation preserved from “MAD 5005 IPE KV440 with 14-inch Propellers” in the supplied interim report.

### [19] - Toray T300 carbon fibre datasheet {#md-ref-19}

**Bibliographic details missing; manual completion required.** Datasheet citation preserved from “Beam Deflection Calculation” in the supplied interim report, which adopts a Young's modulus of 123 GPa.

### [20] - ArduPilot vibration documentation {#md-ref-20}

**Bibliographic details missing; manual completion required.** Documentation citation preserved from “Natural Bending Frequency Calculation” in the supplied interim report, identifying motor rotational frequency as a common source of multirotor vibration.

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

## Electrical Design Sources

Some hardware datasheets used for the Electrical Design report are listed under Navigation & Obstacle Avoidance Sources below ([14]-[17]). 

### ED-H01 - Flight Controller {#ed-h01}
[Pixhawk (3DR)](https://docs.px4.io/v1.16/en/flight_controller/pixhawk). **3DR Pixhawk 1 Flight Controller (Discontinued), PX4 User Guide v1.16, PX4 Dev Team.**  Lists the flight controller's processor, sensors, serial ports, PWM outputs and power input specifications.

### ED-H02 - Jetson NX Orin {#ed-h02}
[Jetson Orin NX](/report-assets/datasheets/Jetson_Orin_NX_DS-10712-001_v0.5.pdf). **NVIDIA Jetson Orin NX Series Data Sheet, DS-10712-001 v0.5, NVIDIA Corporation (undated).**  Lists AI performance (100 TOPS sparse INT8, 1024 CUDA cores, 32 Tensor cores, 2 DLAs), CPU and memory (8× Cortex-A78AE, 16 GB LPDDR5), 10/15/25 W power modes, and interfaces (UART, USB 3.2, CSI, Gigabit Ethernet).

### ED-H03 - Raspberry Pi 5 {#ed-h03}

[Raspberry Pi 5](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008348-DS-10-raspberry-pi-5-product-brief.pdf). **Raspberry Pi 5 Product Brief, RP-008348-DS-10, Raspberry Pi Ltd, 2026.**  Lists CPU and memory (4× Cortex-A76 at 2.4 GHz, LPDDR4X), stated 2–3× CPU performance increase over the Raspberry Pi 4, interfaces (Gigabit Ethernet, USB 3.0, 40-pin GPIO header), and the 5 V / 5 A power input requirement.

### ED-H04 - Battery Specifications {#ed-h04}

[HRB 6S 12000mAh LiPo](https://hrb-power.com/products/hrb-6s-22-2v-12000mah-lipo-battery-xt90s-as150-xt150-for-plane-drone-boat?variant=43721861103808) (accessed 10 November 2026). **HRB 6S 22.2V 12000mAh LiPo Battery (XT90S/AS150/XT150) Product Specifications, HRB-POWER, undated.**  Lists battery capacity and energy, continuous discharge rating, weight, recommended charge rate, and per-cell voltage limits (4.2 V maximum, 3.7 V minimum). The specifications are listed on the manufacturer's product page.

[View HRB 6S 12000mAh LiPo Battery Product Page]

### ED-H05 - Motor Specifications {#ed-h05}

[MAD 5005 IPE 440KV](/report-assets/datasheets/MAD_Motor_datasheet.png). **MAD 5005 IPE 440KV Motor Thrust Test Data (FLUXER PRO 14x4.8 MATT propeller, AMPX 40A PRO ESC, 6S), MAD Components, undated.**  Lists motor thrust and power performance, including throttle-to-thrust response, current draw, input and output power, efficiency, and RPM at 6S (24 V nominal). The test data was captured from the manufacturer's product page.

[View MAD 5005 IPE Product Page](https://mad-motor.com/products/mad-components-5005-ipe?VariantsId=10440) (accessed 10 November 2026)

### ED-H06 - Power Distribution Board {#ed-h06}
[Matek PDB-HEX](/report-assets/datasheets/PDB-HEX_Manual.pdf). **MATEKSYS PDB-HEX Quick Start Guide, Matek Systems.**  Lists the input voltage range, current rating, the 1/21 battery voltage divider, the current-sense signal, and the 5 V regulated output.

## Navigation & Obstacle Avoidance Sources
 
### [1] - Coverage for robotics survey {#nav-ref-1}
 
Choset, H. (2001). Coverage for robotics - A survey of recent results. *Annals of Mathematics and Artificial Intelligence*, 31.  
[Springer (DOI 10.1023/A:1016639210559)](https://doi.org/10.1023/A:1016639210559)  
**Used for:** Background on coverage path planning and parallel-lane (back-and-forth) sweeps.
 
### [2] - Coverage path planning survey {#nav-ref-2}
 
Galceran, E.; Carreras, M. (2013). A survey of coverage path planning for robotics. *Robotics and Autonomous Systems*, 61(12).  
[ScienceDirect (DOI 10.1016/j.robot.2013.09.004)](https://doi.org/10.1016/j.robot.2013.09.004)  
**Used for:** Choosing the lane-by-lane survey pattern and comparing coverage strategies.
 
### [3] - FAA runway design and orientation {#nav-ref-3}
 
Federal Aviation Administration. **Advisory Circular AC 150/5300-13B, Airport Design.**  
[AC 150/5300-13B (Change 1), FAA](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC-150-5300-13B-Airport-Design-Chg1-w-errata.pdf)  
**Used for:** Runway dimensions and runway orientation (95% wind coverage).
 
### [4] - A* path search {#nav-ref-4}
 
Hart, P. E.; Nilsson, N. J.; Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. *IEEE Transactions on Systems Science and Cybernetics*, 4(2).  
[IEEE (DOI 10.1109/TSSC.1968.300136)](https://doi.org/10.1109/TSSC.1968.300136)  
**Used for:** The grid search behind the global rerouting around mapped obstacles.
 
### [5] - Planning Algorithms {#nav-ref-5}
 
LaValle, S. M. (2006). *Planning Algorithms*. Cambridge University Press.  
[Free online edition](https://lavalle.pl/planning/)  
**Used for:** General reference for grid-based planning and replanning.
 
### [6] - Pure pursuit path tracking {#nav-ref-6}
 
Coulter, R. C. (1992). Implementation of the pure pursuit path tracking algorithm. Carnegie Mellon University Robotics Institute, CMU-RI-TR-92-01.  
[CMU Robotics Institute](https://www.ri.cmu.edu/publications/implementation-of-the-pure-pursuit-path-tracking-algorithm/)  
**Used for:** The alternative that was considered and not used, because its look-ahead is larger than the lane pitch.
 
### [7] - Cross-track path tracking {#nav-ref-7}
 
Snider, J. M. (2009). Automatic steering methods for autonomous automobile path tracking. Carnegie Mellon University Robotics Institute, CMU-RI-TR-09-08.  
[CMU Robotics Institute](https://www.ri.cmu.edu/publications/automatic-steering-methods-for-autonomous-automobile-path-tracking)  
**Used for:** The cross-track error correction used to hold the narrow lane.
 
### [8] - PX4 User Guide {#nav-ref-8}
 
PX4 Autopilot. **PX4 User Guide.**  
[Offboard mode](https://docs.px4.io/main/en/flight_modes/offboard) · [EKF2 tuning](https://docs.px4.io/main/en/advanced_config/tuning_the_ecl_ekf) · [Safety (battery failsafes)](https://docs.px4.io/main/en/config/safety)  
**Used for:** Offboard velocity commands, EKF2 position estimate, and the battery failsafe levels.
 
### [9] - Dynamic window approach {#nav-ref-9}
 
Fox, D.; Burgard, W.; Thrun, S. (1997). The dynamic window approach to collision avoidance. *IEEE Robotics & Automation Magazine*, 4(1).  
[IEEE (DOI 10.1109/100.580977)](https://doi.org/10.1109/100.580977)  
**Used for:** The velocity-sampling idea behind the reactive avoider.
 
### [10] - Kalman filter {#nav-ref-10}
 
Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. *Journal of Basic Engineering*, 82(1).  
[ASME (DOI 10.1115/1.3662552)](https://doi.org/10.1115/1.3662552)  
**Used for:** Per-bird tracks (position and velocity estimates) used by the threat assessor.
 
### [11] - Dryden turbulence model {#nav-ref-11}
 
U.S. Department of Defense. **MIL-HDBK-1797, Flying Qualities of Piloted Aircraft.**  
[Dryden model overview, Wikipedia (cites MIL-HDBK-1797)](https://en.wikipedia.org/wiki/Dryden_Wind_Turbulence_Model)  
**Used for:** Basis of the gust model in the wind simulation (σ and τ scaling).
 
### [12] - SDFormat camera specification {#nav-ref-12}
 
SDFormat specification, version 1.9, camera element (default horizontal_fov 1.047 rad).  
[SDFormat 1.9 specification](http://sdformat.org/spec?ver=1.9&elem=sensor)  
**Used for:** Default camera field of view in the simulation.
 
### [13] - ICAO runway standards {#nav-ref-13}
 
International Civil Aviation Organization. **Annex 14, Volume I: Aerodrome Design and Operations.**  
[ICAO Store](https://store.icao.int/en/annex-14-aerodromes)  
**Used for:** International runway standards that the FAA values are checked against.
 
### [14] - Leishen N10 LiDAR datasheet {#nav-ref-14}

[N10 2D 360° LiDAR](/report-assets/datasheets/Leishen_N10_360_LiDAR.pdf). **Leishen Intelligent N10 LiDAR User Manual, WitMotion Shenzhen Co., Ltd (undated).**  Lists 360° 2D scanning LiDAR specifications (5 V supply, about 60 g, 12 m range, ±3 cm accuracy, 4.5 kHz measurement rate), UART interface (230400 baud) and USB adapter wiring, optical window and mounting dimensions, and ROS driver setup. The manual gives no supply current, so the current used in the power budget is an assumption.


### [15] - Benewake TFmini Plus datasheet and user manual {#nav-ref-15}

[TFmini Plus (Datasheet)](/report-assets/datasheets/TFmini_Plus_Datasheet.pdf). **TFmini Plus LiDAR Datasheet, Document PD-TFmini-Plus-Datasheet-A07, Benewake (Beijing) Co., Ltd, 2024.**  Lists single-point ToF LiDAR specifications, operating range and accuracy, field of view, electrical parameters (5 V supply, ≤ 110 mA average, 140 mA peak) and weight.


[TFmini Plus (Manual)](/report-assets/datasheets/TFmini_Plus_User_Manual.pdf). **TFmini Plus User Manual, REV 01/04/2024, Benewake (Beijing) Co., Ltd.**  Lists wiring and pin definitions, serial data output format, configuration command frames, repeatability characteristics, and troubleshooting.


### [16] - Unicore UM980 datasheet {#nav-ref-16}

[UM980 GNSS Module Datasheet](/report-assets/datasheets/UM980_User_Manual_EN_R1.10.pdf). **UM980 GPS/BDS/GLONASS/Galileo/QZSS All-constellation Multi-frequency High-Precision RTK Positioning Module Installation and Operation User Manual, R1.10, Unicore Communications, Inc., June 2026.**  Lists GNSS constellation and frequency support, RTK/PPP positioning accuracy, pin definitions, electrical specifications, antenna feed design, and PCB footprint and soldering requirements.


### [17] - Thermal camera datasheet {#nav-ref-17}

[BNW2T Series Thermal Camera](/report-assets/datasheets/BNW2T_Series_Uncooled_Infrared_Thermal_Module_Product_Manual_V1.pdf). **BNW2T Series Uncooled Infrared Thermal Module Product Manual, Version V1.2, January 9, 2026.**  Lists thermal camera specifications, model selection, lens characteristics, temperature measurement performance, supply voltage and power consumption (5 V, under 0.35 W typical), and interface connections of the BNW2T256T04010ASSWC module. The “C” in the model code indicates no USB, so a USB accessory is required.




