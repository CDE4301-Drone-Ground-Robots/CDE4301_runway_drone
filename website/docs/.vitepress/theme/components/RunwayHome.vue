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
   <div class="hero-actions"><a class="pill primary" href="#mission">Project overview <span aria-hidden="true">↗</span></a><a class="text-link" href="#system">Meet the system <span aria-hidden="true">↓</span></a></div>
  </div>
  <div class="aircraft-scene model-scene"><DroneModel /></div>
  <div class="hero-bottom"><span>INNOVATION & DESIGN PROGRAMME</span><a href="#mission">SCROLL TO DISCOVER <span aria-hidden="true">↓</span></a><span>01 / OVERVIEW</span></div>
 </section>
 <section id="mission" class="mission section-pad">
  <div class="section-top reveal"><span class="eyebrow">01 / THE MISSION</span><span class="small-note">Small objects. Significant consequences.</span></div>
  <div class="mission-layout reveal"><h2>Every detail matters.<br><span>Especially on a runway.</span></h2><div><p>A loose bolt. A fragment of rubber. Foreign object debris can pose a serious hazard to aircraft. Finding it is an engineering challenge worth looking at from above.</p><p class="muted">Our project investigates whether a UAV-based vision system can make runway inspection more flexible — through a scaled prototype, controlled testing, and a practical feasibility study.</p><a class="inline-link" href="#system">Understand the challenge <span aria-hidden="true">↗</span></a></div></div>
  <div class="principles reveal"><div><span class="metric-index">01</span><strong>Detect.</strong><p>Find representative FOD with a vision-based pipeline.</p></div><div><span class="metric-index">02</span><strong>Localise.</strong><p>Estimate object coordinates from captured imagery.</p></div><div><span class="metric-index">03</span><strong>Connect.</strong><p>Communicate detections to a ground robot.</p></div></div>
 </section>
 <section id="system" class="system section-pad">
  <div class="section-top reveal"><span class="eyebrow">02 / AN INTEGRATED APPROACH</span><span class="small-note">From observation to actionable coordinates.</span></div>
  <div class="system-heading reveal"><h2>One mission.<br><span>A connected system.</span></h2><p>Aerial imaging meets onboard intelligence.<br>Explore the proposed inspection workflow.</p></div>
  <div class="pipeline reveal"><div><span class="pipeline-icon">⌁</span><small>01 / CAPTURE</small><h3>See the surface.</h3><p>RGB imagery, with thermal and LED-assisted inspection under investigation.</p></div><span class="pipeline-arrow" aria-hidden="true">→</span><div><span class="pipeline-icon">⌖</span><small>02 / PROCESS</small><h3>Find what matters.</h3><p>FOD detection and vision-based localisation on a candidate companion computer.</p></div><span class="pipeline-arrow" aria-hidden="true">→</span><div><span class="pipeline-icon">↗</span><small>03 / COMMUNICATE</small><h3>Close the loop.</h3><p>Transmit timestamped coordinates to the UGV through a proposed ROS 2 interface.</p></div></div>
  <a class="inline-link reveal" :href="withBase('/scopes')">Explore project scopes <span aria-hidden="true">↗</span></a>
 </section>
 <section class="report-section section-pad">
  <div class="section-top reveal"><span class="eyebrow">03 / THE ENGINEERING REPORT</span><span class="small-note">The next chapter is on its way.</span></div>
  <div class="report-heading reveal"><h2>The story continues.<br><span>Report coming soon.</span></h2><a class="pill secondary" :href="withBase('/report/')">Report status <span aria-hidden="true">&#8599;</span></a></div>
  <p class="report-pending reveal">The FOD ARGUS engineering report will be integrated here when it is ready.</p>
 </section>
 <section class="closing section-pad reveal"><span class="eyebrow">ENGINEERED WITH PURPOSE</span><h2>Safer ground.<br>Higher possibilities.</h2><a class="pill primary" :href="withBase('/team')">Meet the Team <span aria-hidden="true">↗</span></a><p>National University of Singapore<br>College of Design and Engineering</p></section>
 <footer class="home-footer"><a :href="withBase('/')">FOD ARGUS<span> / CDE4301</span></a><span>Autonomous Runway Inspection UAV</span><a :href="withBase('/team')">Meet the Team ↗</a></footer>
</div>
</template>