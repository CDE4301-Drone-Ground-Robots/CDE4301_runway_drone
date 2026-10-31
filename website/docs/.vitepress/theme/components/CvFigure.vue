<script setup lang="ts">
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'
import figures from './cv-figures.json'
const props = defineProps<{ n: string }>()
const figure = computed(() => (figures as Record<string, {src:string;width:number;height:number;caption:string;cropHeight?:number;architecture?:boolean}>)[props.n])
const viewer = ref<HTMLDialogElement | null>(null)
function openViewer(event: MouseEvent) {
 if (!figure.value?.architecture) return
 event.preventDefault()
 viewer.value?.showModal()
}
</script>
<template>
 <figure v-if="figure" :id="'figure-cv-' + n" class="cv-figure" :class="{ 'cv-architecture': figure.architecture }">
  <a class="cv-figure-image" @click="openViewer" :href="withBase(figure.src)" target="_blank" rel="noopener" :aria-label="'Open Figure CV-' + n + ' at full resolution'" :style="{backgroundImage:'linear-gradient(rgba(5,9,15,.91),rgba(5,9,15,.95)),url(' + withBase('/runway-night-photo.png') + ')'}">
   <span v-if="figure.cropHeight" class="cv-figure-crop" :style="{aspectRatio: figure.width + '/' + figure.cropHeight}">
    <img :src="withBase(figure.src)" :alt="figure.caption" :width="figure.width" :height="figure.height" :style="{maxWidth: 'min(100%, ' + figure.width + 'px)'}" loading="lazy" decoding="async">
   </span>
   <img v-else :src="withBase(figure.src)" :alt="figure.caption" :width="figure.width" :height="figure.height" :style="{maxWidth: 'min(100%, ' + figure.width + 'px)'}" loading="lazy" decoding="async">
   <span class="cv-figure-open" aria-hidden="true">{{ figure.architecture ? 'Enlarge diagram' : figure.cropHeight ? 'View original' : 'View full size' }} &#8599;</span>
  </a>
  <dialog v-if="figure.architecture" ref="viewer" class="cv-diagram-viewer" :aria-label="figure.caption" @click="($event.target === viewer) && viewer?.close()">
   <div class="cv-viewer-toolbar"><span>{{ figure.caption }}</span><button type="button" aria-label="Close enlarged diagram" @click="viewer?.close()">Close <span aria-hidden="true">&#215;</span></button></div>
   <div class="cv-viewer-scroll" tabindex="0" aria-label="Enlarged architecture diagram; scroll to explore"><img :src="withBase(figure.src)" :alt="figure.caption" :width="figure.width" :height="figure.height"></div>
  </dialog>
  <figcaption><strong>Figure CV-{{ String(n).padStart(2,'0') }}</strong><span>{{ figure.caption }}</span></figcaption>
 </figure>
</template>
<style scoped>
.cv-figure{margin:28px 0;border:1px solid var(--vp-c-divider);border-radius:16px;overflow:hidden;background:var(--vp-c-bg-soft)}
.cv-figure-image{position:relative;display:flex;align-items:center;justify-content:center;padding:18px;background-size:cover;background-position:center;min-height:120px;text-decoration:none!important}
.cv-figure-image img{display:block;width:100%;height:auto;max-width:100%;max-height:620px;object-fit:contain;margin:0 auto}
.cv-architecture .cv-figure-image{background:#000!important;padding:20px 12px;cursor:zoom-in}
.cv-architecture .cv-figure-image img{height:auto;max-height:none;aspect-ratio:2000/1440}
.cv-architecture .cv-figure-open{opacity:1}
.cv-diagram-viewer{position:fixed;inset:0;width:calc(100vw - 32px);max-width:1600px;max-height:calc(100dvh - 32px);margin:auto;padding:0;border:1px solid #657080;border-radius:12px;background:#08090b;color:#f5f5f7;overflow:hidden}
.cv-diagram-viewer[open]{display:flex;flex-direction:column}
.cv-diagram-viewer::backdrop{background:#000c}
.cv-viewer-toolbar{flex-shrink:0;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:14px 18px;font-size:13px;line-height:1.5;border-bottom:1px solid #ffffff30}
.cv-viewer-toolbar button{flex-shrink:0;padding:8px 14px;border:1px solid #ffffff60;border-radius:8px;cursor:pointer;font:inherit;color:inherit}
.cv-viewer-toolbar button:focus-visible,.cv-viewer-scroll:focus-visible{outline:2px solid #d7aa94;outline-offset:-3px}
.cv-viewer-scroll{min-height:0;flex:1;overflow:auto;max-height:calc(100dvh - 140px);background:#000;overscroll-behavior:contain}
.cv-viewer-scroll img{display:block;width:100%;min-width:1100px;max-width:none;height:auto;max-height:none;margin:0 auto;object-fit:contain}
@media print{.cv-diagram-viewer{display:none}}
.cv-figure-crop{position:relative;display:block;width:100%;overflow:hidden}
.cv-figure-image .cv-figure-crop img{position:absolute;top:0;left:0;width:100%;max-height:none;margin:0}
.cv-figure-open{position:absolute;right:10px;bottom:10px;padding:4px 9px;border:1px solid #ffffff33;border-radius:20px;background:#0c121ee6;color:#e7c8b8;font-size:9px;letter-spacing:.2px;opacity:0;transition:opacity .15s}
.cv-figure-image:hover .cv-figure-open,.cv-figure-image:focus-visible .cv-figure-open{opacity:1}
.cv-figure-image:focus-visible{outline:2px solid #d7aa94;outline-offset:-3px}
.cv-figure figcaption{display:flex;flex-direction:column;gap:6px;padding:16px 18px;font-size:12px;line-height:1.7;color:var(--vp-c-text-2)}
.cv-figure figcaption strong{font-size:10px;letter-spacing:1px;color:var(--vp-c-text-1)}
:global(.dark) .cv-figure{background:linear-gradient(145deg,#171d27cc,#0d121ccc);border-color:#ffffff24}
:global(.dark) .cv-figure figcaption strong{color:#e6b9a2}
@media(hover:none){.cv-figure-open{opacity:1}}
@media(max-width:600px){.cv-figure-image{padding:10px}.cv-figure figcaption{padding:13px;font-size:11px}}
@media(prefers-reduced-motion:reduce){.cv-figure-open{transition:none}}
@media print{.cv-figure{break-inside:avoid}.cv-figure-open{display:none}}
</style>
