<script setup lang="ts">
import { withBase } from 'vitepress'
defineProps<{ src: string; caption: string; poster?: string }>()
</script>
<template>
 <figure class="comms-video">
  <video controls playsinline preload="none" :src="withBase(src)" :poster="poster ? withBase(poster) : undefined" :aria-label="caption">
   Your browser does not support embedded video. <a :href="withBase(src)">Open video</a>.
  </video>
  <figcaption>{{ caption }} <a :href="withBase(src)" target="_blank" rel="noopener">Open video &#8599;</a></figcaption>
 </figure>
</template>
<style scoped>
.comms-video{margin:24px 0;border:1px solid var(--vp-c-divider);border-radius:14px;overflow:hidden;background:var(--vp-c-bg-soft)}
.comms-video video{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:contain;background:#080b10}
.comms-video figcaption{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 16px;padding:12px 16px;font-size:14px;line-height:1.6;color:var(--vp-c-text-2)}
.comms-video figcaption a{white-space:nowrap}
</style>
