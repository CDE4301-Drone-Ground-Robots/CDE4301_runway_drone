<script setup lang="ts">
import { withBase } from 'vitepress'
defineProps<{ name: string; matric: string; portrait: string }>()
</script>

<template>
 <details class="scope-dropdown custom-block details">
  <summary>
   <img :src="withBase(portrait)" alt="" width="64" height="64">
   <span class="scope-member-identity"><strong>{{ name }}</strong><span>{{ matric }}</span></span>
   <svg class="scope-chevron" viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 7 7-7 7" /></svg>
  </summary>
  <div class="scope-member-content"><slot /></div>
 </details>
</template>

<style scoped>
.scope-dropdown{margin:24px 0;padding:0 20px;border:1px solid var(--vp-c-divider);border-radius:12px;background:var(--vp-c-bg-soft)}
.scope-dropdown>summary{display:flex;align-items:center;gap:18px;padding:18px 0;margin:0;list-style:none;cursor:pointer;font-weight:400}
.scope-dropdown>summary::marker{content:''}
.scope-dropdown>summary::-webkit-details-marker{display:none}
.scope-dropdown>summary:focus-visible{outline:2px solid #c99a8d;outline-offset:4px;border-radius:6px}
.scope-dropdown>summary img{display:block;width:64px;height:64px;margin:0;flex-shrink:0;object-fit:cover;object-position:center top;border-radius:12px}
.scope-member-identity{display:flex;flex-direction:column;gap:6px;min-width:0;flex:1;line-height:1.5}
.scope-member-identity strong{font-size:1.05em;font-weight:600;overflow-wrap:anywhere;color:var(--vp-c-text-1)}
.scope-member-identity>span{font-size:.9em;letter-spacing:.4px;color:var(--vp-c-text-2)}
.scope-chevron{width:20px;height:20px;flex-shrink:0;fill:none;stroke:#c99a8d;stroke-width:1.7;transition:transform .2s}
.scope-dropdown[open] .scope-chevron{transform:rotate(90deg)}
.scope-dropdown[open]>summary{border-bottom:1px solid var(--vp-c-divider)}
.scope-member-content{padding:4px 0 16px;font-size:15px}
@media(max-width:600px){.scope-dropdown{padding:0 14px}.scope-dropdown>summary{gap:12px}.scope-dropdown>summary img{width:54px;height:54px}}
@media(prefers-reduced-motion:reduce){.scope-chevron{transition:none}}
</style>
