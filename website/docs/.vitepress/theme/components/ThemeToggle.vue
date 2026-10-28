<script setup lang="ts">
import { useData } from 'vitepress'
const { isDark } = useData()
</script>
<template>
 <button class="argus-theme-toggle" type="button" role="switch" :aria-checked="isDark" aria-label="Dark mode" :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'" @click="isDark = !isDark">
  <svg v-if="isDark" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20.5 13A8.5 8.5 0 0 1 11 3.5a8.5 8.5 0 1 0 9.5 9.5Z"/></svg>
  <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/></svg>
  <span>{{ isDark ? 'Dark' : 'Light' }}</span>
 </button>
</template>
