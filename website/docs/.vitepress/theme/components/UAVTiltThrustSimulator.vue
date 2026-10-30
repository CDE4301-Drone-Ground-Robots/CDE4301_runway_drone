<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, useId, watch } from 'vue'
import { calculateTiltThrust, DESIGN_TILT_DEGREES } from './uav-thrust'
import type { createTiltScene } from './uav-tilt-scene'

const id = useId()
const pitch = ref(0)
const roll = ref(0)
const mass = ref(5)
const showVectors = ref(true)
const result = computed(() => calculateTiltThrust(pitch.value, roll.value, mass.value))
const host = ref<HTMLElement | null>(null)
const state = ref<'waiting' | 'loading' | 'ready' | 'error'>('waiting')
let view: ReturnType<typeof createTiltScene> | undefined
let observer: IntersectionObserver | undefined
let disposed = false
let visible = false

const format = (value: number, places = 2) => value.toFixed(places)
const sync = () => view?.update(pitch.value, roll.value, result.value.thrustRatio, showVectors.value)
watch([pitch, roll, mass, showVectors], sync)
function reset() { pitch.value = 0; roll.value = 0; mass.value = 5 }
function designPreset() { pitch.value = DESIGN_TILT_DEGREES; roll.value = 0 }
async function initialise() {
 if (!host.value || disposed || state.value === 'loading') return
 state.value = 'loading'
 view?.dispose()
 view = undefined
 try {
  // Three.js is split into a client-only chunk and loaded near the viewport.
  const { createTiltScene } = await import('./uav-tilt-scene')
  if (disposed || !host.value) return
  view = createTiltScene(host.value, () => { state.value = 'error' })
  view.setVisible(visible)
  sync()
  state.value = 'ready'
 } catch { if (!disposed) state.value = 'error' }
}
onMounted(() => {
 observer = new IntersectionObserver(entries => {
  visible = entries[0].isIntersecting
  view?.setVisible(visible)
  if (visible && state.value === 'waiting') initialise()
 }, { rootMargin: '200px' })
 if (host.value) observer.observe(host.value)
})
onUnmounted(() => { disposed = true; observer?.disconnect(); view?.dispose() })
</script>

<template>
 <section class="uav-simulator" aria-label="Interactive UAV attitude and thrust simulator">
  <div class="sim-heading"><span>PRELIMINARY THRUST SIZING</span><span>4 MOTORS / YAW = 0°</span></div>
  <div class="sim-layout">
   <div class="sim-visual">
    <div class="sim-stage-wrap">
     <div ref="host" class="sim-stage" :aria-busy="state === 'waiting' || state === 'loading'"></div>
     <div v-if="state !== 'ready'" class="sim-fallback" role="status">
      <template v-if="state === 'error'"><strong>3D view unavailable</strong><span>WebGL may be unavailable or its context was lost. All controls and calculations still work.</span><button type="button" @click="initialise">Retry 3D view</button></template>
      <template v-else><strong>Interactive X-frame quadcopter</strong><span>{{ state === 'loading' ? 'Loading the 3D view…' : 'The 3D view loads when this panel is in view.' }}</span></template>
     </div>
     <div class="sim-attitude-readout" aria-hidden="true"><span>θ {{ format(pitch, 0) }}°</span><span>φ {{ format(roll, 0) }}°</span><strong>β {{ format(result.tiltDegrees, 1) }}°</strong></div>
    </div>
    <div class="sim-legend"><span><i class="sim-cyan"></i>Thrust T</span><span><i class="sim-orange"></i>Weight W</span><span><i class="sim-vertical"></i>World vertical</span></div>
    <p class="sim-view-hint">Drag to orbit · Scroll or pinch to zoom. The grid stays horizontal; the cyan nose marks the front.</p>
    <div class="sim-view-controls">
     <label><input v-model="showVectors" type="checkbox"> Show vectors &amp; β arc</label>
     <div><button type="button" :disabled="state !== 'ready'" aria-label="Orbit camera left" @click="view?.orbitCamera(-1)">↶</button><button type="button" :disabled="state !== 'ready'" aria-label="Orbit camera right" @click="view?.orbitCamera(1)">↷</button><button type="button" :disabled="state !== 'ready'" @click="view?.resetCamera()">Reset view</button></div>
    </div>
    <p class="sim-vector-note">Arrow lengths show the thrust-to-weight ratio, not an absolute force scale. The β arc measures tilt from the world vertical.</p>
   </div>
   <div class="sim-controls">
    <div class="sim-slider">
     <label :for="id + '-pitch'">Pitch angle (θ)<output :for="id + '-pitch'">{{ format(pitch, 0) }}°</output></label>
     <input :id="id + '-pitch'" v-model.number="pitch" name="pitch" type="range" min="-45" max="45" step="1" :aria-valuetext="pitch + ' degrees'">
     <div class="sim-range"><span>−45°</span><span>Nose up +</span><span>+45°</span></div>
    </div>
    <div class="sim-slider">
     <label :for="id + '-roll'">Roll angle (φ)<output :for="id + '-roll'">{{ format(roll, 0) }}°</output></label>
     <input :id="id + '-roll'" v-model.number="roll" name="roll" type="range" min="-45" max="45" step="1" :aria-valuetext="roll + ' degrees'">
     <div class="sim-range"><span>−45°</span><span>Right side down +</span><span>+45°</span></div>
    </div>
    <div class="sim-slider">
     <label :for="id + '-mass'">UAV mass<output :for="id + '-mass'">{{ format(mass, 1) }} kg</output></label>
     <input :id="id + '-mass'" v-model.number="mass" name="mass" type="range" min="3" max="7" step="0.1" :aria-valuetext="mass + ' kilograms'">
     <div class="sim-range"><span>3 kg</span><span>Baseline 5 kg</span><span>7 kg</span></div>
    </div>
    <div class="sim-presets"><button type="button" @click="reset">Reset to level</button><button type="button" @click="designPreset">45° Design Condition</button></div>
    <div class="sim-tilt" :class="{ 'sim-over-design': result.exceedsDesign }">
     <span>Combined tilt β</span><strong data-result="tilt">{{ format(result.tiltDegrees, 2) }}°</strong>
     <span>{{ format(result.thrustRatio, 3) }}× level-flight thrust</span>
    </div>
    <p class="sim-threshold" role="status">{{ result.exceedsDesign ? 'Selected attitude exceeds the preliminary 45° thrust-sizing assumption.' : 'Selected attitude is within the preliminary 45° thrust-sizing assumption.' }} This is not a verified operating limit.</p>
    <dl class="sim-results">
     <div><dt>UAV weight W</dt><dd data-result="weight">{{ format(result.weightN) }} N</dd></div>
     <div><dt>Total required thrust T</dt><dd data-result="total">{{ format(result.totalThrustN) }} N</dd></div>
     <div><dt>Average thrust per motor</dt><dd><span data-result="motor-n">{{ format(result.motorThrustN) }} N</span><small data-result="motor-kgf">{{ format(result.motorThrustKgf, 3) }} kgf</small></dd></div>
    </dl>
   </div>
  </div>

 </section>
</template>

<style scoped>
.uav-simulator { margin: 28px 0; border: 1px solid var(--vp-c-divider); border-radius: 16px; overflow: hidden; background: var(--vp-c-bg-soft); font-family: var(--vp-font-family-base); color: var(--vp-c-text-1); }
.sim-heading { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px; padding: 18px 22px; border-bottom: 1px solid var(--vp-c-divider); color: var(--vp-c-text-2); font-size: 12px; font-weight: 600; letter-spacing: 1.3px; }
.sim-layout { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); }
.sim-visual, .sim-controls { min-width: 0; }
.sim-visual { background: #0b121c; color: #e7edf4; }
.sim-stage-wrap { position: relative; }
.sim-stage { height: 420px; width: 100%; }
.sim-stage :deep(canvas) { display: block; max-width: 100%; touch-action: none; }
.sim-fallback { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 16px; padding: 28px; text-align: center; background: #0b121c; color: #dce6ef; font-size: 16px; line-height: 1.8; }
.sim-attitude-readout { position: absolute; top: 16px; left: 16px; right: 16px; display: flex; flex-wrap: wrap; gap: 8px 16px; pointer-events: none; font-size: 14px; font-variant-numeric: tabular-nums; }
.sim-attitude-readout strong { margin-left: auto; color: #8be1ee; }
.sim-legend { display: flex; flex-wrap: wrap; gap: 12px; padding: 12px 18px 0; font-size: 13px; color: #c1cdd9; }
.sim-legend > span { display: inline-flex; align-items: center; gap: 7px; }
.sim-legend i { width: 14px; height: 3px; display: inline-block; }
.sim-cyan { background: #68e4fa; }.sim-orange { background: #fa9d74; }.sim-vertical { border-top: 2px dashed #8d9db0; }
.uav-simulator .sim-view-hint, .uav-simulator .sim-vector-note { margin: 12px 18px; font-size: 14px; line-height: 1.75; color: #adbcca; }
.sim-view-controls { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 14px; padding: 6px 18px; font-size: 14px; }
.sim-view-controls label { display: flex; align-items: center; gap: 9px; cursor: pointer; }
.sim-view-controls > div { display: flex; gap: 6px; }
.uav-simulator button { padding: 8px 12px; min-height: 40px; border: 1px solid var(--vp-c-divider); border-radius: 8px; font-family: inherit; font-size: 14px; line-height: 1.6; font-weight: 500; background: var(--vp-c-bg); color: var(--vp-c-text-1); cursor: pointer; transition: border-color .15s; }
.sim-visual button { background: #172533; border-color: #365267; color: #d7e6ef; }
.uav-simulator button:hover:not(:disabled) { border-color: #6cabb8; }
.uav-simulator button:disabled { opacity: .45; cursor: default; }
.uav-simulator :is(button, input):focus-visible { outline: 2px solid #6cabb8; outline-offset: 3px; }
.sim-controls { padding: 24px; }
.sim-slider { margin-bottom: 22px; }
.sim-slider label { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap: 8px; font-size: 17px; font-weight: 600; line-height: 1.6; }
.sim-slider output { font-variant-numeric: tabular-nums; font-weight: 500; color: var(--vp-c-text-2); }
.sim-slider input { display: block; width: 100%; height: 30px; margin: 9px 0 0; cursor: pointer; accent-color: #599eac; }
.sim-range { display: flex; justify-content: space-between; gap: 8px; color: var(--vp-c-text-2); font-size: 12px; }
.sim-presets { display: flex; flex-wrap: wrap; gap: 10px; margin: 10px 0 22px; }
.sim-tilt { display: flex; flex-direction: column; padding: 18px; border: 1px solid #599eac66; border-radius: 12px; background: #599eac0d; font-size: 14px; line-height: 1.75; }
.sim-tilt > strong { font-family: Manrope, var(--vp-font-family-base); font-size: 38px; line-height: 1.3; font-weight: 750; font-variant-numeric: tabular-nums; }
.sim-tilt > span:last-child { color: var(--vp-c-text-2); }
.sim-over-design { border-color: #b7854e; background: #b7854e12; }
.uav-simulator .sim-threshold { font-size: 14px; line-height: 1.75; color: var(--vp-c-text-2); margin: 14px 0 20px; }
.sim-results { margin: 0; }
.sim-results > div { display: flex; justify-content: space-between; align-items: baseline; gap: 16px; padding: 12px 0; border-top: 1px solid var(--vp-c-divider); font-size: 16px; line-height: 1.75; }
.sim-results dt { color: var(--vp-c-text-2); }
.sim-results dd { margin: 0; text-align: right; font-weight: 600; white-space: nowrap; font-variant-numeric: tabular-nums; }
.sim-results small { display: block; font-size: 14px; color: var(--vp-c-text-2); font-weight: 400; }
@media (max-width: 1100px) { .sim-layout { grid-template-columns: 1fr; }.sim-stage { height: 390px; } }
@media (max-width: 767px) { .sim-heading { padding: 16px; font-size: 11px; }.sim-stage { height: 340px; }.sim-controls { padding: 20px 16px; }.sim-results > div { font-size: 15px; gap: 12px; } }
@media (prefers-reduced-motion: reduce) { .uav-simulator button { transition: none; } }
</style>
