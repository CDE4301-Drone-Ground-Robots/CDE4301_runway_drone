---
title: "Electrical Design"
outline: false
prev: false
next: false
aside: false
pageClass: subsystem-report-page
---

<script setup>
import ElectricalFigure from './components/ElectricalFigure.vue'

</script>

<div class="cv-report rubric-report" style="--report-chapter: '2'">

<p class="chapter-kicker">FOD ARGUS / ELECTRICAL DESIGN</p>

# 2. Electrical Design {#electrical-design}

<SubsystemLead class="cv-report-byline" name="Kummarikunta Talitha" matric="A0286653R" portrait="/team/Talitha.jpg" />

## 2.1 Objective and Requirements {#a1-objective-scope-context}

The objective is to power and connect the propulsion, flight controller, onboard computer and sensors for a 15 min inspection flight, in both the Jetson-only and the Jetson plus Raspberry Pi 5 configurations.

### 2.1.1 Electrical System Overview {#electrical-overview}

The electrical system connects the battery, propulsion, flight controller, onboard computer and sensor payload (Fig. 58). The 6S battery feeds the main power distribution board (PDB) through a battery fuse. The PDB supplies battery output to the four ESCs and to a DC-DC step-down converter for the Jetson Orin NX, and regulated outputs to the sensors and telemetry radio. The flight controller reads the battery level, sends PWM signals to the ESCs, and talks to the Jetson over the computer link. The Jetson receives the 3D map and FOD input from the LiDAR and cameras, and sends FOD coordinates through the telemetry radio to the UGV.

<ElectricalFigure number="58" n="1" src="/report-assets/electrical-design/electrical-system-interaction.png" :width="1930" :height="985" caption="Electrical System Interaction" />

### 2.1.2 Electrical Design Requirements and Considerations {#electrical-requirements}

<p class="report-table-caption" id="table-23"><strong>Table 23.</strong> Electrical Design Requirements and Considerations</p>

| Design Requirements | What it means and the target |
| --- | --- |
| Flight endurance | Support the 15 min mission (see [Navigation and Obstacle Avoidance, Section 3.5.1 – Endurance vs. Mission Time](./navigation-obstacle-avoidance#endurance-vs-mission-time)) on one pack, using 80% of the capacity (213 Wh of 266 Wh) with real flights expected to give 10–20% less than the model. |
| Thrust-to-weight ratio | Keep thrust-to-weight at or above 2.0 after a 10% derate for 6S voltage sag, so the electronics mass and the battery must be kept low. |
| Low added mass | Minimise the electrical mass because the motors must carry it. Takeoff mass is estimated at 4.55 kg (Best Case) and 4.62 kg (Worst Case), well below the 7 kg target set in the mechanical design. |
| Battery capacity and current | Use a 6S (22.2 V) pack that matches the motor test data and delivers the 36 A average and 98 A peak current, with a 300 A (25C) rating leaving about 3× headroom. |
| Circuit protection | Protect the main path with a fuse rated above the 36 A average and aggressive-manoeuvre currents and below the wiring rating, with a DC rating above the 25.2 V of a full pack (80 A chosen), and fuse the compute branch separately. |
| Wire and connector ratings | Rate every wire and connector after the fuse for at least the fuse current (AS150 connectors, 8 AWG main path), with smaller gauges chosen by branch current. |
| Regulated supplies | Provide a 12 V branch for the Jetson (about 2.3 A) and a 5 V rail for the payload, within the PDB's 5 A regulated output, and supply the flight controller within its 4.8–5.4 V input range. |
| Battery monitoring | Give the flight controller accurate battery voltage and current, through the PDB's 1/21 voltage divider and current-sense output, calibrated against a multimeter and a known load. |
| Interfaces and ports | Give each sensor its own port on the flight controller or onboard computer (UART, USB, CSI, Ethernet) with no duplicated hardware. |
| Both computer cases | Meet the endurance, thrust-to-weight and current requirements in both the Jetson-only (Best Case) and Jetson plus Raspberry Pi 5 (Worst Case) configurations. |
| Verifiability | Base each figure on a datasheet or measurement where possible, and mark assumptions (placeholder sensor currents, estimated weights) so they can be replaced by Semester 2 measurements. |

## 2.2 Electrical Design and Component Selection {#a2-methodology-concept-development}

### 2.2.1 Flight Controller and Onboard Computer Selection {#compute-selection}

The aircraft carries one flight controller and one onboard computer, with no duplicated hardware. The flight controller owns the hard real-time loops (attitude estimation, motor mixing, failsafes), while the onboard computer owns perception and navigation. Two computer configurations are carried through every calculation in this chapter. In the **Best Case** the Jetson Orin NX runs ROS 2 and all AI models alone. In the **Worst Case** the Jetson is overloaded, so a Raspberry Pi 5 takes over ROS 2 navigation and the Jetson runs only the AI models. The Pi 5 is a load-shedding fallback, not a redundancy, and the power budget is sized so that either case flies.

#### 2.2.1.1 Flight Controller: Pixhawk (3DR) {#flight-controller-pixhawk-3dr}

<ElectricalFigure number="59"
  n="2"
  src="/report-assets/electrical-design/pixhawk-3dr.png"
  :width="272"
  :height="150"
  :cardWidth="365"
  caption="Pixhawk (3DR)"
/>



<p class="report-table-caption" id="table-24"><strong>Table 24.</strong> Flight Controller: Pixhawk (3DR)</p>

| Feature | Pixhawk | Why it fits |
| --- | --- | --- |
| Processor | STM32F427 Cortex-M4F with FPU, 256 KB RAM, 2 MB flash; separate failsafe chip | Runs the stabilisation loops; failsafe if the main chip fails |
| Motor outputs | 8 PWM outputs plus 6 auxiliary | 4 ESCs with spare channels |
| Serial ports | 5 UARTs: TELEM 1/2 (flow control), GPS, SERIAL 4/5 | Jetson, RTK and single-point LiDAR each get their own port |
| Sensors | Onboard IMUs (MPU6000, L3GD20 / LSM303D) and MS5611 barometer | Attitude and altitude with no extra boards |
| Power | 4.8–5.4 V from the PDB, with battery voltage and current sensing | Powers the FC and monitors the 6S pack |

The Pixhawk specifications above are taken from the PX4 documentation [\[34\]](../references.md#ed-h01). The Pixhawk covers every interface ARGUS needs, with spare ports for payload. Its specifications also shape navigation. PX4's EKF2 estimator fuses the gyroscopes, accelerometers, magnetometer and MS5611 barometer with the RTK-GNSS and single-point LiDAR to estimate attitude, velocity and position. Attitude is carried as a unit quaternion, which avoids the gimbal-lock singularity of Euler angles and is cheap to propagate, and the floating-point unit keeps the estimator and the cascaded attitude and rate controllers running at hundreds of hertz. The navigation stack never re-fuses these sensors: it consumes the PX4 estimate and returns velocity set-points, so a stable estimate on the Pixhawk underpins everything above it.

#### 2.2.1.2 Onboard Computer: Jetson Orin NX (Best Case) {#onboard-computer-jetson-orin-nx-best-case}

<ElectricalFigure number="60"
  n="3"
  src="/report-assets/electrical-design/jetson-orin-nx.png"
  :width="288"
  :height="213"
  :cardWidth="450"
  caption="Jetson Orin NX (schematic)"
/>



<p class="report-table-caption" id="table-25"><strong>Table 25.</strong> Onboard Computer: Jetson Orin NX (Best Case)</p>

| Feature | Jetson Orin NX 16 GB | Why it fits |
| --- | --- | --- |
| AI compute | 100 TOPS (sparse INT8): 1024 CUDA cores, 32 Tensor cores, 2 DLAs | Runs 4–5 vision models side by side |
| CPU and memory | 8× Cortex-A78AE at 2 GHz, 16 GB LPDDR5 (102.4 GB/s) | ROS 2 and the model pipelines share one memory |
| Power | 10 / 15 / 25 W modes; ≈ 23 W average in our budget | About 3% of flight power |
| Interfaces | UART, USB 3.2, CSI, Gigabit Ethernet | Pixhawk, N10 LiDAR, thermal and RGB camera connect directly |

The Jetson specifications above are taken from the manufacturer's data sheet [\[35\]](../references.md#ed-h02). The Jetson was chosen because it can run four to five vision models concurrently within about 23 W and includes every interface the payload needs. In the Best Case it runs ROS 2 and all FOD models by itself. Published INT8 benchmarks (about 13 frames per second for each of five models) are, however, more optimistic than the estimates from the actual FOD models (see [Computer Vision Based Inspection and Safety System, Section 4.5.2 – Architecture Comparison and Memory Use](../subsystems/computer-vision.md#architecture-comparison-and-memory-use)). The Best Case therefore remains unconfirmed until ROS 2 and the models are benchmarked together.

#### 2.2.1.3 Fallback Computer: Raspberry Pi 5 (Worst Case) {#fallback-computer-raspberry-pi-5-worst-case}

<p class="report-table-caption" id="table-26"><strong>Table 26.</strong> Fallback Computer: Raspberry Pi 5 (Worst Case)</p>

| Feature | Raspberry Pi 5 (8 GB) | Why it fits the Worst Case |
| --- | --- | --- |
| Role | Takes over ROS 2 navigation: SLAM, planner and MAVLink | Jetson is left with the AI models only |
| CPU | 4× Cortex-A76 at 2.4 GHz | 2–3× faster than a Pi 4 |
| Navigation load | N10 LiDAR: 450 points × 10 Hz = 4,500 points/s; velocity commands at 20 Hz | Light data rates for a 4-core CPU |
| Memory and links | 8 GB LPDDR4X, UART, USB 3.0, Gigabit Ethernet | Holds the map and ROS 2 graph; Ethernet carries Jetson detections |
| Cost to the system | ≈ 8 W (1.6 A at 5 V) and 70 g | Adds ≈ 24 W overall (motor draw included) with only a 30 s reduction in flight time |

The Raspberry Pi 5 specifications are taken from its product brief [\[36\]](../references.md#ed-h03), and the 4,500 points/s LiDAR rate follows from the N10's 4.5 kHz measurement rate [\[37\]](../references.md#nav-ref-14). The 8 W and 70 g are estimates used in our budget. Navigation is a light workload (4,500 LiDAR points in and 20 velocity commands out per second) that a four-core Cortex-A76 handles comfortably without competing for the Jetson's GPU. Its cost is small but not negligible: the 70 g forces the motors to draw extra power, so the overall penalty (≈ 24 W) is three times the Pi's own 8 W. There is also virtually no margin left for spare payload, as shown in [the power budget](#power-calculations).

### 2.2.2 Battery Selection {#battery}

#### 2.2.2.1 Battery Requirements and Chosen Pack {#battery-selection}

<p class="report-table-caption" id="table-27"><strong>Table 27.</strong> Battery Requirements and Chosen Pack</p>

| Need | HRB pack | Result |
| --- | --- | --- |
| Voltage | 6S, 22.2 V | Matches the 6S motor test data |
| Runtime | 266 Wh; 213 Wh usable | 16.4 min Best Case, 15.9 min Worst Case (target ≥ 15 min) |
| Current | 25C = 300 A | Avg 35–36 A (3C), Peak 98 A (8C) |
| Weight | ~1.45 kg (est.) | Thrust-to-weight: 2.03 / 2.00 (target ≥ 2.0) |

The pack was selected against four requirements together: the 6S voltage of the motor data, a 15 min flight, the peak current, and a mass that keeps thrust-to-weight at 2.0 or above. It meets the 15 min (see [Navigation and Obstacle Avoidance, Section 3.5.1 – Endurance vs. Mission Time](./navigation-obstacle-avoidance#endurance-vs-mission-time)for justification of design flight time) and 2.0 ratio targets with little margin and about 3× current headroom. The pack capacity, discharge rating and cell voltage limits are taken from the manufacturer's specifications [\[38\]](../references.md#ed-h04). Runtime is mission-weighted with an 80% depth of discharge, and the manufacturer's limit of 3.7 V per cell (22.2 V for the pack) sets the practical lower bound. Real flights should give 10–20% less, and weights are estimates.

## 2.3 Wiring and Hardware Prototype Development {#a3-prototype-development}

The wiring plans below document the proposed arrangement. Wiring assembly and hardware validation are planned for Semester 2.

### 2.3.1 Wiring and Peripheral Communication {#wiring}

#### 2.3.1.1 Electrical Wiring Plan {#electrical-wiring-plan}

<ElectricalFigure number="61"
  n="4"
  src="/report-assets/electrical-design/wiring-plan.png"
  :width="1132"
  :height="544"
  caption="Wiring plan excluding radio link and Pi 5"
/>


As shown in Fig. 61, the battery connects through the 80 A fuse to the PDB (6–60 V, 140 A continuous, 264 A burst [\[39\]](../references.md#ed-h06)), which splits the supply into raw battery voltage for the ESCs, a fused 12 V converter branch for the Jetson, and a regulated 5 V rail for the LiDAR and cameras. The flight controller takes its 5 V from the PDB, and the PDB's 1/21 voltage divider and current-sense output feed the Pixhawk's analogue inputs for battery monitoring, so the PX4 scale factors must be calibrated against a multimeter and a known load. Wire gauge follows branch current: 8 AWG on the main path to match the fuse, 10 AWG for the Jetson branch (about 2.3 A at 12 V) and 20 AWG for the 5 V rail. In the Worst Case the 5 V rail peaks at about 6.1 A against the PDB's 5 A regulated output, so the Pi 5 would need its own 5 V DC converter.

#### 2.3.1.2 Peripheral Communication {#peripheral-communication}

<ElectricalFigure number="62"
  n="5"
  src="/report-assets/electrical-design/peripheral-communication-jetson.png"
  :width="2999"
  :height="1440"
  caption="Peripheral communication, Best Case: Jetson only"
/>


<ElectricalFigure number="63"
  n="6"
  src="/report-assets/electrical-design/peripheral-communication-pi5.png"
  :width="2999"
  :height="1440"
  caption="Peripheral communication, Worst Case: Addition of Pi 5"
/>


<p class="report-table-caption" id="table-28"><strong>Table 28.</strong> Peripheral Communication</p>

| Peripheral | Model | Interface | Power |
| --- | --- | --- | --- |
| RTK-GNSS receiver | Unicore UM980 [\[40\]](../references.md#nav-ref-16) | Pixhawk GPS port (UART) | 5 V from FC |
| Single-point LiDAR | TFmini Plus [\[41\]](../references.md#nav-ref-15) | Pixhawk SERIAL 4/5 (UART) | 5 V from FC |
| 360° LiDAR | N10 [\[37\]](../references.md#nav-ref-14) | USB-UART dongle to Jetson USB-A | 5 V from PDB |
| Thermal camera | BNW2T256T04010ASSWC [\[42\]](../references.md#nav-ref-17) | USB interface board to Jetson USB-A | 5 V from PDB (assumed) |
| RGB camera | To be finalised | CSI or USB | 5 V from PDB (assumed) |

As shown in Fig. 62, the RTK-GNSS and single-point LiDAR feed the state estimator, so they connect to and are powered by the Pixhawk; the high-bandwidth payload connects to the Jetson. TELEM 2 connects to Jetson UART1 on header pins 8 (TXD), 10 (RXD) and 6 (GND), and the FC 5 V pin stays unconnected because the Jetson is powered from the PDB. The 360° LiDAR takes 5 V from the PDB and sends data through a USB-UART dongle. The thermal camera needs a USB interface board, and the RGB camera, not yet purchased, will use CSI or USB.

If the Pi 5 is used (Fig. 63), it takes over the MAVLink connection on TELEM 1 of the Pixhawk and reaches the Jetson over Ethernet. The 360° LiDAR moves to the Pi 5 GPIO pins, and the Pi 5 takes its 5 V from the PDB through its own 5 V converter, as noted above.

This leaves one open design question: how does the Jetson obtain the drone's position and attitude, which it needs to convert detections into FOD coordinates? There are two options, with different trade-offs.

- **Pi 5 relays the pose over Ethernet.** The Pixhawk then has a single companion link, and the wiring and MAVLink configuration stay simple. However, the pose passes through one extra network hop, so timestamps must be aligned between detections and pose.
- **Jetson keeps TELEM 2 as in the Best Case.** The Jetson receives the pose directly with less latency, and the Best Case and Worst Case wiring stay comparable. However, it costs one extra wire, and two computers then talk to the flight controller, which needs more careful MAVLink configuration.

Further testing and verification of latency will decide between them.

## 2.4 Electrical Testing and Verification {#a4-testing}

### 2.4.1 Battery Verification {#battery-verification}

The pack was checked on a balance charger, which measures the internal resistance and voltage of each cell and of the whole pack at full charge. Internal resistance is 1–2 mΩ per cell and 9 mΩ for the whole pack, and cell voltages lie between 4.13 V and 4.20 V.

<p class="report-table-caption" id="table-29"><strong>Table 29.</strong> Battery Verification</p>

| | Per cell | Overall |
| --- | --- | --- |
| Internal resistance measurement | 1, 2, 2, 1, 1, 2 mΩ<br><br>![Balance charger screenshot: internal resistance of each cell](/report-assets/electrical-design/indr.jpg) | 9 mΩ total<br><br>![Balance charger screenshot: overall pack internal resistance](/report-assets/electrical-design/ovrr.jpg) |
| Voltage measurement | 4.19, 4.13, 4.14, 4.20, 4.19, 4.13 V<br><br>![Balance charger screenshot: voltage of each cell](/report-assets/electrical-design/indv.jpg) | 24.98 V (highest 4.202 V, lowest 4.126 V)<br><br>![Balance charger screenshot: overall pack voltage](/report-assets/electrical-design/ovrv.jpg) |

The cells are low in resistance and closely matched, with a spread of 0.076 V, so the pack is healthy and balanced. The 9 mΩ pack resistance is the basis of the voltage sag prediction in Section 2.5.2.

## 2.5 Power and Battery Analysis {#a5-analysis}

### 2.5.1 Power Calculations {#power-calculations}

The power budget is built bottom-up from the component list and the motor test data, for both computer cases, and the same figures size the battery, fuse and wiring. In summary, the Best Case averages 781 W (35.2 A) and the Worst Case 805 W (36.3 A), giving runtimes of 16.4 min and 15.9 min against the 15 min target. Both cases peak near 98 A. The derivations are in the dropdowns below.

<span id="power-budget"></span>

::: details 2.5.1.1 Power Budget

Each load is converted to an average power, $P_{\text{avg}} = V \times I \times \text{duty cycle}$, and electronics are referred to the battery through the regulator efficiencies (5 V rail 90%, 12 V rail 92%). The Jetson is assumed active for 70% of the flight, the Pi 5 for 90% and the radio transmitting for 40%. Propulsion uses the 24 V bench data of the motors [\[43\]](../references.md#ed-h05), weighted by the specified flight-phase profile, plus a 10% real-world margin. Battery current is power divided by the 22.2 V nominal voltage. Weights are estimates (frame 1.5 kg, battery 1.45 kg), giving 4.55 kg (Best Case) and 4.62 kg (Worst Case).

Power budget (peak assumes all four motors at 100% throttle):

<p class="report-table-caption" id="table-30"><strong>Table 30.</strong> Electrical Load Power Budget</p>

| Load | Best Case avg (W) | Worst Case avg (W) | Peak (W) |
| --- | ---: | ---: | ---: |
| Propulsion (4×) | 742 | 757 | 2,115 |
| Compute | 26 | 34 | 35 / 49 |
| Sensors | 11 | 11 | 14 |
| Comms | 3 | 3 | 8 |
| **Total** | **781** | **805** | **2,172 / 2,185** |

System metrics for the two cases:

<p class="report-table-caption" id="table-31"><strong>Table 31.</strong> Power and Endurance Summary</p>

| Metric | Best Case (Jetson only) | Worst Case (Jetson + Pi 5) |
| --- | ---: | ---: |
| Takeoff weight | 4.55 kg | 4.62 kg |
| Avg power | 781 W | 805 W |
| Avg current | 35.2 A | 36.3 A |
| Peak current | 97.8 A | 98.4 A |
| Thrust-to-weight | 2.03 | 2.00 |
| Spare payload | +68 g | ≈ 0 g |
| Runtime | 16.4 min | 15.9 min |

The current and runtime follow directly from the totals. For the Best Case, the average current is 781 W ÷ 22.2 V = 35.2 A, the peak current is 2,172 W ÷ 22.2 V = 97.8 A, and the runtime is 213 Wh ÷ 781 W × 60 = 16.4 min. The Worst Case gives 805 W ÷ 22.2 V = 36.3 A, 2,185 W ÷ 22.2 V = 98.4 A and 213 Wh ÷ 805 W × 60 = 15.9 min.

Propulsion is about 95% of the power, so the computer's own consumption barely changes the budget. What matters is the mass it adds, because the motors must carry every extra gram. The Pi 5 adds 8 W of compute and about 15 W of extra motor power for its 70 g, which lowers thrust-to-weight from 2.03 to 2.00 (derated 10% for 6S voltage sag, against the ≥ 2.0 target) and removes all spare payload. Runtime is the usable energy (80% of 266 Wh, 213 Wh) divided by the average power. The peak current is a sizing case with all motors at full throttle, not normal flight, and is about one third of the pack's 300 A rating.

The main risks are the thin margins and the model inputs. Real flights typically give 10–20% less than the model, which puts both cases at about 13–15 min against the 15 min target. The motor figures are bench data to be replaced by logged flight currents, and several sensor currents are still placeholders or assumptions not yet backed by datasheets: the thermal camera (0.8 A) and RGB camera (0.5 A) are placeholders, the 360° LiDAR current (0.4 A) is assumed because its manual gives no current [\[37\]](../references.md#nav-ref-14), and the telemetry radio (1.2 A while transmitting) is taken from a retailer listing with an unconfirmed current basis. All are deliberately conservative. The TFmini Plus and RTK-GNSS currents come from their datasheets [\[41\]](../references.md#nav-ref-15), [\[40\]](../references.md#nav-ref-16).

:::

<span id="flight-phase-power-profile"></span>

::: details 2.5.1.2 Flight-Phase Power Profile

<p class="report-table-caption" id="table-32"><strong>Table 32.</strong> Flight-Phase Power Profile</p>

| Flight phase | Thrust (× hover) | Time | Power per motor (W) |
| --- | ---: | ---: | ---: |
| Hover | 1.00 | 45% | 165 |
| Forward cruise | 1.10 | 35% | 187 |
| Climb | 1.30 | 10% | 236 |
| Descent | 0.80 | 5% | 119 |
| Aggressive / gust | 1.60 | 5% | 317 |
| **Mission average** | | 100% | **185** |

Each phase takes a multiple of hover thrust, read off the motor test data as power per motor [\[43\]](../references.md#ed-h05), and the phases are weighted by time to give the mission average: 0.45 × 165 + 0.35 × 187 + 0.10 × 236 + 0.05 × 119 + 0.05 × 317 ≈ 185 W per motor. Hover is about 64% throttle, and the aggressive case (1.6× hover thrust, 5% of the flight) represents gusts and avoidance manoeuvres. The profile is a specified assumption, so the logged flight currents in Semester 2 will replace it.

:::

<span id="fuse-selection"></span>

::: details 2.5.1.3 Fuse Selection

An **80 A** battery fuse was chosen. It is about 2.2× the 36 A average and 1.3× the roughly 60 A of an aggressive manoeuvre, so normal flight (hover at about 32 A) will not nuisance-blow it. The 98 A peak needs all four motors at 100% throttle, is brief and is about 1.2× the rating, which typical fuses tolerate for a short time because the blow time falls steeply as the overload grows. However, it must be confirmed against its time–current curve. The pack can deliver far more than 80 A (300 A rating), so a short circuit trips the fuse quickly. Wiring and connectors after the fuse must be rated for at least 80 A (AS150, 8 AWG), and the fuse needs a DC rating above the 25.2 V of a full pack. A 5–10 A inline fuse on the Jetson's 12 V feed protects the compute branch.

:::

### 2.5.2 Predicted Voltage Sag {#predicted-voltage-sag}

The measured 9 mΩ pack resistance predicts a sag of only 0.88 V (3.5%) at the 98 A peak, well inside the 10% assumed in the power calculations. The table and the reasoning are in the dropdown below.

::: details 2.5.2.1 Sag Prediction and Margin

<p class="report-table-caption" id="table-33"><strong>Table 33.</strong> Predicted Voltage Sag</p>

| Load current | Voltage sag | Pack voltage | Per cell | Heat in pack |
| --- | ---: | ---: | ---: | ---: |
| 10 A (Discharge test current) | 0.09 V | 24.89 V | 4.15 V | 1 W |
| 32 A (Hover) | 0.29 V | 24.69 V | 4.12 V | 9 W |
| 35 A (Average flight) | 0.32 V | 24.67 V | 4.11 V | 11 W |
| 60 A (Aggressive manoeuvre) | 0.54 V | 24.44 V | 4.07 V | 32 W |
| 98 A (Peak, all motors 100%) | 0.88 V | 24.10 V | 4.02 V | 86 W |

$$
V_{\text{sag}} = I \times R, \qquad V_{\text{pack}} = V_{\text{rest}} - V_{\text{sag}}, \qquad V_{\text{cell}} = \frac{V_{\text{pack}}}{6}, \qquad P_{\text{heat}} = I^{2} R
$$

At the 98 A peak, $V_{\text{sag}} = 98 \times 0.009 = 0.88$ V, so the pack falls from the 24.98 V rest voltage to 24.10 V (4.02 V per cell), and $P_{\text{heat}} = 98^{2} \times 0.009 \approx 86$ W is dissipated inside the pack.

The power calculations assume a 10% sag, but the predicted sag is only about 3.5% at the 98 A peak, leaving the pack at about 24.1 V, about 1.9 V above the 22.2 V minimum. The sag scales with internal resistance, and 10% (about 2.5 V) would only be reached at about 25 mΩ, nearly three times the measured value. The prediction uses a charger measurement at full charge, the resistance under sustained load is likely higher, and the margin narrows as the pack drains, so it is to be confirmed with a loaded discharge test.

:::

## 2.6 Discussion of Future Works {#a6-problems-project-plan}

### 2.6.1 Semester 2 Development Plan {#electrical-future-works}

The following activities are planned for Semester 2 to replace the assumptions in the power budget with measurements and to validate the wiring, sensors and computer configuration.

<span id="electrical-future-works-1"></span>

::: details 2.6.1.1 Wiring Assembly and Live Power Testing

The AS150 plugs, 80 A fuse, PDB battery output and 5 V rail will be soldered and assembled. The wiring will then be validated by measuring the real power draw against the budget, and flight currents will be logged to confirm the ratings of the components, in particular the fuse and the 5 V rail. The logged currents will replace the bench-data propulsion figures and the placeholder sensor currents (thermal camera, RGB camera, 360° LiDAR and telemetry radio). If the Pi 5 is added, its separate 5 V converter will be wired and its 6.1 A rail peak checked.

:::

::: details 2.6.1.2 Sensor and Power-Monitor Calibration

The sensors, including the PDB voltage and current scale factors, will be calibrated and their outputs verified before they are physically mounted. The PDB's 1/21 voltage divider and current-sense output will be checked against a multimeter and a known load, and the PX4 battery scale parameters adjusted to match, so that the flight controller reports an accurate battery level. Other peripherals, such as the RTK-GNSS receiver and the LiDARs, will be calibrated according to their user manuals [\[37\]](../references.md#nav-ref-14)–[\[40\]](../references.md#nav-ref-16) and tested under various operating conditions before integration.

:::

::: details 2.6.1.3 Loaded Discharge Test of the Battery

The predicted voltage sag will be checked with a loaded discharge test. The available discharger is limited to about 10 A at the pack voltage, so the measured sag at that current will be compared with the 0.09 V prediction and the resistance extrapolated to the 98 A peak. Repeating the test at lower states of charge will show how the margin narrows as the pack drains, and logged in-flight voltage will confirm it at the full load.

:::

::: details 2.6.1.4 Camera and Compute Integration

The thermal camera will be connected through its USB interface board and the RGB camera interface chosen. ROS 2 and the AI models will be benchmarked together on the Jetson to confirm the Best Case, or the Pi 5 will be added. If the Pi 5 is added, latency tests will decide how the Jetson obtains the drone's pose (relayed by the Pi 5 over Ethernet or received directly on TELEM 2). The peripherals will then be integrated and tested for the full-scale navigation and FOD implementation.

:::

::: details 2.6.1.5 Telemetry Radio Selection and Integration

The telemetry radio that sends FOD coordinates to the UGV is still being decided, and its 1.2 A current in the budget is unconfirmed. The chosen radio will then be added to the wiring plan, and its measured current will replace the budget value. It will be connected to either the Jetson or the Pi 5 based on the workload capacity of the Jetson. If the Jetson reaches full capacity with running just the FOD models, then the Communication Architecture will be moved to the Pi 5. Therefore, the chosen radio must be flexible in its connection to either the Jetson or the Pi 5.

:::

</div>