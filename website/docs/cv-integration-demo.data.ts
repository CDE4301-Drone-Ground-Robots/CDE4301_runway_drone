import { existsSync } from 'node:fs'
import { resolve } from 'node:path'
export default {
 watch: ['public/report-assets/computer-vision/*.mp4'],
 load() {
  const src = '/report-assets/computer-vision/integration-demo.mp4'
  return { available: existsSync(resolve(process.cwd(), 'docs/public' + src)), src }
 }
}
