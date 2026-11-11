---
title: "Mechanical Design"
outline: false
prev: false
next: false
aside: false
pageClass: subsystem-report-page
---

<script setup>
import MechanicalFigure from './components/MechanicalFigure.vue'
import UAVTiltThrustSimulator from '../.vitepress/theme/components/UAVTiltThrustSimulator.vue'
</script>

<div class="cv-report rubric-report">

<p class="chapter-kicker">FOD ARGUS / MECHANICAL DESIGN</p>

# Mechanical Design

<SubsystemLead class="cv-report-byline" name="Muruganantham Arun" matric="A0308280J" portrait="/team/Arun.png" />

## A1. Objective, Scope and Context {#a1-objective-scope-context}

### Overview of Mechanical Design of the UAV {#overview-of-mechanical-design-of-the-uav}

Initial requirements were established to guide the mechanical design of the UAV. Additional considerations, including vibration management and manufacturability, were identified as the design progressed. The table below summarises the requirements and considerations intended for the final design.

| Design Requirements | Description |
| --- | --- |
| Component integration | Accommodate all required components with secure mounting and sufficient space for wiring and connections. |
| Low overall mass | Minimise the UAV's total mass to reduce the thrust and propulsion power required, allowing for smaller motor and propeller combinations while improving flight endurance and not compromising the UAV's structural integrity or essential functionalities. CAAS regulations were also considered, with a target takeoff mass below 7 kg to facilitate future flight testing [\[1\]](../references#md-ref-1). |
| Structural strength and stiffness | Withstand thrust, component loads and landing forces without failure or excessive deformation. |
| Balanced mass distribution | Position components to keep the centre of gravity close to the centre of the motors. |
| Unobstructed sensors and camera fields of view | Ensure the airframe and landing gear do not obstruct the cameras and ranging sensors. |
| Vibration management | Reduce vibration transmitted to the flight controller and cameras. |
| Thermal management | Provide adequate ventilation and cooling for heat-generating electronics. |
| Manufacturability | Ensure that the design is feasible and practical for fabrication with available materials, equipment and processes. |
| Water resistance | Ensure reliable UAV operation under adverse weather conditions, particularly during light rainfall. |

## A2. Methodology / Concept Development {#a2-methodology-concept-development}

### Initial Concept Sketch {#initial-concept-sketch}

<MechanicalFigure n="1" src="/report-assets/mechanical-design/initial-concept-sketch.png" :width="1150" :height="863" caption="Initial Concept Sketch" />

An initial concept sketch was developed to provide a foundation for the UAV’s mechanical design. Rather than prescribing the exact geometry, it established a layered layout in which different components were allocated to each level. This arrangement guided subsequent design iterations while allowing flexibility in the detailed design. Furthermore, a quadcopter configuration was selected as a suitable balance between lifting capability, structural simplicity and overall mass, which was targeted to be below 7 kg as mentioned above. Using four motors reduced the number of propulsion components and associated mounting structures compared with six- or eight-rotor configurations. The motors and propellers were subsequently selected to provide sufficient thrust and control margin for the estimated takeoff mass.

### Plus vs X vs H Propeller Configuration {#plus-vs-x-vs-h-propeller-configuration}

<MechanicalFigure n="2" src="/report-assets/mechanical-design/propeller-configurations.png" :width="750" :height="279" caption="Different Propeller Configurations" />

The X configuration was selected over the plus configuration due to its improved attitude control authority and reduced coupling between pitch/roll and yaw dynamics. According to a comparative analysis of a quadcopter in plus and cross configurations [\[2\]](../references#md-ref-2), although both configurations exhibit similar hover power requirements and autonomous stability characteristics, the cross configuration provides up to √2 greater pitch and roll control authority because all four rotors contribute to attitude moments. This improved control authority is advantageous for runway inspection operations where the UAV may experience external disturbances such as wind gusts.

The H configuration was considered, but its limitations in accommodating larger propellers made the X configuration more desirable. Extending the arms diagonally increases motor spacing in both longitudinal and lateral directions. In comparison, an H-frame arrangement would require additional longitudinal extension to prevent propeller overlap.

### Pusher vs Puller Configuration {#pusher-vs-puller-configuration}

<div class="cv-figure-grid">

<MechanicalFigure n="3" src="/report-assets/mechanical-design/pusher-configuration.png" :width="350" :height="302" caption="Pusher Configuration" />

<MechanicalFigure n="4" src="/report-assets/mechanical-design/puller-configuration.png" :width="658" :height="493" caption="Puller Configuration" />

</div>

A puller configuration, with the propellers positioned above the motors and supporting arms, was selected for the UAV. A comparative CFD study reported higher thrust generation for the puller configurations under the conditions investigated [\[3\]](../references#md-ref-3). This arrangement also provides greater propeller ground clearance and reduces the potential for interference with the field of view of the forward-facing thermal camera mounted beneath the body. These considerations supported its suitability for the proposed mechanical layout.

### Placement of Key Onboard Components {#placement-of-key-onboard-components}

The placement of key onboard components supports flight stability and operational requirements. The flight controller, cameras and other electronics were positioned with consideration of mass distribution, accessibility, vibration isolation and electrical connectivity.

#### Central Alignment of GNSS Antenna and RGB Camera {#central-alignment-of-gnss-antenna-and-rgb-camera}

The RGB camera detects foreign object debris (FOD) and identifies its location within captured images, while the GNSS system provides the UAV's geographical position. To simplify geolocation, the GNSS antenna and RGB camera were placed centrally in the X–Y plane along the same vertical axis, separated in height.

<MechanicalFigure n="17" src="/report-assets/mechanical-design/gnss-rgb-vertical-alignment.png" :width="702" :height="306" caption="Side view showing the vertical separation of the GNSS antenna and RGB camera (project CAD)." />

This arrangement simplifies the sensor-to-sensor coordinate transformation because the relative displacement is primarily vertical. A simplified position transformation, derived from the direct georeferencing principles cited in the source report [\[11\]](../references#md-ref-11), is:

$$
\mathbf{p}_C^N=\mathbf{p}_G^N+\mathbf{R}_B^N\mathbf{t}_{GC} \tag{2}
$$

Here, $\mathbf{p}_C^N$ is the RGB camera position in the navigation frame, $\mathbf{p}_G^N$ is the GNSS antenna position in that frame, $\mathbf{R}_B^N$ is the rotation matrix from the UAV body frame to the navigation frame, accounting for attitude, and $\mathbf{t}_{GC}$ is the translation vector from the GNSS antenna to the RGB camera, expressed in the body frame.

For the approximately vertically aligned configuration:

$$
\mathbf{p}_C^N\approx\mathbf{p}_G^N+\mathbf{R}_B^N
\begin{bmatrix}0\\0\\\Delta z\end{bmatrix} \tag{3}
$$

The signed separation $\Delta z$ is measured from the GNSS antenna to the RGB camera along the UAV body Z-axis. Central alignment simplifies the lever-arm offset used for FOD geolocation, but UAV attitude must still be considered when transforming the camera position into the navigation frame.

#### Placement of the Pixhawk Flight Controller near Centre of Gravity {#placement-of-the-pixhawk-flight-controller-near-centre-of-gravity}

The placement of the Pixhawk flight controller in the FOD ARGUS UAV was determined based on recommendations from PX4 and ArduPilot documentation, which recommend placing the flight controller as close as possible to the CG [\[12\]](../references#md-ref-12) [\[13\]](../references#md-ref-13).

<MechanicalFigure n="18" src="/report-assets/mechanical-design/px4-flight-controller-mounting.png" :width="1040" :height="611" caption="Ideal flight controller placement. External PX4 documentation illustration reproduced in the supplied report [12]; the original source URL was not supplied." />

Subsequently, we positioned the flight controller as close to the CG as practically possible in our UAV assembly while also considering spatial constraints, as shown in the images below.

<MechanicalFigure n="19" src="/report-assets/mechanical-design/pixhawk-isometric-view.png" :width="872" :height="617" caption="Isometric view of the Pixhawk placement (project CAD)." />

<div class="cv-figure-grid">

<MechanicalFigure n="20" src="/report-assets/mechanical-design/pixhawk-top-view.png" :width="656" :height="619" caption="Top view of the Pixhawk placement (project CAD)." />

<MechanicalFigure n="21" src="/report-assets/mechanical-design/pixhawk-side-view.png" :width="807" :height="391" caption="Side view of the Pixhawk placement (project CAD)." />

</div>

After completing the overall UAV assembly, we calculated the approximate position of the Pixhawk relative to the UAV's overall CG point.

| Axis | Approximate distance from CG (mm) |
| --- | ---: |
| X | 20 |
| Y | 0 |
| Z | 40 |

The resultant displacement is:

$$
\begin{aligned}
d&=\sqrt{(\Delta x)^2+(\Delta y)^2+(\Delta z)^2}\\
&=\sqrt{20^2+0^2+40^2}\\
&\approx44.72\ \mathrm{mm}
\end{aligned} \tag{4}
$$

The resultant displacement obtained is approximately 45 mm from the CG, which is still within ArduPilot's recommendation of placing the flight controller within a few centimetres of the CG. Although both PX4 and ArduPilot provide software parameters to compensate for positional offsets when the flight controller cannot be mounted directly at the CG, positioning it as close as practically possible remains desirable. This is because a greater displacement from the CG increases the additional accelerations experienced by the IMU during rotational motion, potentially affecting sensor measurements and flight control performance [\[13\]](../references#md-ref-13).

#### Placement of the 360° LiDAR {#placement-of-the-360-lidar}

The 360° LiDAR was initially intended to be mounted centrally on the top plate. However, this position was prioritised for the GNSS antenna to maintain its central alignment with the RGB camera, so the LiDAR was relocated towards the front. It is intended to support obstacle detection and avoidance, as discussed in the [Computer Vision section](./computer-vision#thermal-safety). This placement aims to minimise obstruction of the LiDAR's scanning field by surrounding onboard components while maintaining sufficient clearance from the propellers and structural elements.

<MechanicalFigure n="22" src="/report-assets/mechanical-design/lidar-front-isometric-view.png" :width="916" :height="586" caption="Front placement of the 360° LiDAR in the isometric view (project CAD)." />

#### 45° Placement of the Thermal Camera {#45-degree-placement-of-the-thermal-camera}

The thermal camera is mounted at approximately 45° using a rigid, custom-designed mount that will be 3D-printed. This arrangement allows the thermal camera to complement the 360° LiDAR for obstacle detection. Further details of the planned sensor integration for obstacle detection and avoidance are discussed in the [Computer Vision section](./computer-vision#thermal-safety).

<MechanicalFigure n="23" src="/report-assets/mechanical-design/thermal-camera-side-view.png" :width="928" :height="392" caption="Placement of the thermal camera in the side view (project CAD)." />

#### Placement of Batteries and Other Electrical Components in the Bottom Layer {#placement-of-batteries-and-other-electrical-components-in-the-bottom-layer}

The batteries and other electrical components, particularly the Electronic Speed Controllers (ESCs), were positioned on the bottom layer of the UAV. As the batteries contribute significantly to the overall mass of the UAV as it is the heaviest component, weighing approximately 1.5kg, their placement in the lower section helps lower the CG, as discussed in [the CG analysis](#centre-of-gravity-cg-of-uav).

For the ESCs, although some multirotor designs mount them externally along the propeller arms, the FOD Argus prototype adopts an internal mounting configuration within the bottom layer. This arrangement provides additional protection against direct exposure to water and environmental conditions, particularly since the selected AMPX 40A ESCs do not have a specified waterproof rating.

However, with the planned integration of the Raspberry Pi into the bottom layer, spatial constraints may require the ESCs to be relocated externally. If necessary, 3D printed protective enclosures will be designed to provide water resistance.

## A3. Fabrication of Specimens/Prototypes {#a3-prototype-development}

### Design Iterations {#design-iterations}

The UAV’s mechanical design underwent two preliminary iterations before arriving at the final prototype design. Each iteration refined the component layout and structural arrangement to address the design requirements and issues identified during development.

#### First Iteration {#first-iteration}

<MechanicalFigure n="5" src="/report-assets/mechanical-design/first-iteration-structural-body.png" :width="1380" :height="688" caption="Structural body design for the first iteration" />

<MechanicalFigure n="6" src="/report-assets/mechanical-design/first-iteration-layered-section.png" :width="1381" :height="699" caption="Layered design approach from concept sketch (Sectioned View)" />

<div class="cv-figure-grid">

<MechanicalFigure n="7" src="/report-assets/mechanical-design/first-iteration-bottom-layer.png" :width="609" :height="434" caption="Bottom Layer" />

<MechanicalFigure n="8" src="/report-assets/mechanical-design/first-iteration-top-layer.png" :width="631" :height="428" caption="Top Layer" />

</div>

<MechanicalFigure n="9" src="/report-assets/mechanical-design/propeller-arm.png" :width="633" :height="527" caption="Propeller Arm" />

The first design iteration retained the layered approach established in the concept sketch shown above, focusing on the two central component layers between the RTK-GNSS antenna layer above and camera layer below. As this was a preliminary design, the first layer containing the antenna and the fourth layer housing the cameras were not yet incorporated. The top layer included mounting holes for securing an acrylic plate to support electronic components, while the bottom layer was intended to accommodate the battery, Jetson onboard computer and other key electrical components. The propeller arms were designed with the intention to withstand the bending moments generated by motor thrust and component weight while minimising structural mass.

##### Limitations {#limitations}

The first iteration prioritised component arrangement and structural geometry, with less consideration given to the eventual material selection and manufacturing process. The complex geometry of the top layer structure and the propeller arms was more suited for 3D-printing. However, subsequent research identified carbon-fibre-reinforced polymer (CFRP) as a suitable material for the UAV’s primary structure due to its high stiffness and strength relative to mass [\[4\]](../references#md-ref-4) [\[5\]](../references#md-ref-5) [\[8\]](../references#md-ref-8). Adapting the initial design for CFRP would require custom moulding or substantial changes to accommodate standard sheets and tubes, prompting a revision of the geometry and assembly approach.

##### CFRP Sheets & Tubes vs 3D-Printed Parts {#cfrp-sheets-tubes-vs-3d-printed-parts}

As discussed in the previous section, CFRP offers a higher strength-to-weight ratio than conventional 3D-printed polymers, making it suitable for the UAV’s primary structure. This is particularly important for supporting an estimated takeoff mass of 4–6 kg and withstanding the loads generated by motor thrust while minimising structural mass.

In addition, CFRP offers potential benefits for vibration management. An experiment demonstrated reduced vibration amplitudes in a CFRP motor frame compared with an aluminium-alloy frame [\[7\]](../references#md-ref-7). This characteristic is relevant to our application, where limiting camera vibration is important for maintaining image clarity during FOD detection and minimising interference with the flight controller's inertial sensor measurements.

#### Second Iteration {#second-iteration}

<MechanicalFigure n="10" src="/report-assets/mechanical-design/second-iteration-structural-body.png" :width="1073" :height="751" caption="Structural body design for the second iteration" />

<MechanicalFigure n="11" src="/report-assets/mechanical-design/second-iteration-layered-section.png" :width="1066" :height="790" caption="Layered design approach from concept sketch (Sectioned View)" />

To address the material and manufacturing limitations of the first iteration, the second design retained the layered layout while adapting the structure for CFRP fabrication. The previously proposed 3D-printed propeller arms were replaced with carbon-fibre tubes, and the top and bottom body structures were simplified for fabrication in CFRP. These changes aimed to improve structural stiffness, strength and vibration management while limiting mass. Custom 3D-printed clamps were used to secure the propeller arms and landing legs to the bottom layer.

##### Limitations {#limitations-1}

A key limitation of the second iteration was the geometry of the top and bottom body structures. Although intended for CFRP fabrication, each structure had an overall depth of 50 mm, making machining from solid CFRP stock impractical. Producing these features from thick plates would require substantial material removal, resulting in considerable waste, increased machining time and high fabrication costs. Further redesign was therefore needed to accommodate thinner CFRP plates joined using separate supports.

#### Final Prototype Design {#final-prototype-design}

<MechanicalFigure n="12" src="/report-assets/mechanical-design/final-prototype-cad-assembly.png" :width="1378" :height="665" caption="CAD Assembly of Final Prototype Design" />

<MechanicalFigure n="13" src="/report-assets/mechanical-design/final-prototype-layers.png" :width="734" :height="342" caption="Different Layers of the Prototype Design" />

| Layer / Assembly | Allocated Components |
| --- | --- |
| Top Layer | Pixhawk Flight Controller, Jetson Orin NX, GNSS Antenna and 360° LiDAR |
| Bottom Layer | 12 Ah Battery, Power Distribution Boards, Fuse and Electronic Speed Controllers (ESC) |
| Camera & Sensor Assembly | RGB Camera, Thermal Camera and Single-Point LiDAR |
| Propeller Assembly | Motors and Propellers |

To address the fabrication limitations of the second iteration, the final FOD ARGUS prototype design combines CFRP structural components with 3D-printed parts. CFRP was selected for the main structural components, including the base plates that mount the electrical and key onboard components, motor mounting plates and propeller arms. Its material properties, discussed earlier, and suitability for components with relatively simple geometry address the design requirement for manufacturability. For parts requiring greater geometric complexity and flexibility in customisation, such as enclosures and tube clamps, 3D-printed PETG CF would be used, as it demonstrates better mechanical properties than conventional PETG and PLA filaments [\[9\]](../references#md-ref-9).

## A4. Testing {#a4-testing}

Thrust behaviour is illustrated below using the preliminary model. Physical load-test and flight-test results remain to be documented.

### Interactive Thrust Illustration {#mechanical-thrust-illustration}

<details class="mechanical-flight-case" id="interactive-uav-attitude-thrust-simulator">
<summary>Interactive UAV Attitude and Thrust Simulator</summary>

<UAVTiltThrustSimulator />

This interactive visualisation supports preliminary thrust sizing for an X-configuration quadcopter. It assumes constant altitude with no vertical acceleration, thrust aligned with the body thrust axis, and no aerodynamic disturbances or additional forces.

</details>

## A5. Analysis {#a5-analysis}

### Centre of Gravity (CG) of UAV {#centre-of-gravity-cg-of-uav}

The centre of gravity (CG) of the completed UAV prototype assembly was determined in SolidWorks from the mass distribution of its individual components. The coordinates below are relative to the assembly coordinate origin; the vertical coordinate is distinct from the distance below the propeller plane.

| Axis | CG coordinate (mm) |
| --- | ---: |
| X | −5.85 |
| Y | 0.61 |
| Z | 36.49 |

<div class="cv-figure-grid">

<MechanicalFigure n="14" src="/report-assets/mechanical-design/cg-top-view.png" :width="600" :height="572" caption="CG point in the top view of the SolidWorks assembly (project CAD)." />

<MechanicalFigure n="15" src="/report-assets/mechanical-design/cg-front-view.png" :width="1101" :height="502" caption="CG point in the front view of the SolidWorks assembly (project CAD)." />

</div>

#### Horizontal CG Positioning {#horizontal-cg-positioning}

The SolidWorks mass properties give the horizontal displacement of the CG from the geometric centre of the four motors in the X configuration:

$$
d_{CG}=\sqrt{(-5.85)^2+(0.61)^2}=5.88\ \mathrm{mm} \tag{1}
$$

The calculated horizontal offset is approximately 5.88 mm. This relatively small offset limits the additional pitch and roll moments associated with uneven mass distribution, reducing the differential thrust required to maintain level hover. This can preserve more motor control authority for manoeuvres and responses to external disturbances, such as wind gusts.

#### Vertical CG Positioning {#vertical-cg-positioning}

The SolidWorks assembly places the UAV's CG approximately 40 mm below the propeller plane.

The thesis cited in the source report [\[10\]](../references#md-ref-10) describes how positioning the CG below the propellers can contribute to stability during forward flight and wind disturbances. Aerodynamic drag acting above the CG can generate a stabilising moment opposing an attitude disturbance, as illustrated below.

<MechanicalFigure n="16" src="/report-assets/mechanical-design/vertical-cg-stability-reference.png" :width="1040" :height="378" caption="Influence of vertical CG positioning on multicopter stability. External thesis illustration reproduced in the supplied report [10]; bibliographic details were not supplied." />

FOD ARGUS incorporates a lower CG through the arrangement of its onboard components, particularly the battery. This configuration may contribute to a stabilising aerodynamic response if the resultant aerodynamic forces act above the CG. Overall stability remains dependent on the flight control system, and flight testing is required to evaluate the effectiveness of this arrangement.

### Motor & Propellers Selection {#motor-propellers-selection}

<div class="mechanical-propulsion">

#### Preliminary Mass Estimation and Component Placement {#_5-1-preliminary-mass-estimation-and-component-placement}

The selection of motors and propellers was done prior to the completion of the final FOD Argus prototype design. Therefore, a preliminary mass estimation was conducted to establish a reasonable estimate of the UAV's total mass for subsequent thrust calculations and motor selection.

To achieve this, rough layouts of the top and bottom base plates were developed based on the dimensions and placement requirements of key components that had already been selected, such as the Jetson Orin NX and Pixhawk flight controller. These layouts were used to estimate the required base plate dimensions and provide a basis for the preliminary structural design.

<div class="cv-figure-grid">

<MechanicalFigure n="24" src="/report-assets/mechanical-design/preliminary-top-component-layout.png" :width="607" :height="538" caption="Preliminary component placement on the top base plate." />

<MechanicalFigure n="25" src="/report-assets/mechanical-design/preliminary-bottom-component-layout.png" :width="650" :height="428" caption="Preliminary component placement on the bottom base plate." />

</div>

The masses of structural components, including the carbon fibre base plates, propeller arms and 3D-printed parts, were obtained using the mass properties from SolidWorks. Meanwhile, the masses of already selected onboard components, such as the flight controller and sensors, were obtained from manufacturer specifications. As the battery selection had not yet been finalized also, the highest battery mass identified during the selection process was adopted as the preliminary mass estimate.

| Component | Estimated mass (g) |
| --- | ---: |
| Top base plate, 2 mm carbon fibre | 370.1 |
| Bottom base plate, 3 mm carbon fibre | 589.7 |
| Jetson Orin NX Development Kit | 300 (approximate) |
| 3DR Pixhawk Flight Controller | 38 |
| 12,000–16,000 mAh LiPo battery | 1,000–1,500 |
| LSLIDAR N10, 360° LiDAR | 60 |
| Carbon-fibre propeller arms, four combined | 280 |
| Carbon-fibre landing legs, four combined | 75.4 |
| 3D-printed top plate enclosure | 275 (default SolidWorks mass properties) |
| 3D-printed camera mount body | 147 (default SolidWorks mass properties) |

Based on these estimates, the preliminary mass of the identified components was approximately 3.6 kg. After accounting for additional planned components that had not yet been incorporated into the preliminary design, the total UAV mass was estimated to be approximately 5 kg. Furthermore, as shown in the table, the masses of the 3D-printed components were estimated using SolidWorks' default mass properties, as the final material and fabrication specifications had not yet been determined. This further justifies the adoption of a conservative total UAV mass estimate.

#### Preliminary Thrust Calculations {#_5-2-preliminary-thrust-calculations}

Preliminary thrust calculations were conducted to determine the thrust requirements of the UAV under different flight conditions, providing a basis for the selection of suitable motors and propellers. To simplify the calculations, several assumptions were made, as summarised in the table below.

| Parameter | Symbol | Assumption / value |
| --- | --- | --- |
| Preliminary takeoff mass | $m$ | 5 kg |
| Number of motors | $n$ | 4 |
| Gravitational acceleration | $g$ | 9.81 m/s² |
| Air density | $\rho$ | 1.225 kg/m³ |
| Projected frontal area | $A$ | 0.062038 m², held constant |
| Equivalent drag coefficient | $C_D$ | 1.28, dimensionless |
| Target ground speed | $v_g$ | 15 km/h = 4.1667 m/s |
| Opposing headwind speed | $v_w$ | 2 m/s |
| Forward acceleration in Case 3 | $a$ | 1 m/s², assumed constant |
| Rotating-propeller aerodynamic effects | — | Neglected |
| Motor thrust distribution | — | Equal average thrust across four motors |

##### General Equations {#general-equations}

Let $T_{\mathrm{total}}$ be the combined motor thrust and $\theta$ the forward tilt of its axis from vertical. The required horizontal thrust is $F_H$; it is zero in hover, balances drag in steady cruise, and supplies both drag compensation and acceleration in Case 3. The shared relationships are:

$$
T_{\mathrm{total}}\cos\theta=mg \tag{5}
$$

$$
T_{\mathrm{total}}\sin\theta=F_H \tag{6}
$$

$$
T_{\mathrm{total}}=\sqrt{(mg)^2+F_H^2} \tag{7}
$$

$$
T_{\mathrm{motor}}=\frac{T_{\mathrm{total}}}{4} \tag{8}
$$

$$
\theta=\tan^{-1}\!\left(\frac{F_H}{mg}\right) \tag{9}
$$

Thrust is calculated in newtons. For comparison with motor thrust data, results are also expressed in kilogram-force using 1 kgf ≈ 9.81 N, consistent with the assumed gravitational acceleration.

<details class="mechanical-flight-case" id="5-2-1-case-1-basic-hover-in-still-air">
<summary>5.2.1 Case 1: Basic Hover in Still Air</summary>

In this scenario, the UAV is assumed to hover steadily in still air, with no horizontal movement or acceleration. Therefore, the total upward thrust generated by the four motors must be equal to the UAV's weight to maintain a constant altitude.

<MechanicalFigure n="26" src="/report-assets/mechanical-design/hover-free-body-diagram.png" :width="715" :height="537" caption="Free-body diagram for basic hover in still air. The upward arrows represent the combined rotor contribution." />

Using [Equation (7)](#equation-md-7), [Equation (8)](#equation-md-8) and [Equation (9)](#equation-md-9):

$$
\begin{aligned}
T_{\mathrm{total}}&=5(9.81)=49.05\ \mathrm{N}\\
T_{\mathrm{motor}}&=\frac{49.05}{4}=12.2625\ \mathrm{N}\\
&\approx1.250\ \mathrm{kgf},\qquad\theta=0^\circ
\end{aligned}
$$

Each motor must generate approximately 1.25 kgf of thrust to maintain a steady hover under the assumed UAV mass of 5 kg.

</details>

<details class="mechanical-flight-case" id="5-2-2-case-2-15-km-h-cruise-against-a-2-m-s-headwind">
<summary>5.2.2 Case 2: 15 km/h Cruise Against a 2 m/s Headwind</summary>

For this scenario, the UAV is assumed to cruise at a constant speed of 15 km/h against a headwind of 2 m/s. The headwind velocity was selected based on an article published by The Straits Times, which reported Singapore's average annual wind speed to be approximately 2 m/s [\[14\]](../references#md-ref-14). In addition, the UAV's projected frontal area was approximated as 0.062038 m² based on the overall body geometry obtained from the front view of the preliminary SolidWorks model.

<MechanicalFigure n="27" src="/report-assets/mechanical-design/preliminary-projected-frontal-area.png" :width="515" :height="223" caption="Projected frontal area estimated from the preliminary SolidWorks geometry: 0.062038 m²." />

<MechanicalFigure n="28" src="/report-assets/mechanical-design/cruise-free-body-diagram.png" :width="811" :height="608" caption="Free-body diagram for steady cruise against a headwind, reproduced from the source report. The thrust annotation differs slightly from the recalculated value below." />

For directly opposing wind, relative airspeed and aerodynamic drag are:

$$
v_{\mathrm{rel}}=v_g+v_w \tag{10}
$$

$$
F_D=\frac{1}{2}\rho C_D A v_{\mathrm{rel}}^2 \tag{11}
$$

$$
\begin{aligned}
v_{\mathrm{rel}}&=\frac{15}{3.6}+2\approx6.167\ \mathrm{m/s}\\
F_D&=\tfrac12(1.225)(1.28)(0.062038)\left(\tfrac{15}{3.6}+2\right)^2\\
&\approx1.850\ \mathrm{N}
\end{aligned}
$$

At constant speed, ($F_H=F_D$). Applying [Equations (7)–(9)](#equation-md-7):

$$
\begin{aligned}
T_{\mathrm{total}}&=\sqrt{49.05^2+F_D^2}\approx49.085\ \mathrm{N}\\
\theta&=\tan^{-1}(F_D/49.05)\approx2.16^\circ\\
T_{\mathrm{motor}}&=T_{\mathrm{total}}/4\\
&\approx12.271\ \mathrm{N}\approx1.251\ \mathrm{kgf}
\end{aligned}
$$

Therefore, each motor must generate approximately 1.251 kgf of thrust to maintain a steady cruise speed of 15 km/h against a 2 m/s headwind, under the stated assumptions.

</details>

<details class="mechanical-flight-case" id="5-2-3-case-3-forward-acceleration-at-1-m-s2-towards-15-km-h-against-a-2-m-s-headwind">
<summary>5.2.3 Case 3: Forward Acceleration at 1 m/s² Towards 15 km/h Against a 2 m/s Headwind</summary>

The UAV accelerates forward while maintaining altitude, so horizontal thrust must overcome drag and produce the required acceleration. The thrust calculation below evaluates the condition at the target cruise speed, where drag is approximately 1.850 N. During acceleration from rest, drag varies with relative airspeed according to [Equations (10)](#equation-md-10) and [(11)](#equation-md-11).

<MechanicalFigure n="29" src="/report-assets/mechanical-design/acceleration-free-body-diagram.png" :width="1156" :height="436" caption="Free-body diagram for forward acceleration, evaluated at the target ground speed. The acceleration arrow indicates motion response rather than an additional force." />

The required horizontal thrust is:

$$
F_H=ma+F_D \tag{12}
$$

Using [Equations (7)–(9)](#equation-md-7) and [(12)](#equation-md-12):

$$
\begin{aligned}
F_H&\approx5(1)+1.850=6.850\ \mathrm{N}\\
\theta&=\tan^{-1}(F_H/49.05)\approx7.95^\circ\\
T_{\mathrm{total}}&=\sqrt{49.05^2+F_H^2}\approx49.526\ \mathrm{N}\\
T_{\mathrm{motor}}&=T_{\mathrm{total}}/4\\
&\approx12.381\ \mathrm{N}\approx1.262\ \mathrm{kgf}
\end{aligned}
$$

The idealised time and distance from initial ground speed $u$ to final ground speed $v_g$, assuming constant acceleration, follow separately from kinematics:

$$
t=\frac{v_g-u}{a} \tag{13}
$$

$$
s=ut+\frac12at^2 \tag{14}
$$

For a start from rest, using [Equations (13)](#equation-md-13) and [(14)](#equation-md-14):

$$
\begin{aligned}
t&=\frac{15/3.6-0}{1}\approx4.17\ \mathrm{s}\\
s&=\tfrac12(1)\left(\tfrac{15/3.6}{1}\right)^2\approx8.68\ \mathrm{m}
\end{aligned}
$$

Therefore, the UAV requires approximately 1.262 kgf of thrust per motor when accelerating at 1 m/s² at the target cruise speed against a 2 m/s headwind. Under the constant-acceleration assumption, it would take approximately 4.17 seconds and 8.68 metres to accelerate from rest to 15 km/h.

</details>

##### Results across Different Flight Scenarios {#_5-2-4-results-across-different-flight-scenarios}

| Flight scenario | Relative velocity (m/s) | $F_D$ (N) | $\theta$ (°) | Thrust / motor (kgf) |
| --- | ---: | ---: | ---: | ---: |
| Hover in still air | 0.00 | 0.000 | 0.00 | 1.250 |
| 15 km/h, 2 m/s headwind | 6.17 | 1.850 | 2.16 | 1.251 |
| 15 km/h, 2 m/s wind, $a=1\ \mathrm{m/s^2}$ | 6.17 | 1.850 | 7.95 | 1.262 |
| 15 km/h, 3 m/s headwind | 7.17 | 2.498 | 2.92 | 1.252 |
| 15 km/h, no wind, $a=0.5\ \mathrm{m/s^2}$ | 4.17 | 0.844 | 3.90 | 1.253 |
| 15 km/h, no wind, $a=1\ \mathrm{m/s^2}$ | 4.17 | 0.844 | 6.79 | 1.259 |
| 15 km/h, no wind, $a=2\ \mathrm{m/s^2}$ | 4.17 | 0.844 | 12.47 | 1.280 |
| **15 km/h, 12 m/s headwind** | **16.17** | **12.712** | **14.53** | **1.291** |
| **15 km/h, 12 m/s wind, $a=1\ \mathrm{m/s^2}$** | **16.17** | **12.712** | **19.85** | **1.329** |

The calculated thrust requirements for various flight scenarios are summarised in the table above, considering different headwind speeds and acceleration conditions. The results indicate that increasing headwind speed and acceleration leads to higher pitch angles and thrust requirements. Extreme wind conditions were also evaluated to assess the additional thrust demand where 12 m/s is the approximate wind speed that is considered as a “Strong Breeze”, based on the Beaufort Wind Scale [\[15\]](../references#md-ref-15). These results served as a basis for the team when selecting a suitable motor and propeller combination with sufficient thrust reserve.

#### Setting Conservative Thrust Estimate {#_5-3-setting-conservative-thrust-estimate}

The previous thrust calculations primarily considered longitudinal motion, where the UAV pitches forward during cruising and acceleration. However, lateral wind disturbances and manoeuvring may also require additional roll corrections. To account for these conditions, a conservative maximum combined tilt angle of 45° was adopted for preliminary motor and propeller sizing, with the DJI Matrice 350 RTK's maximum pitch angle of 30° used as a reference [\[16\]](../references#md-ref-16). The DJI Matrice 350 RTK was selected as a reference due to its industrial-grade design and comparable weight class.

<MechanicalFigure n="30" src="/report-assets/mechanical-design/dji-matrice-350-rtk-tilt-reference.png" :width="547" :height="412" caption="DJI Matrice 350 RTK. Maximum pitch angle reference reproduced from the supplied report [16]." />

The combined tilt angle, $\beta$, accounts for both pitch ($\theta$) and roll ($\phi$) of the UAV:

$$
\cos\beta=\cos\theta\cos\phi \tag{15}
$$

Assuming a UAV mass of 5 kg, the total weight is:

$$
W=mg=5(9.81)=49.05\ \mathrm{N}
$$

To maintain vertical force equilibrium at the maximum combined tilt angle, the vertical component of the total thrust must balance the UAV's weight. Applying [Equation (5)](#equation-md-5) with $\beta$ as the combined tilt angle:

$$
T_{\mathrm{total}}\cos\beta=mg
$$

Rearranging for the total required thrust:

$$
T_{\mathrm{total}}=\frac{mg}{\cos\beta}
$$

Substituting $\beta=45^\circ$:

$$
T_{\mathrm{total}}=\frac{49.05}{\cos45^\circ}=69.37\ \mathrm{N}
$$

Assuming equal thrust distribution across all four motors, the required thrust per motor is given by [Equation (8)](#equation-md-8):

$$
T_{\mathrm{motor}}=\frac{T_{\mathrm{total}}}{4}
$$

Converting from newtons to kilogram-force:

$$
T_{\mathrm{motor}}=\frac{69.37}{4(9.81)}\approx1.768\ \mathrm{kgf}
$$

Based on the calculations, a maximum combined tilt angle of 45° requires a total thrust of 69.37 N, equivalent to approximately 1.768 kgf per motor. This value was taken into consideration when evaluating suitable motor and propeller combinations.



#### Motors and Propellers Evaluation {#_5-4-motors-and-propellers-evaluation}

Based on the calculations and estimates conducted, a target thrust-to-weight ratio of 2:1 was adopted to provide sufficient thrust reserve for wind disturbance rejection, manoeuvrability, control authority, and future payload accommodation. For an estimated UAV mass of 5 kg, this corresponds to a minimum required maximum thrust capability of approximately 2.5 kgf per motor. Following a review of commercially available motors, two potential motor options, the T-Motor MN501-S KV360 and MAD 5005 IPE KV440, were shortlisted for further evaluation based on their thrust capabilities and performance characteristics.

<div class="cv-figure-grid">

<MechanicalFigure n="31" src="/report-assets/mechanical-design/t-motor-mn501-s-kv360.png" :width="415" :height="386" caption="T-Motor MN501-S KV360." />

<MechanicalFigure n="32" src="/report-assets/mechanical-design/mad-5005-ipe-kv440.png" :width="441" :height="393" caption="MAD 5005 IPE KV440 motor." />

</div>

<details class="mechanical-flight-case" id="t-motor-mn501-s-kv360-with-17-inch-propellers">
<summary>5.4.1 T-Motor MN501-S KV360 with 17-inch Propellers</summary>

The T-Motor MN501-S KV360 paired with 17-inch propellers was evaluated based on its thrust capability and power consumption. Using the manufacturer's performance data [\[17\]](../references#md-ref-17), linear interpolation was performed to estimate the motor's operating characteristics at the required thrust of 1.251 kgf per motor under the expected cruising condition of 15 km/h with a 2 m/s headwind.

The manufacturer's performance data for the MN501-S KV360 with P17×5.8-inch propellers gives the following values at the two nearest thrust points [\[17\]](../references#md-ref-17).

| Parameter | 48% throttle | 50% throttle |
| --- | ---: | ---: |
| Thrust (kgf) | 1.185 | 1.256 |
| Current (A) | 6.10 | 6.66 |
| Power (W) | 148 | 162 |

The general linear interpolation equation is:

$$
y=y_1+\frac{x-x_1}{x_2-x_1}(y_2-y_1) \tag{16}
$$

For the required thrust of 1.251 kgf:

**Throttle:**

$$
48+\frac{1.251-1.185}{1.256-1.185}(50-48)\approx49.86\%
$$

**Power consumption:**

$$
148+\frac{1.251-1.185}{1.256-1.185}(162-148)\approx161.01\ \mathrm{W}
$$

**Current draw:**

$$
6.10+\frac{1.251-1.185}{1.256-1.185}(6.66-6.10)\approx6.62\ \mathrm{A}
$$

The interpolated results indicate a throttle setting of approximately 49.9%, with an estimated power consumption of 161.01 W and current draw of 6.62 A per motor. Furthermore, the motor has a maximum thrust capability of 3.837 kgf, corresponding to an overall thrust-to-weight ratio of approximately 3.07:1 for the estimated 5 kg UAV. This exceeds the target thrust-to-weight ratio of 2:1, indicating that the motor provides sufficient thrust reserve for the intended operating conditions.

$$
\text{Thrust-to-weight ratio}=\frac{4(3.837)}{5}=3.0696\approx3.07:1
$$

</details>

<details class="mechanical-flight-case" id="mad-5005-ipe-kv440-with-14-inch-propellers">
<summary>5.4.2 MAD 5005 IPE KV440 with 14-inch Propellers</summary>

The MAD 5005 IPE KV440 paired with 14-inch propellers was similarly evaluated based on its thrust capability and power consumption. Using the manufacturer's performance data, linear interpolation was performed to estimate the motor's operating characteristics at similar operating conditions [\[18\]](../references#md-ref-18).

The manufacturer's performance table provides the following values:

| Parameter | 65% throttle | 70% throttle |
| --- | ---: | ---: |
| Thrust (kgf) | 1.171 | 1.365 |
| Current (A) | 6.56 | 7.98 |
| Input power (W) | 156.3 | 190.0 |

For the required thrust of 1.251 kgf, using [Equation (16)](#equation-md-16):

**Throttle:**

$$
65+\frac{1.251-1.171}{1.365-1.171}(70-65)\approx67.06\%
$$

**Power consumption:**

$$
156.3+\frac{1.251-1.171}{1.365-1.171}(190.0-156.3)\approx170.20\ \mathrm{W}
$$

**Current draw:**

$$
6.56+\frac{1.251-1.171}{1.365-1.171}(7.98-6.56)\approx7.15\ \mathrm{A}
$$

The interpolated results indicate a throttle setting of approximately 67.1%, with an estimated power consumption of 170.2 W and current draw of 7.15 A per motor. In addition, the motor has a maximum thrust capability of 2.568 kgf, corresponding to an overall thrust-to-weight ratio of approximately 2.05:1 for the estimated 5 kg UAV, which also satisfies the 2:1 thrust-to-weight ratio.

$$
\text{Thrust-to-weight ratio}=\frac{4(2.568)}{5}=2.0544\approx2.05:1
$$

</details>

##### Motors Comparison {#_5-4-3-motors-comparison}

Following the evaluation of both motor options as shown in the table below, the MAD 5005 IPE KV440 was selected for the UAV design. Although the T-Motor MN501-S KV360 demonstrated slightly lower power consumption during cruising, the MAD motor offered several advantages in terms of size, weight, and cost. Firstly, its smaller 14-inch propellers allow for a more compact UAV frame. Secondly, the MAD motor is lighter and more cost-effective, while still satisfying the target thrust-to-weight ratio of 2:1. Lastly, its IP35 water-resistance rating provides a degree of protection against water exposure, making it suitable for the intended outdoor operating conditions. Considering these factors, the MAD 5005 IPE KV440 was selected as the more suitable motor for our proposed UAV design.

<div class="mechanical-motor-comparison">

| Parameter | T-Motor MN501-S KV360 | MAD 5005 IPE KV440 — Selected |
| --- | --- | --- |
| Cost (USD) | $99.90 | $72.00 |
| Propeller Size | 17 × 5.8 inch | 14 × 4.8 inch |
| Motor Weight | 170 g | 108 g |
| Maximum Thrust | 3.837 kgf | 2.568 kgf |
| Thrust-to-Weight Ratio | 3.07:1 | 2.05:1 |
| Cruise Power (per motor) | 161.01 W | 170.2 W |
| Water Resistance | IP45 (Water-Resistant) | IP35 (Water-Resistant) |

</div>

#### Differential Motor Thrust Calculation {#_5-5-differential-motor-thrust-calculation}

The initial thrust calculations assumed equal thrust distribution across all four motors during flight. However, following the assembly of the UAV prototype in SolidWorks, the centre of gravity (CG) and its corresponding distances from the front and rear motors were determined. Based on the assumptions listed below, these values were subsequently used to calculate the differential thrust required between the front and rear motors to maintain pitch equilibrium during constant-speed cruise. The thrust and tilt angles used were obtained from [the preliminary thrust calculations](#_5-2-preliminary-thrust-calculations) for each respective scenario.

Assumptions:

- Left and right motors within each pair are assumed to produce equal thrust; roll and yaw corrections are neglected.
- Aerodynamic pitching moments are neglected.
- All motor thrust axes are assumed to be parallel and perpendicular to the motor mounting plane.
- Total thrust is evaluated at the specified flight condition; transient variations are neglected.

<MechanicalFigure n="33" src="/report-assets/mechanical-design/differential-motor-thrust-fbd.png" :width="1226" :height="541" caption="FBD of UAV with Differential Motor Thrust." />

<details class="mechanical-flight-case" id="thrust-distribution-during-constant-speed-cruise">
<summary>5.5.1 Thrust Distribution During Constant-Speed Cruise</summary>

| Parameter | Symbol | Value |
| --- | --- | ---: |
| Cruise pitch angle | $\theta$ | 2.16° |
| Total required thrust | $T$ | 49.085 N |
| Front motor distance to CG (From SolidWorks) | $l_f$ | 0.3167 m |
| Rear motor distance to CG (From SolidWorks) | $l_r$ | 0.3053 m |
| Pitch moment of inertia about CG (From SolidWorks) | $I_{zz}$ | 0.112981 kg·m² |
| Pitch angular acceleration | $\alpha_z$ | 0 rad/s² |

**Total Thrust Equilibrium**

The total thrust generated by the four motors must satisfy the required thrust during constant-speed cruise. Assuming equal thrust between the left and right motors within each pair:

$$
2T_{\mathrm{front}}+2T_{\mathrm{rear}}=T \tag{17}
$$

Substituting $T=49.085\ \mathrm{N}$ and dividing by 2:

$$
T_{\mathrm{front}}+T_{\mathrm{rear}}=24.5425\ \mathrm{N}
$$

**Pitch Moment Equilibrium**

Since the UAV maintains a constant pitch angle during cruise, its pitch angular acceleration is assumed to be zero. Applying the rotational equation of motion about the CG:

$$
M_z=I_{zz}\alpha_z \tag{18}
$$

With $\alpha_z=0$, $M_z=0$. Neglecting aerodynamic pitching moments, the front and rear motor thrusts must balance:

$$
M_z=2l_rT_{\mathrm{rear}}-2l_fT_{\mathrm{front}} \tag{19}
$$

Substituting the corresponding distances:

$$
0.6106T_{\mathrm{rear}}-0.6334T_{\mathrm{front}}=0
$$

**Solving for Front and Rear Motor Thrust**

Substituting $T_{\mathrm{front}}=24.5425-T_{\mathrm{rear}}$ into the moment balance:

$$
\begin{aligned}
0&=0.6106T_{\mathrm{rear}}-0.6334(24.5425-T_{\mathrm{rear}})\\
&=1.244T_{\mathrm{rear}}-15.5452
\end{aligned}
$$

Hence, the required thrust per motor is:

$$
\begin{aligned}
T_{\mathrm{rear}}&\approx12.496\ \mathrm{N}\approx1.274\ \mathrm{kgf}\\
T_{\mathrm{front}}&=24.5425-12.496\\
&\approx12.046\ \mathrm{N}\approx1.228\ \mathrm{kgf}
\end{aligned}
$$

The calculated thrust requirements for constant-speed cruise are summarised below.

| Motor position | Thrust per motor (N) | Thrust per motor (kgf) |
| --- | ---: | ---: |
| Front motors | 12.046 | 1.228 |
| Rear motors | 12.496 | 1.274 |

The results indicate that the rear motors require slightly greater thrust than the front motors to maintain pitch equilibrium during constant-speed cruise. This is because the rear motors are positioned closer to the CG, resulting in a shorter moment arm.

</details>

<details class="mechanical-flight-case" id="thrust-distribution-during-forward-acceleration">
<summary>5.5.2 Thrust Distribution During Forward Acceleration at 1 m/s²</summary>

| Parameter | Symbol | Value |
| --- | --- | ---: |
| Forward acceleration | $a$ | 1 m/s² |
| Required pitch angle | $\theta$ | 7.95° |
| Total required thrust | $T$ | 49.526 N |
| Assumed pitch transition time | $t$ | 1 s |
| Front motor distance to CG (From SolidWorks) | $l_f$ | 0.3167 m |
| Rear motor distance to CG (From SolidWorks) | $l_r$ | 0.3053 m |
| Pitch moment of inertia about CG (From SolidWorks) | $I_{zz}$ | 0.112981 kg·m² |

**Calculation of Angular Acceleration**

The required pitch angle is first converted from degrees to radians:

$$
\Delta\theta=7.95\times\frac{\pi}{180}\approx0.13875\ \mathrm{rad}
$$

Assuming the UAV starts and ends the pitch transition at zero angular velocity, with equal angular acceleration and deceleration phases, the maximum angular acceleration is:

$$
\alpha_{\max}=\frac{4\Delta\theta}{t^2} \tag{20}
$$

Substituting the values:

$$
\alpha_{\max}=\frac{4(0.13875)}{1^2}=0.555\ \mathrm{rad/s^2}
$$

**Calculation of Required Pitching Moment**

Using [Equation (18)](#equation-md-18) and the pitch moment of inertia obtained from SolidWorks:

$$
M_z=0.112981(0.555)\approx0.0627\ \mathrm{N\cdot m}
$$

**Total Thrust Equilibrium**

Using [Equation (17)](#equation-md-17) with $T=49.526\ \mathrm{N}$:

$$
T_{\mathrm{front}}+T_{\mathrm{rear}}=24.763\ \mathrm{N}
$$

**Pitch Moment Balance**

During the nose-down angular acceleration phase, the rear motors must generate a greater pitching moment than the front motors to rotate the UAV forward.

Using [Equation (19)](#equation-md-19) with $M_z=0.0627\ \mathrm{N\cdot m}$:

$$
0.0627=0.6106T_{\mathrm{rear}}-0.6334T_{\mathrm{front}}
$$

Substituting $T_{\mathrm{front}}=24.763-T_{\mathrm{rear}}$:

$$
\begin{aligned}
0.0627&=0.6106T_{\mathrm{rear}}-0.6334(24.763-T_{\mathrm{rear}})\\
&=1.244T_{\mathrm{rear}}-15.6849
\end{aligned}
$$

The maximum rear motor thrust and corresponding front motor thrust during nose-down angular acceleration are:

$$
\begin{aligned}
T_{\mathrm{rear}}&\approx12.659\ \mathrm{N}\approx1.290\ \mathrm{kgf}\\
T_{\mathrm{front}}&=24.763-12.659\\
&\approx12.104\ \mathrm{N}\approx1.234\ \mathrm{kgf}
\end{aligned}
$$

The calculated thrust requirements during the nose-down angular acceleration phase are summarised below.

| Motor position | Thrust per motor (N) | Thrust per motor (kgf) |
| --- | ---: | ---: |
| Front motors | 12.104 | 1.234 |
| Rear motors | 12.659 | 1.290 |

</details>


</div>

### Propeller Arm Selection {#propeller-arm-selection}

This section focuses on the selection of an appropriate tube diameter and wall thickness for the UAV's CFRP propeller arms. The selection process considers the structural strength, stiffness, weight and vibration characteristics of different tube configurations to determine a suitable design that minimises weight while maintaining structural integrity during flight.

<div class="mechanical-propulsion">

#### Bending Stress Calculation {#bending-stress-calculation}

To evaluate the structural integrity of the CFRP propeller arms, a simplified beam model was used to determine the reaction forces at the clamp supports and the maximum bending moment induced by motor thrust. The FBD drawn represents how the propeller arm would be clamped based on the FOD Argus prototype design.

<MechanicalFigure n="34" src="/report-assets/mechanical-design/propeller-arm-loading-fbd.png" :width="1354" :height="672" caption="FBD of Propeller Arm Loading." />

Assumptions:

- Clamp support forces are treated as point reactions.
- Motor thrust is treated as a concentrated point load.
- Beam bending is assumed to be two-dimensional and linear.

Taking moments about clamp A:

$$
\begin{aligned}
\sum M_A&=0\\
R_Bs-Fa&=0
\end{aligned}
$$

$$
R_B=\frac{Fa}{s} \tag{21}
$$

Applying vertical force equilibrium:

$$
\begin{aligned}
\sum F_y&=0\\
F-R_A+R_B&=0\\
R_A&=F+R_B
\end{aligned}
$$

$$
R_A=F\left(1+\frac{a}{s}\right) \tag{22}
$$

The bending moment is evaluated across two sections of the propeller arm. From the motor to clamp A ($0\leq x\leq a$):

$$
M_1(x)=Fx \tag{23}
$$

From clamp A to clamp B ($a\leq x\leq a+s$):

$$
M_2(x)=Fx-R_A(x-a) \tag{24}
$$

$$
M_2(x)=Fx-F\left(1+\frac{a}{s}\right)(x-a)
$$

The maximum bending moment occurs at clamp A, where $x=a$.

$$
|M_{\max}|=Fa \tag{25}
$$

<MechanicalFigure n="35" src="/report-assets/mechanical-design/hollow-cfrp-tube-cross-section.png" :width="680" :height="556" caption="Cross-sectional area of a hollow circular carbon-fibre tube." />

The maximum bending stress can subsequently be determined using the flexure formula:

$$
\sigma_{\max}=\frac{M_{\max}c}{I} \tag{26}
$$

For a hollow circular CFRP tube:

$$
I=\frac{\pi}{64}\left(D_o^4-D_i^4\right) \tag{27}
$$

Here, $D_o$ and $D_i$ represent the outer and inner tube diameters, respectively, and:

$$
c=\frac{D_o}{2}
$$

$$
\sigma_{\max}=\frac{32FaD_o}{\pi\left(D_o^4-D_i^4\right)}
$$

#### Beam Deflection Calculation {#beam-deflection-calculation}

The motor-end bending deflection was calculated using Euler–Bernoulli beam theory. A Young's modulus of 123 GPa, obtained from the manufacturer's Toray T300 carbon fibre datasheet, was adopted for the preliminary calculation [\[19\]](../references#md-ref-19).

<MechanicalFigure n="36" src="/report-assets/mechanical-design/propeller-arm-bending-deflection.png" :width="1381" :height="415" caption="Diagram illustrating deflection for a propeller arm." />

The motor-end deflection is calculated using:

$$
\delta_{\mathrm{motor}}=\frac{Fa^2(a+s)}{3EI} \tag{28}
$$

| Parameter | Symbol | Value / definition |
| --- | --- | --- |
| Maximum motor thrust force | $F$ | N |
| Motor-to-clamp A distance | $a$ | 0.219 m |
| Distance between clamps | $s$ | 0.055 m |
| Young's modulus | $E$ | $123\times10^9\ \mathrm{Pa}$ |
| Second moment of area of the hollow circular tube | $I$ | [Equation (27)](#equation-md-27), m⁴ |

#### Natural Bending Frequency Calculation {#natural-bending-frequency-calculation}

<MechanicalFigure n="37" src="/report-assets/mechanical-design/cantilever-bending-modes.png" :width="546" :height="366" caption="Figure showing the different bending modes, reproduced from the supplied report; the original illustration source was not provided." />

The natural bending frequency of different CFRP propeller arm configurations was evaluated to minimise the risk of resonance, which could affect the performance of the UAV's onboard sensors. Based on the ArduPilot documentation, motor rotational frequency was identified as a common source of vibration in multirotor UAVs [\[20\]](../references#md-ref-20).

Using the manufacturer's motor performance datasheet, the motor rotational frequency and blade passing frequency ranges were determined from hover to maximum thrust. These frequency ranges were subsequently used to evaluate the suitability of different CFRP arm configurations. For preliminary calculations, only the first bending mode was considered.

**Motor rotational frequency**

The motor rotational frequency is calculated using the motor speed in revolutions per minute (RPM):

$$
f_{\mathrm{motor}}=\frac{\mathrm{RPM}}{60} \tag{29}
$$

Based on the MAD 5005 KV440 motor performance datasheet with 14-inch propellers, the rotational frequencies at hover and maximum thrust are calculated as follows.

**Blade passing frequency**

The blade passing frequency (BPF) represents the frequency at which propeller blades pass a fixed reference point. For a two-bladed propeller:

$$
f_{\mathrm{BPF}}=2f_{\mathrm{motor}} \tag{30}
$$

| Frequency | Hover | Maximum thrust |
| --- | ---: | ---: |
| Motor rotational frequency | 96.88 Hz | 136.03 Hz |
| Blade passing frequency | 193.76 Hz | 272.06 Hz |

**First bending natural frequency of CFRP arm**

The first bending natural frequency of the CFRP propeller arm was estimated using a simplified cantilever beam model, with the motor and propeller represented as a concentrated mass at the free end. The distributed mass of the unsupported arm section was also considered in the calculation.

$$
f_{n,1}=\frac{1}{2\pi}\sqrt{\frac{3EI}{a^3\left(m_{\mathrm{tip}}+0.236m_{\mathrm{arm}}\right)}} \tag{31}
$$

The parameters used are summarised below.

| Parameter | Symbol | Value |
| --- | --- | --- |
| Flexural modulus | $E$ | $123\times10^9\ \mathrm{Pa}$ |
| Second moment of area | $I$ | Tube-dependent (m⁴) |
| Effective cantilever length | $a$ | 0.219 m |
| Motor and propeller mass (obtained from manufacturer datasheet) | $m_{\mathrm{tip}}$ | 0.1272 kg |
| Mass of unsupported arm section (obtained from SolidWorks) | $m_{\mathrm{arm}}$ | Tube-dependent (kg) |

The mass of the unsupported 219 mm section is calculated using:

$$
m_{\mathrm{arm}}=\rho Aa \tag{32}
$$

For a hollow circular CFRP tube, the cross-sectional area is:

$$
A=\frac{\pi}{4}\left(D_o^2-D_i^2\right) \tag{33}
$$

$$
m_{\mathrm{arm}}=\rho\frac{\pi}{4}\left(D_o^2-D_i^2\right)(0.219)
$$

Here, $\rho$ is the density of the CFRP tube (kg/m³), and $D_o$ and $D_i$ are the outer and inner tube diameters in metres, as defined in [the bending stress calculation](#bending-stress-calculation). The second moment of area is calculated using [Equation (27)](#equation-md-27):

$$
I=\frac{\pi}{64}\left(D_o^4-D_i^4\right)
$$

#### Evaluation of Different Beam Configurations {#evaluation-of-different-beam-configurations}

The propeller arm configurations were evaluated based on their structural performance, natural bending frequency and mass. To minimise the risk of resonance while maintaining a lightweight design, the following selection criteria were established:

1. The first bending natural frequency must fall outside the motor rotational frequency range of 96.88–136.03 Hz.
2. The first bending natural frequency must fall outside the blade passing frequency range of 193.76–272.06 Hz.
3. The lightest configuration satisfying both frequency criteria will be selected.

Based on these criteria, the 20 mm outer diameter with 1.5 mm wall thickness CFRP tube was selected, as it satisfies both frequency requirements while having the lowest mass among the qualifying configurations.

<div class="mechanical-arm-comparison">
<table>
<thead><tr><th scope="col">Outer Diameter (mm)</th><th scope="col">Wall Thickness (mm)</th><th scope="col">SolidWorks Mass (g)</th><th scope="col">Stress (MPa)</th><th scope="col">Deflection (mm)</th><th scope="col">First Bending Natural Frequency (Hz)</th><th scope="col">Selection</th></tr></thead>
<tbody>
<tr class="arm-rejected"><td>16</td><td>1.5</td><td>42.36</td><td>24.32</td><td>0.494</td><td>109.7</td><td>Rejected</td></tr>
<tr class="arm-rejected"><td>16</td><td>2.0</td><td>54.54</td><td>20.07</td><td>0.408</td><td>119.8</td><td>Rejected</td></tr>
<tr class="arm-selected"><td>20</td><td>1.5</td><td>54.05</td><td>14.70</td><td>0.239</td><td>156.6</td><td>Selected</td></tr>
<tr class="arm-considered"><td>20</td><td>2.0</td><td>70.12</td><td>11.90</td><td>0.193</td><td>172.4</td><td>Considered, not selected</td></tr>
<tr class="arm-considered"><td>22</td><td>1.5</td><td>59.89</td><td>11.90</td><td>0.176</td><td>181.9</td><td>Considered, not selected</td></tr>
<tr class="arm-rejected"><td>22</td><td>2.0</td><td>77.91</td><td>9.57</td><td>0.141</td><td>200.7</td><td>Rejected</td></tr>
</tbody>
</table>
</div>

Red indicates configurations rejected because their first bending natural frequency falls within either the motor rotational frequency range (16 × 1.5 mm and 16 × 2.0 mm) or the blade passing frequency range (22 × 2.0 mm). Yellow indicates configurations satisfying both frequency criteria but having greater mass than the selected configuration. Green indicates the selected 20 × 1.5 mm CFRP tube, which satisfies both frequency criteria while minimising mass.

</div>

## A6. Discussion of Problems and Project Plan {#a6-problems-project-plan}

The [first and second design iterations](#design-iterations) describe the limitations encountered and the changes made. Physical verification and dated next-stage milestones remain to be documented.

</div>

<style>
.mechanical-arm-comparison .arm-rejected{--arm-row-bg:#f9e8e8;--arm-row-text:#742929;--arm-row-border:#ddbaba}
.mechanical-arm-comparison .arm-selected{--arm-row-bg:#e3f3e8;--arm-row-text:#17492d;--arm-row-border:#a5cbb2;font-weight:600}
.mechanical-arm-comparison .arm-considered{--arm-row-bg:#fbf3d7;--arm-row-text:#604b10;--arm-row-border:#d8ca96}
.dark .mechanical-arm-comparison .arm-rejected{--arm-row-bg:#3e2529;--arm-row-text:#fbdcdd;--arm-row-border:#795057}
.dark .mechanical-arm-comparison .arm-selected{--arm-row-bg:#183b2a;--arm-row-text:#d6f5df;--arm-row-border:#46765a}
.dark .mechanical-arm-comparison .arm-considered{--arm-row-bg:#3b331d;--arm-row-text:#f6e9b5;--arm-row-border:#786b40}
.vp-doc .mechanical-arm-comparison table tbody td{background:var(--arm-row-bg);color:var(--arm-row-text);border-color:var(--arm-row-border);text-align:right;font-variant-numeric:tabular-nums}
.vp-doc .mechanical-arm-comparison table tbody td:last-child{text-align:left}
.vp-doc .mechanical-motor-comparison table td{background:#f7f8fa;color:#24303b}
.dark .vp-doc .mechanical-motor-comparison table td{background:#18202a;color:#e1e6ef}
.vp-doc .mechanical-motor-comparison table :is(th,td):nth-child(3){background:#e3f3e8;color:#17492d;border-color:#a5cbb2}
.vp-doc .mechanical-motor-comparison table th:nth-child(3){background:#cee9d8;font-weight:700}
.dark .vp-doc .mechanical-motor-comparison table :is(th,td):nth-child(3){background:#183b2a;color:#d6f5df;border-color:#46765a}
.dark .vp-doc .mechanical-motor-comparison table th:nth-child(3){background:#224d36;color:#e5ffed}
.mechanical-flight-case{margin:20px 0;padding:0 20px;border:1px solid var(--vp-c-divider);border-radius:12px;background:var(--vp-c-bg-soft)}
.mechanical-flight-case>summary{padding:18px 0;cursor:pointer;font-size:1em;font-weight:600;line-height:1.6;overflow-wrap:break-word}
.mechanical-flight-case>summary:focus-visible{outline:2px solid var(--vp-c-brand-1);outline-offset:4px;border-radius:4px}
.mechanical-flight-case[open]>summary{border-bottom:1px solid var(--vp-c-divider);margin-bottom:20px}
@media(max-width:600px){.mechanical-flight-case{padding:0 12px}}
.mechanical-propulsion .mechanical-equation-math{padding:12px 2px;overflow-y:hidden}
.mechanical-propulsion mtable{border-spacing:0}
.mechanical-propulsion mtd{padding:.2em 0;text-align:left}
.mechanical-propulsion mtd:first-child{text-align:right;padding-right:.25em}
.mechanical-propulsion mtr + mtr mtd{padding-top:.65em}
.mechanical-equation{position:relative;display:flex;align-items:center;justify-content:center;gap:12px;margin:24px 0;padding:8px 36px;color:var(--vp-c-text-1)}
.mechanical-equation-math{min-width:0;max-width:100%;overflow-x:auto;padding:4px 0;user-select:text}
.mechanical-equation math{font-size:1.15em;white-space:nowrap}
/* Native MathML needs explicit cell alignment for the three-line derivation. */
#equation-md-4{margin:16px 0;padding-top:0;padding-bottom:0}
#equation-md-4 mtable{border-spacing:0}
#equation-md-4 mtd{padding:.2em 0;text-align:left}
#equation-md-4 mtd:first-child{text-align:right;padding-right:.25em}
#equation-md-4 mtr:last-child mtd{padding-top:.65em}
.mechanical-equation-number{position:absolute;right:0;top:50%;transform:translateY(-50%);font-size:14px}
@media(max-width:600px){.mechanical-equation{padding:8px 27px;gap:6px}.mechanical-equation math{font-size:.88em}}
</style>
