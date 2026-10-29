<script setup lang="ts">
import { withBase } from 'vitepress'
defineProps<{name:string;matric:string;portrait:string}>()
</script>
<template>
 <section class="subsystem-lead" aria-label="Subsystem lead">
  <img class="subsystem-lead-photo" :src="withBase(portrait)" :alt="name" width="92" height="92">
  <div class="subsystem-lead-details"><span class="subsystem-lead-label">SUBSYSTEM LEAD</span><strong class="subsystem-lead-name">{{name}}</strong><span class="subsystem-lead-matric">{{matric}}</span></div>
 </section>
</template>
<style scoped>
.subsystem-lead{display:flex;align-items:center;gap:22px;margin:24px 0 28px;padding:20px 0;border-top:1px solid var(--vp-c-divider);border-bottom:1px solid var(--vp-c-divider)}
.subsystem-lead .subsystem-lead-photo{display:block;width:92px;height:92px;flex-shrink:0;object-fit:cover;object-position:center top;border-radius:18px;background:transparent;margin:0}
.subsystem-lead-details{display:flex;flex-direction:column;gap:7px;min-width:0}
.subsystem-lead .subsystem-lead-label{font-size:10px;letter-spacing:1.6px;font-weight:500;color:var(--vp-c-text-2)}
.subsystem-lead .subsystem-lead-name{font-size:24px;font-weight:650;line-height:1.3;color:var(--vp-c-text-1);overflow-wrap:anywhere}
.subsystem-lead .subsystem-lead-matric{font-size:18px;font-weight:500;line-height:1.4;letter-spacing:.5px;color:var(--vp-c-text-1)}
@media(max-width:600px){.subsystem-lead{gap:16px}.subsystem-lead .subsystem-lead-photo{width:76px;height:76px;border-radius:15px}.subsystem-lead .subsystem-lead-name{font-size:20px}.subsystem-lead .subsystem-lead-matric{font-size:16px}.subsystem-lead .subsystem-lead-label{font-size:9px}}
</style>
