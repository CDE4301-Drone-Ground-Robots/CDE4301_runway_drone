---
title: "Mechanical Design"
outline: false
prev: false
next: false
---

<script setup>
import MechanicalFigure from './components/MechanicalFigure.vue'
import UAVTiltThrustSimulator from '../.vitepress/theme/components/UAVTiltThrustSimulator.vue'
</script>

<div class="cv-report">

<p class="chapter-kicker">FOD ARGUS / MECHANICAL DESIGN</p>

# Mechanical Design

<SubsystemLead class="cv-report-byline" name="Muruganantham Arun" matric="A0308280J" portrait="/team/Arun.png" />

## Overview of Mechanical Design of the UAV

Initial requirements were established to guide the mechanical design of the UAV. Additional considerations, including vibration management and manufacturability, were identified as the design progressed. The table below summarises the requirements and considerations intended for the final design.

| Design Requirements | Description |
| --- | --- |
| Component integration | Accommodate all required components with secure mounting and sufficient space for wiring and connections. |
| Low overall mass | Minimise the UAV’s total takeoff mass to below 7 kg to avoid the CAAS requirement for a UA Pilot Licence [\[1\]](../references#md-ref-1). Lower mass also reduces the thrust and propulsion power required, supporting longer flight endurance. |
| Structural strength and stiffness | Withstand thrust, component loads and landing forces without failure or excessive deformation. |
| Balanced mass distribution | Position components to keep the centre of gravity close to the centre of the motors. |
| Unobstructed sensors and camera fields of view | Ensure the airframe and landing gear do not obstruct the cameras and ranging sensors. |
| Vibration management | Reduce vibration transmitted to the flight controller and cameras. |
| Thermal management | Provide adequate ventilation and cooling for heat-generating electronics. |
| Manufacturability | Ensure that the design is feasible and practical for fabrication with available materials, equipment and processes. |
| Water resistance | Ensure reliable UAV operation under adverse weather conditions, particularly during light rainfall. |

### Initial Concept Sketch

<MechanicalFigure n="1" src="/report-assets/mechanical-design/initial-concept-sketch.png" :width="1150" :height="863" caption="Initial Concept Sketch" />

An initial concept sketch was developed to provide a foundation for the UAV’s mechanical design. Rather than prescribing the exact geometry, it established a layered layout in which different components were allocated to each level. This arrangement guided subsequent design iterations while allowing flexibility in the detailed design. Furthermore, a quadcopter configuration was selected as a suitable balance between lifting capability, structural simplicity and overall mass, which was targeted to be below 7 kg as mentioned above. Using four motors reduced the number of propulsion components and associated mounting structures compared with six- or eight-rotor configurations. The motors and propellers were subsequently selected to provide sufficient thrust and control margin for the estimated takeoff mass.

### Plus vs X vs H Propeller Configuration

<MechanicalFigure n="2" src="/report-assets/mechanical-design/propeller-configurations.png" :width="750" :height="279" caption="Different Propeller Configurations" />

The X configuration was selected over the plus configuration due to its improved attitude control authority and reduced coupling between pitch/roll and yaw dynamics. According to a comparative analysis of a quadcopter in plus and cross configurations [\[2\]](../references#md-ref-2), although both configurations exhibit similar hover power requirements and autonomous stability characteristics, the cross configuration provides up to √2 greater pitch and roll control authority because all four rotors contribute to attitude moments. This improved control authority is advantageous for runway inspection operations where the UAV may experience external disturbances such as wind gusts.

The H configuration was considered, but its limitations in accommodating larger propellers made the X configuration more desirable. Extending the arms diagonally increases motor spacing in both longitudinal and lateral directions. In comparison, an H-frame arrangement would require additional longitudinal extension to prevent propeller overlap.

### Pusher vs Puller Configuration

<div class="cv-figure-grid">

<MechanicalFigure n="3" src="/report-assets/mechanical-design/pusher-configuration.png" :width="350" :height="302" caption="Pusher Configuration" />

<MechanicalFigure n="4" src="/report-assets/mechanical-design/puller-configuration.png" :width="658" :height="493" caption="Puller Configuration" />

</div>

A puller configuration, with the propellers positioned above the motors and supporting arms, was selected for the UAV. A comparative CFD study reported higher thrust generation for the puller configurations under the conditions investigated [\[3\]](../references#md-ref-3). This arrangement also provides greater propeller ground clearance and reduces the potential for interference with the field of view of the forward-facing thermal camera mounted beneath the body. These considerations supported its suitability for the proposed mechanical layout.

## Design Iterations

The UAV’s mechanical design underwent two preliminary iterations before arriving at the final prototype design. Each iteration refined the component layout and structural arrangement to address the design requirements and issues identified during development.

### First Iteration

<MechanicalFigure n="5" src="/report-assets/mechanical-design/first-iteration-structural-body.png" :width="1380" :height="688" caption="Structural body design for the first iteration" />

<MechanicalFigure n="6" src="/report-assets/mechanical-design/first-iteration-layered-section.png" :width="1381" :height="699" caption="Layered design approach from concept sketch (Sectioned View)" />

<div class="cv-figure-grid">

<MechanicalFigure n="7" src="/report-assets/mechanical-design/first-iteration-bottom-layer.png" :width="609" :height="434" caption="Bottom Layer" />

<MechanicalFigure n="8" src="/report-assets/mechanical-design/first-iteration-top-layer.png" :width="631" :height="428" caption="Top Layer" />

</div>

<MechanicalFigure n="9" src="/report-assets/mechanical-design/propeller-arm.png" :width="633" :height="527" caption="Propeller Arm" />

The first design iteration retained the layered approach established in the concept sketch shown above, focusing on the two central component layers between the RTK-GNSS antenna layer above and camera layer below. As this was a preliminary design, the first layer containing the antenna and the fourth layer housing the cameras were not yet incorporated. The top layer included mounting holes for securing an acrylic plate to support electronic components, while the bottom layer was intended to accommodate the battery, Jetson onboard computer and other key electrical components. The propeller arms were designed with the intention to withstand the bending moments generated by motor thrust and component weight while minimising structural mass.

#### Limitations

The first iteration prioritised component arrangement and structural geometry, with less consideration given to the eventual material selection and manufacturing process. The complex geometry of the top layer structure and the propeller arms was more suited for 3D-printing. However, subsequent research identified carbon-fibre-reinforced polymer (CFRP) as a suitable material for the UAV’s primary structure due to its high stiffness and strength relative to mass [\[4\]](../references#md-ref-4) [\[5\]](../references#md-ref-5) [\[8\]](../references#md-ref-8). Adapting the initial design for CFRP would require custom moulding or substantial changes to accommodate standard sheets and tubes, prompting a revision of the geometry and assembly approach.

#### CFRP Sheets & Tubes vs 3D-Printed Parts

As discussed in the previous section, CFRP offers a higher strength-to-weight ratio than conventional 3D-printed polymers, making it suitable for the UAV’s primary structure. This is particularly important for supporting an estimated takeoff mass of 4–6 kg and withstanding the loads generated by motor thrust while minimising structural mass.

In addition, CFRP offers potential benefits for vibration management. An experiment demonstrated reduced vibration amplitudes in a CFRP motor frame compared with an aluminium-alloy frame [\[7\]](../references#md-ref-7). This characteristic is relevant to our application, where limiting camera vibration is important for maintaining image clarity during FOD detection and minimising interference with the flight controller's inertial sensor measurements.

### Second Iteration

<MechanicalFigure n="10" src="/report-assets/mechanical-design/second-iteration-structural-body.png" :width="1073" :height="751" caption="Structural body design for the second iteration" />

<MechanicalFigure n="11" src="/report-assets/mechanical-design/second-iteration-layered-section.png" :width="1066" :height="790" caption="Layered design approach from concept sketch (Sectioned View)" />

To address the material and manufacturing limitations of the first iteration, the second design retained the layered layout while adapting the structure for CFRP fabrication. The previously proposed 3D-printed propeller arms were replaced with carbon-fibre tubes, and the top and bottom body structures were simplified for fabrication in CFRP. These changes aimed to improve structural stiffness, strength and vibration management while limiting mass. Custom 3D-printed clamps were used to secure the propeller arms and landing legs to the bottom layer.

#### Limitations

A key limitation of the second iteration was the geometry of the top and bottom body structures. Although intended for CFRP fabrication, each structure had an overall depth of 50 mm, making machining from solid CFRP stock impractical. Producing these features from thick plates would require substantial material removal, resulting in considerable waste, increased machining time and high fabrication costs. Further redesign was therefore needed to accommodate thinner CFRP plates joined using separate supports.

### Final Prototype Design

<MechanicalFigure n="12" src="/report-assets/mechanical-design/final-prototype-cad-assembly.png" :width="1378" :height="665" caption="CAD Assembly of Final Prototype Design" />

<MechanicalFigure n="13" src="/report-assets/mechanical-design/final-prototype-layers.png" :width="734" :height="342" caption="Different Layers of the Prototype Design" />

| Layer / Assembly | Allocated Components |
| --- | --- |
| Top Layer | Pixhawk Flight Controller, Jetson Orin NX, GNSS Antenna and 360° LiDAR |
| Bottom Layer | 12 Ah Battery, Power Distribution Boards, Fuse and Electronic Speed Controllers (ESC) |
| Camera & Sensor Assembly | RGB Camera, Thermal Camera and Single-Point LiDAR |
| Propeller Assembly | Motors and Propellers |

To address the fabrication limitations of the second iteration, the final FOD ARGUS prototype design combines CFRP structural components with 3D-printed parts. CFRP was selected for the main structural components, including the base plates that mount the electrical and key onboard components, motor mounting plates and propeller arms. Its material properties, discussed earlier, and suitability for components with relatively simple geometry address the design requirement for manufacturability. For parts requiring greater geometric complexity and flexibility in customisation, such as enclosures and tube clamps, 3D-printed PETG CF would be used, as it demonstrates better mechanical properties than conventional PETG and PLA filaments [\[9\]](../references#md-ref-9).

## Centre of Gravity (CG) of UAV

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

### 3.1 Horizontal CG Positioning {#horizontal-cg-positioning}

The SolidWorks mass properties give the horizontal displacement of the CG from the geometric centre of the four motors in the X configuration:

$$
d_{CG}=\sqrt{(-5.85)^2+(0.61)^2}=5.88\ \mathrm{mm} \tag{1}
$$

The calculated horizontal offset is approximately 5.88 mm. This relatively small offset limits the additional pitch and roll moments associated with uneven mass distribution, reducing the differential thrust required to maintain level hover. This can preserve more motor control authority for manoeuvres and responses to external disturbances, such as wind gusts.

### 3.2 Vertical CG Positioning {#vertical-cg-positioning}

The SolidWorks assembly places the UAV's CG approximately 40 mm below the propeller plane.

The thesis cited in the source report [\[10\]](../references#md-ref-10) describes how positioning the CG below the propellers can contribute to stability during forward flight and wind disturbances. Aerodynamic drag acting above the CG can generate a stabilising moment opposing an attitude disturbance, as illustrated below.

<MechanicalFigure n="16" src="/report-assets/mechanical-design/vertical-cg-stability-reference.png" :width="1040" :height="378" caption="Influence of vertical CG positioning on multicopter stability. External thesis illustration reproduced in the supplied report [10]; bibliographic details were not supplied." />

FOD ARGUS incorporates a lower CG through the arrangement of its onboard components, particularly the battery. This configuration may contribute to a stabilising aerodynamic response if the resultant aerodynamic forces act above the CG. Overall stability remains dependent on the flight control system, and flight testing is required to evaluate the effectiveness of this arrangement.

## Placement of Key Onboard Components

The placement of key onboard components supports flight stability and operational requirements. The flight controller, cameras and other electronics were positioned with consideration of mass distribution, accessibility, vibration isolation and electrical connectivity.

### 4.1 Central Alignment of GNSS Antenna and RGB Camera {#central-alignment-of-gnss-antenna-and-rgb-camera}

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

### 4.2 Placement of the Pixhawk Flight Controller near Centre of Gravity {#placement-of-the-pixhawk-flight-controller-near-centre-of-gravity}

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

### 4.3 Placement of the 360° LiDAR {#placement-of-the-360-lidar}

The 360° LiDAR was initially intended to be mounted centrally on the top plate. However, this position was prioritised for the GNSS antenna to maintain its central alignment with the RGB camera, so the LiDAR was relocated towards the front. It is intended to support obstacle detection and avoidance, as discussed in the [Computer Vision section](./computer-vision#thermal-safety). This placement aims to minimise obstruction of the LiDAR's scanning field by surrounding onboard components while maintaining sufficient clearance from the propellers and structural elements.

<MechanicalFigure n="22" src="/report-assets/mechanical-design/lidar-front-isometric-view.png" :width="916" :height="586" caption="Front placement of the 360° LiDAR in the isometric view (project CAD)." />

### 4.4 45° Placement of the Thermal Camera {#45-degree-placement-of-the-thermal-camera}

The thermal camera is mounted at approximately 45° using a rigid, custom-designed mount that will be 3D-printed. This arrangement allows the thermal camera to complement the 360° LiDAR for obstacle detection. Further details of the planned sensor integration for obstacle detection and avoidance are discussed in the [Computer Vision section](./computer-vision#thermal-safety).

<MechanicalFigure n="23" src="/report-assets/mechanical-design/thermal-camera-side-view.png" :width="928" :height="392" caption="Placement of the thermal camera in the side view (project CAD)." />

### 4.5 Placement of Batteries and Other Electrical Components in the Bottom Layer {#placement-of-batteries-and-other-electrical-components-in-the-bottom-layer}

The batteries and other electrical components, particularly the Electronic Speed Controllers (ESCs), were positioned on the bottom layer of the UAV. As the batteries contribute significantly to the overall mass of the UAV as it is the heaviest component, weighing approximately 1.5kg, their placement in the lower section helps lower the CG, as discussed in [Section 3](#centre-of-gravity-cg-of-uav).

For the ESCs, although some multirotor designs mount them externally along the propeller arms, the FOD Argus prototype adopts an internal mounting configuration within the bottom layer. This arrangement provides additional protection against direct exposure to water and environmental conditions, particularly since the selected AMPX 40A ESCs do not have a specified waterproof rating.

However, with the planned integration of the Raspberry Pi into the bottom layer, spatial constraints may require the ESCs to be relocated externally. If necessary, 3D printed protective enclosures will be designed to provide water resistance.

## Motor & Propellers Selection


### Interactive UAV Attitude & Thrust Simulator

<UAVTiltThrustSimulator />

This interactive visualisation supports preliminary thrust sizing for an X-configuration quadcopter. It assumes constant altitude with no vertical acceleration, thrust aligned with the body thrust axis, and no aerodynamic disturbances or additional forces. The per-motor value is the average obtained by sharing the total thrust equally across four motors; actual individual thrust can differ as the flight controller generates pitch, roll and yaw moments. This is an idealised steady-altitude calculation, not a full six-degree-of-freedom flight dynamics simulation.

</div>

<style>
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
