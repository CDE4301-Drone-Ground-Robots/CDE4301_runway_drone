---
title: FOD ARGUS Engineering Report
outline: false
aside: false
pageClass: full-report-page
prev: false
next: false
---

<script setup>
import FullReport from '../.vitepress/theme/components/FullReport.vue'
import { reportChapters, reportAnchor } from '../.vitepress/report-chapters'
</script>

<div id="report-overview" class="report-cover">
<p class="report-cover-kicker">NUS CDE4301 / ASI-407</p>
<h1>FOD ARGUS<span>Engineering Report</span></h1>
<p class="report-cover-subtitle">Autonomous Runway Inspection UAV</p>
<p class="report-cover-note">Innovation &amp; Design Programme<br>College of Design and Engineering<br>National University of Singapore</p>
</div>

## About This Report

This report brings together the project scope, research, system architecture, and five subsystem reports on one continuous page. Scroll through the chapters below or use the contents links to jump to a section.

## Report Contents

<ol>
 <li v-for="chapter in reportChapters" :key="chapter.id"><a :href="'#' + reportAnchor(chapter.id)">{{ chapter.title }}</a></li>
</ol>

<FullReport />
