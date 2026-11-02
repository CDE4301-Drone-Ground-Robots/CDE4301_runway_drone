---
title: Timeline
sidebar: false
aside: false
pageClass: timeline-page
---

<script setup>
import TimelineGantt from './components/TimelineGantt.vue'
</script>

<p class="chapter-kicker">FOD ARGUS / PROJECT REPORT</p>

# Timeline

<TimelineGantt />

<style>
/* Give the schedule the available viewport width on this page only. */
.timeline-page .VPDoc .container,
.timeline-page .VPDoc .content,
.timeline-page .VPDoc .content-container {
  max-width: none !important;
  min-width: 0;
  width: 100%;
}
@media (min-width: 960px) {
  .timeline-page .VPDoc { padding-right: 32px; padding-left: 32px; }
  .timeline-page .VPDoc .content { padding-right: 0; padding-left: 0; }
}
</style>
