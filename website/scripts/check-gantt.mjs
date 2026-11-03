// With the dev server and headless Chrome (--remote-debugging-port=9231) running:
// node website/scripts/check-gantt.mjs
import assert from 'node:assert/strict'
import fs from 'node:fs'
import data from '../docs/data/gantt-display.js'
const targets = await fetch('http://127.0.0.1:9231/json/list').then(r => r.json())
const socket = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl)
await new Promise(r => socket.addEventListener('open', r, { once: true }))
let serial = 0
const pending = new Map(), errors = []
socket.addEventListener('message', event => {
  const msg = JSON.parse(event.data)
  if (msg.method === 'Runtime.exceptionThrown') errors.push(msg.params.exceptionDetails.text)
  if (msg.id) { const p = pending.get(msg.id); pending.delete(msg.id); msg.error ? p.reject(msg.error) : p.resolve(msg.result) }
})
function cdp(method, params = {}) { return new Promise((resolve, reject) => { const id = ++serial; pending.set(id, { resolve, reject }); socket.send(JSON.stringify({ id, method, params })) }) }
async function evaluate(expression) {
  const r = await cdp('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true })
  if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails))
  return r.result.value
}
try {
  await cdp('Runtime.enable')
  await cdp('Page.enable')
  await cdp('Emulation.setFocusEmulationEnabled', { enabled: true })
  await cdp('Page.navigate', { url: 'http://127.0.0.1:4173/CDE4301_runway_drone/timeline' })
  for (let n = 0; n < 100; n++) {
    if (await evaluate('!!document.querySelector(".task-bar") && !!document.querySelector(".VPNav")')) break
    await new Promise(r => setTimeout(r, 100))
  }
  for (const width of [1440, 1920, 390]) for (const dark of [false, true]) {
    await cdp('Emulation.setDeviceMetricsOverride', { width, height: 1000, deviceScaleFactor: 1, mobile: width < 600 })
    await evaluate(`document.documentElement.classList.toggle('dark', ${dark})`)
    for (const semester of [1, 2]) {
      await evaluate(`document.querySelectorAll('.semester-toggle button')[${semester - 1}].click(); new Promise(r => setTimeout(r, 50))`)
      const state = await evaluate(`(()=>({
        names:[...document.querySelectorAll('.member-heading strong')].map(x=>x.textContent),
        weeks:[...document.querySelectorAll('.week-label')].map(x=>x.textContent),
        header:document.querySelector('.gantt-axis .task-label').textContent,
        bars:[...document.querySelectorAll('.member-group')].map(m=>({name:m.querySelector('strong').textContent,categories:[...m.querySelectorAll('.category-row')].map(row=>({name:row.dataset.category,label:row.querySelector('.task-label').textContent})),bars:[...m.querySelectorAll('.task-bar')].map(b=>({source:b.dataset.source,category:b.closest('.category-row').dataset.category,label:b.getAttribute('aria-label'),column:b.style.gridColumn,lane:b.style.gridRow,rect:(()=>{const r=b.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom}})()}))})),
        pageOverflow:document.documentElement.scrollWidth>innerWidth,
        chartScroll:document.querySelector('.gantt-scroll').scrollWidth>document.querySelector('.gantt-scroll').clientWidth,
        chartWidth:document.querySelector('.gantt-scroll').clientWidth,
        labelWidth:document.querySelector('.gantt-axis .task-label').getBoundingClientRect().width,
        nav:!!document.querySelector('.VPNav')
      }))()`)
      assert.deepEqual(state.names, ['Arun', 'Charan', 'Talitha'])
      assert.equal(state.header, 'Subsystem / Category')
      const first = semester === 1 ? 4 : 18, last = semester === 1 ? 17 : 38
      assert.deepEqual(state.weeks, data.weeks.filter(w => w.column >= first && w.column <= last).map(w => w.label))
      assert.equal(state.pageOverflow, false)
      assert.equal(state.chartScroll, state.labelWidth + state.weeks.length * 88 > state.chartWidth)
      if (width >= 960) assert.ok(state.chartWidth > width * 0.9, 'Timeline should use the desktop width')
      assert.equal(state.nav, true)
      for (const member of data.members) {
        const rendered = state.bars.find(m => m.name === member.name)
        const actual = rendered.bars
        const expected = [...member.tasks, ...member.milestones].filter(t => t.start <= last && t.end >= first)
        assert.equal(actual.length, expected.length)
        assert.deepEqual(rendered.categories.map(c => c.name), [...new Set(expected.map(t => t.category))])
        assert.ok(rendered.categories.every(c => c.label === c.name))
        for (const task of expected) {
          const bar = actual.find(b => b.source === task.source)
          assert.ok(bar, task.source)
          assert.ok(bar.label.includes(task.description))
          assert.equal(bar.category, task.category, task.source)
          assert.equal(bar.column, `${Math.max(first, task.start) - first + 1} / ${Math.min(last, task.end) - first + 2}`, task.source)
        }
        for (let i = 0; i < actual.length; i++) for (let j = i + 1; j < actual.length; j++) {
          const a = actual[i], b = actual[j]
          const overlaps = a.rect.left < b.rect.right && b.rect.left < a.rect.right && a.rect.top < b.rect.bottom && b.rect.top < a.rect.bottom
          assert.equal(overlaps, false, `Overlapping bars: ${a.source}, ${b.source}`)
        }
      }
      await evaluate(`document.querySelector('.task-bar').focus(); new Promise(r=>setTimeout(r,120))`)
      assert.ok(await evaluate(`document.querySelector('#gantt-tooltip')?.textContent.includes('Excel:')`))
      await evaluate(`document.querySelector('.task-bar').dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));new Promise(r=>setTimeout(r,30))`)
      assert.equal(await evaluate(`!!document.querySelector('#gantt-tooltip')`), false)
      await evaluate(`document.querySelector('.task-bar').dispatchEvent(new MouseEvent('mouseenter')); new Promise(r=>setTimeout(r,30))`)
      assert.ok(await evaluate(`!!document.querySelector('#gantt-tooltip')`))
      await evaluate(`document.querySelector('.gantt-scroll').dispatchEvent(new Event('scroll'));new Promise(r=>setTimeout(r,30))`)
      console.log(`PASS ${width}px ${dark ? 'dark' : 'light'} semester ${semester}: category rows, all tasks assigned, no overlapping bars, tooltips, scrolling, navigation`)
    }
    const shot = await cdp('Page.captureScreenshot', { format: 'png' })
    fs.writeFileSync(`.visual-check/gantt-${width}-${dark ? 'dark' : 'light'}.png`, Buffer.from(shot.data, 'base64'))
  }
  await evaluate(`document.querySelector('#timeline-tab-overview').click();new Promise(r=>setTimeout(r,30))`)
  assert.equal(await evaluate(`document.querySelector('#timeline-panel-overview').getBoundingClientRect().height>0`), true)
  await evaluate(`document.querySelector('#timeline-tab-overview').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));new Promise(r=>setTimeout(r,30))`)
  assert.equal(await evaluate(`document.activeElement.id`), 'timeline-tab-gantt')
  assert.deepEqual(errors, [])
  console.log('PASS overview content, keyboard tab navigation and no runtime exceptions')
} finally {
  if (process.argv.includes('--close-browser')) await cdp('Browser.close')
  socket.close()
}
