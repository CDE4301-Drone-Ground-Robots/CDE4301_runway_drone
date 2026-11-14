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
import CommsDashboardDemo from '../.vitepress/theme/components/CommsDashboardDemo.vue'
</script>

<div class="cv-report comms-report rubric-report" style="--report-chapter: '5'">

<p class="chapter-kicker">FOD ARGUS / COMMUNICATION SYSTEM</p>

# 5. Communication System {#communication-system}

<SubsystemLead class="cv-report-byline" name="Charansagar Ramanujam" matric="A0301658E" portrait="/team/Charan.png" />

## 5.1 Objective and Requirements {#a1-objective-scope-context}

<span id="uav-ugv-communication" class="report-anchor" aria-hidden="true"></span>

ARGUS UAV and HUNTER UGV are designed to work collaboratively for FOD detection and removal. ARGUS searches the runway for FOD. HUNTER receives the detected object locations and navigates to collect them. A communication system is required to transmit the accurate FOD position from ARGUS to HUNTER. The transmitted message includes object classification, detection confidence score and target coordinates. This allows ARGUS to scan while HUNTER handles object retrieval.

The communication subsystem was initially developed and tested using ROS 2 over a local WI-FI network. This provides a preliminary communication framework that’s needed before integration with the actual hardware and choosing a suitable communication method.

### 5.1.1 Base Station {#base-station}

The base station is the control room where operators can receive updates from ARGUS or HUNTER and take the necessary actions if required. The base-station communication link is planned for the final setup.

### 5.1.2 Requirements and Considerations {#requirements}

The operational range must be up to 5 km, as that’s the runway length. The 917-925 MHz band was initially considered for telemetry messages only. The final frequency and power settings must meet the applicable IMDA requirements. The communication device must support live video transmission at a minimum resolution of 1080p (1920 × 1080) and be small and lightweight to fit ARGUS’s payload limits. The thermal live feed is intended for manual override, allowing the operator to guide ARGUS back at night if the drone encounters a problem. Live-feed integration and testing will be carried out after the interim assessment.

## 5.2 Communication Methodology and Architecture Development {#a2-methodology-concept-development}

### 5.2.1 UAV Communication Architecture {#communication-architecture}

<CommunicationFigure number="118" src="/report-assets/communication-system/interim-communication-architecture.svg" :width="1200" :height="680" caption="ARGUS sender queue and message delivery over the interim link. The queue is demonstrated in Stage 2. Live receipt acknowledgements and handshake-based recovery will be implemented and tested after the interim assessment." />

This architecture enables communication between the two systems without requiring the Python scripts to establish direct network socket connections manually.

### 5.2.2 C2 Alert Message Structure {#c2-alert-message}

The communication system uses structured command and control (C2) alert messages to send the detected object. It is formatted as a JSON and sent using ROS 2 std_msgs/String messages.

The message format is as follows:

<p class="report-table-caption" id="table-60"><strong>Table 60.</strong> C2 Alert Message Structure</p>

| Field | Description |
| --- | --- |
| Threat ID | Identifies an individual FOD detection |
| Object classification | Specifies the detected object, such as a screw, bolt or wrench |
| Confidence score | Indicates the detection model's confidence |
| Target coordinates | Specifies the intended target location |
| Timestamp | Records when the alert was generated |
| Mission ID | Associates the alert with the relevant operation |

### 5.2.3 DDS & QoS {#dds-qos}

ROS 2 uses DDS (Data Distribution Service) middleware to exchange messages between ARGUS and HUNTER. DDS handles automatic device discovery and message delivery using the RTPS protocol over UDP/IP, allowing data to be transmitted through a local Wi-Fi network. ROS 2 provides DDS Security, which offers additional security features not yet implemented but planned for future setup. Currently, access protection depends on the network’s security configuration.

ROS 2 quality of service (QoS) settings improve FOD alert transmission reliability and are configured in the UAV publisher. The reliable policy enables message retransmission when necessary and reduces the likelihood of message loss during operation.

TRANSIENT_LOCAL durability allows the subscribers to retrieve the last retained alert.

The KEEP_LAST history policy with a depth of 1 holds the most recent alert. These settings improve communication reliability while maintaining a lightweight message-transmission system.

### 5.2.4 Long-Range Communication Hardware {#long-range-hardware}

Two radio communication methods were explored for the final setup:

<p class="report-table-caption" id="table-61"><strong>Table 61.</strong> Long-Range Communication Hardware</p>

| Parameter | Serial RF: Microhard P900 V2 | Broadband IP: Microhard pMDDL2450 |
| --- | --- | --- |
| Operating frequency | 902-928 MHz. A 917-925 MHz setting was considered, but its configuration and IMDA suitability need checking. | 2.402-2.478 GHz |
| Data rate | Up to 276 kbps link rate | Up to 25 Mbps advertised throughput, depending on settings and signal conditions |
| Interfaces | Serial UART, with USB for connection and configuration | Ethernet, serial and USB |
| RF output capability | Adjustable from 100 mW to 1 W | Adjustable up to 1 W |
| FOD coordinates / JSON alerts | Suitable | Suitable |
| Images and live video | Limited bandwidth, not suitable for the required live feed | Supports wireless images, video and telemetry |
| Range for this project | 5 km requirement, not verified | 5 km requirement, not verified at the permitted power |
| Selection | Not preferred because it cannot support the required live feed | Preferred candidate, final selection pending validation |

Specifications: [\[70\]](../references#com-h02) and [\[71\]](../references#com-h01). The listed RF output capabilities are hardware specifications, not permitted operating powers.

The **pMDDL2450 is the preferred candidate** because its broadband IP radio link supports FOD alerts, crack images and the thermal live feed. The final device will be confirmed after checking its permitted power configuration and testing the required range and video performance. The P900 V2 is suitable for small serial messages but does not provide the bandwidth needed for the live feed.

For the proposed **2.4 GHz UAV link**, IMDA specifies a maximum of **100 mW EIRP (20 dBm)**. The setup must be configured to operate below 100 mW EIRP, including antenna gain and cable losses. The radio's full 1 W setting will not be used under these licence-exempt conditions. Configuration and a reliable 5 km link still need testing at the permitted power ([\[72\]](../references#com-r02)). The 100 mW limit should not be assumed to apply to every frequency band.

### 5.2.5 Interference in Shared Frequency Bands {#shared-frequency-interference}

The proposed 2.4 GHz link uses a shared band, not a frequency reserved for ARGUS. Nearby Wi-Fi, Bluetooth and other devices can interfere when transmissions overlap. This can cause lost or delayed FOD alerts and reduce live-feed quality ([\[73\]](../references#com-t01)). IMDA states that short-range devices operate on a non-interference and non-protection basis, so an interference-free link cannot be assumed ([\[74\]](../references#com-r03)).

Before operation, the plan is to check channel use and select a less busy channel within the permitted settings. Alerts and video will be tested together under quiet and busy conditions. Receipt acknowledgements and retries are planned to handle missing alerts, but they do not remove radio interference. These tests are still pending.

### 5.2.6 Proposed Communication Security {#communication-security}

Encryption is planned to protect FOD messages from being read during transmission. ROS 2 DDS Security also supports certificate-based authentication, message-integrity checks and permissions that limit which nodes can publish or subscribe to each topic ([\[75\]](../references#com-s01)). These features need to be configured and enforced. They are not enabled in the current prototype.

The plan also includes checks for old or repeated alerts and protection of private keys. These measures reduce the risk of unauthorised access and message tampering. They do not prevent radio interference or jamming. Implementation and testing are listed in [Section 5.6.1.5](#message-security-plan).

### 5.2.7 Communication and Vision System Workflow {#vision-communication-workflow}

In the proposed workflow, vision uses navigation data to calculate the precise FOD coordinates. The ARGUS queue stores FOD coordinates in the order they are detected and sends one alert at a time. Each alert stays queued until HUNTER confirms receipt with the same threat ID. If communication is lost, ARGUS keeps the alert and resends it when the link returns. After the matching receipt acknowledgement, ARGUS sends the next queued coordinate without waiting for collection to finish. Live acknowledgements and retransmission will be implemented and tested after the interim assessment.

<CommunicationFigure number="119" src="/report-assets/communication-system/vision-communication-workflow.svg" :width="1200" :height="900" caption="Proposed vision-to-comms workflow with the queue on ARGUS. Unacknowledged alerts are retained for retry. Stage 2 is simulated. Live integration will be implemented and tested after the interim assessment." />

## 5.3 Communication Prototype Implementation {#a3-prototype-development}

### 5.3.1 Interim Communication {#interim-communication}

For interim communication, I implemented ROS 2 Jazzy to establish communication between ARGUS and HUNTER. ROS 2 provides a publisher-subscriber communication architecture that sends information between systems. I implemented communication using Python 3 and the ROS 2 Python client library.

<CommunicationFigure number="120" src="/report-assets/communication-system/software-tools.png" :width="1503" :height="733" caption="Software used for the interim communication system." />

### 5.3.2 Multiple FOD Transmission {#multiple-fod-transmission}

The application queue runs on ARGUS and stores pending FOD alerts in the order they are detected. The planned process is to send one alert and retain it until HUNTER confirms receipt with the same threat ID. ARGUS then sends the next coordinate without waiting for FOD collection to finish. Live receipt acknowledgements will be added during integration. The threat ID would be as follows:

<p class="report-table-caption" id="table-62"><strong>Table 62.</strong> Multiple FOD Transmission</p>

| Object | Threat ID |
| --- | --- |
| Screw | `FOD_THREAT_001` |
| Wrench | `FOD_THREAT_002` |
| Bolt | `FOD_THREAT_003` |

The threat ID sequence resets after the ARGUS drone has finished its run for that particular day. HUNTER will use the mission and threat IDs to avoid duplicate targets.

#### 5.3.2.1 Communication Simulator {#communication-simulator}

Add example FOD alerts to the ARGUS queue. Use "Acknowledge receipt" to simulate HUNTER confirming receipt and release the next coordinate.

<CommunicationDemo />

### 5.3.3 Link Handshake and Communication Loss {#link-handshake-and-communication-loss}

In the proposed setup, ARGUS sends a link-check message to HUNTER every second, and HUNTER replies to confirm that both are still connected. If ARGUS receives no replies for 10 seconds, it informs the base station if reachable and waits for further commands. This handshake only checks the link between them, while the receipt ACK confirms that a specific FOD target was received.

If the base station cannot be reached, the notification will remain stored until its link returns. Undelivered FOD coordinates will stay in the ARGUS queue and be resent when communication returns. This recovery process will be implemented and tested after the interim assessment.

### 5.3.4 FOD Database and Delivery Records {#fod-database-and-delivery-records}

A local database will be added on ARGUS after the interim assessment to store FOD coordinates for resending and bookkeeping. Each record will contain the mission ID, threat ID, object type, X and Y coordinates, detection time and delivery status. The mission ID will distinguish records from different days when the threat ID sequence resets.

Each FOD record will be saved before it enters the transmission queue. The queue controls which target is sent next, while the database keeps the stored records. If communication is lost, unacknowledged records will remain stored and be resent with the same mission and threat IDs when the link returns. If an ACK is lost, ARGUS sends the target again. HUNTER checks the mission and threat IDs to avoid adding the same target twice.

When HUNTER returns a matching receipt ACK, the database will mark the record as acknowledged and save the acknowledgement time. The record will remain available for bookkeeping instead of being deleted. This history will show which FOD coordinates were detected, sent and acknowledged. An acknowledged record confirms delivery, not completed FOD collection. Database storage and integration with ROS 2 will be implemented and tested after the interim assessment.

The database will be connected to the user interface (UI) described in [Future Works: Communication Monitoring Website](#communication-monitoring-interface).

## 5.4 Communication Testing {#a4-testing}

### 5.4.1 Communication Test Demonstrations {#communication-testing}

#### 5.4.1.1 Stage 1: Local Wi-Fi Test {#stage-1-local-wi-fi-test}

The test was done on a laptop running Ubuntu 24.04 through WSL to simulate ARGUS’s onboard computer, while a Raspberry Pi 5 ran ROS 2 Jazzy in a Docker container to simulate HUNTER’s communication system. In this test, both devices shared the same local Wi-Fi network. A simple test message, "Hello World", was sent from one device to another.

<CommunicationVideo src="/report-assets/communication-system/stage-1-wifi.mp4" poster="/report-assets/communication-system/stage-1-poster.jpg" caption="Stage 1: Local Wi-Fi message transmission." />

#### 5.4.1.2 Stage 2: Simulated FOD Queue {#stage-2-simulated-fod-queue}

In this simulation below, ARGUS detects the FOD and, at the backend, asks the Navigation system to send the drone centre coordinates. The Vision system performs precise coordinate extraction of the actual FOD and sends it to the communication system. The terminals on the right show the queueing system built on the ARGUS side. The top terminal queues new FOD coordinates, while the bottom terminal shows the next FOD coordinate that's ready to be published. The queue system was designed so that, when multiple FODs are sent, it can queue them all. This prevents missed detections by storing the FODs' coordinates instead of overwriting them with newer detections. It allows sequential collection where the UGV completes its current target before proceeding to the next. This also supports continuous identification and transmission of FOD locations while the UGV is occupied. The UGV can also manage multiple targets without interruption in this system.

<CommunicationVideo src="/report-assets/communication-system/stage-2-simulation.mp4" poster="/report-assets/communication-system/stage-2-poster.jpg" caption="Stage 2: Simulated FOD coordinates and target queueing. Full integration is pending." />

#### 5.4.1.3 C2 Alert Transmission {#c2-alert-transmission}

The C2 alert transmission test is shown below. A Python script (DemoComs_C2.py) served as a ROS 2 publisher, sending FOD detection information to the Raspberry Pi 5(simulated HUNTER) through the `/c2/target_alert` communication channel. It sends the FOD detection data in JSON format.

On the Raspberry Pi 5, the receiver successfully receives and decodes the messages. It then displays the FOD classification, confidence score and the target coordinates in the terminal. In the background, it converts the received coordinates into a ROS 2 PoseStamped navigation goal and publishes it to the `/goal_pose` topic. This will be explained further in the HUNTER team’s report.

<CommunicationFigure number="121" src="/report-assets/communication-system/argus-publisher-test.png" :width="1252" :height="223" caption="Original ARGUS publisher screenshot from the laptop test." />

<CommunicationFigure number="122" src="/report-assets/communication-system/hunter-receiver-test.png" :width="909" :height="204" caption="Original HUNTER receiver screenshot from Raspberry Pi 5. The log reports Nav2 unavailable, so this shows message reception and goal publication, not completed navigation." />

These tests were successful (shown in the figure above), proving that the ARGUS and HUNTER can exchange structured data over a local wireless network. This served as the baseline foundation for integrating the real-time FOD detection from the vision system with the HUNTER’s autonomous navigation system.

## 5.5 Communication Performance Analysis {#a5-analysis}

### 5.5.1 Communication Performance Evaluation {#performance-evaluation}

<p class="report-table-caption" id="table-63"><strong>Table 63.</strong> Communication Performance Evaluation</p>

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

The 100-message benchmark used ROS 2 Jazzy with the publisher and subscriber on the same device (0 m separation). The C2 alert payload size was measured at 588 bytes, and the estimated application-level bandwidth was 9.408 kbps at two alerts per second. This covers alert payloads only, excluding video and network overhead. Although each alert is only 588 bytes, the link needs extra capacity for network overhead, handshakes, ACKs and resending messages. The live-video target is at least 1080p (1920 × 1080). Video transmission, camera support, frame rate, bandwidth and delay will all be tested after the interim phase. Additionally, a ROS 2 test was conducted using 100 consecutive alerts simulating the C2 alerts at a nominal rate of 10Hz sent from publisher to subscriber. All 100 messages were received successfully hence attaining the 100% delivery rate with no missing or duplicate messages. This checks local ROS 2 message delivery; it does not measure wireless range or performance between separate devices.

## 5.6 Discussion of Future Works {#a6-problems-project-plan}

### 5.6.1 Limitations and Future Works {#future-work}

::: details 5.6.1.1 Long-Range Communication Hardware

- **Current limitation:** The current communication relies on a local Wi-Fi network, which has not been tested for the full runway.
- **Confirm the radio:** Evaluate the preferred pMDDL2450 and antenna setup below 100 mW EIRP for the 2.4 GHz UAV link. Test message delivery and the live feed over the required 5 km range before confirming the final device.
- **Test interference:** Compare message delivery, receipt-acknowledgement delay and live-feed delay on quiet and busy channels, with alerts and video running together at the permitted power.

:::

::: details 5.6.1.2 Vision and Communication Integration

- **Link the scripts:** ARGUS communication scripts are still not linked to the vision system. Integrate with the onboard vision system to automate C2 alerts.

:::

::: details 5.6.1.3 Queue Delivery and Communication-Loss Detection

- **Confirm receipt:** Add a receipt acknowledgement carrying the threat ID.
- **Release the next alert:** Send the next queued alert after the matching receipt acknowledgement returns to ARGUS.
- **Detect missing messages:** Add sequence-number tracking and communication-loss detection.
- **Keep alerts during link loss:** Retain unacknowledged FOD coordinates on ARGUS and resend them when communication returns. Test that valid retries are acknowledged without creating duplicate HUNTER targets.
- **Check the link every second:** Exchange a handshake every second. If no response is received for 10 seconds, inform the base station when its link is available. Keep undelivered coordinates for resending after reconnection. Test link checks separately from FOD receipt ACKs.

:::

::: details 5.6.1.4 Thermal Live-Feed Testing

- **Set and test the video settings:** The live-video target is at least 1080p (1920 × 1080). Video transmission, camera support, frame rate, bandwidth and delay will all be tested after the interim phase.

:::

<span id="message-security-plan" class="report-anchor" aria-hidden="true"></span>

::: details 5.6.1.5 Message Security

- **Enable DDS Security:** Use SROS2 to configure encryption, certificate-based authentication and message-integrity protection. Require secure connections instead of falling back to unsecured operation ([\[75\]](../references#com-s01)).
- **Limit topic access:** Allow only approved nodes to publish FOD targets, receipt acknowledgements and control messages. Restrict subscriptions to authorised recipients.
- **Check old and repeated alerts:** Use mission IDs, threat IDs and timestamps to reject stale alerts and avoid adding the same target twice. Still acknowledge valid retransmissions so the sender can release the next alert.
- **Protect private keys:** Keep private keys out of the shared code repository and restrict access on each device.
- **Test the setup:** Check that unauthorised nodes and incorrect topic permissions are blocked. Test stale alerts and valid retries, and measure any added message delay.

:::

<span id="communication-monitoring-interface" class="report-anchor" aria-hidden="true"></span>

::: details 5.6.1.6 Communication Monitoring Website

Develop a website for operators to view stored FOD coordinates, queue order, receipt acknowledgements, handshake status and error notifications. Connect it to the ARGUS queue, database and ROS 2 messages. Unacknowledged alerts will stay stored for resending after communication loss. Acknowledged records will remain available as delivery history.

The simulator below shows the proposed interface. It uses example records saved in this browser, not a live database or radio connection. Add a FOD, disconnect and restore the HUNTER link, confirm receipt, or simulate 10 seconds without a handshake response. The real interface and its backend are future work.

<CommsDashboardDemo />

:::

<span id="communication-validation-plan" class="report-anchor" aria-hidden="true"></span>

::: details 5.6.1.7 Communication Validation Plan

The final communication device is still to be confirmed. Range, interference and radio video tests need candidate hardware. Queue, ACK, storage and security tests can start using the existing Wi-Fi setup, then be repeated on the final link. The tests below are planned. Undecided performance targets will be set before validation.

<p class="report-table-caption" id="table-64"><strong>Table 64.</strong> Communication Validation Plan</p>

| Test | Planned method | Check or target | Hardware needed |
| --- | --- | --- | --- |
| Alert delivery and ACK timing | Send numbered alerts between two devices and log send, receive and ACK times. | Verify matching FOD receipt ACKs and set the delivery-rate target and acceptable delay. | Start on Wi-Fi, repeat on the radio. |
| Communication-loss recovery | Disconnect HUNTER, add FOD alerts and restore the link. Also test missing ACKs. | Retain coordinates, preserve queue order and avoid duplicate targets. Check the link every second and notify the base station after 10 seconds without a handshake response, if reachable. Verify that a missing FOD ACK alone does not trigger a link-loss notification. | Start on Wi-Fi. |
| Record storage and queue capacity | Restart ARGUS with pending alerts and test the storage limit. | Pending records survive restart. Set queue capacity and define what happens when storage is full. | ARGUS storage and application. |
| Coordinate agreement | Send known coordinates with agreed units, map frame, mission ID and threat ID. | HUNTER receives the same target values and interprets the agreed frame correctly. | Start on Wi-Fi. |
| Radio power configuration | Check applicable IMDA TS SRD conditions, radio settings, antenna gain and cable losses [\[76\]](../references#com-r01). | The proposed 2.4 GHz UAV setup stays below 100 mW EIRP. | Candidate radio and antenna setup. |
| Wireless range | Increase separation towards 5 km and record delivery, delays and dropouts. | Meet the 5 km requirement and the agreed delivery and delay targets. | Candidate radio at the permitted power. |
| Live feed and interference | Run alerts and video together under quiet and busy channel conditions. | Check support for at least 1080p (1920 × 1080). Set the frame rate and acceptable delay, measure bandwidth and check the effect on alert delivery. | Start on Wi-Fi, validate on the radio. |
| Security | Test unauthorised nodes, topic permissions, stale alerts and valid retransmissions. | Block unauthorised access and stale targets. Acknowledge valid retries without creating duplicate targets. | Start on Wi-Fi with DDS Security enabled. |

:::

### 5.6.2 Hunter Group Communication {#hunter-group-communication}

For the HUNTER group's communication report, see [HUNTER Group Communication](https://cde4301-drone-ground-robots.github.io/CDE4301_runway_patrol/report#communications).

</div>
