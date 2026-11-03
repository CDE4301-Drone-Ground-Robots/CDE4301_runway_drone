// Run inspect-gantt.ps1 first, then: node website/scripts/build-gantt-data.mjs <raw.json>
import fs from 'node:fs'
import assert from 'node:assert/strict'
const raw = JSON.parse(fs.readFileSync(process.argv[2], 'utf8').replace(/^\uFEFF/, ''))
const col = s => [...s].reduce((n, c) => n * 26 + c.charCodeAt(0) - 64, 0)
const position = ref => { const [, c, r] = ref.match(/^([A-Z]+)(\d+)$/); return { col: col(c), row: +r } }
const cells = raw.cells.map(c => ({ ...c, ...position(c.ref) }))
const merges = raw.merges.map(ref => { const [a, b] = ref.split(':').map(position); return { ref, a, b } })
const members = [
  { name: 'Arun', role: 'Mechanical Design / UAV', color: 'blue', first: 32, last: 45 },
  { name: 'Charan', role: 'Computer Vision / Communication', color: 'orange', first: 46, last: 61 },
  { name: 'Talitha', role: 'Electrical Design / Navigation', color: 'green', first: 62, last: 73 }
]
const weeks = cells.filter(c => c.row === 5 && c.col >= 4 && c.col <= 38).map(c => ({ column: c.col, label: c.value }))
assert.equal(weeks.length, 35)
assert.equal(weeks[14].label, 'READING WEEK')
for (const member of members) {
  const categories = cells.filter(c => c.col === 3 && c.row >= member.first && c.row <= member.last && c.value)
  member.tasks = cells.filter(c => c.col >= 4 && c.col <= 38 && c.row >= member.first && c.row <= member.last && c.value && !['P32', 'Q32', 'H49'].includes(c.ref)).map(c => {
    const merge = merges.find(m => m.a.col === c.col && m.a.row === c.row)
    // H48:I50 is an unmerged two-week block, with its text continued in H49.
    const description = c.ref === 'H48' ? c.value + '\n' + cells.find(x => x.ref === 'H49').value : c.value
    const category = categories.filter(x => x.row <= c.row).at(-1)?.value
    assert.ok(category, `Missing category: ${c.ref}`)
    return { description, category, start: c.col, end: c.ref === 'H48' ? 9 : merge?.b.col ?? c.col, source: merge?.ref ?? (c.ref === 'H48' ? 'H48:I50' : c.ref) }
  })
  // These two vertically merged milestones apply to all three member sections.
  member.milestones = ['P32', 'Q32'].map(ref => {
    const c = cells.find(c => c.ref === ref)
    return { description: c.value, category: 'Shared milestone', start: c.col, end: c.col, source: merges.find(m => m.a.col === c.col && m.a.row === c.row).ref }
  })
  for (const t of [...member.tasks, ...member.milestones]) assert.ok(t.start >= 4 && t.end <= 38 && t.start <= t.end)
}
const output = { source: { workbook: 'CDE4301_runway_patrol_gantt.xlsx', worksheet: 'Gantt Chart', semester1: 'D–Q', semester2: 'R–AL' }, weeks, members }
fs.mkdirSync('website/docs/data', { recursive: true })
fs.writeFileSync('website/docs/data/gantt.json', JSON.stringify(output, null, 2) + '\n')
console.log(members.map(m => `${m.name}: ${m.tasks.length} activities, ${m.milestones.length} shared milestones`).join('\n'))
