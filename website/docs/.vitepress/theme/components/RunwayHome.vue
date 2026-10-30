<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { withBase } from 'vitepress'
import DroneModel from './DroneModel.vue'
const root = ref<HTMLElement>()
let observer: IntersectionObserver | undefined
onMounted(() => {
 observer = new IntersectionObserver(entries => entries.forEach(entry => {
  if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer?.unobserve(entry.target) }
 }), { threshold: 0.12 })
 root.value?.querySelectorAll('.reveal').forEach(el => observer?.observe(el))
})
onUnmounted(() => observer?.disconnect())
</script>
<template>
<div ref="root" class="runway-home">
 <section class="hero" aria-labelledby="hero-title">
  <div class="hero-runway" :style="{ backgroundImage: 'url(' + withBase('/runway-night-photo.png') + ')' }" aria-hidden="true"></div>
  <div class="hero-copy">
   <p class="eyebrow"><span class="status-dot"></span> NUS CDE4301 <span class="eyebrow-divider">/</span> FINAL YEAR PROJECT</p>
   <h1 id="hero-title"><span class="hero-wordmark">FOD ARGUS.</span></h1>
   <div class="hero-actions"><a class="pill primary" :href="withBase('/report/')">Read the report <span aria-hidden="true">&#8599;</span></a><a class="text-link" href="#acknowledgements">Acknowledgements &amp; Summary <span aria-hidden="true">&#8595;</span></a></div>
  </div>
  <div class="aircraft-scene model-scene"><DroneModel /></div>
  <div class="hero-bottom"><span>INNOVATION & DESIGN PROGRAMME</span><a href="#mission">SCROLL TO DISCOVER <span aria-hidden="true">↓</span></a><span>01 / OVERVIEW</span></div>
 </section>
 <section id="acknowledgements" class="mission section-pad" aria-labelledby="acknowledgements-title">
  <div class="section-top reveal"><span class="eyebrow">01 / ACKNOWLEDGEMENTS</span><span class="small-note">The people behind the project.</span></div>
  <div class="mission-layout reveal">
   <h2 id="acknowledgements-title">Acknowledgements</h2>
   <div>
    <p>Developing FOD ARGUS through the NUS Innovation and Design Programme has challenged our team to turn classroom knowledge into an integrated aerial inspection system. Working across flight, sensing, computing, and communication has required us to learn beyond our individual specialisations. Our progress this semester reflects a shared willingness to experiment, work through setbacks, and support one another.</p>
    <p>We are grateful to the following individuals and groups for their contributions:</p>
    <p><strong>Dr Mark De Lessio and Dr Tang Kok Zuea</strong>, for their supervision, technical direction, and continued guidance. Their engagement with stakeholders helped connect our design decisions to operational needs. We also appreciate their efforts to explore a potential Memorandum of Understanding between the Republic of Singapore Air Force and NUS iDP, creating opportunities for future student projects to address practical challenges.</p>
    <p><strong>Ms Annie Tan</strong>, for her encouragement and practical guidance during our work in the electronics workshop.</p>
    <p><strong>The National Servicemen who spoke with us</strong>, for sharing their experiences of runway operations and FOD clearance. Their accounts helped us understand the demands of manual inspection and informed our approach to aerial detection and coordination with the ground robot.</p>
    <p><strong>Ms Cindy Koh, representative from the Civil Aviation Authority of Singapore (CAAS)</strong>, for sharing her perspective on the aviation sector and helping us understand the operational constraints relevant to our design.</p>
   </div>
  </div>
 </section>
 <section id="executive-summary" class="system section-pad" aria-labelledby="executive-summary-title">
  <div class="section-top reveal"><span class="eyebrow">02 / EXECUTIVE SUMMARY</span><span class="small-note">The project at a glance.</span></div>
  <div class="mission-layout reveal">
   <h2 id="executive-summary-title">Executive Summary</h2>
   <div>
    <p>Runway inspection and Foreign Object Debris (FOD) clearance place significant demands on personnel and airport operations. Introduced to this challenge by industry partner Mr Harry Lim of IO Inspire, our team explored how aerial inspection could support an automated response. Stakeholder interviews informed the proposed approach and highlighted the need to assess its technical feasibility and potential value for airports with low to moderate traffic.</p>
    <p>FOD ARGUS forms the aerial inspection component of the FOD Hunter &times; FOD ARGUS system. The UAV is intended to survey runway surfaces, detect debris, estimate its position, and transmit detection information to FOD Hunter, the ground robot responsible for collection. This division of responsibilities connects aerial observation with ground-based removal.</p>
    <p>The ARGUS design brings together five subsystems: mechanical design, electrical design, navigation and obstacle avoidance, computer vision, and communication. The vision pipeline combines anomaly detection with object detection and surface-crack segmentation to investigate runway hazards, including debris that may not be represented in the training data. Image-based localisation and the proposed UAV-to-UGV communication interface support the transfer of actionable coordinates.</p>
    <p>This report documents the design rationale, subsystem development, and available testing evidence for FOD ARGUS. It also identifies integration challenges, future work, and development priorities for AY2026/27 Semesters 1 and 2. Evaluation through a scaled prototype and controlled testing is intended to establish the capabilities and limitations of the proposed inspection workflow.</p>
    <p>Engagement with the Republic of Singapore Air Force has opened discussions with a potential end user. A site visit and opportunities to test FOD ARGUS alongside FOD Hunter are being pursued to inform further development under representative operating conditions.</p>
    <a class="inline-link" :href="withBase('/report/')">Read the engineering report <span aria-hidden="true">&#8599;</span></a>
   </div>
  </div>
 </section>
 <section id="mission" class="mission section-pad">
  <div class="section-top reveal"><span class="eyebrow">03 / THE MISSION</span><span class="small-note">Small objects. Significant consequences.</span></div>
  <div class="mission-layout reveal"><h2>Every detail matters.<br><span>Especially on a runway.</span></h2><div><p>A loose bolt. A fragment of rubber. Foreign object debris can pose a serious hazard to aircraft. Finding it is an engineering challenge worth looking at from above.</p><p class="muted">Our project investigates whether a UAV-based vision system can make runway inspection more flexible — through a scaled prototype, controlled testing, and a practical feasibility study.</p><a class="inline-link" href="#system">Understand the challenge <span aria-hidden="true">↗</span></a></div></div>
  <div class="principles reveal"><div><span class="metric-index">01</span><strong>Detect.</strong><p>Find representative FOD with a vision-based pipeline.</p></div><div><span class="metric-index">02</span><strong>Localise.</strong><p>Estimate object coordinates from captured imagery.</p></div><div><span class="metric-index">03</span><strong>Connect.</strong><p>Communicate detections to a ground robot.</p></div></div>
 </section>
 <section id="system" class="system section-pad">
  <div class="section-top reveal"><span class="eyebrow">04 / AN INTEGRATED APPROACH</span><span class="small-note">From observation to actionable coordinates.</span></div>
  <div class="system-heading reveal"><h2>One mission.<br><span>A connected system.</span></h2><p>Aerial imaging meets onboard intelligence.<br>Explore the proposed inspection workflow.</p></div>
  <div class="pipeline reveal"><div><span class="pipeline-icon">⌁</span><small>01 / CAPTURE</small><h3>See the surface.</h3><p>RGB imagery, with thermal and LED-assisted inspection under investigation.</p></div><span class="pipeline-arrow" aria-hidden="true">→</span><div><span class="pipeline-icon">⌖</span><small>02 / PROCESS</small><h3>Find what matters.</h3><p>FOD detection and vision-based localisation on a candidate companion computer.</p></div><span class="pipeline-arrow" aria-hidden="true">→</span><div><span class="pipeline-icon">↗</span><small>03 / COMMUNICATE</small><h3>Close the loop.</h3><p>Transmit timestamped coordinates to the UGV through a proposed ROS 2 interface.</p></div></div>
  <a class="inline-link reveal" :href="withBase('/scopes')">Explore project scopes <span aria-hidden="true">↗</span></a>
 </section>
 <section class="closing section-pad reveal"><span class="eyebrow">ENGINEERED WITH PURPOSE</span><h2>Safer ground.<br>Higher possibilities.</h2><a class="pill primary" :href="withBase('/team')">Meet the Team <span aria-hidden="true">↗</span></a><p>National University of Singapore<br>College of Design and Engineering</p></section>
 <footer class="home-footer"><a :href="withBase('/')">FOD ARGUS<span> / CDE4301</span></a><span>Autonomous Runway Inspection UAV</span><a :href="withBase('/team')">Meet the Team ↗</a></footer>
</div>
</template>
<style scoped>
.runway-home p {
 font-size: 18px;
 line-height: 1.85;
}
#mission h2,
#system h2 {
 font-size: clamp(38px, 4.6vw, 64px);
}
.runway-home .pipeline h3 {
 font-size: 26px;
}
.runway-home .pill,
.runway-home .text-link,
.runway-home .inline-link {
 font-size: 16px;
}
.runway-home .eyebrow,
.runway-home .small-note,
.runway-home .metric-index,
.runway-home .pipeline small,
.runway-home .home-footer,
.runway-home .home-footer > a:first-child {
 font-size: 12px;
}
.runway-home .hero-bottom {
 font-size: 11px;
}
@media (max-width: 767px) {
 .runway-home p {
  font-size: 16px;
 }
 .runway-home .pill,
 .runway-home .text-link {
  font-size: 14px;
 }
 .runway-home .hero-actions {
  flex-wrap: wrap;
 }
 .runway-home .hero-bottom {
  font-size: 9px;
  letter-spacing: 1px;
 }
}
#acknowledgements,
#executive-summary {
 color: #fff;
 background: #0d0f12;
}
#acknowledgements h2,
#executive-summary h2 {
 color: #fff;
 font-size: clamp(38px, 4.6vw, 64px);
}
#acknowledgements .mission-layout > div > p,
#executive-summary .mission-layout > div > p {
 color: #fff;
 font-size: 18px;
 line-height: 1.85;
}
#acknowledgements .mission-layout > div > p + p,
#executive-summary .mission-layout > div > p + p {
 margin-top: 22px;
}
#acknowledgements .eyebrow,
#acknowledgements .small-note,
#executive-summary .eyebrow,
#executive-summary .small-note {
 color: #fff;
 font-size: 12px;
}
#executive-summary .inline-link {
 color: #fff;
 font-size: 16px;
}
@media (max-width: 767px) {
 #acknowledgements .mission-layout > div > p,
 #executive-summary .mission-layout > div > p {
  font-size: 16px;
 }
}
/* Highlight both opening actions with a gentle, synchronised pulse. */
.runway-home .hero-actions > a {
 display: inline-flex;
 align-items: center;
 justify-content: center;
 gap: 20px;
 min-height: 48px;
 padding: 13px 22px;
 border: 1px solid #fff;
 border-radius: 28px;
 background: #fff;
 color: #11171e;
 font-weight: 650;
 box-shadow: 0 0 0 0 #ffffff00;
 animation: hero-action-pulse 3s ease-in-out infinite;
 transition: background .2s, transform .2s;
}
.runway-home .hero-actions > a:hover {
 background: #f2f4f7;
 transform: translateY(-2px);
 animation-play-state: paused;
}
.runway-home .hero-actions > a:focus-visible {
 outline: 3px solid #fff;
 outline-offset: 5px;
 animation-play-state: paused;
}
@keyframes hero-action-pulse {
 0%, 100% { box-shadow: 0 0 0 0 #ffffff00, 0 0 12px #ffffff22; }
 50% { box-shadow: 0 0 0 7px #ffffff18, 0 0 26px #ffffff66; }
}
@media (prefers-reduced-motion: reduce) {
 .runway-home .hero-actions > a {
  animation: none;
  transition: none;
 }
}
</style>