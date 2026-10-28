<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
const enabled = ref(false)
const glow = ref<HTMLElement>()
let preference: MediaQueryList | undefined
let frame = 0
let x = 0
let y = 0
function hide() {
 if (frame) cancelAnimationFrame(frame)
 frame = 0
 if (glow.value) glow.value.style.opacity = '0'
}
function updatePreference() {
 enabled.value = preference?.matches ?? false
 hide()
}
function move(event: PointerEvent) {
 if (!enabled.value || event.pointerType !== 'mouse' || document.hidden) return
 x = event.clientX
 y = event.clientY
 if (frame) return
 frame = requestAnimationFrame(() => {
  frame = 0
  if (!glow.value) return
  glow.value.style.transform = 'translate3d(' + (x - 180) + 'px,' + (y - 180) + 'px,0)'
  glow.value.style.opacity = '1'
 })
}
onMounted(() => {
 preference = window.matchMedia('(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)')
 updatePreference()
 preference.addEventListener('change', updatePreference)
 window.addEventListener('pointermove', move, { passive: true })
 document.documentElement.addEventListener('pointerleave', hide)
 window.addEventListener('blur', hide)
 window.addEventListener('scroll', hide, { passive: true, capture: true })
 document.addEventListener('visibilitychange', hide)
})
onUnmounted(() => {
 hide()
 preference?.removeEventListener('change', updatePreference)
 window.removeEventListener('pointermove', move)
 document.documentElement.removeEventListener('pointerleave', hide)
 window.removeEventListener('blur', hide)
 window.removeEventListener('scroll', hide, true)
 document.removeEventListener('visibilitychange', hide)
})
</script>
<template>
 <Teleport to="body"><div v-if="enabled" ref="glow" class="argus-cursor-spotlight" aria-hidden="true"></div></Teleport>
</template>
<style>
.argus-cursor-spotlight{position:fixed;left:0;top:0;width:360px;height:360px;border-radius:50%;pointer-events:none;z-index:100;opacity:0;transform:translate3d(-720px,-720px,0);background:radial-gradient(circle,rgba(177,115,83,.075) 0%,rgba(177,115,83,.025) 38%,transparent 70%);transition:opacity .18s ease;will-change:transform;contain:strict}
.dark .argus-cursor-spotlight{background:radial-gradient(circle,rgba(223,170,145,.1) 0%,rgba(223,170,145,.035) 38%,transparent 70%)}
@media(hover:none),(pointer:coarse),(prefers-reduced-motion:reduce){.argus-cursor-spotlight{display:none}}
@media print{.argus-cursor-spotlight{display:none}}
</style>
