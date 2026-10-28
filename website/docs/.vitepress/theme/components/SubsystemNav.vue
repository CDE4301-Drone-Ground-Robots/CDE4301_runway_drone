<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { withBase, useData } from 'vitepress'
import { subsystems } from './subsystems'
const props = defineProps<{screenMenu?: boolean}>()
const { page } = useData()
const open=ref(false)
const root=ref<HTMLElement>()
function hover(event: PointerEvent) {
 if (!props.screenMenu && event.pointerType === 'mouse' && window.matchMedia('(hover: hover) and (pointer: fine)').matches) open.value = true
}
function leave(event: PointerEvent) {
 if (!props.screenMenu && event.pointerType === 'mouse' && !root.value?.contains(document.activeElement)) open.value = false
}
function outside(event: Event){ if(!root.value?.contains(event.target as Node)) open.value=false }
onMounted(()=>document.addEventListener('click',outside))
onUnmounted(()=>document.removeEventListener('click',outside))
</script>
<template>
<div ref="root" class="subsystem-nav" :class="{'screen-menu':screenMenu, active:page.relativePath.startsWith('subsystems/') || page.relativePath==='engineering/subsystem.md'}" @keydown.esc="open=false" @pointerenter="hover" @pointerleave="leave">
 <a class="subsystem-nav-label" :href="withBase('/engineering/subsystem')" @click="open=false">Subsystems</a>
 <button class="subsystem-nav-toggle" type="button" aria-label="Choose a subsystem" :aria-expanded="open" @click="open=!open"><svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true" focusable="false"><path d="m4 6 4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg></button>
 <div v-if="open" class="subsystem-nav-menu">
  <a v-for="item in subsystems" :key="item.slug" :href="withBase('/subsystems/'+item.slug)" @click="open=false"><small>{{item.owner}}</small><span>{{item.title}}</span></a>
 </div>
</div>
</template>
<style scoped>
.subsystem-nav{position:relative;display:flex;align-items:center;font-size:12px;font-weight:500;padding-left:12px;color:var(--vp-c-text-1)}
.subsystem-nav-label{display:flex;align-items:center;min-height:var(--vp-nav-height)}
.subsystem-nav.active .subsystem-nav-label{color:var(--vp-c-brand-1)}
.subsystem-nav-toggle{display:inline-flex;align-items:center;justify-content:center;width:28px;height:40px;padding:0;color:inherit;cursor:pointer;flex-shrink:0}
.subsystem-nav-toggle svg{display:block;transition:transform .2s}
.subsystem-nav-toggle[aria-expanded="true"] svg{transform:rotate(180deg)}
.subsystem-nav-toggle:hover{color:var(--vp-c-brand-1)}
@media(prefers-reduced-motion:reduce){.subsystem-nav-toggle svg{transition:none}}
.subsystem-nav-menu{position:absolute;top:calc(100% - 6px);right:0;width:360px;max-width:calc(100vw - 32px);padding:8px;border:1px solid var(--vp-c-divider);border-radius:16px;background:var(--vp-c-bg-elv);box-shadow:var(--vp-shadow-3)}
.subsystem-nav-menu a{display:flex;flex-direction:column;gap:4px;padding:12px;border-radius:8px;line-height:1.5}
.subsystem-nav-menu a:hover{background:var(--vp-c-default-soft)}
.subsystem-nav-menu small{font-size:10px;color:var(--vp-c-text-2)}
.subsystem-nav-label:focus-visible,.subsystem-nav-toggle:focus-visible,.subsystem-nav-menu a:focus-visible{outline:2px solid var(--vp-c-brand-1);outline-offset:2px}
.screen-menu{flex-wrap:wrap;padding:0;border-bottom:1px solid var(--vp-c-divider);font-size:14px}
.screen-menu .subsystem-nav-label{min-height:48px;flex:1}
.screen-menu .subsystem-nav-menu{position:static;width:100%;max-width:none;border:0;box-shadow:none;margin-bottom:12px}
</style>
