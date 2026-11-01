<script setup lang="ts">
import { withBase } from 'vitepress'
defineProps<{ src: string; caption: string; width: number; height: number }>()
</script>
<template>
 <figure class="comms-figure">
  <a :href="withBase(src)" target="_blank" rel="noopener" :aria-label="'Open full-size image: ' + caption"><img :src="withBase(src)" :alt="caption" :width="width" :height="height" loading="lazy" decoding="async"><span>View full size &#8599;</span></a>
  <figcaption>{{ caption }}</figcaption>
 </figure>
</template>
<style scoped>
.comms-figure{margin:28px 0;border:1px solid var(--vp-c-divider);border-radius:14px;overflow:hidden;background:var(--vp-c-bg-soft)}
.comms-figure a{position:relative;display:block;padding:14px;background:#0d131d}
.comms-figure img{display:block;width:100%;height:auto;max-width:100%;margin:0;object-fit:contain}
.comms-figure a>span{position:absolute;right:8px;bottom:8px;background:#0d131de6;color:#e6c7b5;border-radius:10px;padding:3px 8px;font-size:11px}
.comms-figure figcaption{padding:14px 16px;font-size:14px;line-height:1.6;color:var(--vp-c-text-2)}
.comms-figure a:focus-visible{outline:2px solid #d7aa94;outline-offset:-3px}
</style>
