<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'
import { withBase } from 'vitepress'
import ProjectScope from '../../../scopes.md'
import Research from '../../../research/index.md'
import SystemArchitecture from '../../../report/system-architecture.md'
import MechanicalDesign from '../../../subsystems/mechanical-design.md'
import ElectricalDesign from '../../../subsystems/electrical-design.md'
import Navigation from '../../../subsystems/navigation-obstacle-avoidance.md'
import ComputerVision from '../../../subsystems/computer-vision.md'
import Communication from '../../../subsystems/communication-system.md'
import Timeline from '../../../timeline.md'
import References from '../../../references.md'
import Appendices from '../../../appendices.md'
import { continuousReportLink, reportAnchor, reportChapters } from '../../report-chapters'

const components = [ProjectScope, Research, SystemArchitecture,
 MechanicalDesign, ElectricalDesign, Navigation, ComputerVision, Communication, Timeline, References, Appendices]
const report = ref<HTMLElement>()

onMounted(async () => {
 await nextTick()
 const base = withBase('/')
 for (const chapter of reportChapters) {
  const section = document.getElementById(reportAnchor(chapter.id))
  if (!section) continue
  // Each chapter keeps its own heading namespace when assembled on one page.
  for (const heading of section.querySelectorAll<HTMLElement>('h1[id], h2[id], h3[id], h4[id], h5[id], h6[id], .mechanical-equation[id], details[id], .report-anchor[id], .ieee-reference[id], .report-table-caption[id]')) {
   heading.id = reportAnchor(chapter.id, heading.id)
  }
  for (const anchor of section.querySelectorAll<HTMLAnchorElement>('a[href]')) {
   const href = anchor.getAttribute('href')!
   if (href.startsWith('#') && href.length > 1) {
    anchor.setAttribute('href', '#' + reportAnchor(chapter.id, decodeURIComponent(href.slice(1))))
    continue
   }
   const url = new URL(href, window.location.href)
   if (url.origin !== window.location.origin || !url.pathname.startsWith(base)) continue
   const local = '/' + url.pathname.slice(base.length) + url.hash
   const target = continuousReportLink(local)
   if (target !== local) anchor.setAttribute('href', withBase(target))
  }
 }
 document.dispatchEvent(new Event('full-report-ready'))
 // Direct subsection links can arrive before the imported chapters mount.
 if (window.location.hash) {
  let id = decodeURIComponent(window.location.hash.slice(1))
  const legacyResearch = id.match(/^report-(primary|secondary)-research(?:--(.+))?$/)
  if (legacyResearch) {
   id = reportAnchor('research', legacyResearch[2] || legacyResearch[1] + '-research')
   window.history.replaceState(window.history.state, '', '#' + encodeURIComponent(id))
  }
  requestAnimationFrame(() => document.getElementById(id)?.scrollIntoView())
 }
})
</script>

<template>
 <div ref="report" class="full-report">
  <section v-for="(chapter, index) in reportChapters" :id="reportAnchor(chapter.id)" :key="chapter.id" class="full-report-chapter" :aria-label="chapter.title">
   <component :is="components[index]" />
  </section>
 </div>
</template>

<style scoped>
.full-report-chapter { min-width: 0; scroll-margin-top: 100px; }
.full-report-chapter + .full-report-chapter { margin-top: 72px; padding-top: 48px; border-top: 1px solid var(--vp-c-divider); }
</style>
