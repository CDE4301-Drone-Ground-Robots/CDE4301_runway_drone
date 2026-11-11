---
title: "Navigation and Obstacle Avoidance"
outline: false
prev: false
next: false
aside: false
pageClass: subsystem-report-page
---

<div class="cv-report rubric-report">

<p class="chapter-kicker">FOD ARGUS / NAVIGATION &amp; OBSTACLE AVOIDANCE</p>

<script setup>
import SectorPlanner from '../.vitepress/theme/components/SectorPlanner.vue' 
</script>

# Navigation & Obstacle Avoidance

<SubsystemLead class="cv-report-byline" name="Kummarikunta Talitha" matric="A0286653R" portrait="/team/Talitha.jpg" />

<!--
VIDEO INSERTS: every "Video will be added here" panel below is a placeholder.
To insert a clip, copy the video files to website/docs/public/report-assets/navigation-obstacle-avoidance/
and replace the <div class="cv-video-pending"> line with the pattern used in computer-vision.md:
<video class="cv-integration-video" controls playsinline preload="none" :src="withBase('/report-assets/navigation-obstacle-avoidance/FILE.mp4')">...</video>
This also needs a script-setup block at the top of the page that imports withBase from 'vitepress'.
-->

## A1. Objective, Scope and Context {#a1-objective-scope-context}

### Design Concerns and Sensor Models {#design-concerns}

#### Initial Concerns and Solutions {#initial-concerns-and-solutions}

Before simulating, we listed the concerns that would most affect a runway survey, and designed a response to each. The table records the concern and the response that was built into the simulation, and the later sections test whether those responses held.

| Concern | Solution in the simulation |
| --- | --- |
| Short LiDAR range on dark targets in sunlight (about 4.7 m) | Cruise capped to stop inside that range: 4.23 m/s, 2.2 m/s in strong sun. Known boundaries pre-loaded as keep-outs |
| Birds move unpredictably | Linear Kalman filter per tracked bird with growing uncertainty, five threat levels, velocity sampling with collision cones |
| Static obstacles on the lane | Mapped after 1.0 s, then bypass or lane truncation. Hold, skip after 10 s, revisit later |
| Wind and drone tilt | Cross-track pull back onto the lane, tilt gate on the scan. Wind guard: slow at 14° lean, land at 33° |
| Endurance and battery | Sector sized to the pack: 30 m sector uses 40% calm, 69% at 15 m/s crosswind. Launch at 95%, return at about 25% |
| FOD coverage criteria | RGB (2 × 2 m footprint) resolves small objects, thermal adds dual coverage |
| Hand-off position to Hunter | Alert format defined; queued and sent at each lane start on a ROS topic (log-only), matching FOD Hunter's message format |

#### Sensor Specifications Used {#sensor-specifications-used}

| Sensor | Specification modelled | Role |
| --- | --- | --- |
| Leishen N10 2D LiDAR | 360°, 450 beams at 10 Hz, 12 m at 70% reflectivity (7.9 m at 30%, 4.7 m in strong sun), ±3 cm, planar | Main avoidance sensor: birds (moving), trees and poles (static); its range sets the speed cap |
| TFmini Plus single-point | 12 m at 90%, 3.6° beam, 3° above the nose, ±3 cm | Forward look-ahead above the flat N10 scan; gain not yet shown in simulation |
| RGB camera (nadir) e-CAM56_CUONX | Sony IMX568, global shutter, 2472 × 2064, fixed M12 lens. Modelled: 640 × 640, 22.6° HFOV = 2 m × 2 m at 5 m, 5 Hz processed, 90% detection (50% at the edge) | Main FOD detection, looking straight down the lane; global shutter avoids motion skew at 4.2 m/s |
| Thermal BNW2T256T04010ASSWC | 256 × 192, 4.0 mm, 45.5° × 33.5°, 45° side tilt: strip 2.7 to 9.3 m beside the track | FOD verification: a second, independent view to the side |
| GNSS Unicore UM980 | RTK: 2 cm horizontal, 3 cm vertical, 10 Hz, fused in PX4 EKF2 | Position: cm-level lane keeping and FOD coordinates |

### Survey Criteria {#survey-criteria}

The survey criteria were set before the path was designed, because they decide how many lanes are needed. The runway is split into sectors, and one sortie surveys one sector. A runway of 300 m to 2.5 km is longer than one 15 min flight, so a 2.5 km runway is about 84 sectors and a 300 m runway is 10 sectors. A cell counts as surveyed only when **both** cameras have covered it.

![Runway split into sectors, with lanes along (36 lanes) and lanes across (about 17 lanes) as the two ways to fly one sector](/report-assets/navigation-obstacle-avoidance/survey-sectors-split.png)

*Figure 5. Runway sectors (30 m × 60 m, not to scale) and the two ways to fly one sector: lanes along (36 lanes) and lanes across (about 17 lanes).*

The two cameras play different roles. The nadir RGB camera detects, and the side-tilted thermal camera independently verifies, so a cell needs both to count. The RGB footprint is 2.0 × 2.0 m, and the thermal footprint is 6.62 × 5.93 m, covering 2.7 to 9.3 m beside the track. The lane pitch of 1.76 m follows from the narrower RGB strip: the 2 m strip with 10% overlap, shifted so that the thermal strip also covers every cell. Cells that still miss one camera after the lanes are revisited, up to 6 passes.

![What each camera covers on one lane, seen from behind, with the next lane's RGB strip 1.76 m over](/report-assets/navigation-obstacle-avoidance/survey-sectors-lane.png)

*Figure 6. Coverage of one lane seen from behind (to scale). Green is RGB and cyan is thermal only in the simulation overlay.*

Sources: runway dimensions follow FAA AC 150/5300-13B [\[3\]](../references#nav-ref-3) and ICAO Annex 14 Vol. I [\[13\]](../references#nav-ref-13); RGB footprint (e-CAM56_CUONX, M12 lens); thermal footprint (BNW2T256T04010ASSWC).

## A2. Methodology / Concept Development {#a2-methodology-concept-development}

### Survey Planning {#survey-planning}

#### Camera Footprint vs. Sector Size {#camera-footprint-vs-sector-size}

The camera footprint was the largest change to the plan between the first and second design iteration. For the same navigation and power model, a narrower camera swath means more lanes, and so a smaller sector per sortie.

| | Previous RGB (5.77 × 4.33 m) | Current RGB (2 × 2 m) |
| --- | ---: | ---: |
| Sector per sortie | 60 × 60 m | 30 × 60 m |
| Lanes (along) | 13 | 36 |
| Flight time, calm (along) | 315 s (5.3 min) | 476 s (7.9 min) |
| Pack used, calm (along) | 26% | 40% |
| Area surveyed per flight | 3,600 m² | 1,800 m² |
| Sorties, 2.5 km runway | 42 | 84 |

The previous camera was a placeholder using the SDFormat default horizontal field of view of 1.047 rad (60°) [\[12\]](../references#nav-ref-12). The footprint is $2h\tan(\mathrm{HFOV}/2)$ with $h = 5\ \text{m}$, giving 5.77 m across and 4.33 m along for a general 640 × 480 image (resolution generalised; the SDFormat default is 320 × 240).

The same relationship can be explored for other cameras with the planner below. It takes an RGB footprint and returns the largest sector that one sortie can cover. Sectors are always sized for the worst simulated condition, a 15 m/s crosswind on the lanes, inside the 70% battery window between the 95% launch and 25% return levels. This keeps every sortie within the battery budget in the least favourable wind tested. Wind costs time mostly at the lane ends, so a wider footprint needs fewer lanes and gains more sector length than the shorter lane spacing alone would suggest. The lanes-across option is a model estimate, because that pattern has not yet been simulated at 15 m/s.

<SectorPlanner />

Source: planner calibrated on the offline kinematic simulation (2 m RGB footprint, turbulence 25%, worst of 3 seeds for wind).

**Potential scalability: fleet and power**

The smaller sector raises the number of sorties for a full runway, and three measures could recover this without changing the navigation: quick battery swaps or UGV on-the-go charging, multiple UAVs flying different sectors, and a higher-range RGB camera specification that restores a wider footprint.

#### Global Planning: Survey Method {#global-planning-survey-method}

Two parallel-sweep patterns were compared for a 30 × 60 m sector: lanes along the runway (36 lanes, 35 turns) and lanes across it (17 lanes, 16 turns). Both give complete coverage because both are exhaustive parallel sweeps [\[1\]](../references#nav-ref-1) [\[2\]](../references#nav-ref-2), so the choice rests on four criteria:

1. Time and energy in the prevailing wind, not only in calm air.
2. Safe landing anywhere: a lane is at most 30 m from a runway edge.
3. Simple resume after a hold or failsafe, as "covered up to lane N".
4. Verification in Gazebo and PX4 with the real controller.

Lanes along the runway has been flown in Gazebo and PX4. Lanes across is being implemented, and its cost in the usual wind along the runway [\[3\]](../references#nav-ref-3), which is a crosswind on every lane, is not yet simulated.

#### Alternatives Evaluated {#alternatives-evaluated}

| Pattern | Calm | 10 m/s, wind along runway | 10 m/s, wind across runway | Worst lane error | Verdict |
| --- | --- | --- | --- | --- | --- |
| Lanes along, sharp turns | 476 s, 39.5% | 546 s, 45.7% | 559 s, 47.0% | 0.7 to 0.9 m | Baseline (simulated) |
| Racetrack (skip 2), rounded turns | 424 s, 35.1% | 484 s, 40.7% | 519 s, 43.5% | 0.9 to 1.2 m | Option: faster, looser tracking |
| Lanes along, rounded turns | 581 s, 48.0% | 672 s, 56.5% | 732 s, 61.6% | 1.2 to 1.4 m | Slower (arc 1.3 m/s); needs tuning |
| Lanes across, sharp turns | 403 s, 33.2% | 455 s, 37.9% | 428 s, 35.7% | 0.6 to 0.7 m | Candidate: fastest; needs to be tested further |

Source: offline kinematic sim, 30 × 60 m sector, 2 m RGB footprint, turbulence 25%, worst of 3 seeds shown plus calm 1 seed. Coverage patterns: Choset (2001) [\[1\]](../references#nav-ref-1); Galceran & Carreras (2013) [\[2\]](../references#nav-ref-2).

The two methods are still being compared on time and energy in calm air and in wind, over several seeds, to decide which is more efficient for a 30 × 60 m sector.

### Obstacle Avoidance {#obstacle-avoidance}

#### Obstacle Avoidance States {#obstacle-avoidance-states}

Obstacle avoidance runs in EVADE and HOLD (Figure 9). The threat assessor grades every tracked object on five levels (Figure 10), and the levels act as the transition triggers. CAUTION moves the machine from SURVEY to EVADE, where the avoider steers around the bird, and AWARE or clear returns it to SURVEY. An obstacle that keeps blocking the lane for 1.0 s moves the machine to HOLD, which ends after 0.5 s of clear air, or the strip is skipped after 10 s in total.

![EVADE and HOLD states and their transitions, highlighted](/report-assets/navigation-obstacle-avoidance/fsm-avoid.png)

*Figure 9. Avoidance states and their transitions (highlighted).*

![Five threat levels: clear, aware, caution, avoid, emergency](/report-assets/navigation-obstacle-avoidance/obstacle-avoidance-states.png)

*Figure 10. The five threat levels used by the threat assessor.*

| Level | Trigger |
| --- | --- |
| CLEAR | No conflict |
| AWARE | Within 25 m: slow to 3 m/s |
| CAUTION | Conflict within 5 s: avoidance planner on |
| AVOID | Conflict within 2.5 s |
| EMERGENCY | Within 0.8 s or too close: escape |

**Moving objects (birds).** The LiDAR scan is clustered into objects. A track is confirmed after 3 hits and dropped after 1 s without a hit, so a single noisy return does not cause a manoeuvre. Each track carries an uncertainty radius that grows with time, so a bird that has not been seen recently is treated more cautiously. Avoidance then uses velocity sampling with collision cones.

**Static objects (trees, poles).** A cell that keeps returning for 1 s becomes static and leaves the mover tracker. The route planner then inserts a bypass or truncates the lane.

#### Global Planning: Rerouting {#global-planning-rerouting}

A static obstacle that has been mapped for 1.0 s moves the machine from SURVEY to REROUTE (Figure 11), which edits the global route before the machine returns to SURVEY. The planner makes one of three edits (Figure 12).

![REROUTE state and its transitions, highlighted](/report-assets/navigation-obstacle-avoidance/fsm-reroute.png)

*Figure 11. Rerouting in the state machine (highlighted): a bypass or a truncated lane returns the machine to SURVEY.*

![Three rerouting cases: bypass, truncate, skip and revisit](/report-assets/navigation-obstacle-avoidance/global-rerouting.png)

*Figure 12. The three rerouting cases: (1) obstacle on the lane, bypass; (2) lane end blocked, truncate; (3) strip blocked, skip and revisit.*

1. **Obstacle on the lane: bypass.** A keep-out circle is placed around the mapped obstacle, with two waypoints beside it on each side. The shorter side is chosen, always inside the geofence.
2. **Lane end blocked: truncate.** If the lane end falls inside a keep-out, the lane is cut short before it.
3. **Strip blocked: skip and revisit.** If blocked for 10 s in total, the strip is skipped and flown later, with up to 6 revisit passes to cover cells still missing.

Timeline: first hit → +1.0 s mapped as static → bypass inserted → blocked for 1.0 s → HOLD → 10 s cumulative → strip skipped → revisit pass.

Take-off, return and revisit transits are straight lines from known coordinates (revisits ordered nearest-first), with the same bypass around any mapped obstacle. The obstacle map is an occupancy grid with 0.4 m cells, static after 1.0 s. References: Hart, Nilsson & Raphael (1968) [\[4\]](../references#nav-ref-4); LaValle, *Planning Algorithms* [\[5\]](../references#nav-ref-5).

#### Localisation and Path Following {#localisation-and-path-following}

The lane is only 1.76 m wide, so the drone must hold its path closely while wind and avoidance moves push it off. The drone is pulled back onto the lane by a feedback loop, using the EKF position as the measurement. EKF2 position (RTK-GNSS + IMU + baro + mag) is compared with the lane every cycle, and the cross-track error $e$ produces a velocity pull that is sent to PX4.

![Path-following feedback loop: lane, error, pull, PX4, drone and EKF2](/report-assets/navigation-obstacle-avoidance/path-loop.png)

*Figure 13. Path-following feedback loop: lane, error, pull, PX4, drone and EKF2.*

$$
\vec{v}_{\text{cmd}} = v_{\text{along}}\,\hat{t} + \operatorname{sat}\!\left(K_p\,e + K_i\!\int e\,dt,\ 1.5\ \text{m/s}\right)\hat{n}
$$

The proportional gain is $K_p = 0.4\ \text{s}^{-1}$ (0.6 in wind). The integral gain $K_i = 0.4$ is active only above 4° lean and is clamped, so it compensates a steady wind push without winding up during manoeuvres. A heading gate makes the drone wait until its yaw is within 12° of the lane before moving along it, and corners and side-steps are flown at 2.5 m/s and 3.0 m/s.

For the return after a 3 m detour, $e(t) = 3\ \text{m}\times e^{-0.4t}$, which is 0.2 m after $\ln(15)/0.4 = 6.8\ \text{s}$.

![Cross-track error decaying from 3 m after a detour, about 7 s to return to the lane](/report-assets/navigation-obstacle-avoidance/path-detour.png)

*Figure 14. Return to the lane after a 3 m detour (about 7 s).*

**Why this controller.** Pure pursuit [\[6\]](../references#nav-ref-6) was considered first, but at cruise it looks about 4 m ahead, and the lane pitch is only 1.76 m, so it would be expected to cut the lane ends. A cross-track term corrects onto the line itself [\[7\]](../references#nav-ref-7), which suits a narrow lane. Because PX4 already handles attitude and rate [\[8\]](../references#nav-ref-8), the outer loop can be a simple first-order pull.

#### Local Planning: Reactive Avoidance {#local-planning-reactive-avoidance}

1. **Sample.** 24 headings × speeds of 25, 50, 75 and 100% (up to 6 m/s).
2. **Reject.** Any path that enters a collision cone is rejected. The cone grows with track uncertainty.
3. **Pick.** A safe candidate becomes the commanded velocity.

![Velocity sampling around a moving obstacle](/report-assets/navigation-obstacle-avoidance/velocity-sampling.png)

*Figure 15. Velocity sampling around a moving obstacle. Red: inside the collision cone, rejected. Yellow: chosen safe velocity.*

**Objective.** Keep the predicted path at least 1.3 m (UAV radius 0.5 m + 0.8 m margin) from every tracked bird, and otherwise stay on the lane. Safe means no candidate path enters the cone.

| Mode | Behaviour |
| --- | --- |
| NOMINAL | Follow the global route |
| AVOID | Use the best safe sample |
| ESCAPE | Maximum predicted clearance |

References: Fox, Burgard & Thrun (1997) [\[9\]](../references#nav-ref-9); Kalman (1960) [\[10\]](../references#nav-ref-10) for the per-bird tracks.

#### Flight Control Kinematics {#flight-control-kinematics}

The navigator streams velocity $(v_x, v_y, v_z)$ and yaw setpoints in the runway frame at about 20 Hz. The offboard_bridge converts the runway frame to NED, PX4 handles attitude, rate and thrust control, and the four ESCs and motors act on the result.

| Parameter | Value |
| --- | --- |
| Survey cruise | 4.23 m/s (cap 5.0) |
| Side-step | 3.0 m/s |
| Corner | 2.5 m/s |
| Transit | 5.0 m/s |
| Evasion maximum | 6.0 m/s |
| Planning acceleration | 3.0 m/s² |
| Yaw rate | 40°/s |
| Altitude | 5 m ± 0.5 m |

Braking into lane ends and corners limits the allowed speed:

$$
v_{\text{allow}} = \sqrt{v_{\text{end}}^{2} + 2\,(0.7\,a_{\max})\,d_{\text{brake}}}
$$

The cross-track pull is $v_{\text{cross}} = \min(0.4\,e,\ 1.5\ \text{m/s})$.

Here $a_{\max}$ is the maximum deceleration (3.0 m/s²), $d_{\text{brake}}$ is the distance left to brake with 0.8 s of command lag added, $v_{\text{end}}$ is the target speed at the end of the braking zone, and 0.7 is the fraction of $a_{\max}$ used. The cross-track pull has a gain of 0.4 per second on the off-lane error $e$ (m), capped at 1.5 m/s.

Basis: $s = v^{2}/2a$ (constant deceleration). A yaw rate of 40°/s is below the PX4 automatic yaw limit (about 45°/s). The acceleration limits keep lean inside the 35° tilt limit (T/W 2.03 / 2.00).

### Failsafes {#failsafes}

#### Failsafe Triggers and Actions {#failsafe-triggers-and-actions}

The failsafes are the red arrows of the state machine (Figure 17), and the table gives the trigger, threshold and basis for each. Mild faults (wind, battery or GNSS degradation) lead to RETURN or a normal landing, and faults that leave no time (motor failure, GNSS loss, 6% battery) lead to an immediate landing.

![Failsafe transitions into RETURN, LAND and DONE, highlighted](/report-assets/navigation-obstacle-avoidance/fsm-failsafe.png)

*Figure 17. Failsafe transitions of the state machine (highlighted). Red arrows end in LAND or DONE, and the blue RETURN arrow is used for the battery and degraded-GNSS cases.*

| Trigger | Threshold | Action | Basis |
| --- | --- | --- | --- |
| Wind slow-down | Smoothed lean above 14° | Reduce lane speed | 14° = 15.4 m/s steady wind (F = 11.5 N, tan θ = F / (m g)) |
| Wind abort | Lean above 33° for 6 s | Land | About 25 m/s; 2° under the 35° limit; 6 s is 2.4 gust time constants |
| Lane | More than 3 m off for 10 s | Abort and land | Worst excursion 2.1 to 2.6 m; recovery from 3 m takes 7 s |
| Swarm | 4 or more tracks + ESCAPE for 0.4 s | Land | Warning under 1 s (confirm at 8 m, closing 10 m/s); fired 5 of 6, false alarms 0 of 30 |
| GNSS degraded | Worse than 0.5 m for 60 s | Return home | RTK is 2 cm, so 0.5 m is 25× nominal; 60 s lets RTK re-converge |
| GNSS lost | No fix for 0.5 s | Land immediately | Drift 3 to 10 m at 8 m/s; 0.5 s is about 2 m of travel |
| Motor failure | Detected within 0.3 s | Land immediately | Free fall from 5 m is 1.0 s; a quad cannot recover (impact 8.8 to 9.6 m/s) |
| Battery: launch | Pack at 95% or more | Else refuse take-off | 25% return + 69% worst sortie (15 m/s, 30 m) + 1% = 95%; a sortie uses 40 to 69% |
| Battery: return | About 25% (20% reserve + return cost 3%) | Return home | Safety net: with a 95% launch the pack never reaches 25% |
| Battery: critical / emergency | Remaining 12% / 6% | Land beside runway edge / straight down | Edge landing 10.8 s (about 1% of the pack); 5 m descent 6 s (about 0.5%) |

Sources: wind force $F = \tfrac{1}{2}\rho\,C_dA\,v^{2}$ with $C_dA = 0.0794\ \text{m}^2$ and $m = 4.7\ \text{kg}$; gust time constant $\tau = 37\ \text{m}/v$ (Dryden, MIL-HDBK-1797 [\[11\]](../references#nav-ref-11)); PX4 User Guide, Safety configuration (battery failsafes staged as warning, return, land, emergency land) [\[8\]](../references#nav-ref-8); Unicore UM980 datasheet [\[16\]](../references#nav-ref-16); simulation stress tests (10 seeds per wind case, 8 per bird case); battery from the offline sim, lanes along, 266 Wh pack, worst of 3 seeds.

### Wind Kinematics {#wind-kinematics}

#### Wind Kinematics Calculations {#wind-kinematics-calculations}

**Approach.** The wind loads on the airframe were not derived again for the navigation work. The Mechanical team's sizing was adopted as the basis: the wind force on the airframe follows the standard drag law on the CAD frontal area, the drone leans until the horizontal component of thrust balances that force, and the thrust per motor then follows from the lean angle. The simulation reuses the same drag area, so the wind loads seen by the navigator are the loads that the airframe was sized for. Only the values that had to differ for a simulation are changed, and each change is justified below.

**Values taken from the Mechanical calculations**

| Parameter | Value | Basis |
| --- | --- | --- |
| Air density ρ | 1.225 kg/m³ | Sea level |
| Frontal area | 0.062038 m² | CAD (Mechanical) |
| Drag coefficient C<sub>d</sub> | 1.28 | Assumed, blunt body |
| Drag area C<sub>d</sub>A | 0.0794 m² | Area × C<sub>d</sub> |
| Required thrust | 1.329 kgf / motor | 12 m/s headwind, a = 1 m/s² (20° tilt) |
| Design thrust | 1.768 kgf / motor | 45° combined tilt, 5 kg |

**Values changed for the simulation, and why**

| Parameter | Mechanical | Simulation | Justification |
| --- | --- | --- | --- |
| Mass | 5.0 kg | 4.7 kg | The simulation model uses 4.7 kg (take-off mass of the modelled airframe) [confirm source]. A lighter drone leans further for the same drag, so the simulation is the harder case: at 15 m/s the lean is 13° at 4.7 kg against 12.5° at 5.0 kg |
| Tilt limit | 45° design, 30° for the M350 | 35° | A single bound for the whole mission, used by the planner's acceleration limits and by the wind abort, which is set 2° below it |
| Turbulence | not modelled | 0.25 of the mean wind | Moderate turbulence, assumed. A calm-air result would not exercise the lane controller |
| Wind guard (lean) | not applicable | 14° / 33° | Slow the lanes at 14° (steady wind of 15.4 m/s); land at 33° for 6 s (gust time constants, see the Failsafes section) |

The comparison with the Mechanical sizing is direct. At 15 m/s the wind force is 10.9 N and the steady lean is 13° (simulation), well inside the 35° limit. The gusts are what take the lean towards the limit, and they are modelled next.

**Turbulence model (Dryden-like gusts)**

Steady wind alone would only test whether the drone can lean far enough. The real difficulty on a survey is that wind changes while the drone is flying a 1.76 m wide lane, so the simulation adds gusts on top of the mean wind. The gust model follows the Dryden turbulence form of MIL-HDBK-1797 [\[11\]](../references#nav-ref-11), which describes turbulence as a random velocity with two parameters: an intensity $\sigma$ and a length scale $L$.

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

Sources: Mechanical calculations (take-off mass, CAD frontal area, assumed $C_d$ 1.28, results across flight scenarios); Dryden turbulence (MIL-HDBK-1797) [\[11\]](../references#nav-ref-11).

**Wind guard in the state machine.** The guard is the only place where wind changes the mission state (Figure 19). At a smoothed lean of 14° the machine moves from SURVEY to LANES SLOWED and returns when the lean falls back under 14°. At 33° for 6 s it lands.

![LANES SLOWED state and its transitions, highlighted](/report-assets/navigation-obstacle-avoidance/fsm-wind.png)

*Figure 19. Wind guard (highlighted): slow the lanes at a lean of 14° or more, resume under 14°, and land at 33° or more for 6 s (red arrow).*

## A3. Fabrication of Specimens/Prototypes {#a3-prototype-development}

### Navigation Architecture {#navigation-architecture}

The navigation system was developed and tested in simulation, using a Gazebo model of the survey drone flown with the PX4 autopilot. The navigator is a closed loop of five stages: **sense, localise, plan, command and act**. PX4's EKF2 fuses the sensors and outputs position, velocity and attitude, which the navigator reuses and never re-fuses. The planner runs in ROS 2 and sends a velocity and yaw set-point to PX4, and the new pose and obstacles re-enter the loop through the sensors.

<!-- TODO: closed-loop diagram (sense, localise, plan, command, act) for the flight control explanation. -->

The mission logic is a finite state machine, shown in Figure 4. Circles are states, arrows are transitions labelled with their trigger, and red arrows are failsafes.

![State transition diagram of the navigation architecture](/report-assets/navigation-obstacle-avoidance/fsm-full.png)

*Figure 4. Navigation state machine. One flight covers one sector (at most 15 min of battery).*

The architecture has the following features:

- **Mission states:** TAKEOFF, SURVEY, HOLD, RETURN, LAND and DONE, with SURVEY as the central state.
- **Behaviours inside SURVEY:** obstacle evasion (EVADE), global rerouting (REROUTE), revisits (REVISIT) and the wind slow-down (LANES SLOWED).
- **Failsafes:** transitions from SURVEY, LANES SLOWED and TAKEOFF to RETURN, LAND or DONE.
- **Localisation:** the EKF2 pose (RTK-GNSS, IMU, barometer and magnetometer) is the input to every transition, and GNSS quality drives three of the failsafes.
- **One sector per flight:** each sortie surveys one sector, then returns and lands.

### Mission States and Timing {#mission-states-and-timing}

Figure 8 highlights the path of a normal sortie through the state machine. The drone launches only with the battery at 95% or above, and otherwise the machine goes straight to DONE without taking off. It climbs to 5 m and enters SURVEY. After the last lane, any cell still missing one of the two cameras is flown again in REVISIT, up to six passes, and the machine then enters RETURN. RETURN can also be entered directly from SURVEY when the battery reaches about 25% or the GNSS stays degraded for 60 s. Every sortie ends in LAND and then DONE.

![Normal sortie path through the state machine: take-off, survey, revisit, return, land and done](/report-assets/navigation-obstacle-avoidance/fsm-mission.png)

*Figure 8. Normal sortie path through the state machine (highlighted).*

The typical duration of each state for a 30 m sector in calm air is given below.

| State | What happens | Typical time |
| --- | --- | ---: |
| TAKEOFF | Climb to 5 m | 2.8 s |
| SURVEY | 36 lanes, side-steps | 457 s |
| HOLD | Wait while a threat blocks | as needed |
| RETURN | Back to home | 9.7 s |
| LAND | Descend 5 m | 6.1 s |

The total is 476 s (7.9 min) in calm air and 533 s (8.9 min) at 10 m/s wind. The climb takes about 3 s at 1.3× hover thrust (944 W), which is about 0.3% of the pack, so it is never the limiting term. A supervisor applies the geofence, the 5 m ± 0.5 m altitude band and a speed clamp to every command.

Source: offline kinematic sim, lanes along the runway, 30 m sector, seed 1 (calm) and mean of 3 seeds (10 m/s). Climb energy from the Power Calculations in the [Electrical Design](./electrical-design#power-calculations) report (climb 1.3× hover, 236 W per motor).

## A4. Testing {#a4-testing}

### Software Used {#software-used}

Functionalities were verified and rendered through simulation software as follows:

- ROS 2 Jazzy: Robotic Node Communication
- Gazebo Harmonic: 3D Physics & Environment Simulator
- PX4 Autopilot SITL (Software-in-the-Loop): Flight Control Software
- Micro XRCE-DDS Agent v2.4.3 (uXRCE-DDS): Bridge between ROS2 and PX4
- Python: Offline Simulation and Scripting

All results for analysis are from offline simulations, run with various seeds per scenario. The Gazebo and PX4 runs confirm that the real controller behaves as the offline model predicts.

### Simulation Demonstrations {#simulation-demonstrations}

In every simulation video the overlay legend is: **RGB covered**, **thermal only**, **planned route** and **flown path**.

#### Baseline Survey {#baseline-survey}

<figure class="cv-video-panel">
 <div class="cv-video-pending" role="status"><span>BASELINE DEMONSTRATION</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video NAV-01</strong><span>Semester 1 deliverable: baseline survey with no wind and no birds. The planned route (white) and the drone following it. Green and cyan fill in as the RGB and thermal cameras cover the ground, and yellow is the flown path. Every cell needs both cameras.</span></figcaption>
</figure>

<figure class="cv-video-panel">
 <div class="cv-video-pending" role="status"><span>BASELINE DEMONSTRATION: ROUNDED TURNS</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video NAV-02</strong><span>Baseline survey with rounded turns. This option needs tuning (see Alternatives Evaluated).</span></figcaption>
</figure>

#### Obstacle Avoidance {#obstacle-avoidance-1}

![Simulation view of the coverage overlay and flown path](/report-assets/navigation-obstacle-avoidance/obstacle-avoidance-view.png)

*Figure 16. Simulation view used in the obstacle avoidance demonstrations: coverage overlay (green RGB, cyan thermal only) and the flown path (yellow).*

<figure class="cv-video-panel">
 <div class="cv-video-pending" role="status"><span>OBSTACLE AVOIDANCE DEMO</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video NAV-03</strong><span>Dodging an obstacle.</span></figcaption>
</figure>

<figure class="cv-video-panel">
 <div class="cv-video-pending" role="status"><span>OBSTACLE AVOIDANCE DEMO</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video NAV-04</strong><span>Revisiting a skipped lane.</span></figcaption>
</figure>

### Emergency Failsafe Demonstrations {#emergency-failsafe-demonstrations}

![Terminal log showing the starting wind speed in the take-off wind failsafe test](/report-assets/navigation-obstacle-avoidance/wind-failsafe-takeoff.png)

*Figure 18. Wind failsafe during take-off: simulation log showing the starting wind speed.*

<figure class="cv-video-panel">
 <div class="cv-video-pending" role="status"><span>WIND FAILSAFE DURING TAKE-OFF</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video NAV-05</strong><span>Wind failsafe during take-off.</span></figcaption>
</figure>

<figure class="cv-video-panel">
 <div class="cv-video-pending" role="status"><span>MOTOR FAILSAFE</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video NAV-06</strong><span>Motor failsafe.</span></figcaption>
</figure>

<figure class="cv-video-panel">
 <div class="cv-video-pending" role="status"><span>GNSS DEGRADED FAILSAFE</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video NAV-07</strong><span>GNSS degraded failsafe.</span></figcaption>
</figure>

<figure class="cv-video-panel">
 <div class="cv-video-pending" role="status"><span>TOTAL LOSS OF GNSS FAILSAFE</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video NAV-08</strong><span>Total loss of GNSS failsafe.</span></figcaption>
</figure>

### Wind Kinematics Demonstrations {#wind-kinematics-demonstrations}

![Drone body axes: roll forward axis, pitch side axis, yaw vertical axis](/report-assets/navigation-obstacle-avoidance/drone-axes.png)

*Figure 20. Axes used in the wind demonstrations: roll (forward axis), pitch (side axis) and yaw (vertical axis).*

<figure class="cv-video-panel">
 <div class="cv-video-pending" role="status"><span>WIND KINEMATICS DEMO: +X</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video NAV-09</strong><span>Turbulent winds from 2 to 7 m/s in the +x direction (0°): the drone leans about the pitch axis.</span></figcaption>
</figure>

<figure class="cv-video-panel">
 <div class="cv-video-pending" role="status"><span>WIND KINEMATICS DEMO: +Y</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video NAV-10</strong><span>Turbulent winds from 6 to 12 m/s in the +y direction (90°): the drone leans about the roll axis.</span></figcaption>
</figure>

<figure class="cv-video-panel">
 <div class="cv-video-pending" role="status"><span>WIND KINEMATICS DEMO: REVISIT</span><p>Video will be added here.</p></div>
 <figcaption><strong>Video NAV-11</strong><span>Turbulent winds from 6 to 12 m/s in the +y direction (90°): revisit pass after the baseline survey finishes.</span></figcaption>
</figure>

## A5. Analysis {#a5-analysis}

### Endurance vs. Mission Time {#endurance-vs-mission-time}

The longest flight time we expect (15 m/s crosswind) takes 13.2 min, inside the 13.9 min between launch and return.

![Battery budget bar: 95% launch, sector budget of 70% of the pack, 25% return, 12% critical, 6% emergency](/report-assets/navigation-obstacle-avoidance/endurance-budget.png)

*Figure 7. Sector budget: 70% of the pack, 13.9 min of flight, between the 95% launch and 25% return levels, followed by the 12% critical and 6% emergency levels.*

| Wind (30 m sector) | Flight time | Pack used | Left from 95% |
| --- | ---: | ---: | ---: |
| Calm | 7.9 min | 39.5% | 55% |
| 10 m/s crosswind | 9.3 min | 47.0% | 48% |
| 12 m/s crosswind | 10.5 min | 53.6% | 41% |
| 14 m/s crosswind | 12.5 min | 65.0% | 30% |
| 15 m/s along runway | 11.1 min | 57.8% | 37% |
| **15 m/s crosswind** | **13.2 min** | **68.9%** | **26%** |

Worst of 3 seeds, lanes along the runway, turbulence 25%.

**Why 15 min?** The pack holds 266 Wh and the drone draws about 805 W, so a full drain lasts 19.8 min, or 15.9 min when use is limited to 80% of the pack. A sortie spends only the window from the 95% launch to the 25% return, which is 70% of the pack or 13.9 min. The worst case flown, a 15 m/s crosswind over a 30 m sector, takes 13.2 min and 69% of the pack, so it fits. At 15 m/s the longest sector that fits is 30 m (35 m needs 73%, 40 m needs 83% and 60 m needs 103%).

### Wind Testing Overall Results {#wind-testing-overall-results}

| Wind (turbulence 25%) | Completed | Worst off-lane | Wind abort fired |
| --- | :---: | ---: | :---: |
| Calm | 3/3 | 0.7 m | No |
| 10 m/s crosswind | 3/3 | 0.7 m | No |
| 12 m/s crosswind | 3/3 | 1.0 m | No |
| 14 m/s crosswind | 3/3 | 1.4 m | No |
| 15 m/s along the runway | 3/3 | 1.0 m | No |
| 15 m/s crosswind | 3/3 | 2.1 m | No |

**Safe flying conditions.** The airframe holds 15 m/s (steady lean about 13°, peak 35° in gusts) and stays within 2.1 m of the lane, inside the 3 m lane failsafe limit.

Results unchanged across camera and coverage changes:

- Take-off and landing in wind (6 to 15 m/s): drift 0.3 to 2.1 m from the target point and touchdown at 0.72 m/s vertical speed.
- Drag-area ($C_dA$) sensitivity (successful runs out of 6 seeds): $C_dA$ 0.10: 5/6 at 15 m/s; $C_dA$ 0.20: 0/6 at 12 m/s.

Source: offline kinematic sim, lanes along the runway, wind blowing across (90°) or along (0°) the runway, seeds 1 to 3, 25% turbulence. The Gazebo demonstrations use a 60 m sector.

## A6. Discussion of Problems and Project Plan {#a6-problems-project-plan}

### Further Concerns and Solutions {#nav-future-works}

#### Further Concerns and Solutions {#further-concerns-and-solutions}

The simulation also exposed concerns that were not foreseen in the design stage. The table records each one with the evidence found and the mitigation we propose, and the mitigations feed the Semester 2 plan.

| Concern found | Evidence from simulation | Proposed mitigation |
| --- | --- | --- |
| Obstacles above or below the 2D LiDAR plane (canopies, wires, thin poles) | Not visible to a planar scan | Gimbal-stabilised or tilting 360° LiDAR, or upgrade to 3D LiDAR |
| Strong sunlight shortens LiDAR range | Range 4.7 m cuts the speed cap from 4.23 to 2.2 m/s; birds seen 16/17 to 5/37 | Shade and filter the sensor, fly at low sun, or upgrade to a longer-range unit |
| Bird flocks beat the avoider | About 9% collisions in the dense stream; flock collisions 8 to 28 as range falls | Swarm failsafe lands; earlier detection (second sensor); avoid peak bird activity |
| Wind limit depends on the real drag area | C<sub>d</sub>A 0.10: 5/6 seeds successful at 15 m/s; C<sub>d</sub>A 0.20: 0/6 successful at 12 m/s | Measure C<sub>d</sub>A and hover power on a thrust stand; set the wind limit from it |
| GNSS degraded or lost | Degraded: off-lane rms 0.7 to 1.4 m. Lost: drift 3 to 10 m at 8 m/s | Return home after 60 s; land at once on loss; add optical flow or a second RTK source |
| Motor failure | Quad cannot recover: impact 8.8 to 9.6 m/s (183 to 218 J) | Motor health monitoring, propulsion redundancy or a parachute; keep clear of people |

### Semester 2 Development Plan {#nav-semester-2-plan}

#### Navigation Future Works {#navigation-future-works}

Semester 2 moves from simulation to hardware. The plan has three steps, ordered so that nothing is flown live until the simulation has predicted it.

**1. Build and bench-test the hardware**

- Finish integration of the full hardware stack and troubleshoot it.
- Thrust stand: measure drag area and hover power.
- Outdoor N10 LiDAR test in sunlight.

**2. Update the simulation and predict**

- Feed the measured values back into the simulation.
- Re-run wind limits, endurance and failsafe thresholds.
- Tune live flight test cases in the simulation.

**3. Live test, then compare**

- Controlled flight testing: implement live flight test cases and only proceed if verified in simulation.
- Compare live logs with the simulation and correct the model.

Repeat the iterative process.

</div>