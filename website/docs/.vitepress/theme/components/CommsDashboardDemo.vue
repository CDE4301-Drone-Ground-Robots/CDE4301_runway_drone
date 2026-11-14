<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'

type DeliveryState = 'queued' | 'awaiting' | 'acknowledged' | 'failed'
type FodRecord = { id: number; object: string; x: number; y: number; state: DeliveryState; retries: number; received: boolean; created: string; sent: string | null; ack: string | null }
type Notice = { id: number; target: string; sent: boolean; reason: string }
type Event = { id: number; time: string; text: string }
const storageKey = 'argus-comms-monitor-demo-v3'
const paused = ref(false)
const linkSilence = ref(0)
const records = ref<FodRecord[]>([])
const notices = ref<Notice[]>([])
const events = ref<Event[]>([])
const hunterOnline = ref(true)
const baseOnline = ref(true)
const ready = ref(false)
const browserStorage = ref(true)
const nextId = ref(1)
const object = ref('Battery')
const x = ref<number | string>(3)
const y = ref<number | string>(4)
const filter = ref('all')
const current = computed(() => records.value.find(r => r.state !== 'acknowledged'))
const pending = computed(() => records.value.filter(r => r.state !== 'acknowledged').length)
const acknowledged = computed(() => records.value.filter(r => r.state === 'acknowledged').length)
const failed = computed(() => notices.value.length)
const visible = computed(() => records.value.filter(r => filter.value === 'all' || (filter.value === 'pending' ? r.state !== 'acknowledged' : r.state === 'acknowledged')))
const validInput = computed(() => x.value !== '' && y.value !== '' && Number.isFinite(Number(x.value)) && Number.isFinite(Number(y.value)))
const canAck = computed(() => !!current.value?.received && hunterOnline.value && !paused.value && current.value.state === 'awaiting')
const canResend = computed(() => hunterOnline.value && !paused.value && current.value?.state === 'awaiting')
const names: Record<DeliveryState, string> = { queued: 'Queued', awaiting: 'Awaiting ACK', acknowledged: 'Acknowledged', failed: 'ACK limit reached' }
const targetId = (r: FodRecord) => 'FOD_THREAT_' + String(r.id).padStart(3, '0')
const coords = (r: FodRecord) => `(${r.x.toFixed(2)}, ${r.y.toFixed(2)}) m`
const clock = (iso: string) => new Date(iso).toLocaleTimeString('en-GB', { hour12: false })

function log(text: string) {
 events.value.unshift({ id: (events.value[0]?.id ?? 0) + 1, time: new Date().toISOString(), text })
 events.value = events.value.slice(0, 6)
}
function deliver(record: FodRecord) {
 record.sent = new Date().toISOString()
 if (!hunterOnline.value) { log(`${targetId(record)}: no response. Alert stays on ARGUS.`); return }
 if (record.received) log(`${targetId(record)} resent. HUNTER keeps one target, not a duplicate.`)
 else { record.received = true; log(`HUNTER received ${targetId(record)}. ARGUS is waiting for the matching ACK.`) }
}
function sendNext() {
 const record = current.value
 if (!record || record.state !== 'queued' || !hunterOnline.value || paused.value) return
 record.state = 'awaiting'
 deliver(record)
}
function addFod() {
 if (!validInput.value) return
 const record: FodRecord = { id: nextId.value++, object: object.value, x: Number(x.value), y: Number(y.value), state: 'queued', retries: 0, received: false, created: new Date().toISOString(), sent: null, ack: null }
 records.value.push(record)
 log(`${targetId(record)} saved to the ARGUS records and added to the queue.`)
 x.value = Number((record.x + 1.2).toFixed(2)); y.value = Number((record.y + 0.5).toFixed(2))
 sendNext()
}
function acknowledge() {
 const record = current.value
 if (!record || !canAck.value) return
 record.state = 'acknowledged'
 record.ack = new Date().toISOString()
 log(`Receipt ACK matched ${targetId(record)}. Next alert released. Collection is not confirmed.`)
 sendNext()
}
function notifyBase(target: string, reason: string) {
 paused.value = true
 notices.value.unshift({ id: (notices.value[0]?.id ?? 0) + 1, target, sent: baseOnline.value, reason })
 log(`${reason} ${baseOnline.value ? 'Error sent to base. Waiting for instructions.' : 'Error stored until the base link returns.'}`)
}
function resendMissingAck() {
 const record = current.value
 if (!record || !canResend.value) return
 record.retries++
 deliver(record)
 log(`${targetId(record)}: resend ${record.retries}/50 has no matching receipt ACK. Link checks still respond.`)
 if (record.retries === 50) {
  record.state = 'failed'
  notifyBase(targetId(record), 'No receipt ACK after 50 resends with an active link.')
 }
}
function simulateAckLimit() {
 while (canResend.value) resendMissingAck()
}
function resumeAfterInstruction() {
 if (!paused.value || !baseOnline.value || !hunterOnline.value) return
 paused.value = false
 linkSilence.value = 0
 if (current.value) { current.value.retries = 0; current.value.state = 'queued' }
 log('Simulated base instruction: resume queued transmissions.')
 sendNext()
}
function handshake() {
 if (hunterOnline.value) {
  linkSilence.value = 0
  log('Handshake response received. HUNTER link is available. FOD receipt ACK is separate.')
  return
 }
 if (linkSilence.value >= 10) return
 linkSilence.value++
 log(`No handshake response for ${linkSilence.value} second(s). Coordinates remain stored.`)
 if (linkSilence.value === 10) {
  notifyBase('HUNTER link', 'No handshake response for 10 seconds.')
 }
}
function simulateLoss() {
 if (hunterOnline.value) return
 while (linkSilence.value < 10) handshake()
}
function toggleHunter() {
 hunterOnline.value = !hunterOnline.value
 linkSilence.value = 0
 log(hunterOnline.value ? 'HUNTER link restored. Handshake response received.' : 'HUNTER link unavailable. Checking for a handshake response every second.')
 if (hunterOnline.value && !paused.value) {
  if (current.value?.state === 'awaiting') deliver(current.value)
  else sendNext()
 }
}
function toggleBase() {
 baseOnline.value = !baseOnline.value
 if (baseOnline.value) {
  const waiting = notices.value.filter(n => !n.sent)
  waiting.forEach(n => n.sent = true)
  log(`Base link restored. ${waiting.length} stored error notification(s) delivered.`)
 } else log('Base link lost. Error notifications will be retained locally.')
}
function reset() {
 records.value = []; notices.value = []; events.value = []
 paused.value = false; linkSilence.value = 0; nextId.value = 1; hunterOnline.value = true; baseOnline.value = true; filter.value = 'all'
 object.value = 'Battery'; x.value = 3; y.value = 4
 for (const sample of ['Battery', 'Plastic part', 'Bolt']) { object.value = sample; addFod() }
 object.value = 'Battery'
 log('Demo mission loaded. Three example FOD records are stored on ARGUS.')
}
function isFod(value: unknown): value is FodRecord {
 if (!value || typeof value !== 'object') return false
 const r = value as FodRecord
 return Number.isInteger(r.id) && r.id > 0 && typeof r.object === 'string' && Number.isFinite(r.x) && Number.isFinite(r.y)
  && Object.hasOwn(names, r.state) && Number.isInteger(r.retries) && r.retries >= 0 && r.retries <= 50
  && typeof r.received === 'boolean' && typeof r.created === 'string' && Number.isFinite(Date.parse(r.created))
  && (r.sent === null || typeof r.sent === 'string') && (r.ack === null || typeof r.ack === 'string')
}
function save() {
 if (!ready.value) return
 try { localStorage.setItem(storageKey, JSON.stringify({ records: records.value, notices: notices.value, events: events.value, nextId: nextId.value, hunterOnline: hunterOnline.value, baseOnline: baseOnline.value, paused: paused.value, linkSilence: linkSilence.value })) }
 catch { browserStorage.value = false }
}
onMounted(() => {
 let restored = false
 try {
  const raw = localStorage.getItem(storageKey) || localStorage.getItem('argus-comms-monitor-demo-v2')
  if (raw) {
   const saved = JSON.parse(raw)
   if (Array.isArray(saved.records)) saved.records = saved.records.map((r: FodRecord) => r && typeof r === 'object' ? { ...r, retries: r.retries ?? 0 } : r)
   if (Array.isArray(saved.records) && saved.records.every(isFod) && new Set(saved.records.map((r: FodRecord) => r.id)).size === saved.records.length) {
    records.value = saved.records
    paused.value = saved.paused === true || saved.hunterOnline === false && saved.linkSilence >= 10
    linkSilence.value = Number.isInteger(saved.linkSilence) ? Math.max(0, Math.min(10, saved.linkSilence)) : 0
    nextId.value = Math.max(0, ...records.value.map(r => r.id)) + 1
    hunterOnline.value = saved.hunterOnline !== false; baseOnline.value = saved.baseOnline !== false
    notices.value = Array.isArray(saved.notices) ? saved.notices.filter((n: Notice) => Number.isInteger(n?.id) && typeof n.target === 'string' && typeof n.sent === 'boolean').map((n: Notice) => ({ ...n, reason: n.reason || 'No handshake response for 10 seconds.' })) : []
    events.value = Array.isArray(saved.events) ? saved.events.filter((e: Event) => Number.isInteger(e?.id) && typeof e.text === 'string' && typeof e.time === 'string').slice(0, 6) : []
    restored = true
   }
  }
 } catch { browserStorage.value = false }
 if (!restored) reset()
 ready.value = true
 sendNext(); save()
})
watch([records, notices, events, nextId, hunterOnline, baseOnline, linkSilence, paused], save, { deep: true })
</script>

<template>
 <section class="comms-monitor" aria-label="Communication monitoring website simulator">
  <header class="monitor-header">
   <div><span class="monitor-eyebrow">ARGUS / CONTROL ROOM</span><h4>Communication monitor</h4><p>FOD records and delivery status</p></div>
   <span class="monitor-preview">Interactive preview</span>
  </header>
  <div class="monitor-banner">Simulated data. No live ROS 2, radio or database connection. {{ browserStorage ? 'Demo records are saved in this browser.' : 'Demo records are stored for this session only.' }}</div>
  <template v-if="ready">
   <div class="monitor-stats" aria-label="Demo delivery counts">
    <div><span>Stored FODs</span><strong data-monitor-stat="stored">{{ records.length }}</strong></div>
    <div><span>Pending delivery</span><strong data-monitor-stat="pending">{{ pending }}</strong></div>
    <div><span>Receipt ACKs</span><strong data-monitor-stat="acknowledged">{{ acknowledged }}</strong></div>
    <div><span>Error notifications</span><strong data-monitor-stat="failed">{{ failed }}</strong></div>
   </div>
   <div class="monitor-connections">
    <span><i :class="{ offline: !hunterOnline }"></i>HUNTER {{ hunterOnline ? 'connected' : 'disconnected' }}</span>
    <button type="button" :aria-pressed="!hunterOnline" @click="toggleHunter">{{ hunterOnline ? 'Disconnect HUNTER' : 'Reconnect HUNTER' }}</button>
    <span><i :class="{ offline: !baseOnline }"></i>Base {{ baseOnline ? 'connected' : 'disconnected' }}</span>
    <button type="button" :aria-pressed="!baseOnline" @click="toggleBase">{{ baseOnline ? 'Disconnect base' : 'Reconnect base' }}</button>
   </div>
   <div class="monitor-connections" aria-label="Simulated link handshake">
    <span>Handshake interval: 1 s. No response: {{ linkSilence }} / 10 s</span>
    <button type="button" @click="handshake">Advance 1 second</button>
    <button type="button" :disabled="hunterOnline || linkSilence >= 10" @click="simulateLoss">Simulate 10 seconds without response</button>
   </div>
   <div v-if="paused" class="monitor-connections" role="status">
    <span>Proposed response: descend and land at a clear location, then wait for base instructions. Targets remain stored.</span>
    <button type="button" :disabled="!baseOnline || !hunterOnline" @click="resumeAfterInstruction">Simulate base instruction: resume</button>
   </div>
   <form class="monitor-form" @submit.prevent="addFod">
    <label>FOD object<select v-model="object"><option>Battery</option><option>Plastic part</option><option>Bolt</option></select></label>
    <label>X coordinate (m)<input v-model="x" type="number" step="0.01" required></label>
    <label>Y coordinate (m)<input v-model="y" type="number" step="0.01" required></label>
    <button type="submit" class="monitor-primary" :disabled="!validInput">Add FOD record</button>
   </form>
   <div class="monitor-grid">
    <section class="monitor-panel monitor-records" aria-label="Stored FOD records">
     <div class="monitor-panel-title"><strong>Stored FOD records</strong><span>Mission DEMO-001</span></div>
     <div class="monitor-filters" role="group" aria-label="Filter FOD records">
      <button v-for="option in ['all', 'pending', 'acknowledged']" :key="option" type="button" :aria-pressed="filter === option" @click="filter = option">{{ option === 'all' ? 'All records' : option === 'pending' ? 'Pending' : 'Acknowledged' }}</button>
     </div>
     <div class="monitor-table-scroll" tabindex="0" aria-label="FOD delivery records. Scroll horizontally on small screens.">
      <table><thead><tr><th>Threat ID</th><th>Object / coordinates</th><th>Status</th><th>HUNTER receipt</th><th>ACK resends</th></tr></thead>
       <tbody><tr v-for="record in visible" :key="record.id" :class="{ selected: current?.id === record.id }">
        <td><code>{{ targetId(record) }}</code><small>{{ clock(record.created) }}</small></td>
        <td>{{ record.object }}<small>{{ coords(record) }}</small></td>
        <td><span class="monitor-state" :class="record.state">{{ names[record.state] }}</span></td>
        <td>{{ record.received ? 'Received' : 'Not received' }}</td>
        <td>{{ record.retries }} / 50</td>
       </tr><tr v-if="!visible.length"><td colspan="5">No records in this view.</td></tr></tbody>
      </table>
     </div>
     <p class="monitor-record-note">Unacknowledged coordinates stay on ARGUS. Acknowledged records remain in the delivery history.</p>
    </section>
    <div class="monitor-side">
     <section class="monitor-panel" aria-label="Current queued transmission">
      <div class="monitor-panel-title"><strong>Current transmission</strong><span>ARGUS queue</span></div>
      <template v-if="current">
       <code class="monitor-current-id">{{ targetId(current) }}</code>
       <p class="monitor-current-object">{{ current.object }} <span>{{ coords(current) }}</span></p>
       <p class="monitor-current-status" role="status">{{ paused ? 'Coordinates retained. Proposed response: land at a clear location and wait for base instructions.' : current.state === 'queued' ? 'Stored on ARGUS. Waiting for the HUNTER link.' : current.received ? 'Received by HUNTER. Waiting for its receipt ACK.' : 'No response from HUNTER. Alert retained on ARGUS.' }}</p>

       <p class="monitor-help">ACK resends: {{ current.retries }} / 50</p>
       <div class="monitor-actions">
        <button type="button" class="monitor-primary receipt-ack-hint" :disabled="!canAck" @click="acknowledge">Acknowledge receipt</button>
        <button type="button" :disabled="!canResend" @click="resendMissingAck">Simulate 1 unacknowledged resend</button>
        <button type="button" :disabled="!canResend" @click="simulateAckLimit">Simulate 50 unacknowledged resends</button>

       </div>
      </template>
      <p v-else>All stored alerts have been acknowledged.</p>
      <p class="monitor-help">A receipt ACK releases the next coordinate. It does not confirm FOD collection. Handshake controls advance simulated seconds. Resend controls simulate failed attempts. Timing is illustrative.</p>
     </section>
     <section class="monitor-panel" aria-label="Base station notifications">
      <div class="monitor-panel-title"><strong>Base station notifications</strong><span>{{ notices.length }}</span></div>
      <ul v-if="notices.length" class="monitor-notices"><li v-for="notice in notices" :key="notice.id"><strong>{{ notice.target }}</strong><span>{{ notice.reason }}</span><small>{{ notice.sent ? 'Error notification sent to base.' : 'Stored error. Waiting for the base link.' }}</small></li></ul>
      <p v-else class="monitor-empty">No communication errors.</p>
     </section>
    </div>
   </div>
   <section class="monitor-panel monitor-log" aria-label="Communication activity">
    <div class="monitor-panel-title"><strong>Activity</strong><button type="button" @click="reset">Reset demo</button></div>
    <ol><li v-for="event in events" :key="event.id"><time>{{ clock(event.time) }}</time><span>{{ event.text }}</span></li></ol>
   </section>
  </template>
 </section>
</template>

<style scoped>
.comms-monitor{--monitor-rose:#c99a8d;--monitor-line:var(--vp-c-divider);margin:24px 0;border:1px solid var(--monitor-line);border-radius:16px;background:var(--vp-c-bg);overflow:hidden;color:var(--vp-c-text-1);font-size:13px;min-width:0}
.comms-monitor *{box-sizing:border-box}
.monitor-header{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:24px;background:var(--vp-c-bg-soft)}
.monitor-eyebrow{font-size:10px;letter-spacing:1.8px;color:var(--monitor-rose);font-weight:600}
.comms-monitor h4{font-size:25px;line-height:1.25;margin:8px 0 4px;letter-spacing:-.7px}
.comms-monitor p{line-height:1.6;margin:0}
.monitor-header p{color:var(--vp-c-text-2)}
.monitor-preview{border:1px solid var(--monitor-rose);border-radius:20px;padding:6px 10px;color:var(--monitor-rose);font-size:11px;white-space:nowrap}
.monitor-banner{padding:12px 24px;border-top:1px solid var(--monitor-line);border-bottom:1px solid var(--monitor-line);font-size:12px;color:var(--vp-c-text-2)}
.monitor-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;padding:20px 24px}
.monitor-stats>div{padding:15px 18px;border:1px solid var(--monitor-line);border-radius:10px;background:var(--vp-c-bg-soft)}
.monitor-stats span{display:block;color:var(--vp-c-text-2);font-size:11px}
.monitor-stats strong{display:block;font-size:28px;margin-top:6px;font-weight:600;line-height:1.2}
.monitor-connections{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 24px;padding:12px 0;border-top:1px solid var(--monitor-line);border-bottom:1px solid var(--monitor-line)}
.monitor-connections>span{display:flex;align-items:center;gap:7px;font-size:12px}
.monitor-connections>span:nth-of-type(2){margin-left:auto}
.monitor-connections i{display:inline-block;width:7px;height:7px;border-radius:50%;background:#579d7d}
.monitor-connections i.offline{background:#c37c77}
.comms-monitor button,.comms-monitor input,.comms-monitor select{font:inherit;color:var(--vp-c-text-1);background:var(--vp-c-bg);border:1px solid var(--monitor-line);border-radius:7px;padding:8px 10px;line-height:1.4;min-width:0}
.comms-monitor button{cursor:pointer;font-weight:500}
.comms-monitor button:hover:not(:disabled){border-color:var(--monitor-rose)}
.comms-monitor button:disabled{opacity:.45;cursor:default}
.comms-monitor button:focus-visible,.comms-monitor input:focus-visible,.comms-monitor select:focus-visible,.monitor-table-scroll:focus-visible{outline:2px solid var(--monitor-rose);outline-offset:2px}
.comms-monitor .monitor-primary{background:#c99a8d20;border-color:var(--monitor-rose)}
.monitor-form{display:grid;grid-template-columns:minmax(120px,1.2fr) minmax(90px,1fr) minmax(90px,1fr) auto;gap:12px;align-items:end;padding:20px 24px}
.monitor-form label{display:flex;flex-direction:column;gap:7px;font-size:11px;color:var(--vp-c-text-2)}
.monitor-form :is(input,select){width:100%}
.monitor-grid{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(270px,1fr);gap:16px;padding:0 24px 20px;align-items:start}
.monitor-panel{border:1px solid var(--monitor-line);border-radius:10px;overflow:hidden;min-width:0;background:var(--vp-c-bg-soft)}
.monitor-panel-title{display:flex;justify-content:space-between;align-items:center;gap:10px;border-bottom:1px solid var(--monitor-line);padding:13px 16px}
.monitor-panel-title strong{font-size:13px;font-weight:600}
.monitor-panel-title>span{font-size:10px;color:var(--vp-c-text-2)}
.monitor-filters{display:flex;gap:6px;padding:12px 14px;flex-wrap:wrap}
.monitor-filters button{font-size:11px;padding:5px 8px}
.monitor-filters [aria-pressed=true]{border-color:var(--monitor-rose);background:#c99a8d20}
.monitor-table-scroll{overflow:auto;max-height:360px}
.comms-monitor table{display:table;width:100%;min-width:550px;margin:0;border-collapse:collapse;font-size:11px}
.comms-monitor :is(th,td){padding:12px 14px;border:0;border-bottom:1px solid var(--monitor-line);text-align:left;background:transparent;white-space:nowrap}
.comms-monitor th{font-size:10px;font-weight:600;color:var(--vp-c-text-2)}
.comms-monitor td small{display:block;margin-top:5px;color:var(--vp-c-text-2);font-size:10px}
.comms-monitor code{background:transparent;padding:0;font-size:10px;color:inherit;white-space:nowrap}
.comms-monitor tr.selected{background:#c99a8d12}
.monitor-state{display:inline-block;padding:4px 6px;border-radius:5px;background:var(--vp-c-bg);border:1px solid var(--monitor-line);font-size:10px}
.monitor-state.awaiting{color:#aa7b49;border-color:#aa7b4960}
.monitor-state.acknowledged{color:#579d7d;border-color:#579d7d60}
.monitor-state.failed{color:#c37c77;border-color:#c37c7760}
.comms-monitor .monitor-record-note{padding:12px 16px;color:var(--vp-c-text-2);font-size:11px}
.monitor-side{display:grid;gap:16px;min-width:0}
.monitor-current-id{display:block;padding:16px 16px 5px!important;color:var(--monitor-rose)!important;font-size:14px!important;font-weight:600}
.comms-monitor .monitor-current-object{padding:0 16px;font-size:13px}
.monitor-current-object span{display:block;color:var(--vp-c-text-2);font-size:12px;margin-top:4px}
.comms-monitor .monitor-current-status{padding:12px 16px;font-size:12px}
.monitor-retry-label{display:flex;justify-content:space-between;gap:10px;padding:0 16px;font-size:11px;color:var(--vp-c-text-2)}
.monitor-retry-label strong{font-weight:500}
.comms-monitor progress{display:block;width:calc(100% - 32px);height:5px;margin:8px 16px 14px;accent-color:var(--monitor-rose)}
.monitor-actions{display:grid;gap:7px;padding:0 16px 12px}
.monitor-actions button{font-size:11px}
.comms-monitor .monitor-help{padding:0 16px 15px;color:var(--vp-c-text-2);font-size:11px}
.monitor-notices{list-style:none;margin:0!important;padding:0 16px!important;max-height:180px;overflow:auto}
.monitor-notices li{display:flex;flex-direction:column;gap:4px;padding:12px 0;line-height:1.5;font-size:11px}
.monitor-notices li+li{border-top:1px solid var(--monitor-line)}
.monitor-notices small{color:var(--vp-c-text-2);font-size:10px}
.comms-monitor .monitor-empty{padding:15px 16px;color:var(--vp-c-text-2);font-size:12px}
.monitor-log{margin:0 24px 24px}
.monitor-log .monitor-panel-title button{font-size:11px;padding:5px 9px}
.monitor-log ol{list-style:none;margin:0!important;padding:4px 16px!important}
.monitor-log li{display:flex;align-items:baseline;gap:14px;margin:0;padding:7px 0;font-size:11px;line-height:1.6}
.monitor-log time{color:var(--vp-c-text-2);font-size:10px;flex-shrink:0;font-variant-numeric:tabular-nums}
@media(max-width:1100px){.monitor-grid{grid-template-columns:1fr}.monitor-side{grid-template-columns:1fr 1fr}.monitor-stats{gap:8px}.monitor-stats>div{padding:12px}.monitor-form{grid-template-columns:1fr 1fr}.monitor-connections>span:nth-of-type(2){margin-left:0}}
@media(max-width:600px){.monitor-header{padding:18px;align-items:flex-start;flex-direction:column;gap:10px}.comms-monitor h4{font-size:23px}.monitor-banner{padding:12px 18px}.monitor-stats{grid-template-columns:1fr 1fr;padding:16px 18px}.monitor-connections{margin:0 18px;display:grid;grid-template-columns:1fr auto}.monitor-form{padding:18px;gap:10px}.monitor-form label:first-child{grid-column:1 / -1}.monitor-grid{padding:0 18px 16px}.monitor-side{grid-template-columns:1fr}.monitor-log{margin:0 18px 18px}.monitor-log li{gap:9px}.monitor-preview{font-size:10px}}

.comms-monitor .receipt-ack-hint:not(:disabled){border-color:#c99a8d;animation:receipt-ack-pulse 2.4s ease-in-out infinite}
@keyframes receipt-ack-pulse{0%,100%{box-shadow:0 0 0 0 #c99a8d00}50%{box-shadow:0 0 0 4px #c99a8d33,0 0 14px #c99a8d33}}
@media(prefers-reduced-motion:reduce){.comms-monitor .receipt-ack-hint:not(:disabled){animation:none}}
</style>
