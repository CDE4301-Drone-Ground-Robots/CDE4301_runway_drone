<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, withBase } from 'vitepress'
import { cvSubsystemSections } from '../../cv-subsystem-sections'
const route = useRoute()
let entries: { heading: HTMLElement; link: HTMLAnchorElement; item: HTMLElement | null }[] = []
let sidebar: HTMLElement | null = null
let active = ''
let frame = 0
let generation = 0
let reveal = false
let disposed = false
let stopWatching: (() => void) | undefined
let sidebarObserver: MutationObserver | undefined
let contentObserver: ResizeObserver | undefined
function clear() {
 for (const entry of entries) {
  entry.link.classList.remove('cv-section-current')
  entry.link.removeAttribute('aria-current')
  entry.item?.classList.remove('cv-section-current')
 }
 sidebar?.removeAttribute('data-cv-scrollspy')
 entries = []
 active = ''
 sidebarObserver?.disconnect()
 contentObserver?.disconnect()
}
function keepVisible(entry: typeof entries[number]) {
 if (!sidebar || !entry.link.getClientRects().length) return
 if (window.innerWidth < 960 && !sidebar.classList.contains('open')) return
 const panel = sidebar.getBoundingClientRect()
 const link = entry.link.getBoundingClientRect()
 const nav = document.querySelector('.VPNav')?.getBoundingClientRect()
 const top = Math.max(panel.top, nav?.bottom ?? 0) + 18
 const bottom = panel.bottom - 24
 // Scroll only the contents panel; never move the reader's document position.
 if (link.top < top) sidebar.scrollTop += link.top - top
 else if (link.bottom > bottom) sidebar.scrollTop += link.bottom - bottom
}
function update() {
 frame = 0
 if (!entries.length) return
 const navBottom = document.querySelector('.VPNav')?.getBoundingClientRect().bottom ?? 72
 const threshold = Math.max(120, navBottom + 36)
 let current = entries[0]
 for (const entry of entries) {
  if (entry.heading.getBoundingClientRect().top <= threshold) current = entry
  else break
 }
 if (window.scrollY > 0 && Math.ceil(window.scrollY + window.innerHeight) >= document.documentElement.scrollHeight - 2) current = entries[entries.length - 1]
 const changed = current.heading.id !== active
 if (changed) {
  active = current.heading.id
  for (const entry of entries) {
   const selected = entry === current
   entry.link.classList.toggle('cv-section-current', selected)
   entry.item?.classList.toggle('cv-section-current', selected)
   if (selected) entry.link.setAttribute('aria-current', 'location')
   else entry.link.removeAttribute('aria-current')
  }
 }
 if (changed || reveal) keepVisible(current)
 reveal = false
}
function schedule() { if (!frame && !disposed) frame = requestAnimationFrame(update) }
async function refresh() {
 const version = ++generation
 clear()
 await nextTick()
 if (disposed || version !== generation) return
 const report = document.querySelector<HTMLElement>('.cv-report')
 sidebar = document.querySelector<HTMLElement>('.VPSidebar')
 if (!report || !sidebar) return
 for (const section of cvSubsystemSections) {
  const heading = report.querySelector<HTMLElement>('[id="' + section.slug + '"]')
  const href = withBase('/subsystems/computer-vision#' + section.slug)
  const link = sidebar.querySelector<HTMLAnchorElement>('a[href="' + href + '"]')
  if (heading && link) entries.push({ heading, link, item: link.closest<HTMLElement>('.VPSidebarItem') })
 }
 sidebar.setAttribute('data-cv-scrollspy', '')
 sidebarObserver = new MutationObserver(() => { reveal = true; schedule() })
 sidebarObserver.observe(sidebar, { attributes: true, attributeFilter: ['class'] })
 contentObserver = new ResizeObserver(schedule)
 contentObserver.observe(report)
 reveal = true
 schedule()
}
onMounted(() => {
 stopWatching = watch(() => route.path, refresh, { immediate: true, flush: 'post' })
 window.addEventListener('scroll', schedule, { passive: true })
 window.addEventListener('resize', schedule, { passive: true })
 document.fonts.ready.then(schedule)
})
onUnmounted(() => {
 disposed = true
 ++generation
 stopWatching?.()
 cancelAnimationFrame(frame)
 window.removeEventListener('scroll', schedule)
 window.removeEventListener('resize', schedule)
 clear()
})
</script>
<template><span hidden aria-hidden="true"></span></template>
