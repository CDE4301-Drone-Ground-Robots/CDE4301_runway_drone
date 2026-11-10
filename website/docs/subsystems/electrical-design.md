---
title: "Electrical Design"
outline: false
prev: false
next: false
---

<script setup>
import ElectricalFigure from './components/ElectricalFigure.vue'

</script>

<div class="cv-report">

<p class="chapter-kicker">FOD ARGUS / ELECTRICAL DESIGN</p>

# Electrical Design

<SubsystemLead class="cv-report-byline" name="Kummarikunta Talitha" matric="A0286653R" portrait="/team/Talitha.jpg" />

## Electrical System Overview {#electrical-overview}

The electrical system connects the battery, propulsion, flight controller, onboard computer and sensor payload (Figure ED-01). The 6S battery feeds the main power distribution board (PDB) through a battery fuse. The PDB supplies battery output to the four ESCs and to a DC-DC step-down converter for the Jetson Orin NX, and regulated outputs to the sensors and telemetry radio. The flight controller reads the battery level, sends PWM signals to the ESCs, and talks to the Jetson over the computer link. The Jetson receives the 3D map and FOD input from the LiDAR and cameras, and sends FOD coordinates through the telemetry radio to the UGV.

<ElectricalFigure n="1" src="/report-assets/electrical-design/electrical-system-interaction.png" :width="1930" :height="985" caption="Electrical System Interaction" />


## Flight Controller and Onboard Computer Selection {#compute-selection}

The aircraft carries one flight controller and one onboard computer, with no duplicated hardware. The flight controller owns the hard real-time loops (attitude estimation, motor mixing, failsafes), while the onboard computer owns perception and navigation. Two computer configurations are carried through every calculation in this chapter. In the **Best Case** the Jetson Orin NX runs ROS 2 and all AI models alone. In the **Worst Case** the Jetson is overloaded, so a Raspberry Pi 5 takes over ROS 2 navigation and the Jetson runs only the AI models. The Pi 5 is a load-shedding fallback, not a redundancy, and the power budget is sized so that either case flies.

### Flight Controller: Pixhawk (3DR)

<ElectricalFigure
  n="2"
  src="/report-assets/electrical-design/pixhawk-3dr.png"
  :width="272"
  :height="150"
  :cardWidth="365"
  caption="Pixhawk (3DR)"
/>



| Feature | Pixhawk | Why it fits |
| --- | --- | --- |
| Processor | STM32F427 Cortex-M4F with FPU, 256 KB RAM, 2 MB flash; separate failsafe chip | Runs the stabilisation loops; failsafe if the main chip fails |
| Motor outputs | 8 PWM outputs plus 6 auxiliary | 4 ESCs with spare channels |
| Serial ports | 5 UARTs: TELEM 1/2 (flow control), GPS, SERIAL 4/5 | Jetson, RTK and single-point LiDAR each get their own port |
| Sensors | Onboard IMUs (MPU6000, L3GD20 / LSM303D) and MS5611 barometer | Attitude and altitude with no extra boards |
| Power | 4.8–5.4 V from the PDB, with battery voltage and current sensing | Powers the FC and monitors the 6S pack |

The Pixhawk specifications above are taken from the PX4 documentation [\[ED-H01\]](../references.md#ed-h01). The Pixhawk covers every interface ARGUS needs, with spare ports for payload. Its specifications also shape navigation. PX4's EKF2 estimator fuses the gyroscopes, accelerometers, magnetometer and MS5611 barometer with the RTK-GNSS and single-point LiDAR to estimate attitude, velocity and position. Attitude is carried as a unit quaternion, which avoids the gimbal-lock singularity of Euler angles and is cheap to propagate, and the floating-point unit keeps the estimator and the cascaded attitude and rate controllers running at hundreds of hertz. The navigation stack never re-fuses these sensors: it consumes the PX4 estimate and returns velocity set-points, so a stable estimate on the Pixhawk underpins everything above it.

### Onboard Computer: Jetson Orin NX (Best Case)

<ElectricalFigure
  n="3"
  src="/report-assets/electrical-design/jetson-orin-nx.png"
  :width="288"
  :height="213"
  :cardWidth="450"
  caption="Jetson Orin NX (schematic)"
/>



| Feature | Jetson Orin NX 16 GB | Why it fits |
| --- | --- | --- |
| AI compute | 100 TOPS (sparse INT8): 1024 CUDA cores, 32 Tensor cores, 2 DLAs | Runs 4–5 vision models side by side |
| CPU and memory | 8× Cortex-A78AE at 2 GHz, 16 GB LPDDR5 (102.4 GB/s) | ROS 2 and the model pipelines share one memory |
| Power | 10 / 15 / 25 W modes; ≈ 23 W average in our budget | About 3% of flight power |
| Interfaces | UART, USB 3.2, CSI, Gigabit Ethernet | Pixhawk, N10 LiDAR, thermal and RGB camera connect directly |

The Jetson specifications above are taken from the manufacturer's data sheet [\[ED-H02\]](../references.md#ed-h02). The Jetson was chosen because it can run four to five vision models concurrently within about 23 W and includes every interface the payload needs. In the Best Case it runs ROS 2 and all FOD models by itself. Published INT8 benchmarks (about 13 frames per second for each of five models) are, however, more optimistic than the estimates from the actual FOD models (see [Computer Vision Based Inspection and Safety System, Section 2 – Architecture Comparison and Memory Use](../subsystems/computer-vision.md#architecture-comparison-and-memory-use)). The Best Case therefore remains unconfirmed until ROS 2 and the models are benchmarked together.

### Fallback Computer: Raspberry Pi 5 (Worst Case)

| Feature | Raspberry Pi 5 (8 GB) | Why it fits the Worst Case |
| --- | --- | --- |
| Role | Takes over ROS 2 navigation: SLAM, planner and MAVLink | Jetson is left with the AI models only |
| CPU | 4× Cortex-A76 at 2.4 GHz | 2–3× faster than a Pi 4 |
| Navigation load | N10 LiDAR: 450 points × 10 Hz = 4,500 points/s; velocity commands at 20 Hz | Light data rates for a 4-core CPU |
| Memory and links | 8 GB LPDDR4X, UART, USB 3.0, Gigabit Ethernet | Holds the map and ROS 2 graph; Ethernet carries Jetson detections |
| Cost to the system | ≈ 8 W (1.6 A at 5 V) and 70 g | Adds ≈ 24 W overall (motor draw included) with only a 30 s reduction in flight time |

The Raspberry Pi 5 specifications are taken from its product brief [\[ED-H03\]](../references.md#ed-h03), and the 4,500 points/s LiDAR rate follows from the N10's 4.5 kHz measurement rate [\[14\]](../references.md#nav-ref-14). The 8 W and 70 g are estimates used in our budget. Navigation is a light workload (4,500 LiDAR points in and 20 velocity commands out per second) that a four-core Cortex-A76 handles comfortably without competing for the Jetson's GPU. Its cost is small but not negligible: the 70 g forces the motors to draw extra power, so the overall penalty (≈ 24 W) is three times the Pi's own 8 W. There is also virtually no margin left for spare payload, as shown in the next section.

## Power Calculations {#power-calculations}

The power budget is built bottom-up from the component list and the motor test data, for various operating cases, and the same figures size the battery, fuse and wiring.

### Power Budget

Each load is converted to an average power, $P_{\text{avg}} = V \times I \times \text{duty cycle}$, and electronics are referred to the battery through the regulator efficiencies (5 V rail 90%, 12 V rail 92%). The Jetson is assumed active for 70% of the flight, the Pi 5 for 90% and the radio transmitting for 40%. Propulsion uses the 24 V bench data of the motors [\[ED-H05\]](../references.md#ed-h05), weighted by the specified flight-phase profile, plus a 10% real-world margin. Battery current is power divided by the 22.2 V nominal voltage. Weights are estimates (frame 1.5 kg, battery 1.45 kg), giving 4.55 kg (Best Case) and 4.62 kg (Worst Case).

Power budget (peak assumes all four motors at 100% throttle):

| Load | Best Case avg (W) | Worst Case avg (W) | Peak (W) |
| --- | ---: | ---: | ---: |
| Propulsion (4×) | 742 | 757 | 2,115 |
| Compute | 26 | 34 | 35 / 49 |
| Sensors | 11 | 11 | 14 |
| Comms | 3 | 3 | 8 |
| **Total** | **781** | **805** | **2,172 / 2,185** |

System metrics for the two cases:

| Metric | Best Case (Jetson only) | Worst Case (Jetson + Pi 5) |
| --- | ---: | ---: |
| Takeoff weight | 4.55 kg | 4.62 kg |
| Avg power | 781 W | 805 W |
| Avg current | 35.2 A | 36.3 A |
| Peak current | 97.8 A | 98.4 A |
| Thrust-to-weight | 2.03 | 2.00 |
| Spare payload | +68 g | ≈ 0 g |
| Runtime | 16.4 min | 15.9 min |

Propulsion is about 95% of the power, so the computer's own consumption barely changes the budget. What matters is the mass it adds, because the motors must carry every extra gram. The Pi 5 adds 8 W of compute and about 15 W of extra motor power for its 70 g, which lowers thrust-to-weight from 2.03 to 2.00 (derated 10% for 6S voltage sag, against the ≥ 2.0 target) and removes all spare payload. Runtime is the usable energy (80% of 266 Wh, 213 Wh) divided by the average power. The peak current is a sizing case with all motors at full throttle, not normal flight, and is about one third of the pack's 300 A rating.

The main risks are the thin margins and the model inputs. Real flights typically give 10–20% less than the model, which puts both cases at about 13–15 min against the 15 min target. The motor figures are bench data to be replaced by logged flight currents, and several sensor currents are still placeholders or assumptions not yet backed by datasheets: the thermal camera (0.8 A) and RGB camera (0.5 A) are placeholders, the 360° LiDAR current (0.4 A) is assumed because its manual gives no current [\[14\]](../references.md#nav-ref-14), and the telemetry radio (1.2 A while transmitting) is taken from a retailer listing with an unconfirmed current basis. All are deliberately conservative. The TFmini Plus and RTK-GNSS currents come from their datasheets [\[15\]](../references.md#nav-ref-15), [\[16\]](../references.md#nav-ref-16).

### Flight-Phase Power Profile

| Flight phase | Thrust (× hover) | Time | Power per motor (W) |
| --- | ---: | ---: | ---: |
| Hover | 1.00 | 45% | 165 |
| Forward cruise | 1.10 | 35% | 187 |
| Climb | 1.30 | 10% | 236 |
| Descent | 0.80 | 5% | 119 |
| Aggressive / gust | 1.60 | 5% | 317 |
| **Mission average** | | 100% | **185** |

Each phase takes a multiple of hover thrust, read off the motor test data as power per motor [\[ED-H05\]](../references.md#ed-h05), and the phases are weighted by time to give the mission average. Hover is about 64% throttle, and the aggressive case (1.6× hover thrust, 5% of the flight) represents gusts and avoidance manoeuvres.

### Fuse Selection

An **80 A** battery fuse was chosen. It is about 2.2× the 36 A average and 1.3× the roughly 60 A of an aggressive manoeuvre, so normal flight (hover at about 32 A) will not nuisance-blow it. The 98 A peak needs all four motors at 100% throttle, is brief and is about 1.2× the rating, which typical fuses tolerate for a short time. However, it must be confirmed against its time–current curve. The pack can deliver far more than 80 A (300 A rating), so a short circuit trips the fuse quickly. Wiring and connectors after the fuse must be rated for at least 80 A (AS150, 8 AWG), and the fuse needs a DC rating above the 25.2 V of a full pack. A 5–10 A inline fuse on the Jetson's 12 V feed protects the compute branch.

## Battery Selection and Initial Verifications {#battery}

### Battery Selection

| Need | HRB pack | Result |
| --- | --- | --- |
| Voltage | 6S, 22.2 V | Matches the 6S motor test data |
| Runtime | 266 Wh; 213 Wh usable | 16.4 min Best Case, 15.9 min Worst Case (target ≥ 15 min) |
| Current | 25C = 300 A | Avg 35–36 A (3C), Peak 98 A (8C) |
| Weight | ~1.45 kg (est.) | Thrust-to-weight: 2.03 / 2.00 (target ≥ 2.0) |

The pack was selected against four requirements together: the 6S voltage of the motor data, a 15 min flight, the peak current, and a mass that keeps thrust-to-weight at 2.0 or above. It meets the 15 min (see *Navigation and Obstacle Avoidance, Section 3 – Why 15 min?*) and 2.0 ratio targets with little margin and about 3× current headroom. The pack capacity, discharge rating and cell voltage limits are taken from the manufacturer's specifications [\[ED-H04\]](../references.md#ed-h04). Runtime is mission-weighted with an 80% depth of discharge, and the manufacturer's limit of 3.7 V per cell (22.2 V for the pack) sets the practical lower bound. Real flights should give 10–20% less, and weights are estimates.

### Battery Verification

The pack was checked on a balance charger. Internal resistance is 1–2 mΩ per cell and 9 mΩ for the whole pack, and cell voltages lie between 4.13 V and 4.20 V.

| | Per cell | Overall |
| --- | --- | --- |
| Internal resistance measurement | 1, 2, 2, 1, 1, 2 mΩ | 9 mΩ total |
| Voltage measurement | 4.19, 4.13, 4.14, 4.20, 4.19, 4.13 V | 24.98 V (highest 4.202 V, lowest 4.126 V) |

The cells are low in resistance and closely matched, with a spread of 0.076 V, so the pack is healthy and balanced.

### Predicted Voltage Sag

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

The power calculations assume a 10% sag, but the predicted sag is only about 3.5% at the 98 A peak, leaving the pack at about 24.1 V, about 1.9 V above the 22.2 V minimum. The sag scales with internal resistance, and 10% would only be reached at about 25 mΩ, nearly three times the measured value. The prediction uses a charger measurement at full charge, the resistance under sustained load is likely higher, and the margin narrows as the pack drains, so it is to be confirmed with a loaded discharge test.

## Wiring and Peripheral Communication {#wiring}

### Electrical Wiring Plan

<ElectricalFigure
  n="4"
  src="/report-assets/electrical-design/wiring-plan.png"
  :width="1132"
  :height="544"
  caption="Wiring plan excluding radio link and Pi 5"
/>


As shown in Figure ED-04, the battery connects through the 80 A fuse to the PDB (6–60 V, 140 A continuous, 264 A burst [\[ED-H06\]](../references.md#ed-h06)), which splits the supply into raw battery voltage for the ESCs, a fused 12 V converter branch for the Jetson, and a regulated 5 V rail for the LiDAR and cameras. The flight controller takes its 5 V from the PDB, and the PDB's 1/21 voltage divider and current-sense output feed the Pixhawk's analogue inputs for battery monitoring, so the PX4 scale factors must be calibrated against a multimeter and a known load. Wire gauge follows branch current: 8 AWG on the main path to match the fuse, 10 AWG for the Jetson branch (about 2.3 A at 12 V) and 20 AWG for the 5 V rail. In the Worst Case the 5 V rail peaks at about 6.1 A against the PDB's 5 A regulated output, so the Pi 5 would need its own 5 V DC converter.

### Peripheral Communication

<ElectricalFigure 
  n="5"
  src="/report-assets/electrical-design/peripheral-communication-jetson.png"
  :width="2999"
  :height="1440"
  caption="Peripheral communication, Best Case: Jetson only"
/>


<ElectricalFigure
  n="6"
  src="/report-assets/electrical-design/peripheral-communication-pi5.png"
  :width="2999"
  :height="1440"
  caption="Peripheral communication, Worst Case: Addition of Pi 5"
/>


| Peripheral | Model | Interface | Power |
| --- | --- | --- | --- |
| RTK-GNSS receiver | Unicore UM980 [\[16\]](../references.md#nav-ref-16) | Pixhawk GPS port (UART) | 5 V from FC |
| Single-point LiDAR | TFmini Plus [\[15\]](../references.md#nav-ref-15) | Pixhawk SERIAL 4/5 (UART) | 5 V from FC |
| 360° LiDAR | N10 [\[14\]](../references.md#nav-ref-14) | USB-UART dongle to Jetson USB-A | 5 V from PDB |
| Thermal camera | BNW2T256T04010ASSWC [\[17\]](../references.md#nav-ref-17) | USB interface board to Jetson USB-A | 5 V from PDB (assumed) |
| RGB camera | To be decided | CSI or USB | 5 V from PDB (assumed) |

As shown in Figure ED-05, the RTK-GNSS and single-point LiDAR feed the state estimator, so they connect to and are powered by the Pixhawk; the high-bandwidth payload connects to the Jetson. TELEM 2 connects to Jetson UART1 on header pins 8 (TXD), 10 (RXD) and 6 (GND), and the FC 5 V pin stays unconnected because the Jetson is powered from the PDB. The 360° LiDAR takes 5 V from the PDB and sends data through a USB-UART dongle. The thermal camera needs a USB interface board, and the RGB camera, not yet purchased, will use CSI or USB.

If the Pi 5 is used (Figure ED-06), it takes over the MAVLink connection on TELEM 1 of the Pixhawk and reaches the Jetson over Ethernet. The 360° LiDAR moves to the Pi 5 GPIO pins, and the Pi 5 takes its 5 V from the PDB through its own 5 V converter, as noted above.

This leaves one open design question: how does the Jetson obtain the drone's position and attitude, which it needs to convert detections into FOD coordinates? There are two options, with different trade-offs.

- **Pi 5 relays the pose over Ethernet.** The Pixhawk then has a single companion link, and the wiring and MAVLink configuration stay simple. However, the pose passes through one extra network hop, so timestamps must be aligned between detections and pose.
- **Jetson keeps TELEM 2 as in the Best Case.** The Jetson receives the pose directly with less latency, and the Best Case and Worst Case wiring stay comparable. However, it costs one extra wire, and two computers then talk to the flight controller, which needs more careful MAVLink configuration.

Further testing and verification of latency will decide between them.

## Semester 2 Development Plan {#electrical-future-works}

### Electrical Future Works

**Wiring assembly for live testing.** The AS150 plugs, 80 A fuse, PDB battery output and 5 V rail will be soldered and assembled. The wiring will then be validated by measuring the real power draw against the budget, and flight currents will be logged to confirm the ratings of the components, in particular the fuse and the 5 V rail.

**Sensor calibration and validation.** The sensors, including the PDB voltage and current scale factors, will be calibrated and their outputs verified before they are physically mounted. Data accuracy will then be validated under different operating conditions, and the predicted voltage sag will be checked with a loaded discharge test. Other peripherals, such as the RTK-GNSS receiver and the LiDARs, will be calibrated according to their user manuals [\[14\]](../references.md#nav-ref-14)–[\[16\]](../references.md#nav-ref-16) and tested under various operating conditions before integration.

**Camera and compute integration.** The thermal camera will be connected through its USB interface board and the RGB camera interface chosen. ROS 2 and the AI models will be benchmarked together on the Jetson to confirm the Best Case, or the Pi 5 will be added. The peripherals will then be integrated and tested for the full-scale navigation and FOD implementation.

</div>