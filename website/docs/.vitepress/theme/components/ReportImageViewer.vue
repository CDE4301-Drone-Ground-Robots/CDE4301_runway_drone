<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, ref } from 'vue'

const viewer = ref<HTMLDialogElement | null>(null)
const image = ref<{ src: string; caption: string } | null>(null)
const actualSize = ref(false)
let trigger: HTMLAnchorElement | null = null

async function openImage(event: MouseEvent) {
 if (event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return
 const target = event.target
 if (!(target instanceof Element)) return
 const link = target.closest<HTMLAnchorElement>('.vp-doc a[href]')
 const thumbnail = link?.querySelector('img')
 if (!link || !thumbnail || !/\.(?:avif|gif|jpe?g|png|svg|webp)$/i.test(new URL(link.href).pathname)) return
 event.preventDefault()
 trigger = link
 actualSize.value = false
 image.value = { src: link.href, caption: thumbnail.alt || 'Report image' }
 await nextTick()
 if (viewer.value && !viewer.value.open) viewer.value.showModal()
}

function restoreFocus() {
 trigger?.focus({ preventScroll: true })
 trigger = null
}
onMounted(() => document.addEventListener('click', openImage))
onUnmounted(() => document.removeEventListener('click', openImage))
</script>

<template>
 <dialog ref="viewer" class="report-image-viewer" aria-labelledby="report-image-viewer-title" @close="restoreFocus" @click="($event.target === viewer) && viewer?.close()">
  <template v-if="image">
   <div class="report-image-toolbar">
    <span id="report-image-viewer-title">{{ image.caption }}</span>
    <button type="button" :aria-pressed="actualSize" @click="actualSize = !actualSize">{{ actualSize ? 'Fit image' : 'Actual size' }}</button>
    <button type="button" autofocus aria-label="Close enlarged image" @click="viewer?.close()">Close</button>
   </div>
   <div class="report-image-content" :class="{ 'actual-size': actualSize }" tabindex="0" aria-label="Enlarged image. Scroll to explore at actual size.">
    <img :src="image.src" :alt="image.caption">
   </div>
  </template>
 </dialog>
</template>

<style scoped>
.report-image-viewer{position:fixed;inset:0;width:calc(100vw - 32px);max-width:1600px;max-height:calc(100dvh - 32px);margin:auto;padding:0;border:1px solid #657080;border-radius:12px;background:#08090b;color:#f5f5f7;overflow:hidden}
.report-image-viewer[open]{display:flex;flex-direction:column}
.report-image-viewer::backdrop{background:#000c}
.report-image-toolbar{display:flex;align-items:center;gap:12px;padding:14px 18px;border-bottom:1px solid #ffffff30;flex-shrink:0}
.report-image-toolbar>span{flex:1;min-width:0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;font-size:13px;line-height:1.5}
.report-image-toolbar button{flex-shrink:0;padding:8px 12px;border:1px solid #ffffff60;border-radius:8px;color:inherit;background:transparent;cursor:pointer;font:inherit;font-size:13px}
.report-image-toolbar button:focus-visible,.report-image-content:focus-visible{outline:2px solid #d7aa94;outline-offset:-3px}
.report-image-content{min-height:0;overflow:auto;overscroll-behavior:contain;max-height:calc(100dvh - 130px)}
.report-image-content img{display:block;width:auto;height:auto;max-width:100%;max-height:calc(100dvh - 140px);margin:0 auto;object-fit:contain}
.report-image-content.actual-size img{max-width:none;max-height:none;margin:0}
@media(max-width:600px){.report-image-viewer{width:calc(100vw - 16px);max-height:calc(100dvh - 16px)}.report-image-toolbar{gap:8px;padding:10px}.report-image-toolbar>span{font-size:12px}.report-image-toolbar button{padding:8px}}
@media print{.report-image-viewer{display:none}}
</style>
