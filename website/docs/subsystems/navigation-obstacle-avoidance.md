---
title: "Navigation and Obstacle Avoidance"
outline: false
prev: false
next: false
aside: false
pageClass: subsystem-report-page
---

<div class="cv-report rubric-report" style="--report-chapter: '3'">

<p class="chapter-kicker">FOD ARGUS / NAVIGATION &amp; OBSTACLE AVOIDANCE</p>

<script setup>
import SectorPlanner from '../.vitepress/theme/components/SectorPlanner.vue'
import ElectricalFigure from './components/ElectricalFigure.vue'
import { withBase } from 'vitepress'
</script>

# 3. Navigation & Obstacle Avoidance {#navigation-obstacle-avoidance}

<SubsystemLead class="cv-report-byline" name="Kummarikunta Talitha" matric="A0286653R" portrait="/team/Talitha.jpg" />

## 3.1 Objective and Requirements {#a1-objective-scope-context}

The objective of the navigation subsystem is to fly the UAV over a runway sector on a planned route, survey it with both cameras, avoid birds and static obstacles, and return and land within the available flight time and battery. The subsystem was developed and tested using simulations in Semester 1, and the same logic will move to the hardware in Semester 2. The requirements below follow from the mission, and the rest of this chapter designs for them and tests against them.

<p class="report-table-caption" id="table-33"><strong>Table 33.</strong> Navigation Requirements</p>

| Requirement | What it means and the target |
| --- | --- |
| Coverage | One sortie must survey one sector of 30 m along the runway by 60 m across. A patch of ground only counts as surveyed once both the RGB camera and the thermal camera have covered it |
| Endurance | One sortie must finish inside the 15 min flight window. In practice the drone takes off with the battery at 95% and must start returning at about 25%, and the 70% of the pack between those two levels lasts about 13.9 min of flight, so a sortie must fit inside 13.9 min |
| Lane keeping | The drone flies along parallel lanes that are 1.76 m apart, which is the sideways distance between the centre lines of two neighbouring lanes, so it must stay close to its lane. If it is more than 3 m away from the lane for 10 s, the flight is aborted and the drone lands |
| Obstacle avoidance | The drone must keep at least 1.3 m away from every tracked bird, and it must go around, or skip, static obstacles such as trees and poles that block a lane |
| Wind | The survey must be completed in winds of up to 15 m/s, including gusts |
| Safety | When a fault occurs (strong wind, low battery, loss of GNSS position, motor failure or a flock of birds), the drone must return home, land immediately, or refuse to take off, depending on how serious the fault is |
| Hand-off | The position of every FOD found must be passed on to FOD Hunter in the message format that FOD Hunter expects |

The chapter follows the order of the design work. Section 3.1 sets the requirements, the concerns that were foreseen and the sensors and software used. Section 3.2 develops the navigation methods, and Section 3.3 shows how they are combined into one state machine. Sections 3.4 and 3.5 test and analyse the result in simulation, and Section 3.6 lists what remains to be done.

### 3.1.1 Design Concerns and Sensor Models {#design-concerns}

#### 3.1.1.1 Initial Concerns and Solutions {#initial-concerns-and-solutions}

Before any simulation was run, the concerns that could affect the navigation design were listed together with the design response to each. The table below records them, and the later sections test whether each response held.

<p class="report-table-caption" id="table-34"><strong>Table 34.</strong> Initial Concerns and Solutions</p>

| Concern | How the design responds, as modelled in the simulation |
| --- | --- |
| The LiDAR range is short on dark targets in strong sunlight (about 4.7 m) | The cruise speed is capped so that the drone can stop within that range: 4.23 m/s normally and 2.2 m/s in strong sunlight. Known boundaries are loaded in advance as keep-out zones |
| Birds move unpredictably | Each tracked bird gets its own linear Kalman filter whose uncertainty grows with time, the threat is graded on five levels, and the avoider chooses a safe velocity using collision cones |
| Static obstacles can block a lane | An obstacle that has been seen continuously for 1.0 s is mapped as static, and the route is then edited with a bypass or a shortened lane. If the lane stays blocked the drone holds, skips the strip after 10 s and revisits it later |
| Wind tilts the drone | A cross-track pull brings the drone back onto the lane, and the LiDAR scan is corrected for the drone's tilt. A wind guard slows the lanes at 14° of lean and lands the drone at 33° |
| Endurance and battery are limited | The sector is sized to the battery pack. A 30 m sector uses about 40% of the pack in calm air and 69% in a 15 m/s crosswind. The drone launches at 95% and returns at about 25% |
| The FOD coverage criterion must be met | The RGB camera (2 × 2 m footprint) resolves small objects, and the thermal camera adds a second, independent view of every cell |
| The position of each FOD must reach FOD Hunter | The alert format is defined, and alerts are queued and sent at the start of each lane on a ROS topic (log-only for now), in the same message format that FOD Hunter uses |

#### 3.1.1.2 Sensor Specifications Used {#sensor-specifications-used}

The simulation models the following sensors. The numbers are taken from the manufacturers' datasheets and the footprints on the ground are calculated for the 5 m flight altitude.

<p class="report-table-caption" id="table-35"><strong>Table 35.</strong> Sensor Specifications Used</p>

| Sensor | What was modelled | What the drone uses it for |
| --- | --- | --- |
| Leishen N10 2D LiDAR [\[37\]](../references#nav-ref-14) | A 360° scan with 450 beams at 10 Hz. Range is 12 m on a target that reflects 70% of the light, 7.9 m at 30% and 4.7 m in strong sunlight. Accuracy is ±3 cm, and the scan is in one flat plane | The main avoidance sensor. It detects birds (moving) and trees and poles (static), and its range sets the maximum flight speed |
| TFmini Plus single-point LiDAR [\[41\]](../references#nav-ref-15) | 12 m range on a target that reflects 90%, a 3.6° beam pointed 3° above the nose, ±3 cm accuracy | A forward look-ahead that sees above the flat N10 scan. Its benefit is not yet shown in simulation |
| RGB camera e-CAM56_CUONX (looking straight down) | Sony IMX568 sensor with a global shutter, 2472 × 2064 pixels and a fixed M12 lens. In the simulation it is modelled as 640 × 640 pixels with a 22.6° horizontal field of view, which covers 2 m × 2 m on the ground at 5 m, processed at 5 Hz with 90% detection (50% at the edge of the image) | The main FOD detector, looking straight down the lane. The global shutter avoids image skew at the 4.2 m/s survey speed |
| Thermal camera BNW2T256T04010ASSWC [\[42\]](../references#nav-ref-17) | 256 × 192 pixels, 4.0 mm lens, 45.5° × 33.5° field of view, tilted 45° to the side so that it sees a strip from 2.7 m to 9.3 m beside the track | Verifies each FOD with a second, independent view taken from the side |
| Unicore UM980 GNSS receiver [\[40\]](../references#nav-ref-16) | RTK positioning, 2 cm horizontal and 3 cm vertical accuracy at 10 Hz, fused with the other sensors in the PX4 EKF2 estimator | The position of the drone, which gives centimetre-level lane keeping and the coordinates of each FOD |

#### 3.1.1.3 Simulation Software Used {#software-used}

Every result in this chapter comes from simulation, so the software is introduced here, before the results are used. The functions were verified and rendered with the following software, and the way the parts connect is shown in Figure NAV-01.

- ROS 2 Jazzy: communication between the robot software nodes
- Gazebo Harmonic: 3D physics and environment simulator
- PX4 Autopilot SITL (Software-in-the-Loop): flight control software
- Micro XRCE-DDS Agent v2.4.3 (uXRCE-DDS): bridge between ROS 2 and PX4
- Python: offline simulation and scripting

<ElectricalFigure n="1" src="/report-assets/navigation-obstacle-avoidance/software-stack.png" :width="1600" :height="900" caption="Simulation software stack." />

The design numbers in the following sections come from an offline simulation in Python, which runs each scenario with several random seeds. The Gazebo and PX4 runs, described in [Section 3.4](#a4-testing), then confirm that the real flight controller behaves as the offline model predicts.

### 3.1.2 Survey Criteria {#survey-criteria}

The survey criteria were set before the path was designed, because they decide how many lanes are needed and when the purpose of the mission has been served. The runway is split into sectors, and one sortie surveys one sector. A runway of 300 m to 2.5 km is longer than one 15 min flight, so a 2.5 km runway is about 84 sectors and a 300 m runway is 10 sectors. A patch of ground counts as surveyed only when **both** cameras have covered it. A sector can be flown with lanes along the runway (36 lanes) or across it (about 17 lanes), as shown in Figure NAV-02.

<ElectricalFigure n="2" src="/report-assets/navigation-obstacle-avoidance/survey-sectors-split.png" :width="1070" :height="403" caption="Runway sectors (30 m × 60 m, not to scale) and the two ways to fly one sector: lanes along (36 lanes) and lanes across (about 17 lanes)." />

The two cameras play different roles. The RGB camera looks straight down and detects FOD, and the thermal camera is tilted to the side and independently verifies it, so a patch of ground needs both to count. The RGB camera sees a strip of ground 2.0 m wide, and the thermal camera sees a strip 6.62 m wide, starting 2.7 m and ending 9.3 m to the side of the track.

The **lane pitch** is the sideways distance between the centre lines of two neighbouring lanes, and it is 1.76 m. It follows from the narrower RGB strip: the next lane is placed 1.76 m to the side, so its 2 m RGB strip overlaps the previous strip by 0.24 m (about 10%). This overlap leaves no gap if the drone drifts slightly off its lane. The thermal strip is much wider than the lane pitch, so as the drone flies lane after lane, the thermal strips of neighbouring lanes also overlap, and every patch of ground is covered by both cameras. Figure NAV-03 shows the coverage of one lane seen from behind, to scale. In the simulation overlay, green is RGB and cyan is thermal only. Any patch that is still missing one camera after all the lanes have been flown is flown again in a revisit pass, up to 6 passes.

<ElectricalFigure n="3" src="/report-assets/navigation-obstacle-avoidance/survey-sectors-lane.png" :width="980" :height="202" caption="Coverage of one lane seen from behind (to scale). Green is RGB and cyan is thermal only in the simulation overlay." />

<details class="custom-block details">
<summary>Sources for the survey criteria</summary>

Sources: runway dimensions follow FAA AC 150/5300-13B [\[44\]](../references#nav-ref-3) and ICAO Annex 14 Vol. I [\[45\]](../references#nav-ref-13). The RGB footprint is calculated from the e-CAM56_CUONX sensor and M12 lens, and the thermal footprint from the BNW2T256T04010ASSWC datasheet [\[42\]](../references#nav-ref-17).

</details>

## 3.2 Navigation Methodology and Concept Development {#a2-methodology-concept-development}

The navigation concept was developed from the top down starting from the mission itself (survey one sector safely within one battery charge) and then broken into questions, designed one at a time: where to fly, how to avoid obstacles, how to stay on the route, what to do when something fails, and how much wind the drone can tolerate.

The survey is first planned as a set of lanes that fits the camera footprint and the battery, as described in [Survey Planning](#survey-planning). Obstacles are then handled at two levels: the global route is edited around static obstacles, and a local planner steers around moving birds, as described in [Obstacle Avoidance](#obstacle-avoidance). The drone is held on the route by a feedback loop on the EKF2 position and is flown within limits on speed and acceleration. Faults are handled by the [Failsafes](#failsafes). Wind is treated in two ways in [Wind Kinematics](#wind-kinematics): first as a **load on the airframe**, meaning the force that pushes the drone sideways and makes it lean to stay in place, and second as a **disturbance on the lane**, meaning the gusts that push the drone off its 1.76 m wide lane while it flies.

All of these act through one mission state machine, shown in Figure NAV-04. In the diagram, circles are states, arrows are transitions labelled with their trigger, and red arrows are failsafes. Each part of the state machine is highlighted in the section that explains it, and the whole machine is described in [Section 3.3](#a3-prototype-development).

<ElectricalFigure n="4" src="/report-assets/navigation-obstacle-avoidance/fsm-full.png" :width="2547" :height="1334" caption="Navigation state machine. One flight covers one sector (at most 15 min of battery)." />

### 3.2.1 Survey Planning {#survey-planning}

#### 3.2.1.1 Camera Footprint vs. Sector Size {#camera-footprint-vs-sector-size}

The camera footprint was the largest change to the plan between the first and second design iteration. For the same navigation and power model, a narrower camera swath means more lanes, and so a smaller sector per sortie.

<p class="report-table-caption" id="table-36"><strong>Table 36.</strong> Camera Footprint vs. Sector Size</p>

| | Previous RGB camera (5.77 × 4.33 m footprint) | Current RGB camera (2 × 2 m footprint) |
| --- | ---: | ---: |
| Sector surveyed per sortie | 60 × 60 m | 30 × 60 m |
| Number of lanes along the runway | 13 | 36 |
| Flight time in calm air (lanes along) | 315 s (5.3 min) | 476 s (7.9 min) |
| Battery used in calm air (lanes along) | 26% | 40% |
| Area surveyed per flight | 3,600 m² | 1,800 m² |
| Sorties needed for a 2.5 km runway | 42 | 84 |

<details class="custom-block details">
<summary>How the previous footprint was derived</summary>

The previous camera was a placeholder using the SDFormat default horizontal field of view of 1.047 rad (60°) [\[46\]](../references#nav-ref-12). The footprint is $2h\tan(\mathrm{HFOV}/2)$ with $h = 5\ \text{m}$, giving 5.77 m across and 4.33 m along for a general 640 × 480 image (resolution generalised as the SDFormat default is 320 × 240).

</details>

The same relationship can be explored for other cameras with the planner below. It takes an RGB footprint and returns the largest sector that one sortie can cover. The sector is always sized for the worst condition that was simulated, which is a 15 m/s crosswind on the lanes, and it must fit inside the 70% of the battery between the 95% launch level and the 25% return level. This keeps every sortie within the battery budget in the least favourable wind tested. Wind costs time mostly at the lane ends, so a wider footprint needs fewer lanes and gains more sector length than the smaller number of lanes alone would suggest. The lanes-across option is a model estimate, because that pattern has not yet been simulated at 15 m/s.

<SectorPlanner />

<details class="custom-block details">
<summary>Planner source and calibration</summary>

Source: the planner is calibrated on the offline kinematic simulation (2 m RGB footprint, turbulence 25%, worst of 3 seeds for wind). The worst case is a 15 m/s crosswind, and the sortie must fit between the 95% launch level and the 25% return level of the battery. The relation between endurance and sector size is explained in [Endurance vs. Mission Time](#endurance-vs-mission-time).

</details>

<details class="custom-block details">
<summary>Potential scalability: fleet and power</summary>

The smaller sector raises the number of sorties needed for a full runway. Three measures could recover this without changing the navigation:

- Quick battery swaps, or charging the UAV on the go from a ground vehicle (UGV).
- Several UAVs flying different sectors at the same time.
- A higher-resolution RGB camera that restores a wider footprint.

</details>

#### 3.2.1.2 Global Planning: Survey Method {#global-planning-survey-method}

Two parallel-sweep patterns were compared for a 30 × 60 m sector: lanes along the runway (36 lanes and 35 turns) and lanes across it (17 lanes and 16 turns). Both give complete coverage because both are exhaustive parallel sweeps [\[47\]](../references#nav-ref-1) [\[48\]](../references#nav-ref-2), so the choice rests on four criteria:

1. **Time and energy in the prevailing wind, not only in calm air.** A pattern that is fast in calm air can lose its advantage when the wind pushes the drone sideways on every lane, so each pattern must be judged in wind.
2. **A safe landing is always close.** With lanes along the runway, no point on any lane is more than 30 m from the nearest runway edge, because the sector is 60 m wide. If the drone has to land at once, it only needs a short flight to the edge, and the table of failsafes shows that this takes about 10.8 s.
3. **A simple resume after a hold or failsafe.** With lanes along the runway the progress of the survey can be recorded as "covered up to lane N". After an interruption the drone restarts at lane N + 1 and does not have to work out which parts of the sector are still missing.
4. **Verification in Gazebo and PX4 with the real controller.** A pattern is only trusted once the real flight controller has flown it, and not just the offline model.

Lanes along the runway have been flown in Gazebo and PX4. Lanes across the runway are still being implemented. Across lanes need fewer lanes and fewer turns, so they are the fastest in the offline simulation, but the usual wind at an airfield blows along the runway [\[44\]](../references#nav-ref-3), which means that the wind would be a crosswind on every across lane. Wind costs time mainly at the lane ends, and across lanes would face this crosswind on every lane. In the offline simulation the across pattern stays the fastest up to 10 m/s (see the table below), but it has not yet been simulated at 15 m/s or in Gazebo and PX4. For this reason, lanes across the runway remain a candidate and not yet the chosen pattern, and the result of this comparison feeds directly into the [Semester 2 plan](#nav-semester-2-plan).

#### 3.2.1.3 Alternatives Evaluated {#alternatives-evaluated}

<p class="report-table-caption" id="table-37"><strong>Table 37.</strong> Alternatives Evaluated</p>

| Pattern | Calm air (time, battery used) | 10 m/s wind along the runway | 10 m/s wind across the runway | Worst distance from the lane | Verdict |
| --- | --- | --- | --- | --- | --- |
| Lanes along, sharp turns | 476 s, 39.5% | 546 s, 45.7% | 559 s, 47.0% | 0.7 to 0.9 m | Baseline pattern, already simulated |
| Racetrack (skip 2), rounded turns | 424 s, 35.1% | 484 s, 40.7% | 519 s, 43.5% | 0.9 to 1.2 m | An option that is faster but tracks the lane less tightly |
| Lanes along, rounded turns | 581 s, 48.0% | 672 s, 56.5% | 732 s, 61.6% | 1.2 to 1.4 m | Slower, because the turn arcs are flown at 1.3 m/s, and the turns need tuning |
| Lanes across, sharp turns | 403 s, 33.2% | 455 s, 37.9% | 428 s, 35.7% | 0.6 to 0.7 m | The fastest candidate, which needs further testing |

<details class="custom-block details">
<summary>Source for Table 37</summary>

Source: offline kinematic simulation, 30 × 60 m sector, 2 m RGB footprint, turbulence 25%. The wind results show the worst of 3 seeds, and the calm results use 1 seed. Coverage patterns: Choset (2001) [\[47\]](../references#nav-ref-1); Galceran & Carreras (2013) [\[48\]](../references#nav-ref-2).

</details>

### 3.2.2 Obstacle Avoidance {#obstacle-avoidance}

#### 3.2.2.1 Obstacle Avoidance States {#obstacle-avoidance-states}

Obstacle avoidance runs in the EVADE and HOLD states of the mission state machine (Figure NAV-04), which are highlighted in Figure NAV-05. The threat assessor grades every tracked object on five levels (Figure NAV-06), and the levels act as the transition triggers. CAUTION moves the machine from SURVEY to EVADE, where the avoider steers around the bird, and AWARE or clear returns it to SURVEY. An obstacle that keeps blocking the lane for 1.0 s moves the machine to HOLD, which ends after 0.5 s of clear air, or the strip is skipped after 10 s in total.

<ElectricalFigure n="5" src="/report-assets/navigation-obstacle-avoidance/fsm-avoid.png" :width="2547" :height="1334" caption="Avoidance states and their transitions (highlighted)." />

<ElectricalFigure n="6" src="/report-assets/navigation-obstacle-avoidance/obstacle-avoidance-states.png" :width="1600" :height="900" caption="The five threat levels used by the threat assessor." />

<p class="report-table-caption" id="table-38"><strong>Table 38.</strong> Obstacle Avoidance States</p>

| Level | When it applies | What the drone does |
| --- | --- | --- |
| CLEAR | There is no conflict with any tracked object | Carries on along the route |
| AWARE | An object is within 25 m | Slows down to 3 m/s |
| CAUTION | The drone and an object would meet within 5 s if both kept their course | Switches the avoidance planner on |
| AVOID | The drone and an object would meet within 2.5 s | Steers to the best safe velocity |
| EMERGENCY | The meeting would be within 0.8 s, or the object is already too close | Escapes with the largest possible clearance |

**Moving objects (birds).** The LiDAR scan is clustered into objects. A track is confirmed after 3 hits and dropped after 1 s without a hit, so a single noisy return does not cause a manoeuvre. Each track carries an uncertainty radius that grows with time, so a bird that has not been seen recently is treated more cautiously. A linear Kalman filter [\[49\]](../references#nav-ref-10) is run for each confirmed track. It estimates the position and the velocity of the bird from the LiDAR hits and predicts where the bird will be at the next scan. Between hits the filter has nothing to correct its prediction, so its uncertainty grows, and this growing uncertainty is the uncertainty radius mentioned above. The predicted position and its uncertainty are what the avoidance planner uses to decide whether a path is safe. How the planner uses them, with velocity sampling and collision cones, is explained in [Local Planning: Reactive Avoidance](#local-planning-reactive-avoidance).

**Static objects (trees, poles).** A cell that keeps returning for 1 s becomes static and leaves the mover tracker. The route planner then inserts a bypass or truncates the lane.

#### 3.2.2.2 Global Planning: Rerouting {#global-planning-rerouting}

A static obstacle that has been mapped for 1.0 s moves the machine from SURVEY to REROUTE (Figure NAV-07), which edits the global route before the machine returns to SURVEY. The planner makes one of three edits (Figure NAV-08).

<ElectricalFigure n="7" src="/report-assets/navigation-obstacle-avoidance/fsm-reroute.png" :width="2547" :height="1334" caption="Rerouting in the state machine (highlighted): a bypass or a truncated lane returns the machine to SURVEY." />

<ElectricalFigure n="8" src="/report-assets/navigation-obstacle-avoidance/global-rerouting.png" :width="1600" :height="900" caption="The three rerouting cases: (1) obstacle on the lane, bypass; (2) lane end blocked, truncate; (3) strip blocked, skip and revisit." />

The sequence of events when an obstacle stays on the lane is as follows. The obstacle is first detected, and after 1.0 s of continuous detection it is mapped as static and a bypass is inserted into the route. If the lane is still blocked for a further 1.0 s, the machine enters HOLD. If the lane has still not cleared after 10 s in total, the strip is skipped and is flown again later in a revisit pass.

<details class="custom-block details">
<summary>Rerouting details: transits, obstacle map and methods</summary>

Take-off, return and revisit transits are flown as straight lines between known coordinates, and the revisits are ordered nearest-first. The same bypass is applied around any mapped obstacle. The obstacle map is an occupancy grid with 0.4 m cells, and a cell becomes static after 1.0 s. The methods follow: Hart, Nilsson & Raphael (1968) [\[50\]](../references#nav-ref-4); LaValle, *Planning Algorithms* [\[51\]](../references#nav-ref-5).

</details>

#### 3.2.2.3 Localisation and Path Following {#localisation-and-path-following}

The lane is only 1.76 m wide, so the drone must hold its path closely while wind and avoidance moves push it off. The drone is pulled back onto the lane by a feedback loop, using the EKF position as the measurement. EKF2 position (RTK-GNSS + IMU + baro + mag) is compared with the lane every cycle, and the cross-track error $e$ produces a velocity pull that is sent to PX4 (Figure NAV-09).

<ElectricalFigure n="9" src="/report-assets/navigation-obstacle-avoidance/path-loop.png" :width="1510" :height="216" caption="Path-following feedback loop: lane, error, pull, PX4, drone and EKF2." />

<details class="custom-block details">
<summary>Path-following controller: equation and gains</summary>

$$
\vec{v}_{\text{cmd}} = v_{\text{along}}\,\hat{t} + \operatorname{sat}\!\left(K_p\,e + K_i\!\int e\,dt,\ 1.5\ \text{m/s}\right)\hat{n}
$$

The proportional gain is $K_p = 0.4\ \text{s}^{-1}$ (0.6 in wind). The integral gain $K_i = 0.4$ is active only above 4° lean and is clamped, so it compensates a steady wind push without winding up during manoeuvres. A heading gate makes the drone wait until its yaw is within 12° of the lane before moving along it, and corners and side-steps are flown at 2.5 m/s and 3.0 m/s.

For the return after a 3 m detour, $e(t) = 3\ \text{m}\times e^{-0.4t}$, which is 0.2 m after $\ln(15)/0.4 = 6.8\ \text{s}$.

</details>

The cross-track error decays exponentially, so a 3 m detour is recovered in about 7 s (Figure NAV-10).

<ElectricalFigure n="10" src="/report-assets/navigation-obstacle-avoidance/path-detour.png" :width="509" :height="332" :cardWidth="640" caption="Return to the lane after a 3 m detour (about 7 s)." />

<details class="custom-block details">
<summary>Why this controller</summary>

Pure pursuit [\[52\]](../references#nav-ref-6) was considered first, but at cruise it looks about 4 m ahead, and the lane pitch is only 1.76 m, so it would be expected to cut the lane ends. A cross-track term corrects onto the line itself [\[53\]](../references#nav-ref-7), which suits a narrow lane. Because PX4 already handles attitude and rate [\[54\]](../references#nav-ref-8), the outer loop can be a simple first-order pull.

</details>

#### 3.2.2.4 Local Planning: Reactive Avoidance {#local-planning-reactive-avoidance}

The global route only knows about static obstacles. A bird can appear and move faster than the route could be re-planned, so when a threat reaches CAUTION the local planner takes over the velocity command for as long as the threat lasts. It does not plan a new route. In every cycle it answers one question: of all the velocities the drone could fly right now, which are safe, and which of the safe ones is closest to what the route wants? It does this in three steps:

1. **Sample:** The planner builds 96 candidate velocities: 24 headings spread evenly around the drone, each at 4 speeds (25, 50, 75 and 100% of the 6 m/s maximum evasion speed).
2. **Reject:** For each candidate the planner checks whether flying it would bring the drone too close to any tracked bird. "Too close" is the 1.3 m keep-out distance (0.5 m UAV radius + 0.8 m margin) plus the uncertainty radius of that bird's track. The bird is checked where the Kalman filter predicts it will be, not where it is now, because it keeps moving. The velocities that end inside this distance form the **collision cone**, and every candidate inside the cone is rejected. A bird that was seen recently has a small uncertainty radius and a narrow cone, and a bird that has not been seen for a while has a larger radius and a wider cone, so the drone gives it more room.
3. **Pick:** From the candidates that are left, the planner chooses one according to the mode in Table 39 and sends it as the commanded velocity. The choice is repeated every cycle, so the drone follows the bird's movement and goes back to the lane once the cone no longer blocks it. For example, if a bird closes in from one side, the candidates pointing towards it are rejected, and the drone flies the remaining candidate that is closest to the lane direction. That is usually a small step away from the bird, or a slower speed, and the cross-track pull then brings the drone back onto the lane.

Figure NAV-11 shows one cycle. The orange dot is the bird and the dashed circle around it is its growing uncertainty. The dashed red lines are the edges of the collision cone, and the red lines inside the cone are the rejected candidates. The green lines are the safe candidates, and the yellow arrow is the one that was chosen.

<ElectricalFigure n="11" src="/report-assets/navigation-obstacle-avoidance/velocity-sampling.png" :width="855" :height="474" :cardWidth="900" caption="Velocity sampling around a moving obstacle. Red: inside the collision cone, rejected. Yellow: chosen safe velocity." />

**Objective.** Keep the predicted path at least 1.3 m (UAV radius 0.5 m + 0.8 m margin) from every tracked bird, and otherwise stay on the lane. Safe means no candidate path enters the cone.

<p class="report-table-caption" id="table-39"><strong>Table 39.</strong> Local Planning: Reactive Avoidance</p>

| Mode | What the avoider does |
| --- | --- |
| NOMINAL | There is no threat, so the drone follows the global route |
| AVOID | The drone flies the best safe sample, which is the sampled velocity that keeps the path clear of the collision cones and stays closest to the lane |
| ESCAPE | The threat is too close for a normal manoeuvre, so the drone flies the sample with the largest predicted clearance |

The method follows the dynamic window approach of Fox, Burgard and Thrun (1997) [\[55\]](../references#nav-ref-9), and the per-bird tracks come from the Kalman filter [\[49\]](../references#nav-ref-10).

#### 3.2.2.5 Flight Control Kinematics {#flight-control-kinematics}

The navigator streams velocity $(v_x, v_y, v_z)$ and yaw setpoints in the runway frame at about 20 Hz. The offboard_bridge converts the runway frame to NED, PX4 handles attitude, rate and thrust control, and the four ESCs and motors act on the result.

<p class="report-table-caption" id="table-40"><strong>Table 40.</strong> Flight Control Kinematics</p>

| Parameter | Value used | Where it applies |
| --- | --- | --- |
| Survey cruise speed | 4.23 m/s, with a cap of 5.0 m/s | Along each lane |
| Side-step speed | 3.0 m/s | Moving across to the next lane |
| Corner speed | 2.5 m/s | Turns at the lane ends |
| Transit speed | 5.0 m/s | Take-off, return and revisit transits |
| Maximum evasion speed | 6.0 m/s | While avoiding a bird |
| Planning acceleration | 3.0 m/s² | Limit on how fast the commanded speed may change |
| Yaw rate | 40°/s | Turning the nose of the drone |
| Altitude | 5 m ± 0.5 m | Held during the whole survey |

The speed allowed into lane ends and corners is limited by braking distance. The calculation is given below.

<details class="custom-block details">
<summary>Speed limit calculation</summary>

Braking into lane ends and corners limits the allowed speed:

$$
v_{\text{allow}} = \sqrt{v_{\text{end}}^{2} + 2\,(0.7\,a_{\max})\,d_{\text{brake}}}
$$

The cross-track pull is $v_{\text{cross}} = \min(0.4\,e,\ 1.5\ \text{m/s})$.

Here $a_{\max}$ is the maximum deceleration (3.0 m/s²), $d_{\text{brake}}$ is the distance left to brake with 0.8 s of command lag added, $v_{\text{end}}$ is the target speed at the end of the braking zone, and 0.7 is the fraction of $a_{\max}$ used. The cross-track pull has a gain of 0.4 per second on the off-lane error $e$ (m), capped at 1.5 m/s.

Basis: $s = v^{2}/2a$ (constant deceleration). A yaw rate of 40°/s is below the PX4 automatic yaw limit (about 45°/s). The acceleration limits keep lean inside the 35° tilt limit (T/W 2.03 / 2.00).

</details>

### 3.2.3 Failsafes {#failsafes}

#### 3.2.3.1 Failsafe Triggers and Actions {#failsafe-triggers-and-actions}

The failsafes are the red arrows of the state machine (Figure NAV-12), and the table gives the trigger, threshold and basis for each. Mild faults (wind, battery or GNSS degradation) lead to RETURN or a normal landing, and faults that leave no time (motor failure, GNSS loss, 6% battery) lead to an immediate landing.

<ElectricalFigure n="12" src="/report-assets/navigation-obstacle-avoidance/fsm-failsafe.png" :width="2547" :height="1334" caption="Failsafe transitions of the state machine (highlighted). Red arrows end in LAND or DONE, and the blue RETURN arrow is used for the battery and degraded-GNSS cases." />

<p class="report-table-caption" id="table-41"><strong>Table 41.</strong> Failsafe Triggers and Actions</p>

| Trigger | Threshold | Action | Why this threshold |
| --- | --- | --- | --- |
| Wind slow-down | The smoothed lean is above 14° | The drone reduces its lane speed | 14° of lean is what a steady 15.4 m/s wind causes (force F = 11.5 N, with tan θ = F / (m g)) |
| Wind abort | The lean is above 33° for 6 s | The drone lands | 33° corresponds to a wind of about 25 m/s and is 2° under the 35° tilt limit. 6 s is 2.4 gust time constants, so a single gust does not trigger it |
| Lane | The drone is more than 3 m off the lane for 10 s | The flight is aborted and the drone lands | The worst excursion in the tests was 2.1 to 2.6 m, and recovering from 3 m takes 7 s |
| Swarm | 4 or more tracked objects together with ESCAPE for 0.4 s | The drone lands | A flock gives a warning of under 1 s (it is confirmed at 8 m with the closing speed at 10 m/s). It fired in 5 of 6 flock runs and gave no false alarm in 30 runs |
| GNSS degraded | The position error is worse than 0.5 m for 60 s | The drone returns home | RTK is accurate to 2 cm, so 0.5 m is 25 times the normal error. 60 s lets RTK re-converge before giving up |
| GNSS lost | There is no fix for 0.5 s | The drone lands immediately | Without a fix the drone drifts 3 to 10 m at 8 m/s, and 0.5 s is about 2 m of travel |
| Motor failure | Detected within 0.3 s | The drone lands immediately | A free fall from 5 m takes 1.0 s and a quadcopter cannot recover from a motor failure (impact speed 8.8 to 9.6 m/s) |
| Battery at launch | The pack is at 95% or more | The drone refuses to take off if it is lower | The 25% return level, plus the 69% used by the worst sortie (15 m/s, 30 m), plus a 1% margin, makes 95%. A sortie uses 40 to 69% |
| Battery for return | About 25% (a 20% reserve plus 3% for the return flight) | The drone returns home | This is a safety net. With a 95% launch the pack never reaches 25% during a normal sortie |
| Battery critical or emergency | 12% or 6% remaining | The drone lands beside the runway edge at 12%, and straight down at 6% | An edge landing takes 10.8 s (about 1% of the pack), and a 5 m descent takes 6 s (about 0.5%) |

<details class="custom-block details">
<summary>Sources for Table 41</summary>

Sources: wind force $F = \tfrac{1}{2}\rho\,C_dA\,v^{2}$ with $C_dA = 0.0794\ \text{m}^2$ and $m = 4.7\ \text{kg}$; gust time constant $\tau = 37\ \text{m}/v$ (Dryden, MIL-HDBK-1797 [\[56\]](../references#nav-ref-11)); PX4 User Guide, Safety configuration (battery failsafes staged as warning, return, land, emergency land) [\[54\]](../references#nav-ref-8); Unicore UM980 datasheet [\[40\]](../references#nav-ref-16); simulation stress tests (10 seeds per wind case, 8 per bird case); battery from the offline sim, lanes along, 266 Wh pack, worst of 3 seeds.

</details>

### 3.2.4 Wind Kinematics {#wind-kinematics}

#### 3.2.4.1 Wind Kinematics Calculations {#wind-kinematics-calculations}

**Approach:** The wind loads on the airframe were taken from the Mechanical Design Calculations ([Section 1.2.4.2](../subsystems/mechanical-design.md#_5-2-preliminary-thrust-calculations)). The wind force on the airframe follows the standard drag law on the CAD frontal area, the drone leans until the horizontal component of thrust balances that force, and the thrust per motor then follows from the lean angle. The simulation reuses the same drag area, so the wind loads seen by the navigator are the loads that the airframe was sized for. Only the values that had to differ for a simulation are changed, and each change is justified below.

<details class="custom-block details">
<summary>Values taken from the Mechanical calculations</summary>

<p class="report-table-caption" id="table-42"><strong>Table 42.</strong> Wind Model Parameters</p>

| Parameter | Value | Where it comes from |
| --- | --- | --- |
| Air density ρ | 1.225 kg/m³ | The value at sea level |
| Frontal area | 0.062038 m² | Measured from the CAD model by the Mechanical team |
| Drag coefficient C<sub>d</sub> | 1.28 | Assumed for a blunt body |
| Drag area C<sub>d</sub>A | 0.0794 m² | The frontal area multiplied by C<sub>d</sub> |
| Required thrust | 1.329 kgf per motor | Needed to hold position in a 12 m/s headwind with an acceleration of 1 m/s² (a tilt of 20°) |
| Design thrust | 1.768 kgf per motor | Needed for a combined tilt of 45° with a 5 kg drone |

</details>

<details class="custom-block details">
<summary>Values changed for the simulation, and why</summary>

<p class="report-table-caption" id="table-43"><strong>Table 43.</strong> Mechanical and Simulation Wind Assumptions</p>

| Parameter | Mechanical calculation | Simulation | Why it was changed |
| --- | --- | --- | --- |
| Mass | 5.0 kg | 4.7 kg | The simulation model uses 4.7 kg (take-off mass of the modelled airframe) (see the Power Calculations in the [Electrical Design](../subsystems/electrical-design#power-calculations) report). A lighter drone leans further for the same drag, so the simulation is the harder case: at 15 m/s the lean is 13° at 4.7 kg against 12.5° at 5.0 kg |
| Tilt limit | 45° design limit, and 30° for the M350 | 35° | One tilt limit is used for the whole mission. The planner's acceleration limits are set to stay within it, and the wind abort is set 2° below it |
| Turbulence | Not modelled | 0.25 of the mean wind | Moderate turbulence was assumed. A result in perfectly steady air would not exercise the lane controller |
| Wind guard (lean) | Not applicable | 14° and 33° | The lanes are slowed at 14° of lean (a steady wind of 15.4 m/s), and the drone lands at 33° held for 6 s (see the [Failsafes](#failsafes) for the gust time constants) |

The comparison with the Mechanical sizing is direct. At 15 m/s the wind force is 10.9 N and the steady lean is 13° (simulation), well inside the 35° limit. The gusts are what take the lean towards the limit, and they are modelled next.

</details>

<details class="custom-block details">
<summary>Turbulence model: Dryden-like gusts</summary>

Steady wind alone would only test whether the drone can lean far enough. The real difficulty on a survey is that wind changes while the drone is flying a 1.76 m wide lane, so the simulation adds gusts on top of the mean wind. The gust model follows the Dryden turbulence form of MIL-HDBK-1797 [\[56\]](../references#nav-ref-11), which describes turbulence as a random velocity with two parameters: an intensity $\sigma$ and a length scale $L$.

$$
\sigma = 0.25\,v, \qquad \tau = \frac{L}{v} = \frac{37\ \text{m}}{v}
$$

- $\sigma$ is the gust intensity (RMS, m/s). It is taken as 25% of the mean wind $v$, so stronger wind is also gustier.
- $L = 37$ m is the turbulence length scale. Dividing by the wind speed gives $\tau$, the time a gust takes to decorrelate: a gust is a patch of air about $L$ long that the drone and the wind carry past each other.
- At 5, 10 and 15 m/s the gust intensity is 1.25, 2.5 and 3.75 m/s, and $\tau$ is 7.4, 3.7 and 2.5 s. Faster wind therefore brings stronger and also quicker gusts.

In the simulation the gust is generated as a first-order random process in the along-wind and cross-wind directions. At every time step $\Delta t$ the new gust value is a decayed copy of the previous one plus fresh noise:

$$
\eta_{k+1} = a\,\eta_k + \sqrt{1-a^{2}}\;\sigma\,w_k, \qquad a = e^{-\Delta t/\tau}, \quad w_k \sim \mathcal{N}(0,1)
$$

The factor $\sqrt{1-a^2}$ keeps the RMS of $\eta$ equal to $\sigma$ whatever the step size, and $\tau$ (never below 1 s in the code) sets how long a gust persists. The wind seen by the drone is the mean wind plus $\eta$, and the seed is fixed per run so that scenarios are repeatable. The wind is applied to the Gazebo model through the force it exerts, which grows with the square of the wind speed.

This model matters to the navigation in three places:

- **Lane control.** The cross-track pull has to reject a disturbance that changes on a timescale of seconds. The 0.4 per second pull gain gives a time constant of 2.5 s, which is the same order as $\tau$ at 15 m/s. The controller therefore reacts at about the speed of the gust, and in the 15 m/s crosswind tests the worst off-lane error was 2.1 m.
- **Failsafe timing.** The wind abort requires the lean to stay above 33° for 6 s, which is 2.4 gust time constants at 15 m/s. A single gust is therefore unlikely to trigger a landing, and a sustained increase in wind is needed.
- **Peak lean.** The steady lean is about 13° at 15 m/s, but gusts take the peak lean to 35°. The wind guard at 14° slows the lanes before gusts can drive the lean to the limit.

Sources: Mechanical calculations (take-off mass, CAD frontal area, assumed $C_d$ 1.28, results across flight scenarios); Dryden turbulence (MIL-HDBK-1797) [\[56\]](../references#nav-ref-11).

</details>

**Wind guard in the state machine:** The guard is the only place where wind changes the mission state (Figure NAV-13). At a smoothed lean of 14° the machine moves from SURVEY to LANES SLOWED and returns when the lean falls back under 14°. At 33° for 6 s it lands.

<ElectricalFigure n="13" src="/report-assets/navigation-obstacle-avoidance/fsm-wind.png" :width="2547" :height="1334" caption="Wind guard (highlighted): slow the lanes at a lean of 14° or more, resume under 14°, and land at 33° or more for 6 s (red arrow)." />

## 3.3 Navigation Prototype Implementation {#a3-prototype-development}

### 3.3.1 Navigation Architecture {#navigation-architecture}

The navigation system was developed and tested in simulation, using a Gazebo model of the survey drone flown with the PX4 autopilot. The navigator is a closed loop of five stages, shown in Figure NAV-14: **sense, localise, plan, command and act**. PX4's EKF2 fuses the sensors and outputs position, velocity and attitude, which the navigator reuses and never re-fuses. The planner runs in ROS 2 and sends a velocity and yaw set-point to PX4, and the new pose and obstacles re-enter the loop through the sensors.

<ElectricalFigure n="14" src="/report-assets/navigation-obstacle-avoidance/navigation-architecture.png" :width="1600" :height="900" caption="Navigation architecture: sense, localise, plan, command, act." />

The mission logic is the finite state machine that was introduced in [Section 3.2](#a2-methodology-concept-development) (Figure NAV-04). The architecture of the five stages above is built around it, and the features of the state machine are as follows:

- **Mission states:** TAKEOFF, SURVEY, HOLD, RETURN, LAND and DONE, with SURVEY as the central state.
- **Behaviours inside SURVEY:** obstacle evasion (EVADE), global rerouting (REROUTE), revisits (REVISIT) and the wind slow-down (LANES SLOWED).
- **Failsafes:** transitions from SURVEY, LANES SLOWED and TAKEOFF to RETURN, LAND or DONE.
- **Localisation:** the EKF2 pose (RTK-GNSS, IMU, barometer and magnetometer) is the input to every transition, and GNSS quality drives three of the failsafes.
- **One sector per flight:** each sortie surveys one sector, then returns and lands.

#### 3.3.1.1 Core Navigation Logic {#core-navigation-logic}

[Section 3.2](#a2-methodology-concept-development) shows the development of each method on its own. Here they are chained into the one decision cycle that the navigator repeats from take-off to landing. Two rules keep the cycle simple: the navigator reuses the EKF2 estimate and never fuses the sensors again, and PX4 stays in charge of attitude and thrust, so the navigator only ever outputs a velocity and yaw set-point. In every cycle the navigator does the following, in order:

1. **Sense and track.** The N10 scan (450 beams at 10 Hz) is corrected for the tilt of the drone and clustered into objects. Moving objects become bird tracks (confirmed after 3 hits, dropped after 1 s without a hit, each with its own Kalman filter), and cells that keep returning for 1.0 s are added to the 0.4 m occupancy grid as static obstacles. The cameras mark the ground cells they cover, and a cell counts as surveyed only when both the RGB and the thermal camera have covered it.
2. **Localise.** The EKF2 pose is compared with the lane to give the cross-track error $e$, and the GNSS quality (fix and position error) is passed on to the failsafe checks.
3. **Assess.** The threat assessor grades every track on the five levels from its predicted time to meeting the drone. In the same step the failsafe monitors compare the lean, the time off the lane, the number of tracks in ESCAPE, the GNSS quality, the motor health and the battery with the thresholds in Table 41.
4. **Decide the state.** These triggers select the state through the transitions of Figure NAV-04. The failsafe transitions are the ones that end the sortie early (RETURN, LAND or DONE), so they take priority over the survey behaviours.
5. **Compute the velocity.** What is computed depends on the state. In SURVEY the command is the along-lane speed plus the cross-track pull, and the along-lane speed is the lowest of the limits that apply: the 4.23 m/s cruise speed (2.2 m/s in strong sunlight), 3 m/s when a threat is AWARE, the slower lane speed of the wind guard, and the braking limit into lane ends and corners. In EVADE the best safe sampled velocity replaces the lane velocity, or the sample with the largest clearance in ESCAPE. In REROUTE the route is edited first (bypass, truncate or skip) and the lane following then continues on the new route. In HOLD the drone waits for the lane to clear, and in RETURN and LAND it flies a straight line home and descends.
6. **Supervise and send.** The supervisor applies the geofence, the 5 m ± 0.5 m altitude band and a speed clamp to the command. The navigator streams the result at about 20 Hz, the offboard_bridge converts it from the runway frame to NED, and PX4 turns it into attitude, rate and thrust. The new pose and obstacles come back through the sensors in the next cycle.

**Survey bookkeeping.** Alongside this cycle the navigator keeps the progress of the survey as "covered up to lane N", so after a hold the survey restarts at lane N + 1. Strips that were skipped, and cells that are still missing a camera, are kept for the REVISIT passes (up to 6, nearest first). Each FOD found is queued as an alert and sent at the start of the next lane on a ROS topic (log-only for now), in the format that FOD Hunter expects.

### 3.3.2 Mission States and Timing {#mission-states-and-timing}

The highlighted path in Figure NAV-15 is a normal sortie through the state machine. The drone launches only with the battery at 95% or above, and otherwise the machine goes straight to DONE without taking off. It climbs to 5 m and enters SURVEY. After the last lane, any cell still missing one of the two cameras is flown again in REVISIT, up to six passes, and the machine then enters RETURN. RETURN can also be entered directly from SURVEY when the battery reaches about 25% or the GNSS stays degraded for 60 s. Every sortie ends in LAND and then DONE.

<ElectricalFigure n="15" src="/report-assets/navigation-obstacle-avoidance/fsm-mission.png" :width="2547" :height="1334" caption="Normal sortie path through the state machine (highlighted)." />

The typical duration of each state for a 30 m sector in calm air is given in Figure NAV-16 and the table below.

<ElectricalFigure n="16" src="/report-assets/navigation-obstacle-avoidance/mission-states.png" :width="1600" :height="900" caption="Mission states and typical durations." />

<p class="report-table-caption" id="table-44"><strong>Table 44.</strong> Mission States and Timing</p>

| State | What the drone does | Typical time |
| --- | --- | ---: |
| TAKEOFF | Climbs to 5 m | 2.8 s |
| SURVEY | Flies the 36 lanes and the side-steps between them | 457 s |
| HOLD | Waits while a threat is blocking the lane | As long as needed |
| RETURN | Flies back to the home point | 9.7 s |
| LAND | Descends the 5 m to the ground | 6.1 s |

The total is 476 s (7.9 min) in calm air and 533 s (8.9 min) at 10 m/s wind. The climb takes about 3 s at 1.3× hover thrust (944 W), which is about 0.3% of the pack, so it is never the limiting term. A supervisor applies the geofence, the 5 m ± 0.5 m altitude band and a speed clamp to every command.

<details class="custom-block details">
<summary>Source for Table 44</summary>

Source: offline kinematic simulation, lanes along the runway, 30 m sector. The calm result uses seed 1, and the 10 m/s result is the mean of 3 seeds. Climb energy from the Power Calculations in the [Electrical Design](../subsystems/electrical-design#power-calculations) report (climb 1.3× hover, 236 W per motor).

</details>

## 3.4 Navigation Simulation Testing {#a4-testing}

The simulation software and the way the individual software connects were introduced in [Simulation Software Used](#software-used). This section shows the Gazebo and PX4 simulations that confirm the offline results, first for the normal survey, then for obstacle avoidance, the failsafes and the wind kinematics. As mentioned in [Section 3.2.1.1](#camera-footprint-vs-sector-size), the simulation demonstrations use the first iterated RGB camera footprint.

### 3.4.1 Simulation Demonstrations {#simulation-demonstrations}

In every simulation video the overlay legend is shown in the figure below:

<ElectricalFigure n="17" src="/report-assets/navigation-obstacle-avoidance/sim_legend.png" :width="400" :height="400" :cardWidth="300" caption="Legend used to verify camera and path coverage." />

#### 3.4.1.1 Baseline Survey {#baseline-survey}

This is the baseline survey with no wind that is completed in around 8 min. The first side terminal window shows the position of the drone during the run. The 'z' value shows how well the drone is able to maintain the height of 5 m. The transition of states from 'Takeoff' to 'Survey' to 'Land' can be observed in the second side terminal window. Additionally, the same window also shows the continuous Odom Checks, which are the flight position feedback loop in action.

<figure class="cv-video-panel">
 <video class="cv-integration-video" controls playsinline preload="metadata" :src="withBase('/report-assets/navigation-obstacle-avoidance/Sem1Del.mp4')" aria-label="Baseline demonstration">
  Your browser does not support embedded video. <a :href="withBase('/report-assets/navigation-obstacle-avoidance/Sem1Del.mp4')">Open the demonstration video</a>.
 </video>
 <figcaption><strong>Video NAV-01</strong><span>Semester 1 deliverable: baseline survey with no wind and no birds. The planned route (white) and the drone following it. Green and cyan fill in as the RGB and thermal cameras cover the ground, and yellow is the flown path. Every cell needs both cameras.</span></figcaption>
</figure>

This is the simulation run for the alternate rounded lane tested for potential optimisations mentioned in [Section 3.2.1.3](#alternatives-evaluated). The overshoot can be observed and further tuning will result in better path following for this alternative. However, it results in a slower speed for every lane switch due to the added precision required.

<figure class="cv-video-panel">
 <video class="cv-integration-video" controls playsinline preload="metadata" :src="withBase('/report-assets/navigation-obstacle-avoidance/RoundedTurns.mp4')" aria-label="Baseline demonstration: rounded turns">
  Your browser does not support embedded video. <a :href="withBase('/report-assets/navigation-obstacle-avoidance/RoundedTurns.mp4')">Open the demonstration video</a>.
 </video>
 <figcaption><strong>Video NAV-02</strong><span>Baseline survey with rounded turns.</span></figcaption>
</figure>

#### 3.4.1.2 Obstacle Avoidance {#obstacle-avoidance-1}

Figure NAV-18 shows the camera coverage during an obstacle avoidance. The black box highlights the area covered only by the thermal camera due to the dodging of the drone. This should trigger a revisit shown in Video NAV-04 since both cameras did not cover it yet.

<ElectricalFigure n="18" src="/report-assets/navigation-obstacle-avoidance/obstacle-avoidance-view.png" :width="1600" :height="900" caption="Camera coverage during an obstacle avoidance." />

<figure class="cv-video-panel">
 <video class="cv-integration-video" controls playsinline preload="metadata" :src="withBase('/report-assets/navigation-obstacle-avoidance/dodge.mp4')" aria-label="Obstacle avoidance demo">
  Your browser does not support embedded video. <a :href="withBase('/report-assets/navigation-obstacle-avoidance/dodge.mp4')">Open the demonstration video</a>.
 </video>
 <figcaption><strong>Video NAV-03</strong><span>Dodging an obstacle.</span></figcaption>
</figure>

<figure class="cv-video-panel">
 <video class="cv-integration-video" controls playsinline preload="metadata" :src="withBase('/report-assets/navigation-obstacle-avoidance/dodge_revisit.mp4')" aria-label="Obstacle avoidance demo">
  Your browser does not support embedded video. <a :href="withBase('/report-assets/navigation-obstacle-avoidance/dodge_revisit.mp4')">Open the demonstration video</a>.
 </video>
 <figcaption><strong>Video NAV-04</strong><span>Revisiting lane with missed coverage from both cameras.</span></figcaption>
</figure>

### 3.4.2 Emergency Failsafe Demonstrations {#emergency-failsafe-demonstrations}

The take-off wind failsafe log is shown in Figure NAV-19, with the starting wind speed of 6 - 7 m/s crosswind during take-off of the drone. As seen in Video NAV-05, the trigger for the drone causing it to land is because it was unable to reach within 3 m of the lane in the 10 s time limit, as the wind progressively gets stronger after take-off (12 m/s). (see [Section 3.2.3](#failsafe-triggers-and-actions) for Table 41.)

<ElectricalFigure n="19" src="/report-assets/navigation-obstacle-avoidance/wind-failsafe-takeoff.png" :width="1600" :height="900" caption="Wind failsafe during take-off: simulation log showing the starting wind speed." />

<figure class="cv-video-panel">
 <video class="cv-integration-video" controls playsinline preload="metadata" :src="withBase('/report-assets/navigation-obstacle-avoidance/windtakeoff.mp4')" aria-label="Wind failsafe during take-off">
  Your browser does not support embedded video. <a :href="withBase('/report-assets/navigation-obstacle-avoidance/windtakeoff.mp4')">Open the demonstration video</a>.
 </video>
 <figcaption><strong>Video NAV-05</strong><span>Wind failsafe during take-off.</span></figcaption>
</figure>

Motor Failsafe: The highlighted section in the terminal window of the video shows the motor fault injector being implemented and the resultant unstable landing. The video is sped up quite a bit, so the tiny jerks are not as clear.

<figure class="cv-video-panel">
 <video class="cv-integration-video" controls playsinline preload="metadata" :src="withBase('/report-assets/navigation-obstacle-avoidance/motor.mp4')" aria-label="Motor failsafe">
  Your browser does not support embedded video. <a :href="withBase('/report-assets/navigation-obstacle-avoidance/motor.mp4')">Open the demonstration video</a>.
 </video>
 <figcaption><strong>Video NAV-06</strong><span>Motor failsafe.</span></figcaption>
</figure>

GNSS Degraded Failsafe: The highlighted section in the terminal window of the video shows the degraded GNSS fault injector being implemented and the resultant instability in flight. Once the position error is worse than 0.5 m for 60 s, the drone returns to home position. (see [Section 3.2.3](#failsafe-triggers-and-actions) for Table 41.)

<figure class="cv-video-panel">
 <video class="cv-integration-video" controls playsinline preload="metadata" :src="withBase('/report-assets/navigation-obstacle-avoidance/gnssdeg.mp4')" aria-label="Gnss degraded failsafe">
  Your browser does not support embedded video. <a :href="withBase('/report-assets/navigation-obstacle-avoidance/gnssdeg.mp4')">Open the demonstration video</a>.
 </video>
 <figcaption><strong>Video NAV-07</strong><span>GNSS degraded failsafe.</span></figcaption>
</figure>

Total GNSS Loss Failsafe: The highlighted section in the terminal window of the video shows the GNSS loss fault injector being implemented and the resultant landing of the drone.

<figure class="cv-video-panel">
 <video class="cv-integration-video" controls playsinline preload="metadata" :src="withBase('/report-assets/navigation-obstacle-avoidance/totalgnssloss.mp4')" aria-label="Total loss of gnss failsafe">
  Your browser does not support embedded video. <a :href="withBase('/report-assets/navigation-obstacle-avoidance/totalgnssloss.mp4')">Open the demonstration video</a>.
 </video>
 <figcaption><strong>Video NAV-08</strong><span>Total loss of GNSS failsafe.</span></figcaption>
</figure>

### 3.4.3 Wind Kinematics Demonstrations {#wind-kinematics-demonstrations}

Video NAV-09 depicts the drone behaviour in a 2 - 7 m/s wind sweep in the direction of the flight path, which becomes a crosswind during lane switching. This causes a lean about the drone's pitch axis at the lane ends.

<figure class="cv-video-panel">
 <video class="cv-integration-video" controls playsinline preload="metadata" :src="withBase('/report-assets/navigation-obstacle-avoidance/wind0.mp4')" aria-label="Wind kinematics demo: +x">
  Your browser does not support embedded video. <a :href="withBase('/report-assets/navigation-obstacle-avoidance/wind0.mp4')">Open the demonstration video</a>.
 </video>
 <figcaption><strong>Video NAV-09</strong><span>Turbulent winds from 2 to 7 m/s in the +x direction (0°): the drone leans about the pitch axis.</span></figcaption>
</figure>

Video NAV-10 depicts the drone behaviour in a stronger 6 - 12 m/s crosswind sweep. This causes a lean about the drone's roll axis at the lane ends (about 13 degrees).

<figure class="cv-video-panel">
 <video class="cv-integration-video" controls playsinline preload="metadata" :src="withBase('/report-assets/navigation-obstacle-avoidance/wind90.mp4')" aria-label="Wind kinematics demo: +y">
  Your browser does not support embedded video. <a :href="withBase('/report-assets/navigation-obstacle-avoidance/wind90.mp4')">Open the demonstration video</a>.
 </video>
 <figcaption><strong>Video NAV-10</strong><span>Turbulent winds from 6 to 12 m/s in the +y direction (90°): the drone leans about the roll axis.</span></figcaption>
</figure>

Due to the strength of the wind sweeps, the drone is unable to cover the full sector in one stretch and revisits are triggered by the architecture. Video NAV-11 depicts the last of three revisits triggered by this simulation run from Video NAV-10.

<figure class="cv-video-panel">
 <video class="cv-integration-video" controls playsinline preload="metadata" :src="withBase('/report-assets/navigation-obstacle-avoidance/wind90revisit.mp4')" aria-label="Wind kinematics demo: revisit">
  Your browser does not support embedded video. <a :href="withBase('/report-assets/navigation-obstacle-avoidance/wind90revisit.mp4')">Open the demonstration video</a>.
 </video>
 <figcaption><strong>Video NAV-11</strong><span>Turbulent winds from 6 to 12 m/s in the +y direction (90°): revisit pass after the baseline survey finishes.</span></figcaption>
</figure>

## 3.5 Navigation Performance Analysis {#a5-analysis}

### 3.5.1 Endurance vs. Mission Time {#endurance-vs-mission-time}

The longest flight time we expect (15 m/s crosswind) takes 13.2 min, inside the 13.9 min between launch and return (Figure NAV-20).

<ElectricalFigure n="20" src="/report-assets/navigation-obstacle-avoidance/endurance-budget.png" :width="1600" :height="900" caption="Sector budget: 70% of the pack, 13.9 min of flight, between the 95% launch and 25% return levels, followed by the 12% critical and 6% emergency levels." />

<p class="report-table-caption" id="table-45"><strong>Table 45.</strong> Endurance vs. Mission Time</p>

| Wind (30 m sector) | Flight time | Battery used | Battery left after the sortie, counted from the 95% launch level |
| --- | ---: | ---: | ---: |
| Calm | 7.9 min | 39.5% | 55% |
| 10 m/s crosswind | 9.3 min | 47.0% | 48% |
| 12 m/s crosswind | 10.5 min | 53.6% | 41% |
| 14 m/s crosswind | 12.5 min | 65.0% | 30% |
| 15 m/s along runway | 11.1 min | 57.8% | 37% |
| **15 m/s crosswind** | **13.2 min** | **68.9%** | **26%** |

Each result is the worst of 3 seeds, with lanes along the runway and turbulence of 25%.

<details class="custom-block details">
<summary>Why 15 min? Endurance calculation</summary>

The pack holds 266 Wh and the drone draws about 805 W, so a full drain lasts 19.8 min, or 15.9 min when use is limited to 80% of the pack. A sortie spends only the window from the 95% launch to the 25% return, which is 70% of the pack or 13.9 min. The worst case flown, a 15 m/s crosswind over a 30 m sector, takes 13.2 min and 69% of the pack, so it fits. At 15 m/s the longest sector that fits is 30 m (35 m needs 73%, 40 m needs 83% and 60 m needs 103%).

</details>

### 3.5.2 Wind Testing Overall Results {#wind-testing-overall-results}

<p class="report-table-caption" id="table-46"><strong>Table 46.</strong> Wind Testing Overall Results</p>

| Wind (turbulence 25%) | Runs completed | Worst distance from the lane | Did the wind abort fire? |
| --- | :---: | ---: | :---: |
| Calm | 3/3 | 0.7 m | No |
| 10 m/s crosswind | 3/3 | 0.7 m | No |
| 12 m/s crosswind | 3/3 | 1.0 m | No |
| 14 m/s crosswind | 3/3 | 1.4 m | No |
| 15 m/s along the runway | 3/3 | 1.0 m | No |
| 15 m/s crosswind | 3/3 | 2.1 m | No |

**Safe flying conditions.** The airframe holds 15 m/s (steady lean about 13°, peak 35° in gusts) and stays within 2.1 m of the lane, inside the 3 m lane failsafe limit.

<details class="custom-block details">
<summary>Additional wind test results (independent of camera and coverage pattern)</summary>

The following results do not change with the camera or the coverage pattern:

- Take-off and landing in winds of 6 to 15 m/s drift 0.3 to 2.1 m from the target point, and the drone touches down at a vertical speed of 0.72 m/s.
- The result is sensitive to the drag area $C_dA$. With $C_dA$ = 0.10, 5 of 6 runs succeeded at 15 m/s, and with $C_dA$ = 0.20, none of the 6 runs succeeded at 12 m/s.

</details>

<details class="custom-block details">
<summary>Source for Table 46</summary>

Source: offline kinematic simulation, lanes along the runway, with the wind blowing across (90°) or along (0°) the runway, seeds 1 to 3 and 25% turbulence. The Gazebo demonstrations use a 60 m sector.

</details>

**Performance against the requirements.** The results above are compared with the requirements of [Section 3.1](#a1-objective-scope-context).

<p class="report-table-caption" id="table-47"><strong>Table 47.</strong> Performance Against Requirements</p>

| Requirement | Result of the simulation | Met? |
| --- | --- | :---: |
| Endurance | The worst sortie took 13.2 min and used 69% of the pack, inside the 13.9 min window | Yes |
| Lane keeping | The worst distance from the lane was 2.1 m, inside the 3 m failsafe limit | Yes |
| Wind | All 3 runs in a 15 m/s crosswind with 25% turbulence were completed | Yes |
| Safety | The swarm failsafe fired in 5 of 6 flock runs, with no false alarms in 30 runs | Yes |
| Obstacle avoidance | Static obstacles were bypassed or skipped, but about 9% of runs in the dense bird stream ended in a collision | Partly |
| Coverage | Lanes along the runway were flown in Gazebo and PX4, but lanes across the runway have not yet been simulated in strong wind | Partly |

## 3.6 Discussion of Future Works {#a6-problems-project-plan}

### 3.6.1 Further Concerns and Solutions {#nav-future-works}

The simulation also exposed concerns that were not foreseen in the design stage. Each one is given in the table below with the evidence found and the mitigation we propose, and the mitigations feed the Semester 2 plan.

#### 3.6.1.1 Further Concerns and Solutions {#further-concerns-and-solutions}

<details class="custom-block details">
<summary>Further concerns found in simulation, with evidence and proposed mitigations (Table 48)</summary>

<p class="report-table-caption" id="table-48"><strong>Table 48.</strong> Further Concerns and Solutions</p>

| Concern found | Evidence from simulation | Proposed mitigation |
| --- | --- | --- |
| Obstacles above or below the 2D LiDAR plane (canopies, wires, thin poles) | The 2D LiDAR only scans one flat plane, so anything above or below that plane cannot be seen by it | Use a gimbal-stabilised or tilting 360° LiDAR, or upgrade to a 3D LiDAR |
| Strong sunlight shortens LiDAR range | In strong sunlight the LiDAR range falls to 4.7 m, which cuts the speed cap from 4.23 m/s to 2.2 m/s. The number of birds that were detected fell from 16 of 17 to 5 of 37 | Shade and filter the sensor, fly when the sun is low, or upgrade to a longer-range unit |
| Bird flocks beat the avoider | About 9% of the runs in the dense bird stream ended in a collision, and the number of flock collisions rose from 8 to 28 as the detection range fell | Rely on the swarm failsafe, which lands the drone, detect flocks earlier with a second sensor, and avoid flying at times of peak bird activity |
| Wind limit depends on the real drag area | With a drag area C<sub>d</sub>A of 0.10, 5 of 6 runs succeeded at 15 m/s, and with a C<sub>d</sub>A of 0.20, none of the 6 runs succeeded at 12 m/s | Measure C<sub>d</sub>A and the hover power on a thrust stand, and set the wind limit from the measured values |
| GNSS degraded or lost | When GNSS is degraded, the distance from the lane (rms) rises to 0.7 to 1.4 m. When GNSS is lost, the drone drifts 3 to 10 m at 8 m/s | Return home after 60 s of degraded GNSS, land at once if it is lost, and add optical flow or a second RTK source as a backup |
| Motor failure | A quadcopter cannot recover from a motor failure, and it hits the ground at 8.8 to 9.6 m/s (183 to 218 J) | Monitor the motor health, add propulsion redundancy or a parachute, and keep the flight path clear of people |

</details>

### 3.6.2 Semester 2 Development Plan {#nav-semester-2-plan}

Semester 2 moves the navigation logic from simulation to the real drone. The drone cannot be flown at full scale at once, so small test cases are developed first, each one built on the one before. The plan has three steps, ordered so that nothing is flown live until the simulation has predicted it.

#### 3.6.2.1 Build and Bench-Test the Hardware {#build-and-bench-test-the-hardware}

<details class="custom-block details">
<summary>Build and bench-test the hardware</summary>

- Finish integrating the full hardware stack and troubleshoot it.
- Measure the drag area and the hover power on a thrust stand.
- Test the N10 LiDAR outdoors in sunlight.

</details>

#### 3.6.2.2 Update the Simulation and Predict {#update-the-simulation-and-predict}

<details class="custom-block details">
<summary>Update the simulation and predict</summary>

- Feed the measured values back into the simulation.
- Re-run the wind limits, the endurance and the failsafe thresholds.
- Tune the live flight test cases in the simulation first.

</details>

#### 3.6.2.3 Live Test, Then Compare {#live-test-then-compare}

<details class="custom-block details">
<summary>Live test cases and comparison with the simulation (Table 49)</summary>

The drone cannot be flown over a full 30 m × 60 m sector straight away, so the live tests are built up from small cases. Each case is flown only after the simulation has predicted its result, and the next case is started only once the previous one has been verified.

<p class="report-table-caption" id="table-49"><strong>Table 49.</strong> Live Test Cases for Semester 2</p>

| Step | Test case | Height and place | What it checks |
| --- | --- | --- | --- |
| 1 | Hover | 1 to 1.5 m, indoors | The drone can take off, hold its position and land under the navigator and PX4 |
| 2 | Hover | 5 m, outdoors | Hover at the survey altitude (5 m ± 0.5 m) with the real EKF2 position, including the effect of outdoor wind |
| 3 | Straight line along a lane | Tested at low height first, then at 5 m | The drone moves along a lane and sticks to it. The cross-track error is compared with the 1.76 m lane pitch and the 3 m lane failsafe limit |
| 4 | Lane shifting | First at a hover height of 1 to 1.5 m, then at 5 m | The drone side-steps from one lane to the next and settles on the new lane |
| 5 | Further cases | 5 m, outdoors | More behaviours are added one at a time (for example a lane end and turn, an obstacle bypass and the failsafes) until a full sector sized to the testing ground can be flown |

The order is chosen so that each case adds only one new thing. If a case fails, the cause is limited to what was added, and the simulation can be corrected before the case is flown again. The lowest height (1 to 1.5 m) is used first for the hover and the lane shift, because a fault at that height has the smallest consequence, and the survey altitude of 5 m is tried only after the behaviour is confirmed.

After each case:

- Compare the live flight logs with the simulation and correct the model where they differ.
- Proceed to the next case only when the live result agrees with what the simulation predicted.

The three steps are then repeated, so that each round of live testing improves the simulation before the next round is flown.

</details>

</div>