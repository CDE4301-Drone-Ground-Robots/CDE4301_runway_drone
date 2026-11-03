<script setup>
import { computed, ref, nextTick, onMounted, onBeforeUnmount } from 'vue'
import schedule from '../data/gantt-display.js'

const tab = ref('gantt')
const semester = ref(1)
const scrollArea = ref(null)
const chartWidth = ref(0)
let resizeObserver
const tip = ref(null)
let closeTimer
const first = computed(() => semester.value === 1 ? 4 : 18)
const last = computed(() => semester.value === 1 ? 17 : 38)
const weeks = computed(() => schedule.weeks.filter(w => w.column >= first.value && w.column <= last.value))
const members = computed(() => schedule.members.map(member => {
  const visible = [...member.tasks, ...member.milestones].filter(t => t.start <= last.value && t.end >= first.value)
  const categories = [...new Set(visible.map(t => t.category))].map(name => {
    const laneEnds = []
    const tasks = visible.filter(t => t.category === name)
      .sort((a, b) => a.start - b.start || a.end - b.end)
      .map(task => {
        const start = Math.max(first.value, task.start)
        let lane = laneEnds.findIndex(end => end < start)
        if (lane === -1) lane = laneEnds.length
        laneEnds[lane] = Math.min(last.value, task.end)
        return { ...task, lane }
      })
    return { name, tasks }
  })
  return { ...member, categories }
}))
const weekName = column => schedule.weeks.find(w => w.column === column).label
const range = task => task.start === task.end ? weekName(task.start) : `${weekName(task.start)} → ${weekName(task.end)}`
const placement = task => ({ gridColumn: `${Math.max(first.value, task.start) - first.value + 1} / ${Math.min(last.value, task.end) - first.value + 2}`, gridRow: task.lane + 1 })
function hideSoon() { closeTimer = setTimeout(() => { tip.value = null }, 150) }
function keepTip() { clearTimeout(closeTimer) }
function focusTip(event, member, task) {
  const target = event.currentTarget
  // Focusing an offscreen bar first scrolls it into view.
  requestAnimationFrame(() => requestAnimationFrame(() => {
    if (document.activeElement === target) showTip({ currentTarget: target }, member, task)
  }))
}
function showTip(event, member, task) {
  clearTimeout(closeTimer)
  const rect = event.currentTarget.getBoundingClientRect()
  const width = Math.min(340, window.innerWidth - 24)
  tip.value = { member: member.name, task, x: Math.max(12, Math.min(rect.left, window.innerWidth - width - 12)), y: rect.top > window.innerHeight / 2 ? rect.top - 10 : rect.bottom + 10, above: rect.top > window.innerHeight / 2, width }
}
async function selectSemester(value) {
  semester.value = value
  tip.value = null
  await nextTick()
  if (scrollArea.value) { scrollArea.value.scrollLeft = 0; scrollArea.value.scrollTop = 0 }
}
function tabKeys(event) {
  if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return
  event.preventDefault()
  tab.value = event.key === 'Home' ? 'overview' : event.key === 'End' ? 'gantt' : tab.value === 'gantt' ? 'overview' : 'gantt'
  nextTick(() => document.getElementById(`timeline-tab-${tab.value}`).focus())
}
onMounted(() => {
  resizeObserver = new ResizeObserver(() => { chartWidth.value = scrollArea.value.clientWidth })
  resizeObserver.observe(scrollArea.value)
})
onBeforeUnmount(() => { clearTimeout(closeTimer); resizeObserver?.disconnect() })
</script>

<template>
  <section class="timeline-schedule" aria-label="Project timeline">
    <div class="timeline-tabs" role="tablist" aria-label="Timeline views" @keydown="tabKeys">
      <button v-for="view in ['overview', 'gantt']" :id="`timeline-tab-${view}`" :key="view" role="tab" :aria-selected="tab === view" :aria-controls="`timeline-panel-${view}`" :tabindex="tab === view ? 0 : -1" @click="tab = view; tip = null">{{ view === 'gantt' ? 'Gantt Chart' : 'Overview' }}</button>
    </div>
    <div v-show="tab === 'overview'" id="timeline-panel-overview" role="tabpanel" aria-labelledby="timeline-tab-overview" tabindex="0">
      <div class="custom-block info"><p class="custom-block-title">Documentation pending</p><p>Project milestones and the development schedule will be added here.</p></div>
    </div>
    <div v-show="tab === 'gantt'" id="timeline-panel-gantt" role="tabpanel" aria-labelledby="timeline-tab-gantt">
      <div class="schedule-toolbar">
        <div><h2>Team schedule</h2><p>Arun, Charan &amp; Talitha · AY2026/27</p></div>
        <div class="semester-toggle" role="group" aria-label="Select semester">
          <button v-for="value in [1, 2]" :key="value" :aria-pressed="semester === value" @click="selectSemester(value)">Semester {{ value }}</button>
        </div>
      </div>
      <p class="schedule-note" aria-live="polite">{{ semester === 1 ? 'Semester 1 Weeks 1–13, including Recess Week after Week 6.' : 'Reading Week → Examination Weeks 1–2 → Vacation Weeks 1–4 → Semester 2 Weeks 1–13, including Recess Week after Week 6.' }}</p>
      <div class="schedule-legend" aria-label="Team colours"><span v-for="member in schedule.members" :key="member.name" :class="member.color"><i />{{ member.name }}</span></div>
      <p class="schedule-help" id="gantt-help">Scroll to explore the schedule. Hover, focus or tap a bar for full details. Shared milestones apply to all three members.</p>
      <div ref="scrollArea" class="gantt-scroll" tabindex="0" role="region" :aria-label="`Semester ${semester} Gantt chart`" aria-describedby="gantt-help" @scroll="tip = null" @keydown.esc="tip = null">
        <div class="gantt" :style="{ '--week-count': weeks.length, '--available-width': `${chartWidth}px` }">
          <div class="gantt-axis gantt-line">
            <div class="task-label">Subsystem / Category</div>
            <div class="week-track"><div v-for="week in weeks" :key="week.column" class="week-label" :class="{ break: !/^Sem [12] W\d+$/.test(week.label) }">{{ week.label }}</div></div>
          </div>
          <section v-for="member in members" :key="member.name" class="member-group" :class="member.color" :aria-label="member.name">
            <div class="member-heading"><strong>{{ member.name }}</strong><span>{{ member.role }}</span></div>
              <div v-for="category in member.categories" :key="category.name" class="gantt-line category-row" :data-category="category.name">
                <div class="task-label category-label">{{ category.name }}</div>
                <div class="week-track task-track">
                  <button v-for="task in category.tasks" :key="task.source" class="task-bar" :data-source="task.source" :style="placement(task)" :aria-label="`${member.name}: ${task.category}. ${task.description}. ${range(task)}`" :aria-describedby="tip?.task === task ? 'gantt-tooltip' : undefined" @mouseenter="showTip($event, member, task)" @mouseleave="hideSoon" @focus="focusTip($event, member, task)" @blur="hideSoon" @click="showTip($event, member, task)" @keydown.esc.stop="tip = null"><span>{{ task.description }}</span></button>
                </div>
              </div>
          </section>
        </div>
      </div>
      <p class="schedule-source">Source: {{ schedule.source.workbook }} · Gantt Chart · {{ semester === 1 ? 'D–Q' : 'R–AL' }}. Spelling and capitalisation edited for clarity.</p>
    </div>
    <Teleport to="body">
      <div v-if="tip && tab === 'gantt'" id="gantt-tooltip" class="gantt-tooltip" role="tooltip" :style="{ left: `${tip.x}px`, top: `${tip.y}px`, width: `${tip.width}px`, transform: tip.above ? 'translateY(-100%)' : undefined }" @mouseenter="keepTip" @mouseleave="hideSoon">
        <strong>{{ tip.member }} · {{ tip.task.category }}</strong><p>{{ tip.task.description }}</p><span>{{ range(tip.task) }}</span><small>Excel: {{ tip.task.source }}</small>
      </div>
    </Teleport>
  </section>
</template>

<style scoped>
.timeline-schedule{margin-top:28px;--blue:#2460a2;--orange:#a64b0b;--green:#23724b}
.timeline-tabs{display:flex;gap:24px;border-bottom:1px solid var(--vp-c-divider);margin-bottom:28px}
.timeline-tabs button{padding:10px 0;font-weight:600;border-bottom:2px solid transparent;color:var(--vp-c-text-2)}
.timeline-tabs button[aria-selected=true]{color:var(--vp-c-brand-1);border-color:var(--vp-c-brand-1)}
.schedule-toolbar{display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap}
.schedule-toolbar h2{border:0;margin:0;padding:0;font-size:23px}
.schedule-toolbar p{margin:6px 0 0;font-size:13px;color:var(--vp-c-text-2)}
.semester-toggle{display:flex;gap:4px;background:var(--vp-c-bg-soft);padding:4px;border:1px solid var(--vp-c-divider);border-radius:10px}
.semester-toggle button{padding:8px 12px;border-radius:7px;font-size:13px;font-weight:600}
.semester-toggle button[aria-pressed=true]{background:var(--vp-c-brand-1);color:#fff}
.timeline-schedule button:focus-visible,.gantt-scroll:focus-visible{outline:3px solid var(--vp-c-brand-1);outline-offset:3px}
.schedule-note,.schedule-help,.schedule-source{font-size:12px;color:var(--vp-c-text-2);line-height:1.6!important}
.schedule-legend{display:flex;gap:20px;flex-wrap:wrap;font-size:13px;margin:20px 0 8px}
.schedule-legend span{display:flex;align-items:center;gap:8px}.schedule-legend i{width:10px;height:10px;border-radius:3px;background:var(--member-color)}
.blue{--member-color:var(--blue)}.orange{--member-color:var(--orange)}.green{--member-color:var(--green)}
.gantt-scroll{overflow:auto;max-height:72vh;border:1px solid var(--vp-c-divider);border-radius:12px;isolation:isolate;position:relative}
.gantt{--label-width:260px;--week-width:max(88px,calc((var(--available-width) - var(--label-width) - 1px) / var(--week-count)));width:calc(var(--label-width) + var(--week-count) * var(--week-width));font-size:12px}
.gantt-line{display:grid;grid-template-columns:var(--label-width) 1fr}
.gantt-axis{position:sticky;top:0;z-index:5;background:var(--vp-c-bg-soft);border-bottom:1px solid var(--vp-c-divider)}
.task-label{position:sticky;left:0;z-index:2;background:var(--vp-c-bg);padding:12px 14px;border-right:1px solid var(--vp-c-divider);line-height:1.55;white-space:pre-line;overflow-wrap:anywhere}
.gantt-axis .task-label{z-index:6;display:flex;align-items:center;background:var(--vp-c-bg-soft);font-weight:600}
.week-track{display:grid;grid-template-columns:repeat(var(--week-count),var(--week-width));position:relative}
.week-label{padding:14px 8px;text-align:center;border-right:1px solid var(--vp-c-divider);font-weight:600;font-size:11px;line-height:1.5;display:flex;align-items:center;justify-content:center;min-height:72px}
.week-label.break{background:var(--vp-c-brand-soft)}
.member-heading{border-top:3px solid var(--member-color);padding:16px 14px;position:sticky;left:0;width:var(--label-width);background:var(--vp-c-bg);box-sizing:border-box}
.member-heading strong{display:block;font-size:17px;color:var(--member-color)}.member-heading span{font-size:11px;line-height:1.5;color:var(--vp-c-text-2);display:block;margin-top:4px}
.category-label{display:flex;align-items:center;font-weight:700;background:var(--vp-c-bg-soft);border-left:3px solid var(--member-color)}
.category-row{border-bottom:1px solid var(--vp-c-divider);min-height:58px}
.task-track{background:repeating-linear-gradient(to right,transparent 0,transparent calc(var(--week-width) - 1px),var(--vp-c-divider) calc(var(--week-width) - 1px),var(--vp-c-divider) var(--week-width));grid-auto-rows:34px;row-gap:8px;align-content:center;padding:12px 0}
.task-bar{margin:0 4px;background:var(--member-color);color:#fff;border-radius:6px;min-height:34px;text-align:left;padding:8px 10px;min-width:0;box-shadow:0 2px 5px #0001}
.task-bar span{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:11px;line-height:1.5}.task-bar:hover{filter:brightness(1.15)}
.schedule-source{margin-top:12px}
@media(max-width:600px){.gantt{--label-width:176px}.schedule-toolbar{gap:16px}.semester-toggle{width:100%}.semester-toggle button{flex:1}.task-label{padding:10px;font-size:11px}.gantt-scroll{max-height:68vh}}
:global(.dark) .timeline-schedule{--blue:#3275bb;--orange:#a95718;--green:#298557}
:global(.dark) .semester-toggle button[aria-pressed=true]{color:#10202c}
</style>
<style>
.gantt-tooltip{position:fixed;z-index:1000;padding:15px 17px;box-sizing:border-box;background:var(--vp-c-bg);border:1px solid var(--vp-c-divider);border-radius:10px;box-shadow:0 8px 32px #0003;color:var(--vp-c-text-1);font:12px/1.6 var(--vp-font-family-base);max-height:45vh;overflow:auto;overflow-wrap:anywhere}
.gantt-tooltip p{margin:9px 0;white-space:pre-line}.gantt-tooltip span{display:block;font-weight:600}.gantt-tooltip small{display:block;margin-top:7px;color:var(--vp-c-text-2)}
</style>
