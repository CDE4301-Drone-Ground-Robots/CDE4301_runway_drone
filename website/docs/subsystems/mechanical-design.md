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

### Interactive UAV Attitude & Thrust Simulator

<UAVTiltThrustSimulator />

This interactive visualisation supports preliminary thrust sizing for an X-configuration quadcopter. It assumes constant altitude with no vertical acceleration, thrust aligned with the body thrust axis, and no aerodynamic disturbances or additional forces. The per-motor value is the average obtained by sharing the total thrust equally across four motors; actual individual thrust can differ as the flight controller generates pitch, roll and yaw moments. This is an idealised steady-altitude calculation, not a full six-degree-of-freedom flight dynamics simulation.

</div>
