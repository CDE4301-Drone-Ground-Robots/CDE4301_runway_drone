---
title: Communication System
outline: [2, 2]
prev: false
next: false
aside: false
pageClass: subsystem-report-page
---

<script setup>
import CommunicationFigure from './components/CommunicationFigure.vue'
import CommunicationVideo from './components/CommunicationVideo.vue'
import CommunicationDemo from '../.vitepress/theme/components/CommunicationDemo.vue'
</script>

<div class="cv-report comms-report rubric-report">

<p class="chapter-kicker">FOD ARGUS / COMMUNICATION SYSTEM</p>

# Communication System

<SubsystemLead class="cv-report-byline" name="Charansagar Ramanujam" matric="A0301658E" portrait="/team/Charan.png" />

## A1. Objective, Scope and Context {#a1-objective-scope-context}

### Summary {#uav-ugv-communication}

ARGUS UAV and HUNTER UGV are designed to work collaboratively for FOD detection and removal. ARGUS searches the runway for FOD. HUNTER receives the detected object locations and navigates to collect them. A communication system is required to transmit the accurate FOD position from ARGUS to HUNTER. The transmitted message includes object classification, detection confidence score and target coordinates. This allows ARGUS to scan while HUNTER handles object retrieval.

The communication subsystem was initially developed and tested using ROS 2 over a local WI-FI network. This provides a preliminary communication framework that’s needed before integration with the actual hardware and choosing a suitable communication method.

### Requirements and Considerations {#requirements}

The operational range must be up to 5 km, as that’s the runway length. The 917-925 MHz band was initially considered; final frequency and power settings must meet the applicable IMDA requirements. The communication device must support live video transmission and be small and lightweight to fit ARGUS’s payload limits. The thermal live feed is intended for manual override, allowing the operator to guide ARGUS back at night if the drone encounters a problem. Live-feed integration and testing are pending.

## A2. Methodology / Concept Development {#a2-methodology-concept-development}

### UAV Communication Architecture {#communication-architecture}

<CommunicationFigure src="/report-assets/communication-system/interim-communication-architecture.svg" :width="1000" :height="480" caption="Interim ARGUS-HUNTER communication over local Wi-Fi." />

This architecture enables communication between the two systems without requiring the Python scripts to establish direct network socket connections manually.

### C2 Alert Message Structure {#c2-alert-message}

The communication system uses structured command and control (C2) alert messages to send the detected object. It is formatted as a JSON and sent using ROS 2 std_msgs/String messages.

The message format is as follows:

| Field | Description |
| --- | --- |
| Threat ID | Identifies an individual FOD detection |
| Object classification | Specifies the detected object, such as a screw, bolt or wrench |
| Confidence score | Indicates the detection model's confidence |
| Target coordinates | Specifies the intended target location |
| Timestamp | Records when the alert was generated |
| Mission ID | Associates the alert with the relevant operation |

### DDS & QoS {#dds-qos}

ROS 2 uses DDS (Data Distribution Service) middleware to exchange messages between ARGUS and HUNTER. DDS handles automatic device discovery and message delivery using the RTPS protocol over UDP/IP, allowing data to be transmitted through a local Wi-Fi network. ROS 2 provides DDS Security, which offers additional security features not yet implemented but planned for future setup. Currently, access protection depends on the network’s security configuration.

ROS 2 quality of service (QoS) settings improve FOD alert transmission reliability and are configured in the UAV publisher. The reliable policy enables message retransmission when necessary and reduces the likelihood of message loss during operation.

TRANSIENT_LOCAL durability allows the subscribers to retrieve the last retained alert.

The KEEP_LAST history policy with a depth of 1 holds the most recent alert. These settings improve communication reliability while maintaining a lightweight message-transmission system.

### Long-Range Communication Hardware {#long-range-hardware}

| Feature | Microhard P900 V2 | Microhard pMDDL2450 |
| --- | --- | --- |
| FOD coordinates / JSON alerts | Yes | Yes |
| Still images | Technically possible, but slow | Yes, more suitable |
| Live video streaming | Not practical | Yes, designed for higher-bandwidth data |
| Communication type | Low-bandwidth serial telemetry | Broadband IP communication |
| Best use for ARGUS | FOD alerts only | FOD alerts + images/video |

Two radio communication methods were explored for future ARGUS – HUNTER communication. The microhard P900 V2 and the microhard pMDDL2450. The P900 provides serial RF communication suitable for transmitting small C2 alert messages. The pMDDL2450 supports higher-bandwidth IP communication. Since ARGUS must send crack images and a thermal live feed to the base station, the pMDDL2450 is a candidate, though it's heavier and consumes more power than the P900.

The pMDDL2450 operates at 2.4 GHz with adjustable output up to 1 W. Full-power operation would exceed IMDA's published 100 mW EIRP limit for licence-exempt UAV use in this band. Antenna gain and cable losses must be included when checking the radiated power. I still need to confirm a compliant setup and test whether it can provide a reliable 5 km link at the permitted power. The radio selection is therefore not final. See [COM-H01](../references#com-h01) and [COM-R02](../references#com-r02).

### Communication and Vision System Workflow {#vision-communication-workflow}

The vision system continuously requests drone centre coordinates from the navigation system. If an FOD is detected, the drone coordinates go through the coordinate extraction method to get the precise FOD coordinate, then through the communication system, where it is published to HUNTER.

<CommunicationFigure src="/report-assets/communication-system/vision-communication-workflow.svg" :width="1000" :height="680" caption="Proposed vision-to-comms workflow. Stage 2 uses a simulation; full integration is pending." />

## A3. Fabrication of Specimens/Prototypes {#a3-prototype-development}

### Interim Communication {#interim-communication}

For interim communication, I implemented ROS 2 Jazzy to establish communication between ARGUS and HUNTER. ROS 2 provides a publisher-subscriber communication architecture that sends information between systems. I implemented communication using Python 3 and the ROS 2 Python client library.

<CommunicationFigure src="/report-assets/communication-system/software-tools.png" :width="1503" :height="733" caption="Software used for the interim communication system." />

### Multiple FOD Transmission {#multiple-fod-transmission}

The application queue runs on ARGUS and stores pending FOD alerts in arrival order. The planned process is to send one alert and retain it until HUNTER confirms receipt with the same threat ID. ARGUS then sends the next coordinate without waiting for FOD collection to finish. Live receipt acknowledgements will be added during integration. The threat ID would be as follows:

| Object | Threat ID |
| --- | --- |
| Screw | `FOD_THREAT_001` |
| Wrench | `FOD_THREAT_002` |
| Bolt | `FOD_THREAT_003` |

This is reset after every run. This is also particularly useful in detecting communication loss. For example, if the HUNTER is supposed to receive _005 but receives _007 instead, it indicates a communication loss or error. Currently, no measures are implemented, but future work will have ARGUS resend those coordinates. If the problem continues, it alerts the base station.

#### Communication Simulator {#communication-simulator}

Add example FOD alerts to the ARGUS queue. Use "Acknowledge receipt" to simulate HUNTER confirming receipt and release the next coordinate.

<CommunicationDemo />

## A4. Testing {#a4-testing}

### Communication Testing {#communication-testing}

#### Stage 1: Local Wi-Fi Test {#stage-1-local-wi-fi-test}

The test was done on a laptop running Ubuntu 24.04 with WSL to simulate ARGUS’s onboard computer, while a Raspberry Pi 5 running ROS 2 Jazzy in a Docker container simulated HUNTER’s communication system. In this test, both devices must share the same local Wi-Fi network. A simple test message, "Hello World", was sent from one device to another.

<CommunicationVideo src="/report-assets/communication-system/stage-1-wifi.mp4" poster="/report-assets/communication-system/stage-1-poster.jpg" caption="Stage 1: Local Wi-Fi message transmission." />

#### Stage 2: Simulated FOD Queue {#stage-2-simulated-fod-queue}

In this simulation below, ARGUS detects the FOD and, at the backend, asks the Navigation system to send the drone centre coordinates. The Vision system performs precise coordinate extraction of the actual FOD and sends it to the communication system. The terminals on the right show the queueing system built on the ARGUS side. The top terminal queues new FOD coordinates, while the bottom terminal shows the next FOD coordinate that's ready to be published. The queue system was designed so that, when multiple FODs are sent, it can queue them all. This prevents missed detections by storing the FODs' coordinates instead of overwriting them with newer detections. It allows sequential collection where the UGV completes its current target before proceeding to the next. This also supports continuous identification and transmission of FOD locations while the UGV is occupied. The UGV can also manage multiple targets without interruption in this system.

<CommunicationVideo src="/report-assets/communication-system/stage-2-simulation.mp4" poster="/report-assets/communication-system/stage-2-poster.jpg" caption="Stage 2: Simulated FOD coordinates and target queueing. Full integration is pending." />

#### C2 Alert Transmission {#c2-alert-transmission}

The C2 alert transmission test is shown below. A Python script (DemoComs_C2.py) served as a ROS 2 publisher, sending FOD detection information to the Raspberry Pi 5(simulated HUNTER) through the `/c2/target_alert` communication channel. It sends the FOD detection data in JSON format.

On the Raspberry Pi 5, the receiver successfully receives and decodes the messages. It then displays the FOD classification, confidence score and the target coordinates in the terminal. In the background, it converts the received coordinates into a ROS 2 PoseStamped navigation goal and publishes it to the `/goal_pose` topic.

<CommunicationFigure src="/report-assets/communication-system/argus-publisher-test.png" :width="1252" :height="223" caption="Original ARGUS publisher screenshot from the laptop test." />

<CommunicationFigure src="/report-assets/communication-system/hunter-receiver-test.png" :width="909" :height="204" caption="Original HUNTER receiver screenshot from Raspberry Pi 5. The log reports Nav2 unavailable, so this shows message reception and goal publication, not completed navigation." />

These tests were successful (shown in the figure above), proving that the ARGUS and HUNTER can exchange structured data over a local wireless network. This served as the baseline foundation for integrating the real-time FOD detection from the vision system with the HUNTER’s autonomous navigation system.

## A5. Analysis {#a5-analysis}

### Communication Performance Evaluation {#performance-evaluation}

| Performance parameter | Result |
| --- | ---: |
| C2 alert JSON payload size | 588 bytes |
| Estimated payload bandwidth (2 alerts/s) | 9.408 kbps |
| Test setup | Publisher and subscriber on the same device (0 m separation) |
| Consecutive messages transmitted | 100 |
| Consecutive messages received | 100 |
| Message delivery rate | 100% |
| Missing messages | 0 |
| Duplicate messages | 0 |
| Nominal benchmark transmission rate | 10 Hz |

The 100-message benchmark used ROS 2 Jazzy with the publisher and subscriber on the same device (0 m separation). The C2 alert payload size was measured at 588 bytes, and the estimated application-level bandwidth was 9.408 kbps at two alerts per second. This covers alert payloads only, excluding video and network overhead. The thermal live-feed resolution, frame rate, bandwidth and delay still need to be confirmed and tested. Additionally, a ROS 2 test was conducted using 100 consecutive alerts simulating the C2 alerts at a nominal rate of 10Hz sent from publisher to subscriber. All 100 messages were received successfully hence attaining the 100% delivery rate with no missing or duplicate messages. This checks local ROS 2 message delivery; it does not measure wireless range or performance between separate devices.

## A6. Discussion of Problems and Project Plan {#a6-problems-project-plan}

### Limitations and Future Works {#future-work}

Although the interim tests demonstrated successful message transmission, several limitations remain. Firstly, the current communication relies on a local Wi-Fi network, which has not been tested for the full runway. Further research led to the decision to use long-range RF communication hardware that meets IMDA regulations within the operating range. ARGUS communications scripts are still not linked to the vision system, so the next stage is to integrate with the onboard vision system to automate C2 alerts. Additional reliable communication methods will be explored, including a receipt acknowledgement carrying the threat ID, sequence-number tracking, and communication-loss detection. The next queued alert will be sent after the matching receipt acknowledgement returns to ARGUS. Finally, security enhancements such as authenticated messages and encryption will improve the protection of transmitted FOD information. The final objective is to establish a reliable communication system that allows ARGUS to detect and send coordinates to HUNTER, supporting timely FOD removal.

### Hunter Group Communication {#hunter-group-communication}

For the HUNTER group's communication report, see [HUNTER Group Communication](https://cde4301-drone-ground-robots.github.io/CDE4301_runway_patrol/report#communications).

</div>
