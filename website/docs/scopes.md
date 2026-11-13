---
title: Project Scope
---

<script setup>
import ScopeDropdown from './.vitepress/theme/components/ScopeDropdown.vue'
</script>

<p class="chapter-kicker">FOD ARGUS / PROJECT REPORT</p>

# Project Scope

<ScopeDropdown id="scope-arun" name="Muruganantham Arun" matric="A0308280J" portrait="/team/Arun.png">

**Assigned subsystem:** [Mechanical Design](/subsystems/mechanical-design).

The scope is to design, fabricate and validate the mechanical structure of ARGUS so it can carry the inspection equipment and support the intended flight operations.

- **Airframe and propulsion:** Develop the frame, base plates, propeller arms and landing gear. Select materials and motor-propeller combinations based on mass, thrust, strength and fabrication requirements.
- **Component placement:** Position and mount the electronics, cameras and sensors while maintaining balanced mass distribution, wiring access and clear sensor views.
- **Structural validation:** Assess centre of gravity, arm deflection and natural frequencies. Use structural FEA, modal analysis and physical tests to check and refine the design.
- **Environmental protection:** Develop protective enclosures, water-resistant ventilation and vibration-damping mounts without blocking cooling or sensor operation.
- **Prototype testing:** Fabricate and assemble the prototype, verify motor and structural integration, and support calibration and controlled flight testing with the other subsystems.

</ScopeDropdown>

<ScopeDropdown id="scope-talitha" name="Kummarikunta Talitha" matric="A0286653R" portrait="/team/Talitha.jpg">

**Assigned subsystems:** [Electrical Design](/subsystems/electrical-design) and [Navigation and Obstacle Avoidance](/subsystems/navigation-obstacle-avoidance).

The scope is to provide the power, wiring and sensor connections for ARGUS, and develop the navigation needed to survey the runway, avoid obstacles and return within the available flight time.

- **Power distribution:** Select and size the battery, power-distribution board, converters, fuse and wiring. Evaluate power demand and endurance for the Jetson-only setup and the Raspberry Pi fallback.
- **Electrical and sensor integration:** Assemble the electrical connections, calibrate the sensors and verify measured voltage, current and power against the design calculations.
- **Runway navigation:** Develop survey routes, position control and mission logic using ROS 2 and PX4. Provide drone position and orientation data for the vision system.
- **Obstacle avoidance and failsafes:** Use LiDAR and navigation data to respond to static obstacles, moving obstacles, wind, battery limits and positioning loss. Assess sensor blind spots and operating limits.
- **Simulation and flight validation:** Develop and test the navigation in Gazebo and offline simulations. Update the models using hardware measurements, then compare controlled flight tests with the predicted behaviour.

</ScopeDropdown>

<ScopeDropdown id="scope-charan" name="Charansagar Ramanujam" matric="A0301658E" portrait="/team/Charan.png">

**Assigned subsystems:** [Computer Vision Based Inspection and Safety System](/subsystems/computer-vision) and [Communication System](/subsystems/communication-system).

The scope is to develop the vision system for runway inspection and the communication system that sends detected FOD coordinates to HUNTER and inspection updates to the base station.

- **Inspection pipeline:** Develop and evaluate PatchCore anomaly detection, YOLO FOD detection and U-Net crack segmentation for FOD, visible cracks and puddles. Compare parallel and sequential processing architectures.
- **Camera setup and small-object detection:** Select the RGB camera and lens for the proposed 5 m inspection height and 1 cm FOD requirement. Develop and test image tiling, camera stabilisation and night lighting for this setup.
- **Datasets and model validation:** Collect suitable test-ground images, control similarity leakage between dataset splits and improve crack detection on rough surfaces. Measure detection performance, false alarms, processing time and memory use.
- **Coordinate extraction:** Combine image detections with navigation position and orientation to calculate FOD ground coordinates. Validate camera calibration, gimbal alignment and coordinate error.
- **Thermal safety:** Develop thermal detection of people and birds, the proposed stop response and the live feed for operator override at night.
- **FOD communication:** Define ROS 2 alert messages and integrate the selected radio link. Maintain the ARGUS-side coordinate queue, receipt acknowledgements, up to 100 retries and base-station error notifications. Test range, interference, video transmission and the proposed security measures.
- **Onboard integration:** Deploy and benchmark the vision and communication systems on Jetson with the other subsystems. Evaluate workload sharing with the Raspberry Pi where needed.

</ScopeDropdown>
