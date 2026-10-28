<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { withBase } from 'vitepress'
import { data as team } from '../../../team.data'
import { subsystems } from './subsystems'
function memberSubsystems(member: typeof team.members[number]) {
 return subsystems.filter(subsystem => member.subsystemSlugs.includes(subsystem.slug))
}
const expanded = ref(false)
const step = ref(0)
const rotation = ref(0)
const active = computed(() => ((step.value % team.members.length) + team.members.length) % team.members.length)
let animation = 0
let reducedMotion: MediaQueryList | undefined
onMounted(() => { reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)') })
onBeforeUnmount(() => cancelAnimationFrame(animation))
function rotate(direction: number) {
 expanded.value = false
 cancelAnimationFrame(animation)
 step.value += direction
 const target = step.value * 120
 const initial = rotation.value
 if (reducedMotion?.matches) { rotation.value = target; return }
 const start = performance.now()
 const tick = (now: number) => {
  const elapsed = Math.min((now - start) / 850, 1)
  rotation.value = initial + (target - initial) * (1 - Math.pow(1 - elapsed, 3))
  if (elapsed < 1) animation = requestAnimationFrame(tick)
 }
 animation = requestAnimationFrame(tick)
}
function select(index: number) {
 const difference = (index - active.value + 3) % 3
 if (difference) rotate(difference === 2 ? -1 : 1)
}
function toggleContributions(index: number) {
 if (index !== active.value) select(index)
 expanded.value = !expanded.value
}
function position(index: number) {
 const angle = (index * 120 - rotation.value) * Math.PI / 180
 const depth = Math.cos(angle)
 return {
  '--member-color': team.members[index].color,
  transform: `translate3d(calc(${Math.sin(angle)} * var(--team-radius)), 0, calc(${depth - 1} * var(--team-depth))) rotateY(${-Math.sin(angle) * 23}deg)`,
  zIndex: Math.round(20 + depth * 10),
  opacity: 1
 }
}
function sheetStyle(member: typeof team.members[number]) {
 if (!team.sheet) return {}
 const crop = member.crop
 return {
  backgroundImage: `url("${withBase(team.sheet)}")`,
  backgroundSize: `${2048 / crop.w * 100}% ${579 / crop.h * 100}%`,
  backgroundPosition: `${crop.x / (2048 - crop.w) * 100}% ${crop.y / (579 - crop.h) * 100}%`
 }
}
function dot(index: number) {
 const angle = (index * 120 - rotation.value) * Math.PI / 180
 return { x: 70 + Math.sin(angle) * 31, y: 47 - Math.cos(angle) * 31 }
}
</script>
<template>
<section class="team-page" :class="{ 'contributions-open': expanded }" aria-labelledby="team-title"><div class="team-runway-backdrop" :style="{ backgroundImage: 'url(' + withBase('/runway-night-photo.png') + ')' }" aria-hidden="true"></div>
 <header class="team-intro"><p class="eyebrow">FOD ARGUS / THE PEOPLE</p><h1 id="team-title">Meet the Team<span>.</span></h1><p>Three disciplines. One shared mission.</p></header>
 <div class="team-carousel" role="region" aria-roledescription="carousel" aria-label="FOD ARGUS project team" tabindex="0" @keydown.left.prevent="rotate(-1)" @keydown.right.prevent="rotate(1)">
  <div class="team-stage">
   <article v-for="(member, index) in team.members" :key="member.name" class="team-card" :class="{ 'is-active': index === active, 'is-expanded': expanded && index === active }" :style="position(index)" :aria-hidden="index !== active" :aria-label="`${index + 1} of 3: ${member.name}`" aria-roledescription="slide" @click="select(index)">
    <div class="team-card-topline"><span class="team-accent"></span><span class="team-card-number">0{{ index + 1 }} / 03</span></div>
    <h2>{{ member.name }}</h2><p class="team-role">{{ member.role }}</p><p v-if="member.detail" class="team-role-detail">{{ member.detail }}</p>
         <nav class="team-subsystems" :aria-label="member.name + ': subsystems'">
      <a v-for="subsystem in memberSubsystems(member)" :key="subsystem.slug" :href="withBase('/subsystems/' + subsystem.slug)" :tabindex="index === active ? 0 : -1" @click.stop>
       <span>{{ subsystem.title }}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10" /></svg>
      </a>
     </nav>
    <div class="team-portrait" :style="{ aspectRatio: `${member.crop.w}/${member.crop.h}` }">
     <img v-if="member.photo" :src="withBase(member.photo)" :alt="member.name" width="200" height="170">
     <div v-else-if="team.sheet" class="team-sheet-photo" :style="sheetStyle(member)" role="img" :aria-label="member.name"></div>
     <div v-else class="team-portrait-placeholder" :aria-label="`${member.name}, portrait pending`"><span>{{ member.initials }}</span><small>PORTRAIT COMING SOON</small></div>
    </div>
    <div class="team-contributions">

     <button class="team-expand" type="button" :aria-expanded="expanded && index === active" :aria-controls="`team-contributions-${index}`" :tabindex="index === active ? 0 : -1" @click.stop="toggleContributions(index)">
      <span>{{ expanded && index === active ? 'Hide contributions' : 'View contributions' }}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>
     </button>
     <div v-show="expanded && index === active" :id="`team-contributions-${index}`" class="team-contribution-panel" role="region" :aria-label="`${member.name}: Semester 1 contributions`">
      <h3>Semester 1 contributions</h3><ul><li v-for="contribution in member.contributions" :key="contribution">{{ contribution }}</li></ul>
     </div>
    </div>
   </article>
  </div>
  <div class="team-controls"><button type="button" aria-label="Previous team member" @click="rotate(-1)"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m14 6-6 6 6 6M8 12h13"/></svg></button><div class="team-current" aria-live="polite" aria-atomic="true"><span>{{ String(active + 1).padStart(2, '0') }} <span class="team-counter-divider">/</span> 03</span><strong>{{ team.members[active].name }}</strong></div><button type="button" aria-label="Next team member" @click="rotate(1)"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m10 6 6 6-6 6M16 12H3"/></svg></button></div>
  <div class="team-orbit"><svg viewBox="0 0 140 100" role="img" aria-label="Top view of the cylindrical card carousel; highlighted card is at the front"><defs><marker id="orbit-arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="m1 1 7 4-7 4" fill="none" stroke="currentColor" stroke-width="1.5"/></marker></defs><circle class="orbit-ring" cx="70" cy="47" r="31"/><circle class="orbit-inner" cx="70" cy="47" r="20"/><path class="orbit-direction" d="M106 22a44 44 0 0 1 0 50" marker-end="url(#orbit-arrow)"/><g v-for="(member,index) in team.members" :key="member.name"><circle :cx="dot(index).x" :cy="dot(index).y" :r="index === active ? 5 : 3.5" :fill="member.color" :opacity="index === active ? 1 : 0.5"/></g><path class="orbit-front" d="m66 5 4 5 4-5"/><text x="70" y="96" text-anchor="middle">TOP VIEW</text></svg><p>Rotate to explore</p></div>
 </div>
</section>
</template>