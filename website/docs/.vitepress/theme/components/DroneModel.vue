<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { withBase } from 'vitepress'
import type { ModelViewerElement } from '@google/model-viewer'
const cameraOrbit = ref('-35deg 58deg 80%')
const viewer = ref<ModelViewerElement | null>(null)
const ready = ref(false)
const loading = ref(true)
const failed = ref(false)
const progress = ref(0)
const rotating = ref(false)
let motionPreference: MediaQueryList | undefined
let layoutPreference: MediaQueryList | undefined
function updateFraming() { cameraOrbit.value = layoutPreference?.matches ? '-35deg 58deg 105%' : '-35deg 58deg 80%' }
let disposed = false
function motionChanged() { if (motionPreference?.matches) rotating.value = false }
async function initialise() {
 ready.value = false
 failed.value = false
 loading.value = true
 progress.value = 0
 try {
  const environment = window as unknown as { ModelViewerElement?: { dracoDecoderLocation?: string } }
  environment.ModelViewerElement ??= {}
  environment.ModelViewerElement.dracoDecoderLocation = withBase('/decoders/draco/')
  const { ModelViewerElement } = await import('@google/model-viewer')
  ModelViewerElement.dracoDecoderLocation = withBase('/decoders/draco/')
  if (!disposed) ready.value = true
 } catch { if (!disposed) onError() }
}
function onProgress(event: Event) {
 const value = (event as CustomEvent<{ totalProgress: number }>).detail.totalProgress
 progress.value = Math.round(value * 100)
}
function onError() { failed.value = true; loading.value = false }
function resetView() {
 if (!viewer.value) return
 viewer.value.cameraOrbit = cameraOrbit.value
 viewer.value.cameraTarget = 'auto auto auto'
 viewer.value.fieldOfView = '30deg'
 viewer.value.jumpCameraToGoal()
}
onMounted(() => {
 layoutPreference = window.matchMedia('(max-width: 767px)')
 updateFraming()
 layoutPreference.addEventListener('change', updateFraming)
 motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)')
 rotating.value = !motionPreference.matches
 motionPreference.addEventListener('change', motionChanged)
 initialise()
})
onUnmounted(() => {
 disposed = true
 motionPreference?.removeEventListener('change', motionChanged)
 layoutPreference?.removeEventListener('change', updateFraming)
})
</script>
<template>
 <div class="drone-model">
  <div class="drone-model-stage" :aria-busy="loading">
   <model-viewer v-if="ready && !failed" ref="viewer" class="drone-viewer" :src="withBase('/models/FOD_Argus.glb')" alt="Interactive 3D SolidWorks assembly of the FOD ARGUS runway inspection drone" camera-controls disable-pan touch-action="pan-y" :auto-rotate="rotating ? '' : null" rotation-per-second="12deg" :camera-orbit="cameraOrbit" field-of-view="30deg" min-camera-orbit="auto 15deg 40%" max-camera-orbit="auto 100deg 180%" environment-image="neutral" tone-mapping="neutral" exposure="0.15" shadow-intensity="0.65" shadow-softness="1" interaction-prompt="none" loading="eager" reveal="auto" @load="loading = false" @error="onError" @progress="onProgress">
    <span slot="progress-bar"></span>
   </model-viewer>
   <div v-if="loading" class="model-loading" role="status"><span class="model-loading-ring" aria-hidden="true"></span><span>Loading FOD ARGUS<span v-if="progress > 0"> &middot; {{ progress }}%</span></span></div>
   <div v-if="failed" class="model-error" role="status"><p>The 3D model could not be displayed.</p><button type="button" @click="initialise">Try again</button></div>
  </div>
  <div class="model-caption"><span class="model-caption-cross" aria-hidden="true">+</span><div><strong>FOD ARGUS</strong><span>Interactive 3D model (use mouse to rotate)</span></div></div>
  <div v-if="ready && !loading && !failed" class="model-toolbar"><span class="model-gesture-hint">Drag to rotate &middot; Pinch or scroll to zoom</span><div><button type="button" :aria-pressed="rotating" @click="rotating = !rotating">{{ rotating ? 'Pause rotation' : 'Rotate model' }}</button><button type="button" @click="resetView">Reset view</button></div></div>
 </div>
</template>