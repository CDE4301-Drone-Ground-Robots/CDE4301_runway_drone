---
title: Research
outline: [2, 2]
pageClass: research-report-page
aside: false
---

<p class="chapter-kicker">FOD ARGUS / PROJECT REPORT</p>

# Research

## Primary Research

### The Problem

Foreign Object Debris (FOD) poses significant safety and financial risks to the aviation industry, as debris on runways can damage aircraft and disrupt operations. El-Sayed estimates the annual global cost of FOD at US$1.26 billion in direct damage and US$13.9 billion when indirect costs, such as delays and cancellations, are included [\[23\]](../references#research-ref-23). An FAA study estimates costs of up to US$22.7 billion in 2020 dollars [\[22\]](../references#research-ref-22). Although only 15% of FOD is found on runways, it accounts for up to half of all FOD-related damage [\[24\]](../references#research-ref-24).

A notable example is the Air France Flight 4590 accident on 25 July 2000, when a Concorde struck a 435 mm titanium strip left on the runway by a departing Continental Airlines DC-10. The impact caused tyre debris to rupture a fuel tank, resulting in a fire and subsequent crash that killed 113 people [\[25\]](../references#research-ref-25). A scheduled runway inspection had been postponed due to a fire drill [\[26\]](../references#research-ref-26).

<figure class="research-figure">

![Concorde with flames trailing during the Air France Flight 4590 accident](/report-assets/research/concorde-accident.jpeg)

<figcaption>Air France Flight 4590 Concorde accident.</figcaption>
</figure>

The accident prompted greater research into FOD detection and prevention [\[24\]](../references#research-ref-24), establishing runway FOD as a critical aviation safety concern [\[27\]](../references#research-ref-27). However, FOD detection and removal remain largely manual, requiring runway closures while personnel locate and retrieve debris [\[24\]](../references#research-ref-24)[\[27\]](../references#research-ref-27). This labour-intensive process can lead to operational disruptions.

In Singapore, declining manpower poses an additional challenge to labour-intensive operations. With the total fertility rate falling to 1.1 in 2020, MINDEF has identified manpower shortages as a significant concern and emphasised the need for manpower optimisation [\[28\]](../references#research-ref-28).

To address this, MINDEF has begun trialling automated vehicles at SAF air bases and AI-enabled drones for runway damage assessment [\[29\]](../references#research-ref-29). With the SAF projecting a one-third reduction in manpower by 2030 [\[30\]](../references#research-ref-30), automation is becoming increasingly important in maintaining operational efficiency while reducing manpower requirements.

### The Stakeholders Affected by the Problem

Foreign Object Debris (FOD) affects both military and civil aviation in Singapore, primarily involving the Republic of Singapore Air Force (RSAF) and the Civil Aviation Authority of Singapore (CAAS). Similar challenges are faced by airports worldwide, particularly with increasing manpower constraints.

As shown in the Stakeholder power–interest map, the RSAF holds high power and interest as the primary end user and deployment authority. CAAS has high power but lower interest due to existing automated FOD detection systems at Changi Airport. Meanwhile, industry partners and insurers have high interest but limited decision-making authority, while servicemen responsible for FOD clearance have little influence despite being directly involved in operations.

<figure class="research-figure research-stakeholder-map">

![Stakeholder power–interest map showing RSAF, CAAS, industry partners, insurance companies and RSAF servicemen](/report-assets/research/stakeholder-power-interest-map.png)

<figcaption>Stakeholder power–interest map.</figcaption>
</figure>

Based on interviews conducted by the [FOD Hunter Team](https://cde4301-drone-ground-robots.github.io/CDE4301_runway_patrol/report#sec-affected) with various stakeholders, the FOD Argus Team identified several challenges specifically related to FOD detection and the application of UAV technologies.

### Stakeholder Interview Findings Relevant to UAV Detection

The key findings are listed below ([see full transcripts here](../appendices#stakeholder-interview-transcripts)).

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

The stakeholder interviews highlighted several challenges associated with runway FOD detection. Common FOD includes small metallic objects, such as screws and rivets, as well as non-metallic debris, which can be difficult to identify through manual inspection. While existing UAV solutions have been used for runway inspections, they still rely on human visual detection.

Stakeholders also highlighted limitations of vision-based systems, including false detections and reduced visibility under adverse weather conditions. Understanding these limitations allows the team to identify potential challenges and explore ways to address them during the development of the UAV's detection system.

Furthermore, Changi Airport's short inspection windows and strict UAV operating restrictions highlight the challenges of deploying UAV-based FOD detection systems at high-traffic airports. Changi Airport has already implemented the iFerret system, which uses fixed cameras to continuously monitor runways for FOD without disrupting aircraft operations.

## Secondary Research

### FOD Detection at Changi Airport

The team also came across a CNA video which provides further insight into FOD detection at Changi Airport, highlighting the types of debris commonly found on runways, the operation of the iFerret detection system, and how AI has been incorporated to improve its detection capabilities.

<figure class="cv-video-panel research-cna-video">
 <iframe class="cv-integration-video" src="https://www.youtube.com/embed/YigBVMgCgVA" title="CNA video about FOD detection and the iFerret system at Changi Airport" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
 <figcaption><span>CNA video about FOD detection and the iFerret system at Changi Airport. <a href="../references#research-cna-01">[SR-01]</a></span><a href="https://www.youtube.com/watch?v=YigBVMgCgVA" target="_blank" rel="noopener noreferrer">Watch the CNA video on YouTube</a></figcaption>
</figure>

**Table: Key Insights from CNA Video**

<div class="research-secondary-table" role="region" aria-label="Key insights from CNA video" tabindex="0">

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

### Problem Statement and Scope

Based on the insights gathered from our primary and secondary research, the team identified the following problem. RSAF air bases rely on servicemen walking or driving along runways to detect and remove Foreign Object Debris (FOD). This process is manpower-intensive, lacks a systematic method of ensuring thorough coverage, and often misses small objects that can cause significant aircraft damage. These challenges are further compounded by Singapore's declining manpower availability.

The project focuses on airports and air bases with low to medium air traffic, such as military air bases in Singapore. High-traffic commercial airports like Changi Airport are currently excluded from the project's scope due to their short runway inspection windows, strict UAV operating restrictions and existing automated FOD detection systems. Within this scope, the project aims to demonstrate how a UAV and an unmanned ground vehicle (UGV) can work together to autonomously detect, locate and remove small FOD from a section of runway, reducing the need for manual intervention.
