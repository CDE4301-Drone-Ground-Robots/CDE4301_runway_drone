<script setup lang="ts">
import { withBase } from 'vitepress'
import { subsystems } from './subsystems'
</script>
<template>
<div class="architecture-scene">
 <div class="architecture-runway" :style="{backgroundImage: 'url(' + withBase('/runway-night-photo.png') + ')'}" aria-hidden="true"></div>
<main class="architecture">
 <header class="architecture-intro"><p class="architecture-kicker">FOD ARGUS / SYSTEM ARCHITECTURE</p><h1>Five disciplines.<br><span>One inspection platform.</span></h1><p class="architecture-lead">Explore the engineering behind FOD ARGUS, from the airframe to inspection and communication.</p></header>
 <section class="architecture-map" aria-label="Subsystem overview">
  <div class="architecture-heading"><span>THE SYSTEM AT A GLANCE</span><span>05 SUBSYSTEMS / 03 TEAM MEMBERS</span></div>
  <div class="architecture-grid">
   <a v-for="(item,index) in subsystems" :key="item.slug" class="architecture-card" :style="{'--subsystem-color':item.color}" :href="withBase('/subsystems/'+item.slug)">
    <div class="architecture-card-top"><span>0{{index+1}}</span><span aria-hidden="true">&#8599;</span></div>
    <p class="architecture-area">{{item.area}}</p><h2>{{item.title}}</h2>
    <div class="architecture-owner"><small>SUBSYSTEM LEAD</small><span>{{item.owner}}</span></div>
   </a>
  </div>
 </section>
 <p class="architecture-note">Select a subsystem to open its documentation.</p>
</main>
</div>
</template>
<style scoped>
.architecture-scene{position:relative;isolation:isolate;overflow:hidden;min-height:calc(100svh - var(--vp-nav-height));background:#08090b}
.architecture-runway{position:absolute;inset:0;z-index:-2;background-size:cover;background-position:65% center;filter:brightness(.6) contrast(1.8) saturate(.75);pointer-events:none}
.architecture-scene::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background:linear-gradient(180deg,rgba(0,2,5,.82),rgba(0,2,5,.48) 40%,rgba(0,2,5,.75)),linear-gradient(90deg,rgba(0,2,5,.55),transparent 55%,rgba(0,2,5,.3))}
.architecture-scene .architecture-intro h1{color:#f5f5f7}
.architecture-scene .architecture-intro h1 span{color:#aeb8c4}
.architecture-scene .architecture-kicker,.architecture-scene .architecture-heading,.architecture-scene .architecture-note{color:#a1b0c0}
.architecture-scene .architecture-lead{color:#b0bcc9}
.architecture-scene .architecture-heading{border-color:#ffffff26}

@media(max-width:600px){.architecture-runway{background-position:78% center}}
@media print{.architecture-runway,.architecture-scene::before{display:none}.architecture-scene{background:transparent}.architecture-scene .architecture-intro h1,.architecture-scene .architecture-intro h1 span,.architecture-scene .architecture-lead,.architecture-scene .architecture-kicker,.architecture-scene .architecture-heading,.architecture-scene .architecture-note{color:#20252b}}

.architecture{max-width:1280px;margin:0 auto;padding:80px 40px 64px;color:var(--vp-c-text-1)}
.architecture-intro{max-width:900px;margin-bottom:64px}
.architecture-kicker{font-size:10px;letter-spacing:2px;color:var(--vp-c-text-2);margin:0 0 24px}
.architecture h1{font-family:Manrope,var(--vp-font-family-base);font-size:clamp(40px,5.5vw,74px);line-height:1.1;letter-spacing:-3px;font-weight:600;margin:0}
.architecture h1 span{color:var(--vp-c-text-2)}
.architecture-lead{font-size:17px;line-height:1.8;max-width:580px;color:var(--vp-c-text-2);margin-top:28px}
.architecture-heading{display:flex;justify-content:space-between;gap:16px;font-size:9px;letter-spacing:1.5px;padding-bottom:20px;border-bottom:1px solid var(--vp-c-divider);color:var(--vp-c-text-2)}
.architecture-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:18px;margin-top:24px}
.architecture-card{grid-column:span 2;display:flex;flex-direction:column;min-height:300px;padding:28px;border:1px solid var(--vp-c-divider);border-radius:20px;background:linear-gradient(145deg,rgba(24,29,36,.55),rgba(10,14,20,.64));color:#f5f5f7;border-color:#ffffff24;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);box-shadow:inset 0 1px 0 #ffffff0c,0 16px 40px #00000020;transition:transform .2s,border-color .2s}
.architecture-card:nth-child(n+4){grid-column:span 3}
.architecture-card:hover{transform:translateY(-4px);border-color:var(--subsystem-color)}
.architecture-card:focus-visible{outline:2px solid var(--subsystem-color);outline-offset:4px}
.architecture-card-top{display:flex;justify-content:space-between;color:var(--subsystem-color);font-size:16px}
.architecture-card-top>span:first-child{font-size:11px;letter-spacing:1px}
.architecture-area{font-size:10px;text-transform:uppercase;letter-spacing:1.3px;color:var(--vp-c-text-2);margin:30px 0 10px}
.architecture h2{font-family:Manrope,var(--vp-font-family-base);font-size:23px;line-height:1.35;letter-spacing:-.5px;margin:0 0 28px;font-weight:600}
.architecture-owner{margin-top:auto;padding-top:20px;border-top:1px solid var(--vp-c-divider);display:flex;flex-direction:column;gap:6px;font-size:12px}
.architecture-owner small{font-size:8px;letter-spacing:1.4px;color:var(--vp-c-text-2)}
.architecture-note{font-size:12px;color:var(--vp-c-text-2);margin:24px 0 0}
@media(max-width:900px){.architecture-card,.architecture-card:nth-child(n+4){grid-column:span 3}.architecture-card:last-child{grid-column:span 6}}
@media(max-width:600px){.architecture{padding:48px 24px}.architecture h1{letter-spacing:-1.7px}.architecture-intro{margin-bottom:40px}.architecture-heading{flex-direction:column;gap:8px}.architecture-grid{grid-template-columns:1fr}.architecture-card,.architecture-card:nth-child(n+4),.architecture-card:last-child{grid-column:auto;min-height:260px}.architecture-lead{font-size:15px}}
@media(prefers-reduced-motion:reduce){.architecture-card{transition:none}.architecture-card:hover{transform:none}}
.architecture-card .architecture-area,.architecture-card .architecture-owner small{color:#a1b0c0}
.architecture-card .architecture-owner{border-color:#ffffff24}
@supports not (backdrop-filter:blur(10px)){.architecture-card{background:rgba(17,22,29,.88)}}
</style>
