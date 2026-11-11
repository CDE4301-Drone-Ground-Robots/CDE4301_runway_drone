<script setup lang="ts">
import { withBase } from 'vitepress'
import { ref } from 'vue'
defineProps<{ src: string; caption: string; poster?: string }>()
const video = ref<HTMLVideoElement | null>(null)
const started = ref(false)
async function play() {
 try {
  await video.value?.play()
 } catch {
  // Keep the poster button available if playback is interrupted.
 }
}
</script>
<template>
 <figure class="mechanical-video">
  <div class="mechanical-video-player">
  <video ref="video" :controls="started || !poster" @play="started = true" playsinline preload="none" :src="withBase(src)" :poster="poster ? withBase(poster) : undefined" :aria-label="caption">
   Your browser does not support embedded video. <a :href="withBase(src)">Open video</a>.
  </video>
  <button v-if="poster && !started" class="mechanical-video-play" type="button" :aria-label="'Play: ' + caption" @click="play"><span aria-hidden="true">&#9654;</span></button>
  </div>
  <figcaption>{{ caption }} <a :href="withBase(src)" target="_blank" rel="noopener">Open video &#8599;</a></figcaption>
 </figure>
</template>
<style scoped>
.mechanical-video{margin:24px 0;border:1px solid var(--vp-c-divider);border-radius:14px;overflow:hidden;background:var(--vp-c-bg-soft)}
.mechanical-video-player{position:relative}
.mechanical-video-play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;width:100%;border:0;background:transparent;cursor:pointer}
.mechanical-video-play span{display:flex;align-items:center;justify-content:center;width:76px;height:76px;padding-left:5px;border:2px solid #ffffffcc;border-radius:50%;background:#101720cc;color:white;font-size:30px;box-shadow:0 4px 24px #0006}
.mechanical-video-play:hover span{background:#1e3045ed}
.mechanical-video-play:focus-visible{outline:3px solid var(--vp-c-brand-1);outline-offset:-4px}
.mechanical-video video{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:contain;background:#080b10}
.mechanical-video figcaption{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 16px;padding:12px 16px;font-size:14px;line-height:1.6;color:var(--vp-c-text-2)}
.mechanical-video figcaption a{white-space:nowrap}
</style>
