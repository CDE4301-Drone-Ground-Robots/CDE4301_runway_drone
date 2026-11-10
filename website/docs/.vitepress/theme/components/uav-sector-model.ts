// Footprint -> sector model, calibrated on the offline simulation tables of the navigation report.
// Sector width is fixed (60 m); the sector length is what the camera footprint and the battery allow.
export type Pattern = 'along' | 'across'
export type WindDir = 'along' | 'across'

export interface SectorInput {
  W: number          // sector width across the runway (m), fixed at 60
  L: number          // sector length along the runway (m)
  wRgb: number       // RGB footprint across the lane (m)
  lRgb: number       // RGB footprint along the lane (m)
  wTh: number        // thermal strip width (m)
  k: number          // pitch / swath ratio
  hz: number         // processed frame rate (Hz)
  Wh: number         // pack energy (Wh)
  pattern: Pattern
  windDir: WindDir
  wind: number       // mean wind (m/s)
}

export interface SectorResult {
  p: number; N: number; Llane: number; v: number; T: number; P: number; pack: number
  thermalLimited: boolean; speedLimited: boolean
}

// Fitted constants (see the report): two calm points fix a and b, the 30 m crosswind series fixes wk and wn,
// the pack-vs-time ratio fixes pc.
export const C = { a: 0.36695, b: 2.2137, wk: 1.3096e-3, wn: 3.2637, pc: 2.0636e-4, P0: 795.84, vCruise: 4.23, aligned: 0.7 }
export const SECTOR_WIDTH = 60
// Design constraints (kept out of the interface on purpose): the sector is sized for the worst simulated
// wind, 15 m/s as a crosswind on the lanes, and for the 95% launch to 25% return battery window.
export const WORST_WIND = 15
export const THERMAL_STRIP = 6.62
export const PACK_WH = 266.4
export const BATTERY_WINDOW = 70
export const MAX_SEARCH_M = 800

export const lanePitch = (wRgb: number, wTh: number, k: number) => k * Math.min(wRgb, wTh)

export function laneLayout(pattern: Pattern, L: number, W: number, p: number) {
  if (pattern === 'along') return { N: Math.ceil(W / p - 1e-9) + 1, Llane: L }
  return { N: Math.max(1, Math.round(L / p)), Llane: W }
}

// 1 = crosswind on the lanes; below 1 = head or tail wind on the lanes
export const windFactor = (pattern: Pattern, windDir: WindDir) => ((pattern === 'along') === (windDir === 'along') ? C.aligned : 1)

export function evalSector(q: SectorInput): SectorResult {
  const p = lanePitch(q.wRgb, q.wTh, q.k)
  const { N, Llane } = laneLayout(q.pattern, q.L, q.W, p)
  const vFoot = q.lRgb * q.hz
  const v = Math.min(C.vCruise, vFoot)
  const wl = q.wind > 0 ? C.wk * Math.pow(q.wind, C.wn) * windFactor(q.pattern, q.windDir) : 0
  const T = (C.a + (1 / v - 1 / C.vCruise)) * N * Llane + (C.b + wl) * N
  const P = C.P0 * (1 + C.pc * q.wind * q.wind)
  return { p, N, Llane, v, T, P, pack: (P * T) / 3600 / q.Wh * 100, thermalLimited: q.wRgb > q.wTh, speedLimited: vFoot < C.vCruise }
}

export function maxLength(q: SectorInput, budgetPct: number): number {
  let best = 0
  for (let L = 1; L <= MAX_SEARCH_M; L += 0.25) {
    if (evalSector({ ...q, L }).pack <= budgetPct) best = L
    else if (best > 0) break
  }
  return best
}

// ---- camera options: sensor size = pixels x pixel pitch, footprint = 5 m x sensor / focal length ----
export interface Sensor { name: string; shutter: 'global' | 'rolling' | 'n/a'; px: number; sw: number; sh: number }
export interface Preset { id: string; name: string; sub: string; sensor: string; shutter: string; px: number; w: number; l: number; price: string; note: string }

const SENSORS: Record<string, Sensor> = {
  imx568: { name: 'Sony IMX568 5 MP', shutter: 'global', px: 2472, sw: 2472 * 2.74e-3, sh: 2064 * 2.74e-3 },
  imx183: { name: 'Sony IMX183 20 MP', shutter: 'rolling', px: 5496, sw: 5496 * 2.4e-3, sh: 3672 * 2.4e-3 },
  imx455: { name: 'Sony IMX455 61 MP', shutter: 'global', px: 9568, sw: 9568 * 3.76e-3, sh: 6380 * 3.76e-3 },
}
const make = (id: string, name: string, sub: string, s: Sensor, f: number, price: string, note = ''): Preset => ({
  id, name, sub, sensor: s.name, shutter: s.shutter, px: s.px,
  w: +(5 * s.sw / f).toFixed(2), l: +(5 * s.sh / f).toFixed(2), price, note,
})

export const PRESETS: Preset[] = [
  { id: 'prev', name: 'Previous placeholder', sub: '60° HFOV, 640 × 480', sensor: 'Gazebo default', shutter: 'n/a', px: 640, w: 5.77, l: 4.33, price: 'n/a', note: 'Used in the earlier design' },
  make('cur', 'Current (report)', 'IMX568, f 16.9 mm', SENSORS.imx568, 16.9, 'USD 469 (sample module)', 'Native sensor footprint; the simulation uses a square 2 × 2 m crop of it'),
  make('mid', 'IMX568, f 8 mm', 'Same sensor, wider lens', SENSORS.imx568, 8, 'USD 469 + lens'),
  make('wide', 'IMX568, f 5 mm', 'Near the previous placeholder', SENSORS.imx568, 5, 'USD 469 + lens'),
  make('q20', 'IMX183 20 MP, f 10 mm', 'Rolling shutter', SENSORS.imx183, 10, 'EUR 419 to 461', 'Rolling shutter skews at 4 m/s'),
  make('q61a', 'IMX455 61 MP, f 25 mm', 'Full frame, global shutter', SENSORS.imx455, 25, 'On quote'),
  make('q61b', 'IMX455 61 MP, f 15 mm', 'Wider than the thermal strip', SENSORS.imx455, 15, 'On quote', 'Needs a wider thermal camera'),
]

// ---- simulation values from the report, used for the on-page model check ----
export const BASE: SectorInput = { W: 60, L: 30, wRgb: 2, lRgb: 2, wTh: 6.62, k: 0.88, hz: 5, Wh: 266.4, pattern: 'along', windDir: 'across', wind: 0 }
export const CHECKS: { name: string; over: Partial<SectorInput>; key: 'T' | 'pack'; sim: number; fitted: boolean }[] = [
  { name: '2 m camera, 30 m, calm (time, s)', over: {}, key: 'T', sim: 476, fitted: true },
  { name: 'Previous camera, 60 m, calm (time, s)', over: { wRgb: 5.77, lRgb: 4.33, L: 60 }, key: 'T', sim: 315, fitted: true },
  { name: 'Lanes across, 30 m, calm (time, s)', over: { pattern: 'across' }, key: 'T', sim: 403, fitted: false },
  { name: 'Lanes across, 10 m/s along runway (time, s)', over: { pattern: 'across', wind: 10, windDir: 'along' }, key: 'T', sim: 455, fitted: false },
  { name: 'Lanes across, 10 m/s across runway (time, s)', over: { pattern: 'across', wind: 10, windDir: 'across' }, key: 'T', sim: 428, fitted: false },
  { name: '15 m/s crosswind, 30 m (pack, %)', over: { wind: 15, L: 30 }, key: 'pack', sim: 68.9, fitted: true },
  { name: '15 m/s crosswind, 35 m (pack, %)', over: { wind: 15, L: 35 }, key: 'pack', sim: 73, fitted: false },
  { name: '15 m/s crosswind, 40 m (pack, %)', over: { wind: 15, L: 40 }, key: 'pack', sim: 83, fitted: false },
  { name: '15 m/s crosswind, 60 m (pack, %)', over: { wind: 15, L: 60 }, key: 'pack', sim: 103, fitted: false },
]