<script setup lang="ts">
import { withBase } from 'vitepress'
</script>
<template>
 <span class="header-identity">
  <span class="header-nus-tile"><img :src="withBase('/nus-logo.png')" alt="National University of Singapore" width="32" height="16"></span>
  <span class="header-project-badge">AIS-407</span>
 </span>
</template>