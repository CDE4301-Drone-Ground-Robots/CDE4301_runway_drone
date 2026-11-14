---
title: Research
outline: [2, 2]
pageClass: research-report-page
aside: false
---

<script setup>
import { withBase } from 'vitepress'
</script>

<p class="chapter-kicker">FOD ARGUS / PROJECT REPORT</p>

# Research

## Primary Research

### The Problem

Foreign Object Debris (FOD) poses significant safety and financial risks to the aviation industry, as debris on runways can damage aircraft and disrupt operations. El-Sayed estimates the annual global cost of FOD at US$1.26 billion in direct damage and US$13.9 billion when indirect costs, such as delays and cancellations, are included [\[1\]](../references#research-ref-23). An FAA study estimates costs of up to US$22.7 billion in 2020 dollars [\[2\]](../references#research-ref-22). Although only 15% of FOD is found on runways, it accounts for up to half of all FOD-related damage [\[3\]](../references#research-ref-24).

A notable example is the Air France Flight 4590 accident on 25 July 2000, when a Concorde struck a 435 mm titanium strip left on the runway by a departing Continental Airlines DC-10. The impact caused tyre debris to rupture a fuel tank, resulting in a fire and subsequent crash that killed 113 people [\[4\]](../references#research-ref-25). A scheduled runway inspection had been postponed due to a fire drill [\[5\]](../references#research-ref-26).

<figure class="research-figure">

![Concorde with flames trailing during the Air France Flight 4590 accident](/report-assets/research/concorde-accident.jpeg)

<figcaption><strong>Fig. 1.</strong> Air France Flight 4590 Concorde accident.</figcaption>
</figure>

The accident prompted greater research into FOD detection and prevention [\[3\]](../references#research-ref-24), establishing runway FOD as a critical aviation safety concern [\[6\]](../references#research-ref-27). However, FOD detection and removal remain largely manual, requiring runway closures while personnel locate and retrieve debris [\[3\]](../references#research-ref-24), [\[6\]](../references#research-ref-27). This labour-intensive process can lead to operational disruptions.

In Singapore, declining manpower poses an additional challenge to labour-intensive operations. With the total fertility rate falling to 1.1 in 2020, MINDEF has identified manpower shortages as a significant concern and emphasised the need for manpower optimisation [\[7\]](../references#research-ref-28).

To address this, MINDEF has begun trialling automated vehicles at SAF air bases and AI-enabled drones for runway damage assessment [\[8\]](../references#research-ref-29). With the SAF projecting a one-third reduction in manpower by 2030 [\[9\]](../references#research-ref-30), automation is becoming increasingly important in maintaining operational efficiency while reducing manpower requirements.

### The Stakeholders Affected by the Problem

Foreign Object Debris (FOD) affects both military and civil aviation in Singapore, primarily involving the Republic of Singapore Air Force (RSAF) and the Civil Aviation Authority of Singapore (CAAS). Similar challenges are faced by airports worldwide, particularly with increasing manpower constraints.

As shown in the Stakeholder power–interest map, the RSAF holds high power and interest as the primary end user and deployment authority. CAAS has high power but lower interest due to existing automated FOD detection systems at Changi Airport. Meanwhile, industry partners and insurers have high interest but limited decision-making authority, while servicemen responsible for FOD clearance have little influence despite being directly involved in operations.

<figure class="research-figure research-stakeholder-map">

![Stakeholder power–interest map showing RSAF, CAAS, industry partners, insurance companies and RSAF servicemen](/report-assets/research/stakeholder-power-interest-map.png)

<figcaption><strong>Fig. 2.</strong> Stakeholder power–interest map.</figcaption>
</figure>

Based on interviews conducted by the [FOD Hunter Team](https://cde4301-drone-ground-robots.github.io/CDE4301_runway_patrol/report#sec-affected) with various stakeholders, the FOD Argus Team identified some key insights that could help develop our FOD Argus solution.

### Stakeholder Interview Findings Relevant to UAV Detection

The FOD Argus Team categorised the primary research findings into six key areas relevant to UAV detection and scanning. The findings and their corresponding insights are summarised in the table below ([see full transcripts here](../appendices#stakeholder-interview-transcripts)).

<ul class="research-interview-legend" aria-label="Interview insight categories">
<li class="insight-fod">Types and characteristics of FOD</li>
<li class="insight-manual">Limitations of manual inspection</li>
<li class="insight-operations">Operational constraints at Changi Airport</li>
<li class="insight-vision">Limitations of vision-based detection</li>
<li class="insight-uav">Existing UAV/Detection Solutions</li>
<li class="insight-frequency">Current Inspection Frequency</li>
</ul>

<div class="research-interview-table" role="region" aria-label="Stakeholder interview findings relevant to UAV detection" tabindex="0">
<table>
<caption class="report-table-caption"><strong>Table 1.</strong> Stakeholder Interview Findings Relevant to UAV Detection</caption>
<thead><tr><th scope="col">Stakeholder</th><th scope="col">What They Said</th><th scope="col">Key Insight</th></tr></thead>
<tbody>
<tr class="insight-fod"><th scope="rowgroup" rowspan="3"><a href="../appendices#appendix-a">Industry partner</a><span class="interview-date">10 September 2026</span></th><td class="interview-quote"><q>On that day, it's a small metal piece, about 2 cm.</q></td><td><span class="insight-category">Types and characteristics of FOD</span>The UAV should be capable of detecting small FOD, such as metal debris approximately 2 cm in size.</td></tr>
<tr class="insight-manual"><td class="interview-quote"><q>That's how they inspect. And there's no fixed route around the runway. It's pretty random; they go left, right, center.</q></td><td><span class="insight-category">Limitations of manual inspection</span>A systematic UAV scanning route can improve runway coverage and reduce the likelihood of missing FOD.</td></tr>
<tr class="insight-frequency"><td class="interview-quote"><q>Three times a day.</q></td><td><span class="insight-category">Current Inspection Frequency</span>RSAF runway inspections were reported to take place three times daily, following a scheduled inspection routine.</td></tr>
</tbody>
<tbody>
<tr class="insight-fod"><th scope="rowgroup" rowspan="3"><a href="../appendices#appendix-b">RSAF technician, Paya Lebar Air Base</a><span class="interview-date">16 September 2026</span></th><td class="interview-quote"><q>So, uh, screws, rivets. Screws, rivets are quite common. Uh, rocks from the... Rocks, screws, rivets.</q></td><td><span class="insight-category">Types and characteristics of FOD</span>The detection system should be able to identify common FOD such as screws, rivets and loose pavement debris.</td></tr>
<tr class="insight-manual"><td class="interview-quote"><q>I can't, I can't specify how long, it's ballpark of 4 kilometers, but it's around there. Walk and broom. Walk and broom.</q></td><td><span class="insight-category">Limitations of manual inspection</span>Automated UAV scanning could reduce the manpower and time required for runway inspections.</td></tr>
<tr class="insight-manual"><td class="interview-quote"><q>No, it's the smaller pieces which we need help with, because the big, the big sweeper does not pick up the small pieces. It will always miss the small pieces.</q></td><td><span class="insight-category">Limitations of manual inspection</span>Small FOD can remain undetected after conventional sweeping, highlighting the need for more reliable detection.</td></tr>
</tbody>
<tbody>
<tr class="insight-uav"><th scope="rowgroup" rowspan="1"><a href="../appendices#appendix-c">RSAF air traffic controller, Tengah Air Base</a><span class="interview-date">16 September 2026</span></th><td class="interview-quote"><q>Yeah, so the drone has a set course plotted already. So, you just take off from the tower, then it goes up and down the runway to get everything. You have to see visually. There's no indicators that pop up.</q></td><td><span class="insight-category">Existing UAV/Detection Solutions</span>Existing UAV inspections rely on manual visual detection, creating an opportunity for automated FOD identification and localisation.</td></tr>
</tbody>
<tbody>
<tr class="insight-fod"><th scope="rowgroup" rowspan="10"><a href="../appendices#appendix-d">CAAS officer</a><span class="interview-date">28 September 2026</span></th><td class="interview-quote"><q>We get bolts and nuts quite often. Get cloth, plastics, paper.</q></td><td><span class="insight-category">Types and characteristics of FOD</span>The detection system must account for different FOD materials, sizes and appearances.</td></tr>
<tr class="insight-operations"><td class="interview-quote"><q>Even today, the time that we are given to enter the runway to do a 4 km run, followed by I mean, 60 m wide, to just check for any pavement anomalies, right, is 5 minutes.</q></td><td><span class="insight-category">Operational constraints at Changi Airport</span>The short runway inspection window highlights Changi Airport's high traffic volume and the importance of minimising disruptions to flight operations.</td></tr>
<tr class="insight-frequency"><td class="interview-quote"><q>So, we have that about I think five times a day.</q></td><td><span class="insight-category">Current Inspection Frequency</span>Changi Airport conducts approximately five scheduled runway inspections daily, in addition to its continuous automated FOD monitoring.</td></tr>
<tr class="insight-vision"><td class="interview-quote"><q>In order not to disrupt operations, we still need a human eye to validate, is this a bird, or no, it's just a shadow?</q></td><td><span class="insight-category">Limitations of vision-based detection</span>Shadows can trigger false detections, highlighting the importance of minimising false positives.</td></tr>
<tr class="insight-vision"><td class="interview-quote"><q>Imagine one day the haze is so bad, I I wonder whether my iFerret can work if it's vision-based.</q></td><td><span class="insight-category">Limitations of vision-based detection</span>Poor visibility, such as haze, may reduce the effectiveness of camera-based FOD detection.</td></tr>
<tr class="insight-vision"><td class="interview-quote"><q>We had the same bird that flew from one spot to another spot, and that and then from that spot flew to another spot, and we keep capturing that one bird, but maybe I I would get alerted 10 times.</q></td><td><span class="insight-category">Limitations of vision-based detection</span>Repeated detection of the same object can generate unnecessary alerts, increasing the need for reliable object tracking.</td></tr>
<tr class="insight-operations"><td class="interview-quote"><q>Drones are only flown when the runway is closed.</q></td><td><span class="insight-category">Operational constraints at Changi Airport</span>UAV operations at Changi Airport are restricted to periods when the runway is closed to aircraft traffic, limiting opportunities for deployment.</td></tr>
<tr class="insight-uav"><td class="interview-quote"><q>They are fixed cameras located at two sides, parallel to the runway, um scanning the runway 24/7 to identify what we call objects, or obstacles, or anything, lah. ... So, it is forever scanning, and the runway is open. That means the runway is operational. Aircraft is taking off, he's still scanning.</q></td><td><span class="insight-category">Existing UAV/Detection Solutions</span>Changi Airport uses fixed cameras to continuously monitor its runways for FOD without interrupting aircraft operations.</td></tr>
<tr class="insight-uav"><td class="interview-quote"><q>The FOD detection system detects the FOD. It sends a notification to an operator. So, we do have an operator sitting in front of a screen, validating whether this is a true FOD or a false alarm. ... But if it is indeed like a dead bird, and it's very clear it's a dead bird, then what the operator now will do is he will straightaway uh activate what we call the the ground rovers.</q></td><td><span class="insight-category">Existing UAV/Detection Solutions</span>iFerret automates initial FOD detection, while human operators verify alerts before retrieval.</td></tr>
<tr class="insight-uav"><td class="interview-quote"><q>Because by installing, or rather by investing, by investing in iFerret, we effectively shaved off a lot of time that we need to be on the runway, and every minute is money. ... And then I can allow more landings and I take more traffic.</q></td><td><span class="insight-category">Existing UAV/Detection Solutions</span>Automated FOD detection has reduced the need for manual runway inspections and minimised operational disruptions.</td></tr>
</tbody>
</table>
</div>

The stakeholder interviews highlighted several challenges associated with runway FOD detection. Common FOD includes small metallic objects as small as 2 cm, such as screws and rivets, as well as non-metallic debris, which can be difficult to identify through manual inspection. While existing UAV solutions have been used for runway inspections, they still rely on human visual detection.

Stakeholders also highlighted limitations of vision-based systems, including false detections and reduced visibility under adverse weather conditions. Understanding these limitations allows the team to identify potential challenges and explore ways to address them during the development of the UAV's detection system.

Furthermore, Changi Airport's short inspection windows and strict UAV operating restrictions highlight the challenges of deploying UAV-based FOD detection systems at high-traffic airports. Changi Airport has already implemented the iFerret system, which uses fixed cameras to continuously monitor runways for FOD without disrupting aircraft operations.

## Secondary Research

### FOD Detection at Changi Airport

The team also came across a CNA video which provides further insight into FOD detection at Changi Airport, highlighting the types of debris commonly found on runways, the operation of the iFerret detection system, and how AI has been incorporated to improve its detection capabilities.

<figure class="cv-video-panel research-cna-video">
 <iframe class="cv-integration-video" src="https://www.youtube.com/embed/YigBVMgCgVA" title="CNA video about FOD detection and the iFerret system at Changi Airport" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
 <figcaption><span>CNA video about FOD detection and the iFerret system at Changi Airport. <a href="../references#research-cna-01">[10]</a></span><a href="https://www.youtube.com/watch?v=YigBVMgCgVA" target="_blank" rel="noopener noreferrer">Watch the CNA video on YouTube</a></figcaption>
</figure>


<div class="research-secondary-table" role="region" aria-label="Key insights from CNA video" tabindex="0">

<p class="report-table-caption" id="table-2"><strong>Table 2.</strong> Key Insights from the CNA Video</p>

| Area | Findings from the Video |
| --- | --- |
| Types of FOD | Common debris includes speed tape, cloth, small stones, screws and nuts. |
| iFerret detection capability | Fixed high-definition cameras continuously monitor the runways and can reportedly detect objects as small as 4 cm. |
| AI-based detection | AI was introduced in 2021 to improve object identification, adapt to changing lighting conditions and reduce false alerts by approximately 90%. |
| Operational efficiency | iFerret allows FOD detection while runways remain operational, with retrieval typically taking 1–5 minutes. |
| Human verification | Operators verify detected objects before dispatching personnel for retrieval. |

</div>

The CNA video provides further insight into FOD detection at Changi Airport, supporting findings from the primary research regarding common FOD types and the implementation of the iFerret system. The video also highlights how iFerret has incorporated AI-based detection to improve accuracy and reduce false alarms, further strengthening its effectiveness in a high-traffic airport like Changi.

With such a robust detection system already in place, implementing the team's UAV solution at Changi Airport would be challenging, particularly given the airport's strict operational constraints. These findings give us a clearer picture of where the FOD Argus UAV could provide greater value, particularly at airports or air bases with low to medium air traffic, where automated FOD detection infrastructure may be less extensive and UAV deployment could be more feasible.

### Existing Detection Technologies

In addition to iFerret 2.0, several existing FOD detection technologies were reviewed to understand their operating principles and limitations. Table 3 provides a comparison of these systems.

<div class="research-secondary-table research-detection-table" role="region" aria-label="Comparison of existing FOD detection technologies" tabindex="0">
<table>
<caption class="report-table-caption"><strong>Table 3.</strong> Comparison of Existing FOD Detection Technologies</caption>
<thead><tr><th scope="col">Image</th><th scope="col">System</th><th scope="col">How it works</th><th scope="col">Shortcomings</th></tr></thead>
<tbody>
<tr><td><figure class="report-inline-figure"><img src="/report-assets/research/qinetiq-tarsier.jpeg" alt="QinetiQ Tarsier detection system" loading="lazy" /><figcaption><strong>Fig. 3.</strong> QinetiQ Tarsier detection system</figcaption></figure></td><th scope="row">QinetiQ Tarsier</th><td>Stationary radar detects; a camera pans to confirm <a href="../references#research-ref-31">[11]</a></td><td>Radar cannot classify FOD and is sensitive to ground clutter</td></tr>
<tr><td><figure class="report-inline-figure"><img src="/report-assets/research/xsight-fodetect-runwize.jpeg" alt="Xsight FODetect and RunWize detection system" loading="lazy" /><figcaption><strong>Fig. 4.</strong> Xsight FODetect and RunWize detection system</figcaption></figure></td><th scope="row">Xsight FODetect and RunWize</th><td>Radar and optical sensors mounted along the runway edge lights, with laser illumination <a href="../references#research-ref-31">[11]</a></td><td>Hardware-intensive deployment along the full runway</td></tr>
<tr><td><figure class="report-inline-figure"><img src="/report-assets/research/iferret-2-changi.jpeg" alt="iFerret 2.0 detection system at Changi" loading="lazy" /><figcaption><strong>Fig. 5.</strong> iFerret 2.0 detection system at Changi</figcaption></figure></td><th scope="row">iFerret 2.0 (Changi)</th><td>Fixed AI-powered cameras detect and verify FOD visually <a href="../references#research-ref-31">[11]</a></td><td>Vision-based detection may be less reliable under poor visibility conditions, highlighting the need for supplementary sensing technologies (see <a href="../appendices#appendix-d">Appendix D</a>).</td></tr>
<tr><td><figure class="report-inline-figure"><img src="/report-assets/research/elva-1.jpeg" alt="ELVA-1 detection system" loading="lazy" /><figcaption><strong>Fig. 6.</strong> ELVA-1 detection system</figcaption></figure></td><th scope="row">ELVA-1</th><td>Stationary radar</td><td>Long scan time of about 3 minutes</td></tr>
<tr><td><figure class="report-inline-figure"><img src="/report-assets/research/trex-fod-finder-xm.jpeg" alt="Trex FOD Finder XM vehicle-mounted detection system" loading="lazy" /><figcaption><strong>Fig. 7.</strong> Trex FOD Finder XM vehicle-mounted detection system</figcaption></figure></td><th scope="row">Trex FOD Finder XM</th><td>Radar mounted on a vehicle <a href="../references#research-ref-31">[11]</a></td><td>Intermittent scanning; needs a driver at all times</td></tr>
</tbody>
</table>
</div>

The existing technologies reviewed demonstrate that FOD detection is relatively established, with various systems employing radar, optical sensors and AI-powered cameras. However, these systems have limitations, and furthermore, detection alone does not eliminate the need for human intervention in FOD removal, which is the core issue the team is trying to tackle. Therefore, FOD detection using a UAV alone is not a particularly novel solution. To address this gap, our proposed solution integrates FOD Argus, a UAV responsible for detecting and locating FOD, with FOD Hunter, an autonomous ground rover responsible for navigating to and collecting the detected objects.

Integrated detection and collection solutions are also emerging. One example is Roboxi, a Norwegian multifunctional airside robot designed to detect and collect FOD while also inspecting runway pavement and lighting. The system began a four-month trial at Berlin Brandenburg Airport in 2026 [\[12\]](../references#research-ref-32), [\[13\]](../references#research-ref-33). However, its cost has not been publicly disclosed, and independent performance data on its FOD detection and removal capabilities remain limited. This further demonstrates that autonomous FOD detection and collection is an emerging field, with opportunities for further development and improvement.

### Problem Statement and Scope

Based on the insights gathered from our primary and secondary research, the team identified the following problem. RSAF air bases rely on servicemen walking or driving along runways to detect and remove Foreign Object Debris (FOD). This process is manpower-intensive, lacks a systematic method of ensuring thorough coverage, and often misses small objects that can cause significant aircraft damage. These challenges are further compounded by Singapore's declining manpower availability.

The project focuses on airports and air bases with low to medium air traffic, such as military air bases in Singapore. High-traffic commercial airports like Changi Airport are currently excluded from the project's scope due to their short runway inspection windows, strict UAV operating restrictions and existing automated FOD detection systems. Within this scope, the project aims to demonstrate how a UAV and an unmanned ground vehicle (UGV) can work together to autonomously detect, locate and remove small FOD from a section of runway, reducing the need for manual intervention.

### Multi-Robot Approach

A multi-robot approach was adopted to overcome the limitations of using a single robot for both FOD detection and collection. While FOD Argus can efficiently survey large runway areas from the air, it cannot physically remove debris. Conversely, FOD Hunter can collect FOD but requires more time to cover the same area. By combining both systems, FOD Argus can identify and relay FOD locations to FOD Hunter, allowing the ground rover to navigate directly to detected objects rather than scanning the entire runway.

This approach is further supported by research conducted by Öztürk and Kuzucuoğlu [\[3\]](../references#research-ref-24), which demonstrated the potential efficiency of multi-robot systems, with coordinated robots completing FOD collection faster than a conventional manual vehicle in simulation. However, the cost benefits depend on operational conditions, particularly runway closure costs and usage frequency.

A more detailed analysis of multi-robot coordination, operational efficiency and cost considerations is presented in the [FOD Hunter report – Why a Multi-Robot Approach](https://cde4301-drone-ground-robots.github.io/CDE4301_runway_patrol/report#sec-multirobot).

### User Journey and Demonstration

<figure class="research-figure research-journey-illustration">

![Six-panel operational journey showing runway debris, FOD Argus scanning, data transmission, FOD Hunter navigation and pickup, and both robots returning to base](/report-assets/research/user-journey.png)

<figcaption>FOD Argus and FOD Hunter operational journey.</figcaption>
</figure>

<div class="research-journey-flow" role="group" aria-label="Six-step operational flowchart">
  <div class="research-journey-step">
    <h4>Step 1: FOD on the runway</h4>
    <p>Bolts, nuts, screws, stones and dead birds lie on the runway, posing a risk to aircraft.</p>
  </div>
  <div class="research-journey-arrow" aria-hidden="true">↓</div>
  <div class="research-journey-step">
    <h4>Step 2: Aerial scanning</h4>
    <p>FOD Argus flies a pre-planned path during a scheduled inspection or closure window and flags candidate FOD with its location.</p>
  </div>
  <div class="research-journey-arrow" aria-hidden="true">↓</div>
  <div class="research-journey-step">
    <h4>Step 3: Data transmission</h4>
    <p>FOD Argus sends the detected locations to the ground station, where the operator confirms each flag and filters false positives.</p>
  </div>
  <div class="research-journey-arrow" aria-hidden="true">↓</div>
  <div class="research-journey-step">
    <h4>Step 4: Ground navigation</h4>
    <p>FOD Hunter travels to each confirmed location and verifies the target using its onboard sensors.</p>
  </div>
  <div class="research-journey-arrow" aria-hidden="true">↓</div>
  <div class="research-journey-step">
    <h4>Step 5: Pickup</h4>
    <p>FOD Hunter removes the item using the sweep box and vacuum.</p>
  </div>
  <div class="research-journey-arrow" aria-hidden="true">↓</div>
  <div class="research-journey-step">
    <h4>Step 6: Return to home</h4>
    <p>FOD Hunter returns to base, and FOD Argus lands on top. Each item is logged with its location and time.</p>
  </div>
</div>

The video below is a simulation demonstrating the coordination between the FOD Argus and FOD Hunter.

<figure class="research-figure research-journey-video">
  <video controls playsinline preload="metadata" :src="withBase('/report-assets/research/user-journey-simulation.mp4')" aria-label="Simulation of FOD Argus and FOD Hunter coordination">
    Your browser does not support embedded video. <a :href="withBase('/report-assets/research/user-journey-simulation.mp4')">Open the simulation video</a>.
  </video>
  <figcaption>Simulation of coordination between FOD Argus and FOD Hunter.</figcaption>
</figure>

### Value Proposition {#value-proposition}

The value proposition of FOD Argus and FOD Hunter lies in their ability to support a more efficient and systematic approach to runway FOD detection. Based on the findings from primary and secondary research, several key stakeholder needs were identified, including reducing manual inspection requirements, improving FOD detection and ensuring repeatable runway coverage.

By integrating AI-assisted aerial detection using FOD Argus with autonomous ground-based collection through FOD Hunter, the proposed system aims to address these needs while reducing reliance on conventional manual inspection and removal processes. The relationship between the identified stakeholder needs, existing challenges and proposed capabilities of FOD Argus and FOD Hunter is summarised in the following table.

#### Stakeholder Needs–Solution Matrix

<div class="research-value-table research-needs-table" role="region" aria-label="Stakeholder Needs–Solution Matrix" tabindex="0">
<table>
<caption>Table 4: Stakeholder Needs–Solution Matrix</caption>
<colgroup><col style="width:17%"><col style="width:23%"><col style="width:20%"><col style="width:22%"><col style="width:18%"></colgroup>
<thead><tr><th scope="col">Stakeholder need</th><th scope="col">Existing challenge</th><th scope="col">FOD Argus contribution</th><th scope="col">FOD Hunter contribution</th><th scope="col">Expected benefit</th></tr></thead>
<tbody>
<tr><th scope="row">Reduce manpower requirements</th><td>Current FOD inspection and clearance processes are labour-intensive</td><td>Conducts autonomous aerial runway scanning</td><td>Performs autonomous debris collection at identified locations</td><td>Reduced manpower required for runway FOD operations</td></tr>
<tr><th scope="row">Improve FOD detection</th><td>Small FOD items may be overlooked during manual or conventional inspection</td><td>Detects candidate FOD using AI-assisted aerial sensing</td><td>Verifies the detected object at close range prior to removal</td><td>Improved likelihood of identifying and addressing FOD</td></tr>
<tr><th scope="row">Ensure repeatable inspections</th><td>Manual inspection patterns may vary between runs</td><td>Follows pre-planned flight paths for consistent coverage</td><td>Navigates to confirmed locations based on transmitted coordinates</td><td>More repeatable and systematic inspection coverage</td></tr>
<tr><th scope="row">Improve inspection efficiency</th><td>Ground-based inspection and search can be time-consuming</td><td>Rapid aerial scanning and localisation of candidate FOD</td><td>Targeted travel to confirmed locations and direct removal</td><td>Faster and more focused inspection and collection workflow</td></tr>
<tr><th scope="row">Support safe runway operations</th><td>Runway debris creates hazards to aircraft during take-off and landing</td><td>Identifies potential hazards on the runway surface</td><td>Removes debris from the runway environment</td><td>Enhanced runway safety</td></tr>
</tbody>
</table>
</div>

#### Quality Function Deployment (QFD)

This simplified QFD relationship matrix maps the five stakeholder needs to the proposed technical capabilities of FOD Argus and FOD Hunter.

<div class="research-value-table research-qfd-table" role="region" aria-label="Quality Function Deployment relationship matrix" tabindex="0">
<table aria-describedby="qfd-legend qfd-note">
<caption>Table 5: Quality Function Deployment (QFD) Relationship Matrix</caption>
<colgroup><col style="width:28%"><col style="width:22%"><col style="width:16%"><col style="width:16%"><col style="width:18%"></colgroup>
<thead><tr><th scope="col">Stakeholder requirement</th><th scope="col">AI FOD Detection from Argus</th><th scope="col">Pre-planned flight</th><th scope="col">FOD geolocation</th><th scope="col">FOD Hunter Integration</th></tr></thead>
<tbody>
<tr><th scope="row">Reduce manual inspection</th><td class="qfd-strong"><span role="img" aria-label="Strong relationship">●</span></td><td class="qfd-strong"><span role="img" aria-label="Strong relationship">●</span></td><td class="qfd-supporting"><span role="img" aria-label="Supporting relationship">○</span></td><td class="qfd-strong"><span role="img" aria-label="Strong relationship">●</span></td></tr>
<tr><th scope="row">Improve detection capability</th><td class="qfd-strong"><span role="img" aria-label="Strong relationship">●</span></td><td class="qfd-supporting"><span role="img" aria-label="Supporting relationship">○</span></td><td class="qfd-supporting"><span role="img" aria-label="Supporting relationship">○</span></td><td class="qfd-supporting"><span role="img" aria-label="Supporting relationship">○</span></td></tr>
<tr><th scope="row">Repeatable runway coverage</th><td class="qfd-supporting"><span role="img" aria-label="Supporting relationship">○</span></td><td class="qfd-strong"><span role="img" aria-label="Strong relationship">●</span></td><td class="qfd-supporting"><span role="img" aria-label="Supporting relationship">○</span></td><td class="qfd-none"><span role="img" aria-label="No direct relationship">—</span></td></tr>
<tr><th scope="row">Faster targeted collection</th><td class="qfd-supporting"><span role="img" aria-label="Supporting relationship">○</span></td><td class="qfd-supporting"><span role="img" aria-label="Supporting relationship">○</span></td><td class="qfd-strong"><span role="img" aria-label="Strong relationship">●</span></td><td class="qfd-strong"><span role="img" aria-label="Strong relationship">●</span></td></tr>
<tr><th scope="row">Traceable detection records</th><td class="qfd-supporting"><span role="img" aria-label="Supporting relationship">○</span></td><td class="qfd-supporting"><span role="img" aria-label="Supporting relationship">○</span></td><td class="qfd-strong"><span role="img" aria-label="Strong relationship">●</span></td><td class="qfd-supporting"><span role="img" aria-label="Supporting relationship">○</span></td></tr>
</tbody>
</table>
</div>

<ul id="qfd-legend" class="research-qfd-legend" aria-label="QFD relationship legend">
<li><span class="qfd-strong" aria-hidden="true">●</span> Strong relationship</li>
<li><span class="qfd-supporting" aria-hidden="true">○</span> Supporting relationship</li>
<li><span class="qfd-none" aria-hidden="true">—</span> No direct relationship</li>
</ul>

<p id="qfd-note" class="research-qfd-note">The relationships represent qualitative assessments and have not been validated through quantitative QFD scoring.</p>
