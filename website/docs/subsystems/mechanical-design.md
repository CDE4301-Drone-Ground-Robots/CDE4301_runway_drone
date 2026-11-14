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
import MechanicalVideo from './components/MechanicalVideo.vue'
import UAVTiltThrustSimulator from '../.vitepress/theme/components/UAVTiltThrustSimulator.vue'
</script>

<div class="cv-report rubric-report" style="--report-chapter: '1'">

<p class="chapter-kicker">FOD ARGUS / MECHANICAL DESIGN</p>

# 1. Mechanical Design {#mechanical-design}

<SubsystemLead class="cv-report-byline" name="Muruganantham Arun" matric="A0308280J" portrait="/team/Arun.png" />

## 1.1 Objective and Requirements {#a1-objective-scope-context}

<span id="objectives-scope-design-requirements" class="report-anchor" aria-hidden="true"></span>

### 1.1.1 Mechanical Design Objectives and Scope {#overview-of-mechanical-design-of-the-uav}

The objective is to design a lightweight UAV structure that supports the inspection payload.

Initial requirements were established to guide the mechanical design of the UAV. Additional considerations, including vibration management and manufacturability, were identified as the design progressed. The table below summarises the requirements and considerations intended for the final design.

### 1.1.2 Mechanical Design Requirements and Considerations {#mechanical-design-requirements-considerations}

<p class="report-table-caption" id="table-5"><strong>Table 5.</strong> Mechanical Design Requirements and Considerations</p>

| Design Requirements | Description |
| --- | --- |
| Component integration | Accommodate all required components with secure mounting and sufficient space for wiring and connections. |
| Low overall mass | Minimise the UAV's total mass to reduce the thrust and propulsion power required, allowing for smaller motor and propeller combinations while improving flight endurance and not compromising the UAV's structural integrity or essential functionalities. CAAS regulations were also considered, with a target takeoff mass below 7 kg to facilitate future flight testing [\[14\]](../references#md-ref-1). |
| Structural strength and stiffness | Withstand thrust, component loads and landing forces without failure or excessive deformation. |
| Balanced mass distribution | Position components to keep the centre of gravity close to the centre of the motors. |
| Unobstructed sensors and camera fields of view | Ensure the airframe and landing gear do not obstruct the cameras and ranging sensors. |
| Vibration management | Reduce vibration transmitted to the flight controller and cameras. |
| Thermal management | Provide adequate ventilation and cooling for heat-generating electronics. |
| Manufacturability | Ensure that the design is feasible and practical for fabrication with available materials, equipment and processes. |
| Water resistance | Ensure reliable UAV operation under adverse weather conditions, particularly during light rainfall. |

## 1.2 Mechanical Design and Concept Development {#a2-methodology-concept-development}

<span id="mechanical-design-methodology-development" class="report-anchor" aria-hidden="true"></span>

### 1.2.1 Initial Concept Sketch {#initial-concept-sketch}

<MechanicalFigure number="8" n="1" src="/report-assets/mechanical-design/initial-concept-sketch.png" :width="1150" :height="863" caption="Initial Concept Sketch" />

The initial concept sketch established a layered component layout, guiding subsequent iterations without fixing detailed geometry. A quadcopter balanced lifting capability, structural simplicity and a target takeoff mass below 7 kg. Four motors reduced propulsion components and mounting structures compared with six- or eight-rotor configurations; subsequent motor and propeller selection targeted the required thrust and control margin.

### 1.2.2 UAV Configuration Selection {#uav-configuration-selection}

#### 1.2.2.1 Plus vs X vs H Configuration {#plus-vs-x-vs-h-propeller-configuration}

<MechanicalFigure number="9" n="2" src="/report-assets/mechanical-design/propeller-configurations.png" :width="750" :height="279" caption="Different Propeller Configurations" />

The X configuration was selected over plus for greater attitude control authority and reduced pitch/roll–yaw coupling. A comparative study [\[15\]](../references#md-ref-2) found similar hover power requirements and autonomous stability, but up to √2 greater pitch and roll control authority for X because all four rotors contribute to attitude moments, supporting wind disturbance rejection during runway inspection.

Diagonal arms also increase longitudinal and lateral motor spacing to accommodate larger propellers. An H frame would require additional longitudinal extension to prevent propeller overlap, favouring X.

#### 1.2.2.2 Pusher vs Puller Configuration {#pusher-vs-puller-configuration}

<div class="cv-figure-grid">

<MechanicalFigure number="10" n="3" src="/report-assets/mechanical-design/pusher-configuration.png" :width="350" :height="302" caption="Pusher Configuration" />

<MechanicalFigure number="11" n="4" src="/report-assets/mechanical-design/puller-configuration.png" :width="658" :height="493" caption="Puller Configuration" />

</div>

The selected puller configuration positions propellers above the motors and arms. A comparative CFD study reported higher thrust under the investigated conditions [\[16\]](../references#md-ref-3). It also increases propeller ground clearance and reduces interference with the forward-facing thermal camera's field of view beneath the body.

### 1.2.3 Mechanical Design Iterations {#design-iterations}

Two preliminary iterations refined the component layout and structure before the final prototype design.

#### 1.2.3.1 First Design Iteration {#first-iteration}

<MechanicalFigure number="12" n="5" src="/report-assets/mechanical-design/first-iteration-structural-body.png" :width="1380" :height="688" caption="Structural body design for the first iteration" />

<MechanicalFigure number="13" n="6" src="/report-assets/mechanical-design/first-iteration-layered-section.png" :width="1381" :height="699" caption="Layered design approach from concept sketch (Sectioned View)" />

<div class="cv-figure-grid">

<MechanicalFigure number="14" n="7" src="/report-assets/mechanical-design/first-iteration-bottom-layer.png" :width="609" :height="434" caption="Bottom Layer" />

<MechanicalFigure number="15" n="8" src="/report-assets/mechanical-design/first-iteration-top-layer.png" :width="631" :height="428" caption="Top Layer" />

</div>

<MechanicalFigure number="16" n="9" src="/report-assets/mechanical-design/propeller-arm.png" :width="633" :height="527" caption="Propeller Arm" />

The first iteration developed the two central layers of the concept sketch; the RTK-GNSS antenna layer above and camera layer below were not yet incorporated. The top layer provided mounting holes for an acrylic electronics plate, while the bottom layer was intended to accommodate the battery, Jetson computer and other electronics. Propeller arms were designed to withstand motor-thrust and component-weight bending moments while minimising mass.

##### 1.2.3.1.1 Limitations {#limitations}

The first iteration prioritised layout and geometry over materials and manufacturing. Its complex top-layer and arm geometry suited 3D printing. Subsequent research favoured carbon-fibre-reinforced polymer (CFRP) for its stiffness and strength relative to mass [\[17\]](../references#md-ref-4) [\[18\]](../references#md-ref-5) [\[19\]](../references#md-ref-8). Adapting the geometry required custom moulding or redesign for standard sheets and tubes.

#### 1.2.3.2 CFRP Sheets & Tubes vs 3D-Printed Parts {#cfrp-sheets-tubes-vs-3d-printed-parts}

CFRP's higher strength-to-weight ratio than conventional 3D-printed polymers supports the estimated 4–6 kg takeoff mass and motor-thrust loads while limiting structural mass.

An experiment found lower vibration amplitudes in a CFRP motor frame than an aluminium-alloy frame [\[20\]](../references#md-ref-7). This suggests potential benefits for FOD camera clarity and reduced interference with flight-controller inertial measurements.

#### 1.2.3.3 Second Design Iteration {#second-iteration}

<MechanicalFigure number="17" n="10" src="/report-assets/mechanical-design/second-iteration-structural-body.png" :width="1073" :height="751" caption="Structural body design for the second iteration" />

<MechanicalFigure number="18" n="11" src="/report-assets/mechanical-design/second-iteration-layered-section.png" :width="1066" :height="790" caption="Layered design approach from concept sketch (Sectioned View)" />

The second iteration retained the layered layout but replaced 3D-printed arms with carbon-fibre tubes and simplified the top and bottom structures for CFRP fabrication. These changes targeted stiffness, strength and vibration management at low mass. Custom 3D-printed clamps secured the arms and landing legs to the bottom layer.

##### 1.2.3.3.1 Limitations {#limitations-1}

The 50 mm overall depth of each top and bottom structure made machining from solid CFRP stock impractical: substantial material removal would increase waste, machining time and cost. Further redesign therefore adopted thinner CFRP plates joined by separate supports.

### 1.2.4 Motor and Propeller Selection {#motor-propellers-selection}

<div class="mechanical-propulsion">

#### 1.2.4.1 Preliminary Mass Estimation {#_5-1-preliminary-mass-estimation-and-component-placement}

Motor and propeller selection preceded the final prototype design, requiring a preliminary mass estimate for thrust calculations and propulsion sizing.

Preliminary top and bottom plate layouts used the dimensions and placement requirements of selected components, including the Jetson Orin NX and Pixhawk, to estimate plate dimensions and establish the initial structure.

<div class="cv-figure-grid">

<MechanicalFigure number="19" n="24" src="/report-assets/mechanical-design/preliminary-top-component-layout.png" :width="607" :height="538" caption="Preliminary component placement on the top base plate." />

<MechanicalFigure number="20" n="25" src="/report-assets/mechanical-design/preliminary-bottom-component-layout.png" :width="650" :height="428" caption="Preliminary component placement on the bottom base plate." />

</div>

Structural masses, including CFRP plates, arms and 3D-printed parts, came from SolidWorks mass properties; selected electronics and sensor masses came from manufacturer specifications. Pending battery selection, the highest identified battery mass was adopted conservatively.

<p class="report-table-caption" id="table-6"><strong>Table 6.</strong> Preliminary Mass Estimation</p>

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

Identified components totalled approximately 3.6 kg. Allowing for planned components absent from the preliminary design gave a conservative 5 kg UAV estimate. The 3D-printed masses used SolidWorks' default properties because final material and fabrication specifications were undetermined, reinforcing this allowance.

#### 1.2.4.2 Preliminary Thrust Calculations {#_5-2-preliminary-thrust-calculations}

Preliminary thrust calculations supported motor and propeller sizing across flight conditions using the assumptions tabulated below.

<p class="report-table-caption" id="table-7"><strong>Table 7.</strong> Preliminary Thrust Calculations</p>

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

##### 1.2.4.2.1 General Equations {#general-equations}

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
<summary>1.2.4.2.1 Case 1: Basic Hover in Still Air</summary>

In this scenario, the UAV is assumed to hover steadily in still air, with no horizontal movement or acceleration. Therefore, the total upward thrust generated by the four motors must be equal to the UAV's weight to maintain a constant altitude.

<MechanicalFigure number="21" n="26" src="/report-assets/mechanical-design/hover-free-body-diagram.png" :width="715" :height="537" caption="Free-body diagram for basic hover in still air. The upward arrows represent the combined rotor contribution." />

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
<summary>1.2.4.2.2 Case 2: 15 km/h Cruise Against a 2 m/s Headwind</summary>

For this scenario, the UAV is assumed to cruise at a constant speed of 15 km/h against a headwind of 2 m/s. The headwind velocity was selected based on an article published by The Straits Times, which reported Singapore's average annual wind speed to be approximately 2 m/s [\[21\]](../references#md-ref-14). In addition, the UAV's projected frontal area was approximated as 0.062038 m² based on the overall body geometry obtained from the front view of the preliminary SolidWorks model.

<MechanicalFigure number="22" n="27" src="/report-assets/mechanical-design/preliminary-projected-frontal-area.png" :width="515" :height="223" caption="Projected frontal area estimated from the preliminary SolidWorks geometry: 0.062038 m²." />

<MechanicalFigure number="23" n="28" src="/report-assets/mechanical-design/cruise-free-body-diagram.png" :width="811" :height="608" caption="Free-body diagram for steady cruise against a headwind, reproduced from the source report. The thrust annotation differs slightly from the recalculated value below." />

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
<summary>1.2.4.2.3 Case 3: Forward Acceleration at 1 m/s² Towards 15 km/h Against a 2 m/s Headwind</summary>

The UAV accelerates forward while maintaining altitude, so horizontal thrust must overcome drag and produce the required acceleration. The thrust calculation below evaluates the condition at the target cruise speed, where drag is approximately 1.850 N. During acceleration from rest, drag varies with relative airspeed according to [Equations (10)](#equation-md-10) and [(11)](#equation-md-11).

<MechanicalFigure number="24" n="29" src="/report-assets/mechanical-design/acceleration-free-body-diagram.png" :width="1156" :height="436" caption="Free-body diagram for forward acceleration, evaluated at the target ground speed. The acceleration arrow indicates motion response rather than an additional force." />

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

##### 1.2.4.2.2 Results across Different Flight Scenarios {#_5-2-4-results-across-different-flight-scenarios}

<p class="report-table-caption" id="table-8"><strong>Table 8.</strong> Results across Different Flight Scenarios</p>

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

The results show increasing pitch and thrust requirements with headwind speed and acceleration. The 12 m/s case assesses additional demand near Beaufort “Strong Breeze” conditions [\[22\]](../references#md-ref-15). These scenarios informed propulsion sizing and thrust reserve.

#### 1.2.4.3 Conservative Thrust Estimation {#_5-3-setting-conservative-thrust-estimate}

Longitudinal cruise and acceleration calculations consider pitch, while lateral disturbances and manoeuvres also require roll. Preliminary sizing therefore adopted a conservative maximum combined tilt of 45°. The industrial-grade DJI Matrice 350 RTK, of comparable weight class, provided a 30° maximum-pitch reference [\[23\]](../references#md-ref-16).

<MechanicalFigure number="25" n="30" src="/report-assets/mechanical-design/dji-matrice-350-rtk-tilt-reference.png" :width="547" :height="412" caption="DJI Matrice 350 RTK. Maximum pitch angle reference reproduced from the supplied report [16]." />

The combined tilt angle, $\beta$, accounts for both pitch ($\theta$) and roll ($\phi$) of the UAV:

$$
\cos\beta=\cos\theta\cos\phi \tag{15}
$$

Assuming a UAV mass of 5 kg, the total weight is:

$$
W=mg=5(9.81)=49.05\ \mathrm{N}
$$

Vertical equilibrium requires thrust to balance weight. Applying [Equation (5)](#equation-md-5) at combined tilt $\beta$:

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

With equal thrust across four motors, [Equation (8)](#equation-md-8) gives:

$$
T_{\mathrm{motor}}=\frac{T_{\mathrm{total}}}{4}
$$

Converting from newtons to kilogram-force:

$$
T_{\mathrm{motor}}=\frac{69.37}{4(9.81)}\approx1.768\ \mathrm{kgf}
$$

The 45° sizing condition requires 69.37 N total thrust, or approximately 1.768 kgf per motor, informing motor and propeller evaluation.



##### 1.2.4.3.1 Interactive Thrust Illustration {#mechanical-thrust-illustration}

Thrust behaviour is illustrated below using the preliminary model. Physical load-test and flight-test results remain to be documented.

<details class="mechanical-flight-case" id="interactive-uav-attitude-thrust-simulator">
<summary>1.2.4.3.1.1 Interactive UAV Attitude and Thrust Simulator</summary>

<UAVTiltThrustSimulator />

This interactive visualisation supports preliminary thrust sizing for an X-configuration quadcopter. It assumes constant altitude with no vertical acceleration, thrust aligned with the body thrust axis, and no aerodynamic disturbances or additional forces.

</details>

#### 1.2.4.4 Motor and Propeller Evaluation {#_5-4-motors-and-propellers-evaluation}

A 2:1 thrust-to-weight target provided reserve for wind disturbance rejection, manoeuvrability, control authority and future payloads. At 5 kg, this requires approximately 2.5 kgf maximum thrust per motor. The T-Motor MN501-S KV360 and MAD 5005 IPE KV440 were shortlisted based on thrust capability and performance.

<div class="cv-figure-grid">

<MechanicalFigure number="26" n="31" src="/report-assets/mechanical-design/t-motor-mn501-s-kv360.png" :width="415" :height="386" caption="T-Motor MN501-S KV360." />

<MechanicalFigure number="27" n="32" src="/report-assets/mechanical-design/mad-5005-ipe-kv440.png" :width="441" :height="393" caption="MAD 5005 IPE KV440 motor." />

</div>

<details class="mechanical-flight-case" id="t-motor-mn501-s-kv360-with-17-inch-propellers">
<summary>1.2.4.4.1 T-Motor MN501-S KV360 with 17-inch Propellers</summary>

The T-Motor MN501-S KV360 paired with 17-inch propellers was evaluated based on its thrust capability and power consumption. Using the manufacturer's performance data [\[24\]](../references#md-ref-17), linear interpolation was performed to estimate the motor's operating characteristics at the required thrust of 1.251 kgf per motor under the expected cruising condition of 15 km/h with a 2 m/s headwind.

The manufacturer's performance data for the MN501-S KV360 with P17×5.8-inch propellers gives the following values at the two nearest thrust points [\[24\]](../references#md-ref-17).

<p class="report-table-caption" id="table-9"><strong>Table 9.</strong> T-Motor MN501-S KV360 with 17-inch Propellers</p>

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
<summary>1.2.4.4.2 MAD 5005 IPE KV440 with 14-inch Propellers</summary>

The MAD 5005 IPE KV440 paired with 14-inch propellers was similarly evaluated based on its thrust capability and power consumption. Using the manufacturer's performance data, linear interpolation was performed to estimate the motor's operating characteristics at similar operating conditions [\[25\]](../references#md-ref-18).

The manufacturer's performance table provides the following values:

<p class="report-table-caption" id="table-10"><strong>Table 10.</strong> MAD 5005 IPE KV440 with 14-inch Propellers</p>

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

##### 1.2.4.4.1 Motors Comparison {#_5-4-3-motors-comparison}

The MAD 5005 IPE KV440 was selected despite the T-Motor's slightly lower cruise power consumption. Its 14-inch propellers permit a more compact frame, while lower motor weight and cost favour integration. It meets the 2:1 thrust-to-weight target, and its IP35 rating provides a degree of water-exposure protection for outdoor operation.

<div class="mechanical-motor-comparison">

<p class="report-table-caption" id="table-11"><strong>Table 11.</strong> Motors Comparison</p>

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

#### 1.2.4.5 Differential Motor Thrust Calculations {#_5-5-differential-motor-thrust-calculation}

Initial calculations assumed equal motor thrust. SolidWorks assembly CG coordinates and distances to the front and rear motors were subsequently used to determine differential thrust for pitch equilibrium during constant-speed cruise and acceleration. Each scenario uses thrust and tilt from [the preliminary calculations](#_5-2-preliminary-thrust-calculations), subject to the following assumptions.

Assumptions:

- Left and right motors within each pair are assumed to produce equal thrust; roll and yaw corrections are neglected.
- Aerodynamic pitching moments are neglected.
- All motor thrust axes are assumed to be parallel and perpendicular to the motor mounting plane.
- Total thrust is evaluated at the specified flight condition; transient variations are neglected.

<MechanicalFigure number="28" n="33" src="/report-assets/mechanical-design/differential-motor-thrust-fbd.png" :width="1226" :height="541" caption="FBD of UAV with Differential Motor Thrust." />

<details class="mechanical-flight-case" id="thrust-distribution-during-constant-speed-cruise">
<summary>1.2.4.5.1 Thrust Distribution During Constant-Speed Cruise</summary>

<p class="report-table-caption" id="table-12"><strong>Table 12.</strong> Constant-Speed Cruise Parameters</p>

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

<p class="report-table-caption" id="table-13"><strong>Table 13.</strong> Motor Thrust Distribution During Constant-Speed Cruise</p>

| Motor position | Thrust per motor (N) | Thrust per motor (kgf) |
| --- | ---: | ---: |
| Front motors | 12.046 | 1.228 |
| Rear motors | 12.496 | 1.274 |

The results indicate that the rear motors require slightly greater thrust than the front motors to maintain pitch equilibrium during constant-speed cruise. This is because the rear motors are positioned closer to the CG, resulting in a shorter moment arm.

</details>

<details class="mechanical-flight-case" id="thrust-distribution-during-forward-acceleration">
<summary>1.2.4.5.2 Thrust Distribution During Forward Acceleration at 1 m/s²</summary>

<p class="report-table-caption" id="table-14"><strong>Table 14.</strong> Forward-Acceleration Parameters</p>

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

<p class="report-table-caption" id="table-15"><strong>Table 15.</strong> Motor Thrust Distribution During Forward Acceleration</p>

| Motor position | Thrust per motor (N) | Thrust per motor (kgf) |
| --- | ---: | ---: |
| Front motors | 12.104 | 1.234 |
| Rear motors | 12.659 | 1.290 |

</details>


</div>

### 1.2.5 Propeller Arm Selection {#propeller-arm-selection}

CFRP arm diameter and wall thickness were selected by comparing strength, stiffness, mass and vibration characteristics to minimise weight while maintaining flight structural integrity.

<div class="mechanical-propulsion">

#### 1.2.5.1 Bending Stress Calculation {#bending-stress-calculation}

A simplified beam model represents the prototype's arm clamping arrangement, determining clamp reactions and the maximum bending moment from motor thrust.

<MechanicalFigure number="29" n="34" src="/report-assets/mechanical-design/propeller-arm-loading-fbd.png" :width="1354" :height="672" caption="FBD of Propeller Arm Loading." />

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

<MechanicalFigure number="30" n="35" src="/report-assets/mechanical-design/hollow-cfrp-tube-cross-section.png" :width="680" :height="556" caption="Cross-sectional area of a hollow circular carbon-fibre tube." />

Maximum bending stress follows from the flexure formula:

$$
\sigma_{\max}=\frac{M_{\max}c}{I} \tag{26}
$$

For a hollow circular CFRP tube:

$$
I=\frac{\pi}{64}\left(D_o^4-D_i^4\right) \tag{27}
$$

Here, $D_o$ and $D_i$ are the outer and inner tube diameters, respectively:

$$
c=\frac{D_o}{2}
$$

$$
\sigma_{\max}=\frac{32FaD_o}{\pi\left(D_o^4-D_i^4\right)}
$$

#### 1.2.5.2 Beam Deflection Calculation {#beam-deflection-calculation}

The motor-end bending deflection was calculated using Euler–Bernoulli beam theory. A Young's modulus of 123 GPa, obtained from the manufacturer's Toray T300 carbon fibre datasheet, was adopted for the preliminary calculation [\[26\]](../references#md-ref-19).

<MechanicalFigure number="31" n="36" src="/report-assets/mechanical-design/propeller-arm-bending-deflection.png" :width="1381" :height="415" caption="Diagram illustrating deflection for a propeller arm." />

The motor-end deflection is calculated using:

$$
\delta_{\mathrm{motor}}=\frac{Fa^2(a+s)}{3EI} \tag{28}
$$

<p class="report-table-caption" id="table-16"><strong>Table 16.</strong> Beam Deflection Calculation</p>

| Parameter | Symbol | Value / definition |
| --- | --- | --- |
| Maximum motor thrust force | $F$ | N |
| Motor-to-clamp A distance | $a$ | 0.219 m |
| Distance between clamps | $s$ | 0.055 m |
| Young's modulus | $E$ | $123\times10^9\ \mathrm{Pa}$ |
| Second moment of area of the hollow circular tube | $I$ | [Equation (27)](#equation-md-27), m⁴ |

#### 1.2.5.3 Natural Bending Frequency Calculation {#natural-bending-frequency-calculation}

<MechanicalFigure number="32" n="37" src="/report-assets/mechanical-design/cantilever-bending-modes.png" :width="546" :height="366" caption="Figure showing the different bending modes, reproduced from the supplied report; the original illustration source was not provided." />

Natural bending frequencies were evaluated to limit resonance affecting onboard sensors. ArduPilot identifies motor rotational frequency as a common multirotor vibration source [\[27\]](../references#md-ref-20).

Manufacturer data provided motor rotational and blade passing frequency ranges from hover to maximum thrust for arm comparison. Preliminary calculations considered only the first bending mode.

**Motor rotational frequency**

Rotational frequency follows from motor speed in revolutions per minute (RPM):

$$
f_{\mathrm{motor}}=\frac{\mathrm{RPM}}{60} \tag{29}
$$

Hover and maximum-thrust values use the MAD 5005 KV440 datasheet with 14-inch propellers.

**Blade passing frequency**

Blade passing frequency (BPF) counts blade passages past a fixed point. For two blades:

$$
f_{\mathrm{BPF}}=2f_{\mathrm{motor}} \tag{30}
$$

<p class="report-table-caption" id="table-17"><strong>Table 17.</strong> Motor Excitation Frequencies</p>

| Frequency | Hover | Maximum thrust |
| --- | ---: | ---: |
| Motor rotational frequency | 96.88 Hz | 136.03 Hz |
| Blade passing frequency | 193.76 Hz | 272.06 Hz |

**First bending natural frequency of CFRP arm**

A simplified cantilever model estimates the arm's first bending frequency, representing the motor and propeller as a concentrated free-end mass and including the unsupported arm's distributed mass.

$$
f_{n,1}=\frac{1}{2\pi}\sqrt{\frac{3EI}{a^3\left(m_{\mathrm{tip}}+0.236m_{\mathrm{arm}}\right)}} \tag{31}
$$

Parameters:

<p class="report-table-caption" id="table-18"><strong>Table 18.</strong> Natural Bending Frequency Parameters</p>

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

Here, $\rho$ is CFRP density (kg/m³); $D_o$ and $D_i$ are tube diameters in metres, defined in [the bending stress calculation](#bending-stress-calculation). The second moment of area follows [Equation (27)](#equation-md-27):

$$
I=\frac{\pi}{64}\left(D_o^4-D_i^4\right)
$$

#### 1.2.5.4 Evaluation of Different Tube Configurations {#evaluation-of-different-beam-configurations}

Configurations were compared for structural performance, natural frequency and mass, using these resonance-avoidance and weight criteria:

1. The first bending natural frequency must fall outside the motor rotational frequency range of 96.88–136.03 Hz.
2. The first bending natural frequency must fall outside the blade passing frequency range of 193.76–272.06 Hz.
3. The lightest configuration satisfying both frequency criteria will be selected.

The selected 20 mm outer diameter, 1.5 mm wall thickness CFRP tube satisfies both frequency criteria at the lowest qualifying mass.

<div class="mechanical-arm-comparison">
<table>
<caption class="report-table-caption"><strong>Table 19.</strong> Evaluation of Different Tube Configurations</caption>
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

Red marks configurations within the motor rotational frequency range (16 × 1.5 mm and 16 × 2.0 mm) or blade passing frequency range (22 × 2.0 mm). Yellow marks heavier qualifying configurations. Green marks the selected 20 × 1.5 mm tube, satisfying both frequency criteria at minimum mass.

</div>

### 1.2.6 Third Design Iteration (Final Prototype Design) {#final-prototype-design}

<MechanicalFigure number="33" n="12" src="/report-assets/mechanical-design/final-prototype-cad-assembly.png" :width="1378" :height="665" caption="CAD Assembly of Final Prototype Design" />

<MechanicalFigure number="34" n="13" src="/report-assets/mechanical-design/final-prototype-layers.png" :width="734" :height="342" caption="Different Layers of the Prototype Design" />

<p class="report-table-caption" id="table-20"><strong>Table 20.</strong> Third Design Iteration (Final Prototype Design)</p>

| Layer / Assembly | Allocated Components |
| --- | --- |
| Top Layer | Pixhawk Flight Controller, Jetson Orin NX, GNSS Antenna and 360° LiDAR |
| Bottom Layer | 12 Ah Battery, Power Distribution Boards, Fuse and Electronic Speed Controllers (ESC) |
| Camera & Sensor Assembly | RGB Camera, Thermal Camera and Single-Point LiDAR |
| Propeller Assembly | Motors and Propellers |

The final design addresses the second iteration's fabrication limitations by combining CFRP base plates, motor mounting plates and propeller arms with 3D-printed components. CFRP suits these relatively simple structural geometries. More complex, customisable enclosures and tube clamps would use PETG CF for its improved mechanical properties over conventional PETG and PLA [\[28\]](../references#md-ref-9).

### 1.2.7 Placement of Key Onboard Components {#placement-of-key-onboard-components}

Component placement considered mass distribution, accessibility, vibration isolation and electrical connectivity to support stability and operational requirements.

#### 1.2.7.1 Central Alignment of GNSS Antenna and RGB Camera {#central-alignment-of-gnss-antenna-and-rgb-camera}

The RGB camera detects and locates FOD within images; GNSS supplies the UAV's geographical position. Their central X–Y alignment along a common vertical axis simplifies geolocation while retaining vertical separation.

<MechanicalFigure number="35" n="17" src="/report-assets/mechanical-design/gnss-rgb-vertical-alignment.png" :width="702" :height="306" caption="Side view showing the vertical separation of the GNSS antenna and RGB camera (project CAD)." />

The primarily vertical displacement simplifies sensor-to-sensor transformation. From the cited direct georeferencing principles [\[29\]](../references#md-ref-11):

$$
\mathbf{p}_C^N=\mathbf{p}_G^N+\mathbf{R}_B^N\mathbf{t}_{GC} \tag{2}
$$

Here, $\mathbf{p}_C^N$ and $\mathbf{p}_G^N$ are camera and GNSS positions in the navigation frame; $\mathbf{R}_B^N$ rotates from body to navigation coordinates, accounting for attitude; and $\mathbf{t}_{GC}$ is the GNSS-to-camera translation in body coordinates.

For the approximately vertically aligned configuration:

$$
\mathbf{p}_C^N\approx\mathbf{p}_G^N+\mathbf{R}_B^N
\begin{bmatrix}0\\0\\\Delta z\end{bmatrix} \tag{3}
$$

The signed $\Delta z$ runs from GNSS antenna to RGB camera along body Z. Central alignment simplifies the geolocation lever arm, but navigation-frame transformation still requires UAV attitude.

#### 1.2.7.2 Placement of the Pixhawk Flight Controller near Centre of Gravity {#placement-of-the-pixhawk-flight-controller-near-centre-of-gravity}

PX4 and ArduPilot recommend positioning the flight controller as close as possible to the CG [\[30\]](../references#md-ref-12) [\[31\]](../references#md-ref-13).

<MechanicalFigure number="36" n="18" src="/report-assets/mechanical-design/px4-flight-controller-mounting.png" :width="1040" :height="611" caption="Ideal flight controller placement. External PX4 documentation illustration reproduced in the supplied report [12]; the original source URL was not supplied." />

The assembly places the Pixhawk near the CG within available space, as shown below.

<MechanicalFigure number="37" n="19" src="/report-assets/mechanical-design/pixhawk-isometric-view.png" :width="872" :height="617" caption="Isometric view of the Pixhawk placement (project CAD)." />

<div class="cv-figure-grid">

<MechanicalFigure number="38" n="20" src="/report-assets/mechanical-design/pixhawk-top-view.png" :width="656" :height="619" caption="Top view of the Pixhawk placement (project CAD)." />

<MechanicalFigure number="39" n="21" src="/report-assets/mechanical-design/pixhawk-side-view.png" :width="807" :height="391" caption="Side view of the Pixhawk placement (project CAD)." />

</div>

The completed assembly gave the following approximate Pixhawk offsets from the overall CG.

<p class="report-table-caption" id="table-21"><strong>Table 21.</strong> Placement of the Pixhawk Flight Controller near Centre of Gravity</p>

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

The approximately 45 mm displacement remains within ArduPilot's recommendation of a few centimetres. PX4 and ArduPilot offer offset-compensation parameters, but close placement remains preferable: larger offsets increase IMU accelerations during rotation and may affect measurements and control [\[31\]](../references#md-ref-13).

#### 1.2.7.3 Placement of the 360° LiDAR {#placement-of-the-360-lidar}

The 360° LiDAR moved from the top plate's centre to the front because GNSS–RGB alignment took priority. This position aims to minimise surrounding-component obstruction while preserving propeller and structural clearance. Its obstacle-detection role is discussed in the [Computer Vision section](./computer-vision#thermal-safety).

<MechanicalFigure number="40" n="22" src="/report-assets/mechanical-design/lidar-front-isometric-view.png" :width="916" :height="586" caption="Front placement of the 360° LiDAR in the isometric view (project CAD)." />

#### 1.2.7.4 45° Placement of the Thermal Camera {#45-degree-placement-of-the-thermal-camera}

The thermal camera is mounted at approximately 45° on a rigid, custom-designed mount that will be 3D-printed, complementing the 360° LiDAR for obstacle detection. Planned integration is discussed in the [Computer Vision section](./computer-vision#thermal-safety).

<MechanicalFigure number="41" n="23" src="/report-assets/mechanical-design/thermal-camera-side-view.png" :width="928" :height="392" caption="Placement of the thermal camera in the side view (project CAD)." />

#### 1.2.7.5 Placement of Batteries and Other Electrical Components in the Bottom Layer {#placement-of-batteries-and-other-electrical-components-in-the-bottom-layer}

The battery and other electronics, particularly ESCs, occupy the bottom layer. At approximately 1.5kg, the battery is the heaviest component; its low placement lowers the CG, as discussed in [the CG analysis](#centre-of-gravity-cg-of-uav).

Unlike external arm-mounted ESC layouts, internal bottom-layer mounting provides additional protection from water and environmental exposure, since the selected AMPX 40A ESCs have no specified waterproof rating.

Raspberry Pi integration may require external ESC relocation if bottom-layer space is insufficient. If necessary, 3D-printed protective enclosures will provide water resistance.

## 1.3 Mechanical Prototype Development {#a3-prototype-development}

<span id="prototype-fabrication-assembly" class="report-anchor" aria-hidden="true"></span>

### 1.3.1 Structural Prototype {#structural-prototype}

<div class="cv-figure-grid">

<MechanicalFigure number="42" n="38" src="/report-assets/mechanical-design/structural-prototype-isometric.jpeg" :width="491" :height="655" caption="Initial structural prototype with acrylic base plates and carbon-fibre tube arms." />

<MechanicalFigure number="43" n="39" src="/report-assets/mechanical-design/structural-prototype-side.jpeg" :width="476" :height="634" caption="Assembled structural prototype showing the base plates, propeller arms and landing legs." />

</div>

The initial structural prototype was fabricated primarily to assess potential assembly concerns and provide a platform for preliminary motor testing before progressing to the final UAV assembly.

For this prototype, the upper and lower base plates were fabricated using acrylic sheets, while the propeller arms were constructed using spare carbon-fibre tubes with an outer diameter of 22 mm and a wall thickness of 1 mm. The available carbon-fibre tubes were cut into four individual arms according to the required lengths specified in the mechanical design.

These spare 22 mm outer diameter, 1 mm wall thickness tubes were used for preliminary prototyping and differ from the final selected [20 mm outer diameter, 1.5 mm wall thickness tube configuration](#evaluation-of-different-beam-configurations).

The base plates, propeller arms and landing legs were assembled using 3D-printed clamps and mounts developed based on the prototype design.

### 1.3.2 3D-Printed Carbon Fibre Tube Clamps {#3d-printed-carbon-fibre-tube-clamps}

<div class="cv-figure-grid">

<MechanicalFigure number="44" n="40" src="/report-assets/mechanical-design/tube-clamp-heat-set-threaded-inserts.png" :width="566" :height="384" caption="Installation of heat-set threaded inserts into the 3D-printed carbon-fibre tube clamps." />

<MechanicalFigure number="45" n="41" src="/report-assets/mechanical-design/fabricated-carbon-fibre-tube-clamps.png" :width="960" :height="1280" caption="Fabricated PETG tube clamp components, including installed threaded inserts." />

</div>

The carbon-fibre tube clamps were fabricated using PETG (polyethylene terephthalate glycol) through 3D printing, primarily due to its toughness and impact resistance [\[32\]](../references#md-ref-21).

The clamps were fabricated to evaluate the functionality of the clamping mechanism in securing the carbon-fibre tubes and base plates. In addition, heat-set threaded inserts were installed into the 3D-printed clamps to provide secure fastening points for assembly and disassembly. The prototyping was done to assess the fitment of the components and the practicality of the clamping mechanism before finalising the design. The findings from the preliminary clamp evaluation and the subsequent proposed design modifications are discussed in [Section 1.5.2 - 3D-Printed Carbon Fibre Tube Clamp Analysis After Testing](#tube-clamp-analysis-after-testing).

### 1.3.3 3D-Printed Drone Leg Mounts {#3d-printed-drone-leg-mounts}

<div class="cv-figure-grid">

<MechanicalFigure number="46" n="42" src="/report-assets/mechanical-design/fabricated-drone-leg-mounts.png" :width="868" :height="1280" caption="Fabricated PETG landing leg mounts with slotted clamping features." />

<MechanicalFigure number="47" n="43" src="/report-assets/mechanical-design/drone-leg-mount-slot-clamping-mechanism.png" :width="444" :height="449" caption="CAD detail of the slotted clamping mechanism around a carbon-fibre landing leg." />

</div>

The drone leg mounts were designed to position the landing legs at an outward inclination of 20° to provide a wider support base and improve the stability of the UAV when resting on the ground.

The mounts were fabricated using PETG due to its toughness and flexibility, particularly around the slot incorporated into the clamping mechanism. The slot allows the mount to deform slightly when the fasteners are tightened, generating a clamping force that secures the carbon-fibre landing legs in place. The prototyping was done to assess the functionality of the clamping mechanism of the carbon-fibre landing legs. The findings from the landing leg mount evaluation and the proposed alternative solution are discussed in [Section 1.5.3 - 3D-Printed Drone Leg Mount Analysis After Testing](#drone-leg-mount-analysis-after-testing).

## 1.4 Mechanical Testing and Verification {#a4-testing}

<span id="prototype-testing" class="report-anchor" aria-hidden="true"></span>

### 1.4.1 Motor Testing {#motor-testing}

Preliminary motor testing was conducted using the assembled structural prototype to verify the integration between the Pixhawk flight controller, Electronic Speed Controllers (ESCs) and motors. The tests also aimed to verify the motor output assignments and evaluate the motors' response to control commands before proceeding with further UAV integration and flight testing. The tests were conducted using a bench power supply set to 24 V with a current limit of 5 A, which is below the total current required for hovering flight.

Due to the current limitation of the bench power supply, testing was limited to verifying basic motor functionality and system integration rather than evaluating motor performance under actual flight operating conditions.

#### 1.4.1.1 Individual Motor Testing Using MAVProxy {#individual-motor-testing-mavproxy}

MAVProxy was used to configure the flight controller and conduct individual motor tests. The UAV configuration was first verified by checking the `FRAME_CLASS` and `FRAME_TYPE` parameters, both set to `1`, corresponding to a quadcopter with an X-frame configuration.

The motor output functions were then assigned to the first four output channels using the `SERVO1_FUNCTION` to `SERVO4_FUNCTION` parameters, with values ranging from `33` to `36`, respectively. This established the intended motor output assignments for the quadcopter configuration.

Individual motor tests were subsequently conducted using the `motortest` command, with a commanded throttle percentage of 40% and a test duration of 5 seconds. These tests were intended to verify the response of each motor to commands issued through the flight controller and identify potential integration or output assignment issues.

<MechanicalFigure number="48" n="44" src="/report-assets/mechanical-design/mavproxy-individual-motor-testing.png" :width="756" :height="430" caption="MAVProxy verification of the quadcopter X-frame configuration, motor output assignments and individual motor test commands at 40% commanded throttle for 5 seconds." />

<MechanicalVideo src="/report-assets/mechanical-design/individual-motor-testing-1.mov" poster="/report-assets/mechanical-design/individual-motor-testing-1-poster.jpg" caption="Individual motor testing, recording 1." />

<MechanicalVideo src="/report-assets/mechanical-design/individual-motor-testing-2.mov" poster="/report-assets/mechanical-design/individual-motor-testing-2-poster.jpg" caption="Individual motor testing, recording 2." />

#### 1.4.1.2 Simultaneous Motor Testing Using Mission Planner {#simultaneous-motor-testing-mission-planner}

Following the individual motor tests, Mission Planner was used to conduct simultaneous testing of all four motors.

The Motor Test interface was configured for a quadcopter with an X-frame configuration. A commanded throttle percentage of 40% and a test duration of 5 seconds were selected for the test.

The simultaneous motor test was intended to assess the response of all four motors when commanded together and further verify the integration of the Pixhawk flight controller, ESCs and motors within the assembled FOD Argus prototype.

<MechanicalFigure number="49" n="45" src="/report-assets/mechanical-design/mission-planner-simultaneous-motor-testing.png" :width="800" :height="726" caption="Mission Planner Motor Test interface showing the Quad/X configuration, motor assignments, 40% commanded throttle, 5-second duration and test controls." />

<MechanicalVideo src="/report-assets/mechanical-design/simultaneous-motor-testing.mov" poster="/report-assets/mechanical-design/simultaneous-motor-testing-poster.jpg" caption="Simultaneous motor testing." />

## 1.5 Mechanical Analysis {#a5-analysis}

<span id="analysis" class="report-anchor" aria-hidden="true"></span>

### 1.5.1 Centre of Gravity (CG) Analysis {#centre-of-gravity-cg-of-uav}

The centre of gravity (CG) of the completed UAV prototype assembly was determined in SolidWorks from the mass distribution of its individual components. The coordinates below are relative to the assembly coordinate origin; the vertical coordinate is distinct from the distance below the propeller plane.

<p class="report-table-caption" id="table-22"><strong>Table 22.</strong> Centre of Gravity (CG) Analysis</p>

| Axis | CG coordinate (mm) |
| --- | ---: |
| X | −5.85 |
| Y | 0.61 |
| Z | 36.49 |

<div class="cv-figure-grid">

<MechanicalFigure number="50" n="14" src="/report-assets/mechanical-design/cg-top-view.png" :width="600" :height="572" caption="CG point in the top view of the SolidWorks assembly (project CAD)." />

<MechanicalFigure number="51" n="15" src="/report-assets/mechanical-design/cg-front-view.png" :width="1101" :height="502" caption="CG point in the front view of the SolidWorks assembly (project CAD)." />

</div>

#### 1.5.1.1 Horizontal CG Positioning {#horizontal-cg-positioning}

The SolidWorks mass properties give the horizontal displacement of the CG from the geometric centre of the four motors in the X configuration:

$$
d_{CG}=\sqrt{(-5.85)^2+(0.61)^2}=5.88\ \mathrm{mm} \tag{1}
$$

The calculated horizontal offset is approximately 5.88 mm. This relatively small offset limits the additional pitch and roll moments associated with uneven mass distribution, reducing the differential thrust required to maintain level hover. This can preserve more motor control authority for manoeuvres and responses to external disturbances, such as wind gusts.

#### 1.5.1.2 Vertical CG Positioning {#vertical-cg-positioning}

The SolidWorks assembly places the UAV's CG approximately 40 mm below the propeller plane.

The thesis cited in the source report [\[33\]](../references#md-ref-10) describes how positioning the CG below the propellers can contribute to stability during forward flight and wind disturbances. Aerodynamic drag acting above the CG can generate a stabilising moment opposing an attitude disturbance, as illustrated below.

<MechanicalFigure number="52" n="16" src="/report-assets/mechanical-design/vertical-cg-stability-reference.png" :width="1040" :height="378" caption="Influence of vertical CG positioning on multicopter stability. External thesis illustration reproduced in the supplied report [10]; bibliographic details were not supplied." />

FOD ARGUS incorporates a lower CG through the arrangement of its onboard components, particularly the battery. This configuration may contribute to a stabilising aerodynamic response if the resultant aerodynamic forces act above the CG. Overall stability remains dependent on the flight control system, and flight testing is required to evaluate the effectiveness of this arrangement.

### 1.5.2 3D-Printed Carbon Fibre Tube Clamp Analysis After Testing {#tube-clamp-analysis-after-testing}

<MechanicalFigure number="53" n="46" src="/report-assets/mechanical-design/tube-clamp-potential-slippage.png" :width="590" :height="402" caption="Potential axial and rotational slippage in the original tube clamping mechanism." />

During preliminary testing, the 3D-printed clamps were found to provide a tight fit around the carbon-fibre tubes. However, the team identified a potential limitation of the clamping mechanism, where the tubes could experience axial slippage or rotational movement within the clamps, particularly when subjected to loads during flight.

One possible solution was to apply epoxy adhesive between the clamps and carbon-fibre tubes to prevent relative movement. However, this would create a largely permanent connection, making subsequent clamp modifications or replacements difficult during prototyping.

<MechanicalFigure number="54" n="47" src="/report-assets/mechanical-design/proposed-keyed-tube-clamp-cad.png" :width="874" :height="236" caption="Proposed keyed clamping mechanism: modified clamp with a corresponding slot (left) and keyed insert (right)." />

To address this limitation while maintaining the modularity of the design, a keyed connection was proposed. This involves bonding a keyed insert to the end of each carbon-fibre tube using epoxy adhesive and incorporating a corresponding slot into the 3D-printed clamp. The resulting mechanical interlock is intended to restrict both axial and rotational movement without permanently bonding the clamp to the tube. This approach would allow the team to modify or replace the 3D-printed clamps during subsequent design iterations, provided that the corresponding slot geometry is maintained.

### 1.5.3 3D-Printed Drone Leg Mount Analysis After Testing {#drone-leg-mount-analysis-after-testing}

<div class="cv-figure-grid">

<MechanicalFigure number="55" n="48" src="/report-assets/mechanical-design/assembled-prototype-landing-leg-mount.jpeg" :width="355" :height="473" caption="Assembled 3D-printed landing leg mount on the structural prototype." />

<MechanicalFigure number="56" n="49" src="/report-assets/mechanical-design/landing-leg-clamp-fastening-detail.png" :width="960" :height="1280" caption="Close-up of the original slotted landing leg clamp and bolt-and-nut fastening mechanism." />

</div>

The 3D-printed drone leg mounts were also evaluated during the assembly of the structural prototype. Although the clamping mechanism provided a sufficiently tight fit around the carbon-fibre landing legs, several practical difficulties were encountered during assembly.

The mounts required bolts and nuts for fastening, which made the assembly and disassembly process relatively tedious. Furthermore, certain features of the mounts lacked sufficient wall thickness to accommodate heat-set threaded inserts, limiting the practicality of improving the fastening mechanism.

To address these limitations, a commercially available aluminium landing leg mount with a 20° inclination was identified on Taobao. The mount was found to be geometrically compatible with the UAV design while maintaining the intended outward inclination of the landing legs. Compared to the 3D-printed PETG mounts, the aluminium material is expected to provide greater structural strength and rigidity, offering higher confidence in the reliability of the landing leg connections. The threaded holes in the aluminium mount are also expected to simplify assembly.

<MechanicalFigure number="57" n="50" src="/report-assets/mechanical-design/proposed-aluminium-landing-leg-mount.png" :width="485" :height="609" caption="Proposed commercially available aluminium landing leg mount from Taobao, with supplier dimensions shown; this alternative has not been installed or validated by the team." />

## 1.6 Discussion of Future Works {#a6-problems-project-plan}

<span id="challenges-limitations-future-work" class="report-anchor" aria-hidden="true"></span>

### 1.6.1 Semester 2 Development Plan {#semester-2-development-plan}

The following development activities are planned for Semester 2 to refine the mechanical design, address outstanding limitations and validate the UAV's structural and flight performance.

<details class="mechanical-flight-case" id="waterproofing-onboard-electronics">
<summary>1.6.1.1 Waterproofing and Protection of Onboard Electronics</summary>

- **Design side enclosures:** Develop side enclosure panels for the UAV frame to reduce the exposure of internal components to rain, splashes and debris.
- **Identify vulnerable electronic components:** Review the onboard electronics to determine which components are not inherently water resistant and require additional protection.
- **Design protective housings:** Develop dedicated enclosures or covers for sensitive components while maintaining accessibility for assembly, inspection and maintenance.
- **Investigate water ingress prevention:** Identify potential leakage paths through enclosure joints, openings and cable entry points.
- **Research existing waterproofing techniques:** Evaluate methods such as gaskets, overlapping joints, sealants and cable glands currently used in similar engineering applications.
- **Select and implement a suitable design:** Compare potential solutions based on water resistance, ease of fabrication, assembly practicality and compatibility with the UAV structure.
- **Prototype and validate the enclosure:** Fabricate the proposed enclosure design and assess its effectiveness in reducing water ingress.

</details>

<details class="mechanical-flight-case" id="base-plate-structural-validation">
<summary>1.6.1.2 Base Plate Finalisation and Structural Validation</summary>

- **Finalise base plate design:** Refine the geometry, thickness and mounting features of the upper and lower base plates based on the final UAV configuration.
- **Optimise component placement:** Review the arrangement of onboard electronics to accommodate the Raspberry Pi and additional systems while considering accessibility, cable routing and weight distribution.
- **Verify centre of gravity:** Reassess the UAV's centre of gravity following any changes to the component arrangement to ensure acceptable mass distribution.
- **Conduct structural FEA:** Evaluate the stress distribution and deformation of the UAV structure under representative operating loads to validate the material selection and structural calculations performed in Semester 1.
- **Conduct modal analysis:** Determine the natural frequencies and mode shapes of the UAV structure to assess potential resonance with motor excitation frequencies and verify the analytical natural-frequency calculations conducted in Semester 1.
- **Implement design improvements:** Refine the mechanical design based on the FEA and modal analysis results before proceeding with final fabrication.

</details>

<details class="mechanical-flight-case" id="jetson-water-resistant-ventilation">
<summary>1.6.1.3 Water-Resistant Ventilation for Jetson Orin NX</summary>

- **Assess thermal management requirements:** Evaluate the cooling requirements of the Jetson Orin NX, particularly the heat generated during operation and the airflow needed to maintain acceptable operating temperatures.
- **Design water-resistant ventilation openings:** Develop ventilation features for the Jetson Orin NX enclosure that allow heat dissipation while minimising the risk of water ingress.
- **Research existing ventilation solutions:** Investigate techniques such as louvred vents, labyrinth airflow channels and waterproof breathable membranes used in electronics enclosures.
- **Evaluate ventilation designs:** Compare the proposed solutions based on airflow resistance, water resistance, ease of fabrication and compatibility with the UAV's mechanical design.
- **Prototype and validate the selected design:** Fabricate the proposed enclosure and assess its thermal performance and resistance to water ingress under representative operating conditions.
- **Refine the enclosure design:** Implement improvements based on the testing results to achieve a suitable balance between thermal management and environmental protection.

</details>

<details class="mechanical-flight-case" id="additional-vibration-damping">
<summary>1.6.1.4 Additional Vibration-Damping Measures</summary>

- **Assess vibration characteristics:** Evaluate the vibrations generated by the motors and propellers during operation, particularly their effects on the UAV structure and sensitive onboard components.
- **Identify components requiring vibration isolation:** Determine whether additional vibration-damping measures are necessary for components such as the Pixhawk flight controller, cameras and onboard sensors.
- **Research existing vibration-damping solutions:** Investigate techniques such as foam pads, rubber dampers and vibration-isolating mounts commonly used in UAV applications.
- **Evaluate suitable damping materials and configurations:** Compare the effectiveness, weight, ease of integration and compatibility of different vibration-damping solutions with the existing mechanical design.
- **Prototype and test selected solutions:** Incorporate suitable vibration-damping components where necessary and evaluate their effectiveness by comparing vibration measurements before and after implementation.
- **Refine component mounting arrangements:** Optimise the positioning and mounting of vibration-sensitive components based on the testing results to minimise vibration transmission without compromising structural stability.

</details>

<details class="mechanical-flight-case" id="uav-flight-testing-calibration">
<summary>1.6.1.5 UAV Flight Testing and Calibration</summary>

- **Complete final UAV assembly:** Integrate the mechanical structure, propulsion system, flight controller and onboard electronics to prepare the UAV for flight testing.
- **Calibrate the flight controller and sensors:** Conduct the necessary Pixhawk calibrations, including the accelerometer, gyroscope, compass, radio controller and ESCs where applicable, to ensure accurate sensor readings and motor control.
- **Conduct preliminary ground testing:** Verify motor rotation directions, output assignments, control responses and system behaviour before attempting flight.
- **Perform manual flight testing using the radio controller:** Conduct initial hover and basic manoeuvring tests using the RadioMaster TX16S radio controller to evaluate attitude stability, motor responsiveness and overall flight behaviour before progressing to autonomous operation.
- **Evaluate manual flight performance:** Assess the UAV's response to roll, pitch, yaw and throttle commands, identifying any issues with the mechanical configuration or flight control parameters.
- **Progress to autonomous flight testing:** Once stable and reliable manual flight has been demonstrated, work with the navigation and control teams to conduct controlled autonomous flight tests, including waypoint navigation and position-holding performance.
- **Refine and validate the UAV configuration:** Make necessary adjustments to the mechanical design and flight controller parameters based on testing results, followed by further testing to verify improvements.

</details>

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
