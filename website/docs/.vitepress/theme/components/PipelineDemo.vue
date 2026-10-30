<script setup lang="ts">
import { computed, onUnmounted, ref } from 'vue'
const progress = ref(0)
const mode = ref('parallel')
const scenario = ref('fod')
const playing = ref(false)
let timer: ReturnType<typeof setInterval> | undefined
const scenarios = [ { id: 'fod', label: 'FOD object' }, { id: 'crack', label: 'Surface crack' }, { id: 'unknown', label: 'Unknown anomaly' } ]
const branchesDone = computed(() => progress.value >= 80)
const branchState = (branch: string) => {
 const start = mode.value === 'parallel' || branch === 'yolo' ? 45 : 63
 const end = mode.value === 'parallel' || branch === 'unet' ? 80 : 63
 return progress.value >= end ? 'done' : progress.value >= start ? 'active' : 'waiting'
}
const stage = computed(() => progress.value < 20 ? 'Inspect the runway' : progress.value < 45 ? 'PatchCore finds an unusual region' : progress.value < 80 ? mode.value === 'parallel' ? 'YOLO and U-Net inspect the crop in parallel' : progress.value < 63 ? 'YOLO inspects the crop first' : 'U-Net checks the same crop next' : 'Send the result to the next system')
const outcome = computed(() => scenario.value === 'fod' ? 'FOD identified \u2192 coordinates to UGV' : scenario.value === 'crack' ? 'Crack mask \u2192 report to base station' : 'Unknown anomaly \u2192 base station review')
const droneX = computed(() => 105 + Math.min(progress.value / 45, 1) * 305)
function stop() { if (timer) clearInterval(timer); timer = undefined; playing.value = false }
function play() {
 if (playing.value) { stop(); return }
 if (progress.value >= 100) progress.value = 0
 playing.value = true
 timer = setInterval(() => { progress.value = Math.min(100, progress.value + .5); if (progress.value >= 100) stop() }, 50)
}
function reset() { stop(); progress.value = 0 }
onUnmounted(stop)
</script>

<template>
 <section class="pipeline-demo" aria-label="Interactive computer vision pipeline illustration">
  <div class="pipeline-heading"><div><span class="pipeline-eyebrow">FOD ARGUS / PIPELINE EXPLORER</span><h4>Follow an anomaly.</h4></div><span class="pipeline-demo-tag">Illustrative demo</span></div>
  <p class="pipeline-intro">Move the slider to follow a runway inspection, from image capture to the final result.</p>
  <div class="pipeline-controls">
   <div class="pipeline-modes" role="group" aria-label="Execution architecture"><button v-for="item in ['parallel', 'sequential']" :key="item" type="button" :aria-pressed="mode === item" @click="mode = item">{{ item === 'parallel' ? 'Parallel' : 'Sequential fallback' }}</button></div>
   <label class="pipeline-scenario"><span>Change here</span> <select v-model="scenario"><option v-for="item in scenarios" :key="item.id" :value="item.id">{{ item.label }}</option></select></label>
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
    <g transform="translate(452 139)"><path v-if="scenario === 'crack'" d="M-15-7L-3-2L-7 5L7 8L17 18" fill="none" stroke="#d7b9a7" stroke-width="4"/><path v-else-if="scenario === 'unknown'" d="M-11-8L9-12L17 8L-2 14L-15 5Z" fill="#bfa7d7"/><rect v-else x="-12" y="-6" width="24" height="12" rx="3" transform="rotate(-20)" fill="#d6ac6a"/>
     <rect v-if="progress >= 20" x="-27" y="-25" width="56" height="55" rx="5" fill="none" :stroke="progress >= 45 ? '#4cdb9b' : '#8bd6ff'" stroke-width="2" stroke-dasharray="5 4"/>
    </g>
    <text x="28" y="220" fill="#b0c4d6" font-size="11" letter-spacing="2">SCHEMATIC RUNWAY VIEW</text><text v-if="progress >= 20" x="490" y="160" fill="#9de5cb" font-size="12">{{ progress >= 45 ? 'ANOMALY CROP' : 'CAPTURED REGION' }}</text>
   </svg>
  </div>
  <div class="pipeline-scrubber"><button type="button" class="pipeline-play" :aria-label="playing ? 'Pause pipeline demo' : 'Play pipeline demo'" @click="play">{{ playing ? 'Pause' : 'Play' }}</button><label class="pipeline-range"><span>Inspection progress <strong>{{ Math.round(progress) }}%</strong></span><input v-model.number="progress" type="range" min="0" max="100" step="0.5" aria-label="Inspection progress" :aria-valuetext="`${Math.round(progress)} percent: ${stage}`" @input="stop" /></label><button type="button" class="pipeline-reset" @click="reset">Reset</button></div>
  <p class="pipeline-stage" aria-live="off">{{ stage }}</p>
  <div class="pipeline-flow">
   <div class="pipeline-node" :class="progress >= 45 ? 'done' : progress >= 20 ? 'active' : 'waiting'"><small>01 / ANOMALY DETECTION</small><strong>PatchCore</strong><span>{{ progress >= 45 ? 'Unusual region cropped' : progress >= 20 ? 'Compare with normal surface' : 'Waiting for an image' }}</span></div>
   <div class="pipeline-branches" :class="{ sequential: mode === 'sequential' }">
    <div class="pipeline-node" :class="branchState('yolo')"><small>02 / OBJECT DETECTION</small><strong>YOLO</strong><span>{{ branchState('yolo') === 'done' ? scenario === 'fod' ? 'FOD identified' : 'No known FOD identified' : branchState('yolo') === 'active' ? 'Inspect the anomaly crop' : 'Waiting for crop' }}</span></div>
    <div class="pipeline-node" :class="branchState('unet')"><small>{{ mode === 'sequential' ? '03' : '02' }} / CRACK SEGMENTATION</small><strong>U-Net</strong><span>{{ branchState('unet') === 'done' ? scenario === 'crack' ? 'Crack mask produced' : 'No crack identified' : branchState('unet') === 'active' ? 'Check the crop for cracks' : 'Waiting for crop' }}</span></div>
   </div>
   <div class="pipeline-node pipeline-output" :class="branchesDone ? 'done' : 'waiting'"><small>OUTPUT / NEXT ACTION</small><strong>{{ branchesDone ? scenario === 'fod' ? 'Send to UGV' : 'Send to base' : 'Await both models' }}</strong><span>{{ branchesDone ? outcome : 'Both detectors check every anomaly crop' }}</span></div>
  </div>
  <p class="pipeline-note">This demo illustrates the RGB pipeline. Slider speed and example detections are illustrative; no AI models run here. Thermal safety operates separately.</p>
 </section>
</template>

<style scoped>
.pipeline-demo{margin:32px 0;padding:26px;border:1px solid var(--vp-c-divider);border-radius:22px;background:var(--vp-c-bg-soft);overflow:hidden}
.pipeline-heading{display:flex;align-items:flex-start;justify-content:space-between;gap:15px}.pipeline-eyebrow{font-size:10px;letter-spacing:1.7px;color:var(--vp-c-text-2)}.pipeline-heading h4{margin:9px 0;font-size:32px;line-height:1.2;letter-spacing:-1px}.pipeline-demo-tag{font-size:10px;border:1px solid var(--vp-c-divider);padding:5px 10px;border-radius:30px;white-space:nowrap;color:var(--vp-c-text-2)}
.vp-doc .pipeline-demo .pipeline-intro{font-size:15px;line-height:1.65;margin:8px 0 20px}.pipeline-controls{display:flex;flex-wrap:wrap;justify-content:space-between;gap:15px;align-items:center;margin-bottom:20px}.pipeline-modes{display:flex;gap:4px;padding:4px;border:1px solid var(--vp-c-divider);border-radius:12px}.pipeline-modes button,.pipeline-play,.pipeline-reset{font:inherit;font-size:12px;line-height:1.5;padding:8px 12px;border-radius:8px;cursor:pointer}.pipeline-modes button[aria-pressed=true]{background:rgba(189,146,124,.19);color:var(--vp-c-text-1)}.pipeline-scenario{display:flex;align-items:center;gap:10px;font-size:12px;color:var(--vp-c-text-2)}.pipeline-scenario select{background:var(--vp-c-bg);color:var(--vp-c-text-1);padding:8px;border:1px solid var(--vp-c-divider);border-radius:8px;font:inherit}.pipeline-runway{border:1px solid #34404d;border-radius:14px;overflow:hidden}.pipeline-runway svg{display:block;width:100%;height:auto}.pipeline-scrubber{display:flex;align-items:center;gap:16px;margin-top:20px}.pipeline-play{background:#bd927c;color:#141014;min-width:62px;font-weight:650}.pipeline-reset{border:1px solid var(--vp-c-divider);color:var(--vp-c-text-2)}.pipeline-range{flex:1;min-width:0}.pipeline-range>span{display:flex;justify-content:space-between;font-size:12px;gap:8px;color:var(--vp-c-text-2)}.pipeline-range input{display:block;width:100%;margin:10px 0 0;accent-color:#bd927c;cursor:ew-resize}.vp-doc .pipeline-demo .pipeline-stage{font-size:16px;font-weight:600;line-height:1.5;min-height:48px;margin:20px 0}.pipeline-flow{display:grid;grid-template-columns:1fr 1.2fr 1fr;gap:12px;align-items:stretch}.pipeline-branches{display:flex;flex-direction:column;gap:10px}.pipeline-node{border:1px solid var(--vp-c-divider);border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:8px;justify-content:center;min-width:0;transition:border-color .2s,background .2s}.pipeline-node small{font-size:9px;letter-spacing:1px;line-height:1.5;color:var(--vp-c-text-2)}.pipeline-node strong{font-size:18px;line-height:1.3}.pipeline-node span{font-size:12px;line-height:1.6;color:var(--vp-c-text-2)}.pipeline-node.active{border-color:#bd927c;background:rgba(189,146,124,.12)}.pipeline-node.done{border-color:#328565;background:rgba(55,165,113,.08)}.pipeline-node.done small{color:#168250}.dark .pipeline-node.done small{color:#77d8ad}.pipeline-node.waiting{opacity:.65}.pipeline-branches.sequential{position:relative}.pipeline-branches.sequential:after{content:'\2193';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:#bd927c;background:var(--vp-c-bg-soft);line-height:1;padding:0 6px}.vp-doc .pipeline-demo .pipeline-note{font-size:12px;line-height:1.7;margin:20px 0 0;color:var(--vp-c-text-2)}.pipeline-demo button:focus-visible,.pipeline-demo select:focus-visible,.pipeline-demo input:focus-visible{outline:2px solid #bd927c;outline-offset:4px}
@media(max-width:650px){.pipeline-demo{padding:17px}.pipeline-heading{flex-wrap:wrap}.pipeline-heading h4{font-size:28px}.pipeline-flow{grid-template-columns:1fr}.pipeline-branches{display:grid;grid-template-columns:1fr 1fr}.pipeline-branches.sequential{display:flex}.pipeline-scrubber{gap:10px}.pipeline-node{padding:13px}.pipeline-stage{min-height:48px}}
/* Larger controls and copy keep the demo readable in the report. */
.pipeline-demo{--pipeline-copy:var(--vp-c-text-1)}
.dark .pipeline-demo{--pipeline-copy:#f5f7fa}
.pipeline-eyebrow{font-size:12px;color:var(--pipeline-copy)}
.pipeline-demo-tag{font-size:12px;color:var(--pipeline-copy)}
.vp-doc .pipeline-demo .pipeline-intro{font-size:18px;color:var(--pipeline-copy)}
.pipeline-modes button,.pipeline-play,.pipeline-reset{font-size:15px;color:var(--pipeline-copy)}
.pipeline-play{color:#141014}
.pipeline-scenario{font-size:16px;font-weight:600;color:var(--pipeline-copy)}
.pipeline-scenario select{appearance:auto;min-width:175px;font-size:16px;font-weight:500;color:var(--pipeline-copy);padding:10px 13px;border-color:#bd927c;animation:pipeline-select-pulse 2.6s ease-in-out infinite}
.pipeline-range>span{font-size:15px;color:var(--pipeline-copy)}
.vp-doc .pipeline-demo .pipeline-stage{font-size:19px;color:var(--pipeline-copy)}
.pipeline-node small{font-size:11px;color:var(--pipeline-copy)}
.pipeline-node strong{font-size:21px;color:var(--pipeline-copy)}
.pipeline-node span{font-size:15px;color:var(--pipeline-copy)}
.pipeline-node.waiting{opacity:1}
.vp-doc .pipeline-demo .pipeline-note{font-size:14px;color:var(--pipeline-copy)}
@keyframes pipeline-select-pulse{0%,100%{box-shadow:0 0 0 0 rgba(189,146,124,.08)}50%{box-shadow:0 0 0 5px rgba(189,146,124,.22)}}
@media(max-width:650px){.pipeline-modes button{font-size:14px;padding:8px 10px}.pipeline-range>span{font-size:13px}.pipeline-node strong{font-size:20px}.pipeline-play,.pipeline-reset{font-size:14px;padding:8px 10px}.pipeline-controls{gap:20px}.pipeline-scenario{flex-wrap:wrap}.vp-doc .pipeline-demo .pipeline-intro{font-size:17px}}
@media(prefers-reduced-motion:reduce){.pipeline-node{transition:none}.pipeline-scenario select{animation:none}}

</style>
