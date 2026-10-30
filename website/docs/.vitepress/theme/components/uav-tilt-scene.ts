import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'

/**
 * Aerospace convention: body x = forward, y = right, z = down (FRD).
 * Three.js world is Y-up: FRD x -> -Z, y -> +X, z -> -Y.
 * With yaw = 0, R = Rx(pitch) Rz(-roll) in scene coordinates, equivalent
 * to the aerospace yaw-pitch-roll sequence. Positive pitch raises the nose;
 * positive roll lowers the right arm. Local +Y is the body thrust direction.
 * OrbitControls move the camera only and never modify this attitude group.
 */
export function createTiltScene(host: HTMLElement, onContextLost: () => void) {
 const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false })
 renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2))
 renderer.setClearColor(0x0b121c)
 renderer.outputColorSpace = THREE.SRGBColorSpace
 renderer.domElement.setAttribute('aria-label', 'X-frame quadcopter: cyan nose is forward; grid stays horizontal')
 renderer.domElement.setAttribute('role', 'img')
 host.appendChild(renderer.domElement)

 const scene = new THREE.Scene()
 const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 60)
 const controls = new OrbitControls(camera, renderer.domElement)
 controls.enableDamping = false // Render on change; no permanent animation loop.
 controls.enablePan = false
 controls.minDistance = 5.5
 controls.maxDistance = 14
 controls.minPolarAngle = 0.15
 controls.maxPolarAngle = Math.PI / 2 - 0.03
 controls.target.set(0, 0.35, 0)
 const drone = new THREE.Group()
 scene.add(drone)
 let frame = 0
 let visible = true
 let disposed = false
 const render = () => {
  if (!disposed && visible && !frame) frame = requestAnimationFrame(() => {
   frame = 0
   if (!disposed && visible && !renderer.getContext().isContextLost()) renderer.render(scene, camera)
  })
 }
 controls.addEventListener('change', render)
 const resetCamera = () => {
  camera.position.set(5.2, 4.4, 6.5)
  controls.target.set(0, 0.35, 0)
  controls.update()
  render()
 }
 const contextLost = (event: Event) => { event.preventDefault(); onContextLost() }
 renderer.domElement.addEventListener('webglcontextlost', contextLost)
 const resize = new ResizeObserver(() => {
  const { width, height } = host.getBoundingClientRect()
  if (!width || !height || disposed) return
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
  render()
 })
 const dispose = () => {
  disposed = true
  cancelAnimationFrame(frame)
  resize.disconnect()
  controls.removeEventListener('change', render)
  controls.dispose()
  renderer.domElement.removeEventListener('webglcontextlost', contextLost)
  const geometries = new Set<THREE.BufferGeometry>()
  const materials = new Set<THREE.Material>()
  scene.traverse(object => {
   const item = object as THREE.Mesh
   if (item.geometry) geometries.add(item.geometry)
   if (item.material) for (const material of Array.isArray(item.material) ? item.material : [item.material]) materials.add(material)
  })
  geometries.forEach(geometry => geometry.dispose())
  materials.forEach(material => {
   const map = (material as THREE.SpriteMaterial).map
   map?.dispose()
   material.dispose()
  })
  renderer.dispose()
  renderer.forceContextLoss()
  renderer.domElement.remove()
 }

 try {
  scene.add(new THREE.HemisphereLight(0xc6edff, 0x293444, 2.6))
  const key = new THREE.DirectionalLight(0xffffff, 3)
  key.position.set(3, 7, 4)
  scene.add(key)
  const rim = new THREE.DirectionalLight(0x58d8f5, 2.5)
  rim.position.set(-4, 2, -3)
  scene.add(rim)

  const carbon = new THREE.MeshStandardMaterial({ color: 0x273442, roughness: 0.5, metalness: 0.55 })
  const metal = new THREE.MeshStandardMaterial({ color: 0x9baab7, roughness: 0.4, metalness: 0.7 })
  const cyan = new THREE.MeshStandardMaterial({ color: 0x68ddeb, emissive: 0x1c5866, roughness: 0.4, metalness: 0.3 })
  const blade = new THREE.MeshStandardMaterial({ color: 0xb8cbd5, roughness: 0.6, metalness: 0.2 })
  const mesh = (geometry: THREE.BufferGeometry, material: THREE.Material, parent: THREE.Object3D, x = 0, y = 0, z = 0) => {
   const object = new THREE.Mesh(geometry, material)
   object.position.set(x, y, z)
   parent.add(object)
   return object
  }
  const tube = (start: THREE.Vector3, end: THREE.Vector3, radius: number, material: THREE.Material) => {
   const delta = end.clone().sub(start)
   const object = mesh(new THREE.CylinderGeometry(radius, radius, delta.length(), 12), material, drone)
   object.position.copy(start).add(end).multiplyScalar(0.5)
   object.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), delta.normalize())
  }

  mesh(new THREE.BoxGeometry(1.05, 0.1, 0.88), carbon, drone, 0, 0.15)
  mesh(new THREE.BoxGeometry(1.05, 0.08, 0.88), metal, drone, 0, -0.16)
  mesh(new THREE.BoxGeometry(0.6, 0.22, 0.55), carbon, drone)
  mesh(new THREE.BoxGeometry(0.45, 0.15, 0.36), metal, drone, 0, 0.28)
  mesh(new THREE.BoxGeometry(0.34, 0.055, 0.12), cyan, drone, 0, 0.22, -0.44)
  for (const x of [-0.4, 0.4]) for (const z of [-0.32, 0.32]) {
   mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.3, 8), metal, drone, x, 0, z)
  }
  for (const x of [-1.18, 1.18]) for (const z of [-1.18, 1.18]) {
   tube(new THREE.Vector3(x * 0.18, 0, z * 0.18), new THREE.Vector3(x, 0, z), 0.065, carbon)
   mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.22, 24), metal, drone, x, 0.12, z)
   mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.045, 24), z < 0 ? cyan : carbon, drone, x, 0.24, z)
   const prop = mesh(new THREE.BoxGeometry(1.1, 0.035, 0.105), blade, drone, x, 0.31, z)
   prop.rotation.y = x * z > 0 ? 0.4 : -0.4
   mesh(new THREE.SphereGeometry(0.07, 12, 8), carbon, drone, x, 0.32, z)
  }
  for (const x of [-0.64, 0.64]) {
   for (const z of [-0.58, 0.58]) tube(new THREE.Vector3(x * 0.58, -0.15, z * 0.6), new THREE.Vector3(x, -0.82, z), 0.04, metal)
   tube(new THREE.Vector3(x, -0.82, -0.85), new THREE.Vector3(x, -0.82, 0.85), 0.045, carbon)
  }
  const nose = new THREE.BufferGeometry().setFromPoints([
   new THREE.Vector3(-0.16, 0.215, -0.17), new THREE.Vector3(0.16, 0.215, -0.17), new THREE.Vector3(0, 0.215, -0.39)
  ])
  nose.setIndex([0, 1, 2])
  nose.computeVertexNormals()
  mesh(nose, new THREE.MeshBasicMaterial({ color: 0x8cf2fa, side: THREE.DoubleSide }), drone)

  // World grid and axes never inherit the vehicle attitude.
  const grid = new THREE.GridHelper(9, 18, 0x3c677a, 0x1b3141)
  grid.position.y = -1.6
  scene.add(grid)
  const makeLabel = (text: string, parent: THREE.Object3D, position: THREE.Vector3, color: string) => {
   const canvas = document.createElement('canvas')
   canvas.width = 256
   canvas.height = 64
   const context = canvas.getContext('2d')!
   context.font = `600 30px ${getComputedStyle(host).fontFamily}`
   context.textAlign = 'center'
   context.fillStyle = color
   context.fillText(text, 128, 43)
   const texture = new THREE.CanvasTexture(canvas)
   texture.colorSpace = THREE.SRGBColorSpace
   const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: texture, depthTest: false }))
   sprite.position.copy(position)
   sprite.scale.set(1.15, 0.29, 1)
   parent.add(sprite)
  }
  makeLabel('FRONT', drone, new THREE.Vector3(0, 0.1, -1.95), '#8cf2fa')
  makeLabel('HORIZONTAL', scene, new THREE.Vector3(0, -1.58, 3.4), '#9cbed1')

  const vectors = new THREE.Group()
  scene.add(vectors)
  const up = new THREE.Vector3(0, 1, 0)
  const origin = new THREE.Vector3()
  const thrust = new THREE.ArrowHelper(up, origin, 1.8, 0x68e4fa, 0.25, 0.14)
  const weight = new THREE.ArrowHelper(new THREE.Vector3(0, -1, 0), origin, 1.4, 0xfa9d74, 0.24, 0.14)
  vectors.add(thrust, weight)
  const vertical = new THREE.Line(
   new THREE.BufferGeometry().setFromPoints([origin, new THREE.Vector3(0, 3.25, 0)]),
   new THREE.LineDashedMaterial({ color: 0x8d9db0, dashSize: 0.12, gapSize: 0.08 })
  )
  vertical.computeLineDistances()
  vectors.add(vertical)
  const arc = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0x9de8f2 }))
  vectors.add(arc)

  const update = (pitch: number, roll: number, ratio: number, showVectors: boolean) => {
   drone.rotation.set(THREE.MathUtils.degToRad(pitch), 0, -THREE.MathUtils.degToRad(roll), 'XYZ')
   const direction = up.clone().applyQuaternion(drone.quaternion)
   thrust.setDirection(direction)
   thrust.setLength(1.4 * ratio, 0.25, 0.14)
   vectors.visible = showVectors
   const tilt = Math.acos(THREE.MathUtils.clamp(direction.y, -1, 1))
   const horizontal = new THREE.Vector3(direction.x, 0, direction.z).normalize()
   const points: THREE.Vector3[] = []
   for (let i = 0; i <= 32; i++) {
    const angle = tilt * i / 32
    points.push(up.clone().multiplyScalar(Math.cos(angle)).addScaledVector(horizontal, Math.sin(angle)).multiplyScalar(0.9))
   }
   arc.geometry.dispose()
   arc.geometry = new THREE.BufferGeometry().setFromPoints(points)
   arc.visible = tilt > 0.001
   ;(arc.material as THREE.LineBasicMaterial).color.setHex(tilt > Math.PI / 4 + 1e-9 ? 0xfac18b : 0x9de8f2)
   render()
  }
  resize.observe(host)
  resetCamera()
  return {
   update, resetCamera, dispose,
   setVisible(value: boolean) { visible = value; if (visible) render() },
   orbitCamera(direction: number) {
    const offset = camera.position.clone().sub(controls.target)
    offset.applyAxisAngle(up, direction * Math.PI / 8)
    camera.position.copy(controls.target).add(offset)
    controls.update()
    render()
   }
  }
 } catch (error) {
  dispose()
  throw error
 }
}
