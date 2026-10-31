<script setup lang="ts">
import { computed, onUnmounted, ref, watch } from 'vue'
const progress = ref(0)
const mode = ref('parallel')
const scenario = ref('fod')
const playing = ref(false)
let timer: ReturnType<typeof setInterval> | undefined
const modes = [ { id: 'parallel', label: 'Parallel' }, { id: 'sequential1', label: 'Sequential 1' }, { id: 'sequential2', label: 'Sequential 2' } ]
const scenarios = [ { id: 'fod', label: 'FOD object' }, { id: 'crack', label: 'Surface crack' }, { id: 'both', label: 'FOD + crack' }, { id: 'unknown', label: 'Unknown anomaly' }, { id: 'clear', label: 'No anomaly' } ]
const hasFod = computed(() => ['fod', 'both'].includes(scenario.value))
const hasCrack = computed(() => ['crack', 'both'].includes(scenario.value))
const clear = computed(() => scenario.value === 'clear')
const skipCrack = computed(() => mode.value === 'sequential2' && hasFod.value)
const yoloEnd = computed(() => mode.value === 'parallel' ? 70 : 60)
const crackEnd = computed(() => mode.value === 'parallel' ? 70 : 82)
const coordinateEnd = computed(() => yoloEnd.value + 12)
const ugvEnd = computed(() => coordinateEnd.value + 8)
const sendBase = computed(() => !clear.value && !skipCrack.value && (mode.value !== 'parallel' || hasCrack.value || !hasFod.value))
function state(start: number, end: number) {
 return progress.value >= end ? 'done' : progress.value >= start ? 'active' : 'waiting'
}
function branchState(branch: string) {
 if (clear.value && progress.value >= 45) return 'skipped'
 if (branch === 'unet' && skipCrack.value && progress.value >= yoloEnd.value) return 'skipped'
 return branch === 'yolo' ? state(45, yoloEnd.value) : state(mode.value === 'parallel' ? 45 : yoloEnd.value, crackEnd.value)
}
const coordinateState = computed(() => !hasFod.value ? progress.value >= (clear.value ? 45 : yoloEnd.value) ? 'skipped' : 'waiting' : state(yoloEnd.value, coordinateEnd.value))
const ugvState = computed(() => !hasFod.value ? progress.value >= (clear.value ? 45 : yoloEnd.value) ? 'skipped' : 'waiting' : state(coordinateEnd.value, ugvEnd.value))
const baseState = computed(() => !sendBase.value ? progress.value >= (clear.value ? 45 : 90) ? 'skipped' : 'waiting' : state(90, 96))
const stage = computed(() => {
 const p = progress.value
 if (p < 20) return 'Capture runway'
 if (p < 45) return clear.value ? 'Check for anomalies' : 'Find anomaly and crop'
 if (clear.value) return 'Clear runway: continue'
 if (p < yoloEnd.value) return mode.value === 'parallel' ? 'YOLO + U-Net' : 'YOLO first'
 if (hasFod.value && p < coordinateEnd.value) return mode.value === 'sequential1' ? 'Extract coordinates + run U-Net' : 'Extract FOD coordinates'
 if (hasFod.value && p < ugvEnd.value) return 'Send coordinates to UGV'
 if (!skipCrack.value && p < crackEnd.value) return 'Check for cracks'
 if (skipCrack.value && p < 96) return 'Crack check skipped'
 if (sendBase.value && p < 96) return 'Report to base'
 return 'Continue inspection'
})
const outcome = computed(() => {
 if (clear.value) return 'Clear runway'
 if (skipCrack.value) return hasCrack.value ? 'FOD sent; crack missed' : 'FOD sent; crack check skipped'
 if (hasFod.value && hasCrack.value) return 'FOD to UGV; crack to base'
 if (hasFod.value) return mode.value === 'sequential1' ? 'FOD to UGV; no-crack report to base' : 'FOD to UGV; no crack'
 return hasCrack.value ? 'Crack reported' : 'Unknown anomaly reported'
})
const droneX = computed(() => 105 + Math.min(progress.value / 45, 1) * 305)
function stop() { if (timer) clearInterval(timer); timer = undefined; playing.value = false }
function play() {
 if (playing.value) { stop(); return }
 if (progress.value >= 100) progress.value = 0
 playing.value = true
 timer = setInterval(() => { progress.value = Math.min(100, progress.value + .5); if (progress.value >= 100) stop() }, 50)
}
function reset() { stop(); progress.value = 0 }
watch([mode, scenario], reset)
onUnmounted(stop)
</script>

<template>
 <section class="pipeline-demo" aria-label="Interactive computer vision pipeline illustration">
  <div class="pipeline-heading"><h4>Pipeline demo</h4><span class="pipeline-demo-tag">Illustrative</span></div>
  <div class="pipeline-controls">
   <div class="pipeline-modes" role="group" aria-label="Execution architecture"><button v-for="item in modes" :key="item.id" type="button" :aria-pressed="mode === item.id" @click="mode = item.id">{{ item.label }}</button></div>
   <label class="pipeline-scenario"><span>Scenario</span> <select v-model="scenario"><option v-for="item in scenarios" :key="item.id" :value="item.id">{{ item.label }}</option></select></label>
  </div>
  <div class="pipeline-runway">
   <svg viewBox="0 0 760 230" role="img" :aria-label="`Drone inspecting a runway: ${stage}`">
    <defs><linearGradient id="pipeline-asphalt" x2="0" y2="1"><stop stop-color="#19212c"/><stop offset="1" stop-color="#090e15"/></linearGradient><radialGradient id="pipeline-light"><stop stop-color="#86dcff" stop-opacity=".25"/><stop offset="1" stop-color="#86dcff" stop-opacity="0"/></radialGradient></defs>
    <rect width="760" height="230" fill="#060a10"/>
    <path d="M40 30H720L755 205H5Z" fill="url(#pipeline-asphalt)" stroke="#354151"/>
    <path d="M65 46H695M34 187H726" stroke="#a9d8ff" stroke-opacity=".35"/>
    <path d="M50 117H710" stroke="#c4d1dd" stroke-opacity=".35" stroke-width="4" stroke-dasharray="32 22"/>
    <g v-for="x in [65, 135, 205, 275, 345, 415, 485, 555, 625, 695]" :key="x"><circle :cx="x" cy="42" r="3" fill="#92caff"/><circle :cx="x" cy="191" r="3" fill="#92caff"/></g>
    <g :transform="`translate(${droneX} 103)`"><ellipse cy="25" rx="90" ry="72" fill="url(#pipeline-light)"/><path d="M-23-16L23 16M23-16L-23 16" stroke="#bd927c" stroke-width="6"/><rect x="-12" y="-9" width="24" height="18" rx="6" fill="#d9b8a5"/><g v-for="(pos, i) in [[-25,-18],[25,-18],[-25,18],[25,18]]" :key="i"><ellipse :cx="pos[0]" :cy="pos[1]" rx="15" ry="8" fill="#101a25" stroke="#cee4f2" stroke-width="2"/></g><circle r="3" fill="#8cd9ff"/></g>
    <g v-if="!clear" transform="translate(452 139)"><path v-if="hasCrack" d="M-15-7L-3-2L-7 5L7 8L17 18" fill="none" stroke="#d7b9a7" stroke-width="4"/><path v-else-if="scenario === 'unknown'" d="M-11-8L9-12L17 8L-2 14L-15 5Z" fill="#bfa7d7"/><rect v-if="hasFod" x="-12" y="-6" width="24" height="12" rx="3" transform="rotate(-20)" fill="#d6ac6a"/>
     <rect v-if="progress >= 20" x="-27" y="-25" width="56" height="55" rx="5" fill="none" :stroke="progress >= 45 ? '#4cdb9b' : '#8bd6ff'" stroke-width="2" stroke-dasharray="5 4"/>
    </g>
    <text x="28" y="220" fill="#b0c4d6" font-size="11" letter-spacing="2">SCHEMATIC RUNWAY VIEW</text><text v-if="progress >= 20 && !clear" x="490" y="160" fill="#9de5cb" font-size="12">{{ progress >= 45 ? 'ANOMALY CROP' : 'CAPTURED REGION' }}</text>
   </svg>
  </div>
  <div class="pipeline-scrubber"><button type="button" class="pipeline-play" :aria-label="playing ? 'Pause pipeline demo' : 'Play pipeline demo'" @click="play">{{ playing ? 'Pause' : 'Play' }}</button><label class="pipeline-range"><span>Progress <strong>{{ Math.round(progress) }}%</strong></span><input v-model.number="progress" type="range" min="0" max="100" step="0.5" aria-label="Inspection progress" :aria-valuetext="`${Math.round(progress)} percent: ${stage}`" @input="stop" /></label><button type="button" class="pipeline-reset" @click="reset">Reset</button></div>
  <p class="pipeline-stage" aria-live="off">{{ stage }}</p>
  <div class="pipeline-map" :aria-label="mode === 'parallel' ? 'Parallel model checks, then coordinate extraction and reporting' : 'YOLO first, then crack checks, coordinate extraction and reporting'">
   <svg class="pipeline-arrows" viewBox="0 0 600 306" preserveAspectRatio="none" aria-hidden="true">
    <defs><marker id="pipeline-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="context-stroke" /></marker></defs>
    <path v-if="!clear" d="M300 54V68H92V83" :class="branchState('yolo')" />
    <path v-if="!clear && mode === 'parallel'" d="M300 68H508V83" :class="branchState('unet')" />
    <path v-if="!clear && mode !== 'parallel'" d="M184 111H415" :class="branchState('unet')" />
    <path v-if="!clear" d="M92 138V167" :class="coordinateState" />
    <path v-if="!clear" d="M92 222V251" :class="ugvState" />
    <path v-if="!clear" d="M184 279H207" :class="ugvState" />
    <path v-if="!clear" d="M508 138V167" :class="baseState" />
    <path v-if="!clear" d="M508 222V279H393" :class="baseState" />
    <path v-if="clear" d="M300 54V251" :class="progress >= 45 ? 'done' : 'waiting'" />
   </svg>
   <span v-if="!clear && mode !== 'parallel'" class="pipeline-route-label pipeline-model-route">{{ mode === 'sequential2' ? 'No FOD' : 'then' }}</span>
   <span v-if="!clear" class="pipeline-route-label pipeline-fod-route">FOD</span>
   <span v-if="clear" class="pipeline-route-label pipeline-clear-route">No anomaly</span>
   <div class="pipeline-node pipeline-patchcore" :class="progress >= 45 ? 'done' : progress >= 20 ? 'active' : 'waiting'"><strong>PatchCore</strong><span>{{ progress >= 45 ? clear ? 'Clear' : 'Crop ready' : progress >= 20 ? 'Checking' : 'Waiting' }}</span></div>
   <div class="pipeline-node pipeline-yolo" :class="branchState('yolo')"><strong>YOLO</strong><span>{{ branchState('yolo') === 'skipped' ? 'Skipped' : branchState('yolo') === 'done' ? hasFod ? 'FOD found' : 'No FOD' : branchState('yolo') === 'active' ? 'Checking' : 'Waiting' }}</span></div>
   <div class="pipeline-node pipeline-unet" :class="branchState('unet')"><strong>U-Net</strong><span>{{ branchState('unet') === 'skipped' ? 'Skipped' : branchState('unet') === 'done' ? hasCrack ? 'Crack found' : 'No crack' : branchState('unet') === 'active' ? 'Checking' : 'Waiting' }}</span></div>
   <div class="pipeline-node pipeline-coordinates" :class="coordinateState"><strong>Coordinates</strong><span>{{ coordinateState === 'done' ? 'Extracted' : coordinateState === 'active' ? 'Extracting' : coordinateState === 'skipped' ? 'Not needed' : 'Waiting' }}</span></div>
   <div class="pipeline-node pipeline-base" :class="baseState"><strong>Base</strong><span>{{ baseState === 'done' ? hasCrack ? 'Crack sent' : hasFod ? 'No-crack sent' : 'Review sent' : baseState === 'active' ? 'Sending' : baseState === 'skipped' ? 'Not needed' : 'Waiting' }}</span></div>
   <div class="pipeline-node pipeline-ugv" :class="ugvState"><strong>UGV</strong><span>{{ ugvState === 'done' ? 'Coords sent' : ugvState === 'active' ? 'Sending' : ugvState === 'skipped' ? 'Not needed' : 'Waiting' }}</span></div>
   <div class="pipeline-node pipeline-output" :class="progress >= (clear ? 45 : 96) ? 'done' : 'waiting'"><strong>Continue</strong><span>{{ progress >= (clear ? 45 : 96) ? 'Next frame' : 'Waiting' }}</span></div>
  </div>
  <p class="pipeline-summary" aria-live="off">{{ progress >= (clear ? 45 : 96) ? outcome : mode === 'sequential2' ? 'Sequential 2 skips U-Net when FOD is found.' : 'Both models check each crop.' }}</p>
  <p class="pipeline-note">Illustration only; no live models or coordinates.</p>
 </section>
</template>

<style scoped>
.pipeline-demo{margin:24px 0;padding:16px;border:1px solid var(--vp-c-divider);border-radius:16px;background:var(--vp-c-bg-soft);color:var(--vp-c-text-1);overflow:hidden}
.pipeline-heading{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:10px}
.pipeline-heading h4{font-size:23px;line-height:1.2;margin:0;letter-spacing:-.5px}
.pipeline-demo-tag{font-size:11px;color:var(--vp-c-text-2)}
.pipeline-controls{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;margin-bottom:10px}
.pipeline-modes{display:flex;flex-wrap:wrap;gap:2px;padding:3px;border:1px solid var(--vp-c-divider);border-radius:9px}
.pipeline-modes button,.pipeline-play,.pipeline-reset{font:inherit;font-size:13px;line-height:1.4;padding:7px 9px;border-radius:6px;cursor:pointer;color:inherit}
.pipeline-modes button[aria-pressed=true]{background:rgba(189,146,124,.2)}
.pipeline-scenario{display:flex;align-items:center;gap:7px;font-size:13px}
.pipeline-scenario select{font:inherit;appearance:auto;padding:6px 8px;border:1px solid var(--vp-c-divider);border-radius:7px;background:var(--vp-c-bg);color:inherit}
.pipeline-runway{border:1px solid #34404d;border-radius:9px;overflow:hidden;background:#060a10}
.pipeline-runway svg{display:block;width:100%;height:120px;object-fit:contain}
.pipeline-scrubber{display:flex;gap:10px;align-items:center;margin-top:10px}
.pipeline-play{background:#bd927c;color:#141014;min-width:52px;font-weight:600}
.pipeline-reset{border:1px solid var(--vp-c-divider)}
.pipeline-range{flex:1;min-width:0}.pipeline-range>span{display:flex;justify-content:space-between;gap:8px;font-size:12px}
.pipeline-range input{display:block;width:100%;margin:5px 0 0;accent-color:#bd927c}
.vp-doc .pipeline-demo .pipeline-stage{margin:8px 0;font-size:14px;line-height:1.4;min-height:20px;font-weight:600}
.pipeline-map{position:relative;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:4%;grid-template-rows:repeat(4,54px);row-gap:30px;height:306px}
.pipeline-arrows{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none}
.pipeline-arrows>path{fill:none;stroke:#82909e;stroke-width:2;vector-effect:non-scaling-stroke;marker-end:url(#pipeline-arrow)}
.pipeline-arrows>path.active{stroke:#bd927c}.pipeline-arrows>path.done{stroke:#259369}.pipeline-arrows>path.skipped{stroke-dasharray:4 4;opacity:.5}
.pipeline-node{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;padding:5px;border:1px solid var(--vp-c-divider);border-radius:8px;background:var(--vp-c-bg);min-width:0;text-align:center;z-index:1}
.pipeline-node strong{font-size:15px;line-height:1.2}.pipeline-node span{font-size:12px;line-height:1.2;color:var(--vp-c-text-2)}
.pipeline-node.active{border-color:#bd927c;background:var(--vp-c-brand-soft)}.pipeline-node.done{border-color:#328565}.pipeline-node.skipped{border-style:dashed;opacity:.55}
.pipeline-patchcore{grid-area:1/2}.pipeline-yolo{grid-area:2/1}.pipeline-unet{grid-area:2/3}.pipeline-coordinates{grid-area:3/1}.pipeline-base{grid-area:3/3}.pipeline-ugv{grid-area:4/1}.pipeline-output{grid-area:4/2}
.pipeline-route-label{position:absolute;z-index:1;background:var(--vp-c-bg-soft);padding:0 4px;font-size:10px;line-height:14px;color:var(--vp-c-text-2);transform:translateX(-50%)}
.pipeline-model-route{left:50%;top:91px}.pipeline-fod-route{left:15.333%;top:145px}.pipeline-clear-route{left:50%;top:145px}
.vp-doc .pipeline-demo .pipeline-summary{font-size:13px;line-height:1.4;margin:8px 0 0;min-height:19px}
.vp-doc .pipeline-demo .pipeline-note{font-size:11px;line-height:1.4;color:var(--vp-c-text-2);margin:5px 0 0}
.pipeline-demo button:focus-visible,.pipeline-demo select:focus-visible,.pipeline-demo input:focus-visible{outline:2px solid #bd927c;outline-offset:3px}
@media(max-width:650px){.pipeline-demo{padding:12px}.pipeline-heading h4{font-size:21px}.pipeline-controls{gap:7px}.pipeline-modes button{font-size:12px;padding:6px 8px}.pipeline-scenario{font-size:12px}.pipeline-runway svg{height:82px}.pipeline-node strong{font-size:13px}.pipeline-node span{font-size:11px}.pipeline-scrubber{gap:7px}.pipeline-play,.pipeline-reset{font-size:12px;padding:6px 8px}.pipeline-map{grid-template-rows:repeat(4,46.588px);row-gap:25.882px;height:264px}.pipeline-model-route{top:80px}.pipeline-fod-route,.pipeline-clear-route{top:125px}}
</style>
