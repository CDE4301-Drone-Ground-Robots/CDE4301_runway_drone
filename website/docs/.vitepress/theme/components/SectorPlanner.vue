<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import {
  BATTERY_WINDOW, PACK_WH, PRESETS, SECTOR_WIDTH, THERMAL_STRIP, WORST_WIND, evalSector, maxLength,
  type Pattern, type Preset, type SectorInput,
} from './uav-sector-model'

const form = reactive({ preset: 'cur', wRgb: 2, lRgb: 1.67, pattern: 'along' as Pattern })

// Sized for the worst simulated wind: a crosswind on the lanes, whichever pattern is chosen.
const input = (): SectorInput => ({
  W: SECTOR_WIDTH, L: 30, wRgb: form.wRgb, lRgb: form.lRgb, wTh: THERMAL_STRIP, k: 0.88, hz: 5, Wh: PACK_WH,
  pattern: form.pattern, windDir: form.pattern === 'along' ? 'across' : 'along', wind: WORST_WIND,
})
const length = computed(() => maxLength(input(), BATTERY_WINDOW))
const res = computed(() => evalSector({ ...input(), L: length.value }))
const f = (x: number, d = 1) => x.toFixed(d)

// ---- camera drop-down ----
const open = ref(false)
const root = ref<HTMLElement | null>(null)
const trigger = ref<HTMLButtonElement | null>(null)
const current = computed(() => PRESETS.find(p => p.id === form.preset))
function choose(p: Preset) {
  form.preset = p.id; form.wRgb = p.w; form.lRgb = p.l
  open.value = false; trigger.value?.focus()
}
const onDoc = (e: MouseEvent) => { if (open.value && root.value && !root.value.contains(e.target as Node)) open.value = false }
const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape' && open.value) { open.value = false; trigger.value?.focus() } }
onMounted(() => { document.addEventListener('mousedown', onDoc); document.addEventListener('keydown', onKey) })
onBeforeUnmount(() => { document.removeEventListener('mousedown', onDoc); document.removeEventListener('keydown', onKey) })

// ---- sliders: filled track, end labels ----
const pct = (v: number, lo: number, hi: number) => `${((v - lo) / (hi - lo)) * 100}%`

// ---- plan view: runway runs up the page, the 60 m width runs across, always drawn to the same scale ----
const S = 6.5, ML = 70, MT = 16, MR = 20, MB = 54
const pane = ref<HTMLElement | null>(null)
const scrollable = computed(() => plan.value.vbH > 640)
let drag: { y: number; top: number } | null = null
const down = (e: PointerEvent) => { if (pane.value && e.pointerType === 'mouse' && scrollable.value) { drag = { y: e.clientY, top: pane.value.scrollTop }; pane.value.setPointerCapture(e.pointerId) } }
const move = (e: PointerEvent) => { if (drag && pane.value) pane.value.scrollTop = drag.top - (e.clientY - drag.y) }
const up = () => { drag = null }
const plan = computed(() => {
  const L = length.value, W = SECTOR_WIDTH, r = res.value
  const w = W * S, h = L * S, along = form.pattern === 'along'
  const lanes = Array.from({ length: r.N }, (_, i) => Math.min(along ? i * r.p : (i + 0.5) * r.p, along ? W : L))
  const pts: number[][] = []
  lanes.forEach((d, i) => {
    const down = i % 2 === 0
    if (along) { const x = ML + d * S; pts.push(down ? [x, MT] : [x, MT + h], down ? [x, MT + h] : [x, MT]) }
    else { const y = MT + d * S; pts.push(down ? [ML, y] : [ML + w, y], down ? [ML + w, y] : [ML, y]) }
  })
  return {
    w, h, vbW: ML + w + MR, vbH: MT + h + MB,
    line: pts.map(p => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' '),
    start: along ? [ML + (lanes[0] ?? 0) * S, MT] : [ML, MT + (lanes[0] ?? 0) * S],
  }
})
</script>

<template>
 <section class="sp" aria-label="Sector size planner">
  <div class="sp-head"><span>SECTOR SIZE PLANNER</span><span>WIDTH 60 m</span></div>
  <div class="sp-layout">
   <div class="sp-visual" aria-live="polite">
    <div ref="pane" class="sp-pane" :class="{ pan: scrollable }" tabindex="0" aria-label="Sector drawing, scroll or drag to see the full length"
     @pointerdown="down" @pointermove="move" @pointerup="up" @pointercancel="up">
    <svg :viewBox="`0 0 ${plan.vbW} ${plan.vbH}`" :style="{ maxWidth: Math.round(plan.vbW) + 'px' }" role="img"
     :aria-label="`Sector ${f(length, 0)} metres along the runway by 60 metres wide, with ${res.N} lanes`">
      <rect :x="ML" :y="MT" :width="plan.w" :height="plan.h" class="sector" />
      <polyline :points="plan.line" class="path" />
      <circle :cx="plan.start[0]" :cy="plan.start[1]" r="4" class="start" />
      <line :x1="ML" :x2="ML + plan.w" :y1="MT + plan.h + 22" :y2="MT + plan.h + 22" class="dim" />
      <line :x1="ML" :x2="ML" :y1="MT + plan.h + 16" :y2="MT + plan.h + 28" class="dim" />
      <line :x1="ML + plan.w" :x2="ML + plan.w" :y1="MT + plan.h + 16" :y2="MT + plan.h + 28" class="dim" />
      <text :x="ML + plan.w / 2" :y="MT + plan.h + 46" text-anchor="middle" class="strong">60 m</text>
      <line :x1="ML - 24" :x2="ML - 24" :y1="MT" :y2="MT + plan.h" class="dim" />
      <line :x1="ML - 30" :x2="ML - 18" :y1="MT" :y2="MT" class="dim" />
      <line :x1="ML - 30" :x2="ML - 18" :y1="MT + plan.h" :y2="MT + plan.h" class="dim" />
      <text :transform="`rotate(-90 ${ML - 36} ${MT + Math.min(plan.h, 260) / 2})`" :x="ML - 36" :y="MT + Math.min(plan.h, 260) / 2" text-anchor="middle" class="strong">{{ f(length, 0) }} m along the runway</text>
    </svg>
    </div>
    <p v-if="scrollable" class="sp-hint">Scroll or drag to see the full {{ f(length, 0) }} m</p>
   </div>

   <div class="sp-side">
    <div class="sp-hero" aria-live="polite">
     <span>Sector size per sortie</span>
     <strong>{{ length >= 800 ? '800+' : f(length, 0) }} m <small>× 60 m</small></strong>
    </div>
    <div class="sp-stats">
     <div><span>Lane spacing</span><strong>{{ f(res.p, 2) }} m</strong></div>
     <div><span>Lanes</span><strong>{{ res.N }}</strong></div>
     <div><span>Flight time</span><strong>{{ f(res.T / 60) }} min</strong></div>
     <div><span>Pack used</span><strong>{{ f(res.pack, 0) }}%</strong></div>
    </div>

    <div class="sp-field" ref="root">
     <div class="sp-lab" id="sp-cam-l">RGB camera<em>{{ PRESETS.length }} options</em></div>
     <button ref="trigger" type="button" class="sp-dd" aria-haspopup="listbox" :aria-expanded="open" aria-labelledby="sp-cam-l sp-cam-v" @click="open = !open">
      <span id="sp-cam-v" class="sp-dd-v">
       <b>{{ current ? current.name : 'Custom footprint' }}</b>
       <small>{{ f(form.wRgb) }} × {{ f(form.lRgb) }} m{{ current && current.id !== 'prev' ? ' · native sensor footprint' : '' }}</small>
      </span>
      <svg viewBox="0 0 20 20" class="chev" :class="{ up: open }" aria-hidden="true"><path d="M5 7.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" /></svg>
     </button>
     <ul v-show="open" class="sp-list" role="listbox" aria-labelledby="sp-cam-l">
      <li v-for="p in PRESETS" :key="p.id" role="option" :aria-selected="form.preset === p.id">
       <button type="button" :class="{ on: form.preset === p.id }" @click="choose(p)">
        <span><b>{{ p.name }}</b><small>{{ p.sub }}</small></span>
        <em>{{ p.w.toFixed(1) }} × {{ p.l.toFixed(1) }} m</em>
       </button>
      </li>
     </ul>
    </div>

    <div class="sp-field">
     <div class="sp-lab">Footprint on the ground</div>
     <div class="sp-fp">
      <div><span>Width</span><strong>{{ f(form.wRgb) }} m</strong></div>
      <div><span>Length</span><strong>{{ f(form.lRgb) }} m</strong></div>
     </div>
    </div>
    <div class="sp-field">
     <div class="sp-lab">Lanes</div>
     <div class="sp-seg">
      <button type="button" :aria-pressed="form.pattern === 'along'" @click="form.pattern = 'along'">Along the runway</button>
      <button type="button" :aria-pressed="form.pattern === 'across'" @click="form.pattern = 'across'">Across the runway</button>
     </div>
    </div>
    <p v-if="form.wRgb > THERMAL_STRIP" class="sp-note">Wider than the thermal strip ({{ THERMAL_STRIP }} m), so the lane spacing stops shrinking.</p>
   </div>
  </div>
 </section>
</template>

<style scoped>
.sp { --sp-accent: #599eac; margin: 28px 0; border: 1px solid var(--vp-c-divider); border-radius: 16px; background: var(--vp-c-bg-soft); font-family: var(--vp-font-family-base); color: var(--vp-c-text-1); }
.sp-head { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px; padding: 18px 22px; border-bottom: 1px solid var(--vp-c-divider); color: var(--vp-c-text-2); font-size: 12px; font-weight: 600; letter-spacing: 1.3px; }
.sp-layout { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 340px); gap: 28px; padding: 24px; align-items: start; }
.sp-visual { min-width: 0; padding: 8px 0; }
.sp-side { display: flex; flex-direction: column; gap: 18px; min-width: 0; }
.sp-hero { display: flex; flex-direction: column; padding: 16px 18px; border: 1px solid var(--sp-accent); border-radius: 12px; background: color-mix(in srgb, var(--sp-accent) 10%, var(--vp-c-bg)); }
.sp-hero span, .sp-stats span { font-size: 12px; font-weight: 600; color: var(--vp-c-text-2); }
.sp-hero strong { font-size: 44px; line-height: 1.2; font-weight: 750; color: var(--sp-accent); font-variant-numeric: tabular-nums; }
.sp-hero strong small { font-size: 16px; font-weight: 600; color: var(--vp-c-text-2); }
.sp-stats { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
.sp-stats > div { display: flex; flex-direction: column; padding: 10px 12px; border: 1px solid var(--vp-c-divider); border-radius: 12px; background: var(--vp-c-bg); }
.sp-stats strong { font-size: 17px; white-space: nowrap; font-weight: 750; font-variant-numeric: tabular-nums; }
.sp-field { position: relative; }
.sp-field label, .sp-lab { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; font-size: 15px; font-weight: 600; line-height: 1.6; }
.sp-lab em { font-style: normal; font-size: 12px; font-weight: 500; color: var(--vp-c-text-2); }
.sp-field output { font-variant-numeric: tabular-nums; font-weight: 600; color: var(--sp-accent); }
/* drop-down */
.sp-dd { display: flex; align-items: center; justify-content: space-between; gap: 10px; width: 100%; margin-top: 6px; padding: 10px 12px; font: inherit; text-align: left; color: var(--vp-c-text-1); background: var(--vp-c-bg); border: 1px solid var(--vp-c-divider); border-radius: 10px; cursor: pointer; transition: border-color .15s, box-shadow .15s; }
.sp-dd:hover, .sp-dd[aria-expanded='true'] { border-color: var(--sp-accent); }
.sp-dd[aria-expanded='true'] { box-shadow: 0 0 0 3px color-mix(in srgb, var(--sp-accent) 20%, transparent); }
.sp-dd-v { display: flex; flex-direction: column; min-width: 0; line-height: 1.4; }
.sp-dd-v b { font-size: 15px; font-weight: 650; }
.sp-dd-v small { font-size: 12px; color: var(--vp-c-text-2); }
.chev { flex: none; width: 20px; height: 20px; color: var(--sp-accent); transition: transform .18s; }
.chev.up { transform: rotate(180deg); }
.sp-list { position: absolute; z-index: 20; left: 0; right: 0; top: calc(100% + 6px); max-height: 340px; overflow-y: auto; margin: 0; padding: 6px; list-style: none; background: var(--vp-c-bg); border: 1px solid var(--vp-c-divider); border-radius: 12px; box-shadow: 0 14px 34px rgba(0, 0, 0, .35); }
.sp-list li { margin: 0; padding: 0; }
.sp-list button { display: flex; justify-content: space-between; align-items: center; gap: 10px; width: 100%; padding: 9px 10px; font: inherit; text-align: left; color: var(--vp-c-text-1); background: transparent; border: 0; border-radius: 8px; cursor: pointer; }
.sp-list button:hover { background: color-mix(in srgb, var(--sp-accent) 12%, transparent); }
.sp-list button.on { background: color-mix(in srgb, var(--sp-accent) 18%, transparent); }
.sp-list span { display: flex; flex-direction: column; min-width: 0; line-height: 1.4; }
.sp-list b { font-size: 14px; font-weight: 650; }
.sp-list small { font-size: 12px; color: var(--vp-c-text-2); }
.sp-list em { flex: none; font-style: normal; font-size: 12.5px; font-variant-numeric: tabular-nums; color: var(--sp-accent); }
/* sliders */
.sp input[type='range'] { -webkit-appearance: none; appearance: none; display: block; width: 100%; height: 22px; margin: 6px 0 0; background: transparent; cursor: pointer; }
.sp input[type='range']::-webkit-slider-runnable-track { height: 6px; border-radius: 3px; background: linear-gradient(to right, var(--sp-accent) var(--pct), var(--vp-c-divider) var(--pct)); }
.sp input[type='range']::-moz-range-track { height: 6px; border-radius: 3px; background: var(--vp-c-divider); }
.sp input[type='range']::-moz-range-progress { height: 6px; border-radius: 3px; background: var(--sp-accent); }
.sp input[type='range']::-webkit-slider-thumb { -webkit-appearance: none; width: 18px; height: 18px; margin-top: -6px; border-radius: 50%; border: 2px solid var(--sp-accent); background: var(--vp-c-bg); }
.sp input[type='range']::-moz-range-thumb { width: 14px; height: 14px; border-radius: 50%; border: 2px solid var(--sp-accent); background: var(--vp-c-bg); }
.sp-fp { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 6px; }
.sp-fp > div { display: flex; flex-direction: column; padding: 10px 12px; border: 1px solid var(--vp-c-divider); border-radius: 12px; background: var(--vp-c-bg); }
.sp-fp span { font-size: 12px; font-weight: 600; color: var(--vp-c-text-2); }
.sp-fp strong { font-size: 17px; font-weight: 750; font-variant-numeric: tabular-nums; color: var(--sp-accent); }
.sp-ends { display: flex; justify-content: space-between; font-size: 11.5px; color: var(--vp-c-text-2); font-variant-numeric: tabular-nums; }
.sp-seg { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 6px; }
.sp-seg button { font: inherit; font-size: 14px; line-height: 1.4; min-height: 40px; padding: 8px 10px; border: 1px solid var(--vp-c-divider); border-radius: 8px; background: var(--vp-c-bg); color: var(--vp-c-text-1); cursor: pointer; transition: border-color .15s; }
.sp-seg button:hover { border-color: var(--sp-accent); }
.sp-seg button[aria-pressed='true'] { border-color: var(--sp-accent); background: color-mix(in srgb, var(--sp-accent) 14%, var(--vp-c-bg)); font-weight: 700; }
.sp :is(button, input):focus-visible { outline: 2px solid var(--sp-accent); outline-offset: 2px; }
.sp-note { margin: 0; font-size: 13px; color: var(--vp-c-text-2); }
.sp-pane { max-height: 640px; overflow-y: auto; overflow-x: hidden; overscroll-behavior: contain; border-radius: 8px; }
.sp-pane.pan { cursor: grab; touch-action: pan-y; }
.sp-pane.pan:active { cursor: grabbing; }
.sp-hint { margin: 6px 0 0; text-align: center; font-size: 12px; color: var(--vp-c-text-2); }
svg { display: block; width: 100%; height: auto; margin: 0 auto; }
svg text { fill: var(--vp-c-text-2); font-size: 12.5px; }
svg text.strong { fill: var(--vp-c-text-1); font-weight: 700; font-size: 14px; }
.sector { fill: var(--vp-c-bg); stroke: var(--vp-c-text-2); stroke-width: 1.2; }
.path { fill: none; stroke: var(--sp-accent); stroke-width: 1.3; stroke-linejoin: round; }
.start { fill: var(--vp-c-text-1); }
.dim { stroke: var(--vp-c-text-2); stroke-width: 1.2; }
svg.chev { width: 20px; margin: 0; }
@media (max-width: 900px) { .sp-layout { grid-template-columns: minmax(0, 1fr); } }
@media (max-width: 767px) { .sp-head { padding: 16px; font-size: 11px; } .sp-layout { padding: 16px; } .sp-hero strong { font-size: 36px; } }
@media (prefers-reduced-motion: reduce) { .sp-dd, .chev, .sp-seg button { transition: none; } }
</style>
