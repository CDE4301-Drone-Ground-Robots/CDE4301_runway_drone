<script setup lang="ts">
import { withBase } from 'vitepress'

type Feature = {
 id: string
 title: string
 metric: string
 status: string
 description: string
 icon: string
 image?: { src: string; alt: string; caption: string }
 details: string[]
 links: { label: string; href: string }[]
}

// Targets come from the feature brief; implementation details come from the
// linked reports. Keep validation limits explicit when these reports evolve.
const features: Feature[] = [
 {
  id: 'endurance', title: 'Flight Endurance', metric: '15 min', status: 'Design target',
  description: 'A 15-minute flight target to support runway inspection missions.',
  icon: 'M26 8h12 M32 8v6 M46 16l4 4 M32 23v13l9 5 M52 36a20 20 0 1 1-40 0 20 20 0 0 1 40 0Z',
  details: [
   'The endurance objective is approximately 15 minutes per flight, giving the UAV time to carry out an inspection mission before returning for recharging.',
   'The mechanical report identifies low structural mass as a way to reduce thrust and propulsion power requirements. Battery selection, payload and propulsion must be considered together to assess achievable endurance.',
   'The 15-minute value is a design target from the feature brief. A measured flight-endurance result is not yet documented.'
  ],
  links: [{ label: 'Mechanical design', href: '/subsystems/mechanical-design#overview-of-mechanical-design-of-the-uav' }, { label: 'Electrical design', href: '/subsystems/electrical-design' }]
 },
 {
  id: 'lightweight', title: 'Lightweight Design', metric: '< 7 kg', status: 'Target takeoff mass',
  description: 'A lightweight airframe designed around a below-7 kg takeoff mass target.',
  icon: 'M24 17a8 8 0 0 1 16 0 M17 20h30l6 34H11l6-34Z',
  image: { src: '/report-assets/mechanical-design/final-prototype-layers.png', alt: 'CAD side view showing the layered airframe, arms and sensor assembly', caption: 'Prototype CAD · mechanical report' },
  details: [
   'The mechanical design sets a total takeoff mass target below 7 kg. Keeping the airframe light supports the endurance objective while leaving capacity for the inspection payload.',
   'CFRP plates and tubes are proposed for the primary structure. Custom PETG CF enclosures and clamps accommodate more complex shapes, balancing structural needs with manufacturability.',
   'The target applies to the complete UAV, including its battery and onboard equipment. A measured final takeoff mass is not yet documented.'
  ],
  links: [{ label: 'Final prototype design', href: '/subsystems/mechanical-design#final-prototype-design' }]
 },
 {
  id: 'detection', title: 'FOD and Crack Detection', metric: 'Inspect', status: 'Prototype development',
  description: 'Computer vision for runway debris and surface-defect inspection.',
  icon: 'M10 24V12h12 M42 12h12v12 M54 40v12H42 M22 52H10V40 M23 24h18v16H23Z',
  image: { src: '/report-assets/computer-vision/cv-23.jpg', alt: 'Sample YOLO detection output identifying a battery', caption: 'Sample YOLO output · computer vision report' },
  details: [
   'The RGB inspection pipeline uses PatchCore to locate anomalous regions, YOLO to identify known FOD classes and a U-Net model to segment cracks. The system is intended to retrieve coordinates for reporting detected hazards.',
   'A downward-facing camera simplifies inspection geometry. Mechanical mounting and vibration management help maintain image clarity; night lighting and onboard integration are also part of development.',
   'The report documents preliminary sample tests and laptop benchmarks. Formal detection testing against subsystem requirements and evaluation on the Jetson remain outstanding.'
  ],
  links: [{ label: 'Vision pipeline', href: '/subsystems/computer-vision#subsystem-overview' }, { label: 'Integration and evaluation', href: '/subsystems/computer-vision#integration-evaluation' }]
 },
 {
  id: 'avoidance', title: 'Human and Wildlife Avoidance', metric: 'Protect', status: 'Safety objective',
  description: 'Thermal monitoring intended to support safer autonomous operation.',
  icon: 'M32 7 52 15v16c0 13-20 24-20 24S12 44 12 31V15L32 7Z M24 31l6 6 12-14',
  image: { src: '/report-assets/computer-vision/cv-38.webp', alt: 'Software thermal-detection examples with birds and people labelled', caption: 'Software thermal examples · computer vision report' },
  details: [
   'The safety objective is to identify people, birds and other potential obstacles before they enter the UAV’s path. The proposed thermal camera looks forward and downward to complement the LiDAR coverage at flight height.',
   'When a thermal target is detected, the intended response is to stop and hold until the obstacle clears. This requires coordination between perception, navigation and the flight controller.',
   'Thermal detection has been simulated in software. Flight-controller emergency-stop integration and testing are future work; autonomous avoidance is not yet verified.'
  ],
  links: [{ label: 'Thermal safety', href: '/subsystems/computer-vision#thermal-safety' }, { label: 'Navigation and obstacle avoidance', href: '/subsystems/navigation-obstacle-avoidance' }]
 },
 {
  id: 'planning', title: 'Optimised Path Planning for FOD Detection', metric: 'Cover', status: 'Proposed capability',
  description: 'Autonomous route planning intended to support systematic runway coverage.',
  icon: 'M14 13h30a8 8 0 0 1 0 16H20a8 8 0 0 0 0 16h30 M14 8v10 M9 13h10 M46 41l5 4-5 4',
  details: [
   'The planning objective is to cover the inspection area systematically, helping the vision system examine the runway along an organised route.',
   'Route planning will need to account for the camera’s inspection coverage, the flight-endurance budget and obstacle handling. The CV development plan also calls for navigation coordinates to be passed to the vision system for hazard reporting.',
   'The navigation report currently contains author details only. A planning algorithm, coverage performance and flight validation have not yet been documented.'
  ],
  links: [{ label: 'Navigation report', href: '/subsystems/navigation-obstacle-avoidance' }, { label: 'CV integration plan', href: '/subsystems/computer-vision#semester-2-development-plan' }]
 },
 {
  id: 'battery', title: 'Rechargeable Battery', metric: 'Recharge', status: 'Power-system objective',
  description: 'A rechargeable onboard power system intended for repeated operations.',
  icon: 'M54 26h4v12h-4 M9 20h43v24H9V20Z M32 23l-7 10h8l-3 8 10-13h-9l1-5Z',
  details: [
   'Rechargeable onboard power is intended to support repeated inspection operations between charging sessions.',
   'The mechanical layout allocates a 12 Ah battery to the bottom layer, alongside power distribution boards, a fuse and ESCs. Secure mounting, wiring access and balanced mass distribution are part of the mechanical requirements.',
   'The electrical report is not yet populated. Charging method, turnaround time and cycle performance remain to be documented; an automated charging dock is not established in the current reports.'
  ],
  links: [{ label: 'Battery allocation', href: '/subsystems/mechanical-design#final-prototype-design' }, { label: 'Electrical report', href: '/subsystems/electrical-design' }]
 }
]
</script>

<template>
 <section class="drone-features" aria-labelledby="drone-specification-title">
  <div class="features-shell">
   <header class="features-header">
    <p class="features-kicker">FOD ARGUS / ENGINEERING / 01</p>
    <a class="features-back" :href="withBase('/')"><span aria-hidden="true">←</span> Back to overview</a>
   </header>
   <div class="features-intro">
    <div class="features-copy">
     <p class="features-eyebrow">AUTONOMOUS RUNWAY INSPECTION UAV</p>
     <h1 id="drone-specification-title">Drone<br>Specification<span>.</span></h1>
     <p class="features-lead">Built around the mission.<br><span>From a lightweight airframe to intelligent inspection.</span></p>
    </div>
    <figure class="features-prototype">
     <img :src="withBase('/report-assets/mechanical-design/final-prototype-cad-assembly.png')" alt="FOD ARGUS prototype CAD assembly with four propellers, layered body and underslung camera" width="1378" height="665" fetchpriority="high" decoding="async">
     <figcaption><span>THE PLATFORM</span> FOD ARGUS / Prototype CAD assembly</figcaption>
    </figure>
   </div>

   <section class="features-showcase" aria-labelledby="key-features-title">
    <div class="features-section-heading">
     <div>
      <p class="features-eyebrow">MISSION-LED DESIGN</p>
      <h2 id="key-features-title">FOD ARGUS — Key Features</h2>
     </div>
     <span class="features-count">06 FEATURES / ONE PLATFORM</span>
    </div>
    <p class="features-description">Six capabilities and design objectives guide the development of our runway inspection UAV. Select a card to explore the engineering behind it.</p>
    <p class="features-status-note"><span class="features-status-dot" aria-hidden="true"></span>Prototype in development. Targets and proposed capabilities are labelled below; measured results are described in the linked reports.</p>

    <!-- Native disclosures support keyboard, touch and static HTML before hydration. -->
    <div class="features-grid">
     <details v-for="(feature, index) in features" :id="'feature-' + feature.id" :key="feature.id" class="feature-card">
      <summary>
       <span class="feature-visual" :class="{ 'feature-visual-photo': feature.image }">
        <img v-if="feature.image" :src="withBase(feature.image.src)" :alt="feature.image.alt" width="640" height="320" loading="lazy" decoding="async">
        <svg v-else class="feature-icon" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path :d="feature.icon" /></svg>
        <span class="feature-index" aria-hidden="true">0{{ index + 1 }} / ARGUS</span>
        <span v-if="!feature.image" class="feature-metric">{{ feature.metric }}</span>
       </span>
       <span class="feature-card-body">
        <span class="feature-status">{{ feature.status }}</span>
        <span class="feature-title">{{ feature.title }}</span>
        <span class="feature-description">{{ feature.description }}</span>
        <span class="feature-action"><span class="feature-action-open">Explore feature</span><span class="feature-action-close">Close details</span><span class="feature-toggle" aria-hidden="true">+</span></span>
       </span>
      </summary>
      <div class="feature-details">
       <p v-if="feature.image" class="feature-image-caption">{{ feature.image.caption }}</p>
       <p v-for="paragraph in feature.details" :key="paragraph">{{ paragraph }}</p>
       <div class="feature-links" aria-label="Related engineering reports">
        <a v-for="link in feature.links" :key="link.href" :href="withBase(link.href)">{{ link.label }} <span aria-hidden="true">↗</span></a>
       </div>
      </div>
     </details>
    </div>
   </section>
   <footer class="features-footer"><span>AUTONOMOUS RUNWAY INSPECTION UAV</span><span>NUS / CDE4301 / AIS-407</span></footer>
  </div>
 </section>
</template>

<style scoped>
.drone-features {
 --feature-accent: #8cdae3;
 --feature-muted: var(--vp-c-text-2);
 --feature-text: var(--vp-c-text-1);
 font-family: var(--vp-font-family-base);
 font-weight: 400;
 color: var(--feature-text);
 background: radial-gradient(ellipse at 85% 5%, #16344255, transparent 42%), #080c11;
 min-height: calc(100svh - var(--vp-nav-height));
}
/* Match report typography while keeping the existing dark showcase in both themes. */
:global(html:not(.dark)) .drone-features { --feature-text: #eeeef0; --feature-muted: #a6aeb9; }
.features-shell { max-width: 1360px; margin: 0 auto; padding: 42px 48px 32px; }
.features-header, .features-section-heading, .features-footer { display: flex; align-items: center; justify-content: space-between; gap: 24px; }
.features-kicker, .features-eyebrow, .features-count, .features-footer { font-size: 12px; font-weight: 600; line-height: 1.7; letter-spacing: 1.7px; }
.features-kicker { color: var(--feature-muted); margin: 0; }
.features-back { font-size: 14px; color: var(--feature-muted); padding: 10px 0; }
.features-back:hover { color: var(--feature-accent); }
.features-intro { display: grid; grid-template-columns: .9fr 1.1fr; gap: 56px; align-items: center; padding: 56px 0 64px; }
.features-eyebrow { color: var(--feature-accent); margin: 0 0 20px; }
.features-copy h1 { font-family: Manrope, var(--vp-font-family-base); font-size: clamp(32px, 4vw, 44px); line-height: 1.18; letter-spacing: -1.7px; font-weight: 750; margin: 0; }
.features-copy h1 > span { color: var(--feature-accent); }
.features-lead { font-size: 18px; line-height: 1.85; margin: 26px 0 0; }
.features-lead > span { color: var(--feature-muted); font-size: inherit; }
.features-prototype { margin: 0; border: 1px solid #ffffff24; border-radius: 18px; overflow: hidden; background: #111923; }
.features-prototype img { display: block; width: 100%; height: auto; aspect-ratio: 1378 / 665; object-fit: contain; background: #e3e6ee; }
.features-prototype figcaption { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px; padding: 15px 18px; font-size: 14px; line-height: 1.75; color: var(--feature-muted); }
.features-prototype figcaption > span { color: var(--feature-accent); font-size: 12px; font-weight: 600; letter-spacing: 1.5px; }
.features-showcase { border-top: 1px solid #ffffff24; padding-top: 36px; }
.features-section-heading .features-eyebrow { margin-bottom: 12px; }
.features-section-heading h2 { margin: 0; font-family: Manrope, var(--vp-font-family-base); font-size: clamp(26px, 3vw, 38px); line-height: 1.18; font-weight: 750; letter-spacing: -1px; }
.features-count { align-self: flex-end; color: var(--feature-muted); white-space: nowrap; padding-bottom: 5px; }
.features-description { max-width: 730px; color: var(--feature-text); font-size: 18px; line-height: 1.85; margin: 20px 0 14px; }
.features-status-note { display: flex; align-items: baseline; gap: 10px; color: var(--feature-muted); font-size: 14px; line-height: 1.75; margin: 0 0 28px; }
.features-status-dot { display: inline-block; flex: 0 0 5px; width: 5px; height: 5px; border-radius: 50%; background: var(--feature-accent); }
.features-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 22px; align-items: start; }
.feature-card { min-width: 0; border: 1px solid #ffffff24; border-radius: 16px; background: #111820; overflow: hidden; transition: border-color .2s, transform .2s; scroll-margin-top: 100px; }
.feature-card[open] { border-color: #8cdae380; }
.feature-card summary { display: block; list-style: none; cursor: pointer; border-radius: 15px; }
.feature-card summary::-webkit-details-marker { display: none; }
.feature-card summary::marker { content: ''; }
.feature-card summary:focus-visible { outline: 2px solid var(--feature-accent); outline-offset: -4px; }
.feature-visual { position: relative; display: flex; align-items: center; justify-content: center; height: 180px; overflow: hidden; color: var(--feature-accent); background: radial-gradient(ellipse at 60% 40%, #264d5a66, transparent 70%), repeating-linear-gradient(0deg, transparent 0 29px, #91cbd709 29px 30px), repeating-linear-gradient(90deg, transparent 0 29px, #91cbd709 29px 30px), #0c141d; border-bottom: 1px solid #ffffff12; }
.feature-visual img { width: 100%; height: 100%; object-fit: contain; background: #17212c; opacity: .8; transition: opacity .2s; }
.feature-index { position: absolute; top: 14px; left: 16px; padding: 4px 7px; background: #080c11df; color: var(--feature-text); border: 1px solid #ffffff20; border-radius: 4px; font-size: 12px; font-weight: 600; letter-spacing: 1.3px; }
.feature-icon { width: 76px; height: 76px; margin-top: -18px; }
.feature-metric { position: absolute; bottom: 14px; left: 18px; font-size: 22px; font-family: Manrope, var(--vp-font-family-base); letter-spacing: -.4px; color: var(--feature-text); }
.feature-card-body { display: flex; flex-direction: column; padding: 23px 22px 18px; min-height: 250px; background: linear-gradient(145deg, #1b283033, transparent); }
.feature-status { align-self: flex-start; font-size: 12px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; line-height: 1.5; color: var(--feature-accent); margin-bottom: 12px; }
.feature-title { display: block; font-family: var(--vp-font-family-base); font-size: 25px; line-height: 1.35; font-weight: 600; letter-spacing: -.45px; }
.feature-description { display: block; color: var(--feature-text); font-size: 18px; line-height: 1.85; margin: 12px 0 22px; }
.feature-action { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: auto; padding-top: 14px; border-top: 1px solid #ffffff18; color: var(--feature-muted); font-size: 14px; line-height: 1.75; }
.feature-toggle { display: grid; place-items: center; width: 24px; height: 24px; border: 1px solid #8cdae34d; border-radius: 50%; font-size: 18px; line-height: 1; transition: transform .2s; }
.feature-action-close, .feature-card[open] .feature-action-open { display: none; }
.feature-card[open] .feature-action-close { display: inline; }
.feature-card[open] .feature-toggle { transform: rotate(45deg); }
.feature-details { padding: 0 22px 24px; border-top: 1px solid #ffffff18; }
.feature-details p { margin: 18px 0 0; color: var(--feature-text); font-size: 18px; line-height: 1.85; }
.feature-details .feature-image-caption { font-size: 14px; line-height: 1.75; color: var(--feature-muted); }
.feature-links { display: flex; flex-direction: column; gap: 10px; margin-top: 22px; }
.feature-links a { display: flex; justify-content: space-between; gap: 14px; font-size: 14px; line-height: 1.75; color: var(--feature-accent); text-decoration: underline; text-underline-offset: 4px; padding: 5px 0; }
.feature-links a:hover { color: #e1f9fc; }
.features-back:focus-visible, .feature-links a:focus-visible { outline: 2px solid var(--feature-accent); outline-offset: 5px; border-radius: 2px; }
.features-footer { margin-top: 58px; padding-top: 24px; border-top: 1px solid #ffffff24; color: var(--feature-muted); font-size: 12px; }
@media (hover: hover) {
 .feature-card:hover { transform: translateY(-3px); border-color: #8cdae380; }
 .feature-card:hover .feature-visual img { opacity: 1; }
}
@media (max-width: 1050px) {
 .features-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
 .features-intro { gap: 32px; }
 .features-count { display: none; }
}
@media (max-width: 767px) {
 .features-lead, .features-description, .feature-description, .feature-details p { font-size: 17px; line-height: 1.8; }
 .feature-title { font-size: 22px; }
 .features-prototype figcaption, .feature-details .feature-image-caption { font-size: 13px; line-height: 1.75; }
}
@media (max-width: 700px) {
 .features-shell { padding: 24px 24px 28px; }
 .features-intro { grid-template-columns: 1fr; gap: 32px; padding: 38px 0 40px; }
 .features-copy h1 { letter-spacing: -1px; }
 .features-header { align-items: flex-start; gap: 12px; }
 .features-kicker { max-width: 160px; font-size: 12px; }
 .features-back { padding: 0; font-size: 14px; white-space: nowrap; }
 .features-showcase { padding-top: 28px; }
 .features-footer { align-items: flex-start; flex-direction: column; gap: 8px; margin-top: 36px; }
}
@media (max-width: 560px) {
 .features-grid { grid-template-columns: 1fr; gap: 18px; }
 .feature-card-body { min-height: 0; padding: 22px; }
 .feature-visual { height: 190px; }
}
@media (prefers-reduced-motion: reduce) {
 .feature-card, .feature-visual img, .feature-toggle { transition: none; }
 .feature-card:hover { transform: none; }
}
@media print {
 .drone-features { background: white; color: #16212c; }
 .features-shell { padding: 20px; }
 .features-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
 .feature-card { break-inside: avoid; }
 .features-back { display: none; }
}
</style>
