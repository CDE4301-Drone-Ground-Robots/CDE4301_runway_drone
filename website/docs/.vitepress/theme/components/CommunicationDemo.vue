<script setup lang="ts">
import { computed, onUnmounted, ref } from 'vue'

type Fod = 'Battery' | 'Plastic part' | 'Bolt'
type Alert = { id: number; object: Fod; x: number; y: number }
const object = ref<Fod>('Battery')
const generated = ref(0)
const waiting = ref<Alert[]>([])
const current = ref<Alert | null>(null)
const sent = ref(0)
const received = ref(0)
const acknowledged = ref(0)
const awaitingAck = ref<Alert | null>(null)
const lastReceived = ref<Alert | null>(null)
const lastAck = ref<Alert | null>(null)
const status = ref('Add an example FOD alert to the ARGUS queue.')
const inTransit = ref<Alert | null>(null)
const outbound = computed(() => inTransit.value ?? awaitingAck.value)
let sequence = 0
let timer: ReturnType<typeof setTimeout> | undefined
const objects: Fod[] = ['Battery', 'Plastic part', 'Bolt']
const label = (alert: Alert) => 'FOD_THREAT_' + String(alert.id).padStart(3, '0')
const coordinates = (alert: Alert) => `(${alert.x.toFixed(1)}, ${alert.y.toFixed(1)}) m`

function transmit() {
 if (timer || inTransit.value || awaitingAck.value || !waiting.value.length) return
 const alert = waiting.value.shift()!
 inTransit.value = alert
 awaitingAck.value = alert
 sent.value++
 timer = setTimeout(() => {
  timer = undefined
  inTransit.value = null
  received.value++
  current.value = alert
  lastReceived.value = alert
  status.value = `${label(alert)} received. ARGUS is waiting for its receipt ACK.`
 }, 650)
}
function send(count = 1) {
 for (let i = 0; i < count; i++) {
  const id = ++sequence
  const alert: Alert = {
   id, object: count === 1 ? object.value : objects[i % objects.length],
   x: 3 + (id - 1) * 1.2, y: 4 + (id - 1) * 0.5
  }
  waiting.value.push(alert)
  generated.value++
 }
 status.value = `${count} example alert${count === 1 ? '' : 's'} added to the ARGUS queue.`
 transmit()
}
function acknowledge() {
 if (!current.value || current.value.id !== awaitingAck.value?.id) return
 const confirmed = current.value
 lastAck.value = confirmed
 acknowledged.value++
 current.value = null
 awaitingAck.value = null
 transmit()
 status.value = `ACK for ${label(confirmed)} returned to ARGUS. ${inTransit.value ? label(inTransit.value) + ' is being sent next.' : 'No pending alerts.'}`
}
function stop() { if (timer) clearTimeout(timer); timer = undefined }
function reset() {
 stop()
 sequence = 0
 generated.value = 0
 inTransit.value = null
 waiting.value = []
 current.value = null
 awaitingAck.value = null
 lastReceived.value = null
 lastAck.value = null
 sent.value = received.value = acknowledged.value = 0
 status.value = 'Add an example FOD alert to the ARGUS queue.'
}
onUnmounted(stop)
</script>

<template>
 <section class="com-demo" aria-label="Communication queue simulator">
  <div class="com-demo-heading"><h4>Alert delivery</h4><span>Illustrative</span></div>
  <div class="com-demo-controls">
   <label>Object <select v-model="object" aria-label="Example FOD object"><option v-for="item in objects" :key="item">{{ item }}</option></select></label>
   <button type="button" class="com-demo-primary" @click="send()">Add FOD</button>
   <button type="button" @click="send(3)">Add 3 FODs</button>
   <button type="button" class="com-demo-reset" @click="reset">Reset</button>
  </div>
  <div class="com-demo-flow">
   <div class="com-demo-node com-demo-queue">
    <span class="com-demo-kicker">ARGUS APPLICATION QUEUE</span><strong>{{ waiting.length }} waiting</strong>
    <ol v-if="waiting.length" aria-label="Waiting FOD targets on ARGUS"><li v-for="alert in waiting" :key="alert.id"><code>{{ label(alert) }}</code><span>{{ alert.object }}</span></li></ol>
    <span v-else>No waiting alerts</span>
    <span v-if="awaitingAck" class="com-demo-held">Retained until ACK:<br><code>{{ label(awaitingAck) }}</code></span>
   </div>
   <div class="com-demo-arrow" :class="{ busy: inTransit }" aria-hidden="true">&#8594;</div>
   <div class="com-demo-node" :class="{ busy: inTransit }">
    <span class="com-demo-kicker">ARGUS OUTGOING MESSAGE</span><strong>C2 alert</strong>
    <template v-if="outbound"><code>{{ label(outbound) }}</code><span>{{ outbound.object }}</span><span>{{ coordinates(outbound) }}</span></template>
    <span v-else>No target awaiting delivery</span>
   </div>
   <div class="com-demo-arrow" :class="{ busy: inTransit }" aria-hidden="true">&#8594;</div>
   <div class="com-demo-node com-demo-link" :class="{ busy: inTransit }">
    <span class="com-demo-kicker">ROS 2 / WI-FI</span><strong>{{ inTransit ? 'Sending' : awaitingAck ? 'Awaiting ACK' : 'Ready' }}</strong>
    <code v-if="inTransit">{{ label(inTransit) }}</code>
    <span>{{ inTransit ? 'ARGUS to HUNTER' : 'No alert in transit' }}</span>
   </div>
   <div class="com-demo-arrow" :class="{ busy: inTransit }" aria-hidden="true">&#8594;</div>
   <div class="com-demo-node" :class="{ active: current }">
    <span class="com-demo-kicker">HUNTER</span><strong>{{ current ? 'Confirm receipt' : lastReceived ? 'Receipt confirmed' : 'Ready to receive' }}</strong>
    <template v-if="lastReceived"><code>{{ label(lastReceived) }}</code><span>{{ lastReceived.object }}</span><span>{{ coordinates(lastReceived) }}</span></template>
    <span v-else>No alert received</span>
    <button type="button" :disabled="!current" @click="acknowledge">Acknowledge receipt</button>
   </div>
  </div>
  <div class="com-demo-ack" :class="{ active: lastAck }">ARGUS &#8592; {{ lastAck ? 'ACK: ' + label(lastAck) : 'Receipt ACK' }} &#8592; HUNTER</div>
  <div class="com-demo-stats" aria-label="Simulated alert counts"><span>Added <strong data-stat="added">{{ generated }}</strong></span><span>Sent <strong data-stat="sent">{{ sent }}</strong></span><span>Received <strong data-stat="received">{{ received }}</strong></span><span>Acknowledged <strong data-stat="acknowledged">{{ acknowledged }}</strong></span></div>
  <p class="com-demo-status" role="status">{{ status }}</p>
  <p class="com-demo-note">Planned receipt-ACK workflow. The button simulates HUNTER confirming receipt, which releases the next alert from ARGUS. It does not mean the FOD has been collected. No live ROS 2 link; timing is illustrative.</p>
 </section>
</template>

<style scoped>
.com-demo{margin:24px 0;padding:18px;border:1px solid var(--vp-c-divider);border-radius:14px;background:var(--vp-c-bg-soft);min-width:0}
.com-demo-heading{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px}
.vp-doc .com-demo h4{margin:0;font-size:22px;line-height:1.3;letter-spacing:-.5px}
.com-demo-heading>span{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--vp-c-text-2)}
.com-demo-controls{display:flex;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.com-demo-controls label{display:flex;align-items:center;gap:7px;font-size:13px}
.com-demo button,.com-demo select{border:1px solid var(--vp-c-divider);border-radius:7px;padding:7px 10px;background:var(--vp-c-bg);color:var(--vp-c-text-1);font:inherit;font-size:13px;line-height:1.4}
.com-demo select{padding-right:24px}
.com-demo button{cursor:pointer;font-weight:600}
.com-demo button:hover:not(:disabled){border-color:var(--vp-c-brand-1);background:var(--vp-c-brand-soft)}
.com-demo button:disabled{cursor:default;opacity:.45}
.com-demo-controls .com-demo-primary{background:var(--vp-c-brand-soft);border-color:var(--vp-c-brand-1)}
.com-demo-controls .com-demo-reset{margin-left:auto}
.com-demo-flow{display:grid;grid-template-columns:minmax(0,1fr) 24px minmax(0,1.2fr) 24px minmax(0,1fr) 24px minmax(0,1.15fr);align-items:stretch}
.com-demo-node{display:flex;flex-direction:column;align-items:center;justify-content:flex-start;gap:7px;min-width:0;min-height:180px;border:1px solid var(--vp-c-divider);border-radius:9px;padding:12px 7px;background:var(--vp-c-bg);text-align:center}
.com-demo-kicker{font-size:9px!important;letter-spacing:.7px;color:var(--vp-c-text-2);line-height:1.5}
.com-demo-node strong{font-size:15px;line-height:1.3}
.com-demo-node>span:not(.com-demo-kicker){font-size:12px;line-height:1.4;color:var(--vp-c-text-2)}
.vp-doc .com-demo code{font-size:10px;line-height:1.5;white-space:normal;overflow-wrap:anywhere;padding:1px 3px}
.com-demo-node>button{margin-top:auto;padding:5px 6px;font-size:12px;max-width:100%}
.com-demo-node.active{border-color:#328565;background:color-mix(in srgb,var(--vp-c-bg) 93%,#328565)}
.com-demo-node.busy{border-color:var(--vp-c-brand-1)}
.com-demo-arrow{display:flex;align-items:center;justify-content:center;font-size:24px;color:var(--vp-c-text-3)}
.com-demo-arrow.busy{color:var(--vp-c-brand-1)}
.vp-doc .com-demo ol{margin:0;padding:0;width:100%;list-style:none;max-height:126px;overflow:auto}
.vp-doc .com-demo li{display:flex;flex-direction:column;gap:2px;padding:5px 2px;margin:0;border-top:1px solid var(--vp-c-divider);font-size:11px;line-height:1.4}
.com-demo-ack{text-align:right;padding-top:10px;font-size:11px;line-height:1.5;color:var(--vp-c-text-2);overflow-wrap:anywhere}
.com-demo-ack.active{color:var(--vp-c-brand-1)}
.com-demo-node .com-demo-held{font-size:10px;line-height:1.5;border-top:1px solid var(--vp-c-divider);padding-top:6px;width:100%}
.com-demo-stats{display:flex;justify-content:center;flex-wrap:wrap;gap:20px;margin-top:14px;font-size:12px;color:var(--vp-c-text-2)}
.com-demo-stats strong{margin-left:4px;color:var(--vp-c-text-1)}
.vp-doc .com-demo .com-demo-status{font-size:13px;line-height:1.5;min-height:20px;margin:9px 0 0}
.vp-doc .com-demo .com-demo-note{font-size:11px;line-height:1.5;color:var(--vp-c-text-2);margin:7px 0 0}
.com-demo button:focus-visible,.com-demo select:focus-visible{outline:2px solid var(--vp-c-brand-1);outline-offset:3px}
@media(max-width:650px){
 .com-demo{padding:12px}
 .com-demo-flow{grid-template-columns:minmax(0,1fr)}
 .com-demo-node{min-height:0;padding:11px;gap:5px}
 .com-demo-arrow{height:26px;font-size:0}
 .com-demo-arrow::after{content:'\2193';font-size:24px}
 .com-demo-node>button{margin-top:7px}
 .com-demo-controls .com-demo-reset{margin-left:0}
 .vp-doc .com-demo code{font-size:12px}
 .com-demo-kicker{font-size:10px!important}
}
</style>
