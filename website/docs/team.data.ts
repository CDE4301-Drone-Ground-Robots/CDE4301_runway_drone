import { existsSync, readdirSync } from 'node:fs'
import { resolve } from 'node:path'

const members = [
 {
  name: 'Charansagar Ramanujam', initials: 'CR', role: 'Computer Vision & Communication', detail: 'Design & Programming', color: '#ef5350', portrait: 'charan',
  subsystemSlugs: ["computer-vision","communication-system"],
  crop: { x: 15, y: 32, w: 322, h: 274 },
  contributions: [
   'Computer Vision System Architecture & Pipeline Development.',
   'PatchCore Anomaly Detection Integration.',
   'YOLO-Based FOD Detection & Model Benchmarking.',
   'U-Net Crack Segmentation Integration.',
   'FOD Dataset Integrity Audit & Similarity-Aware Data Splitting.',
   'Synthetic FOD Dataset Generation & Domain Adaptation.',
   'RGB Camera Evaluation, Selection & Imaging Requirement Analysis.',
   'Thermal Camera Evaluation & Safety-Monitoring Integration.',
   'Image-to-World Coordinate Localisation for FOD/Crack Detection.',
   'Jetson Orin NX Vision Pipeline & Latency Feasibility Analysis.',
   'UAV-UGV Coordinate Communication Architecture using ROS 2 software.',
   'Secondary Research.',
   'Website Report Design (GitHub).'
  ]
 },
 {
  name: 'Muruganantham Arun', initials: 'MA', role: 'Mechanical Design', detail: '', color: '#ad73de', portrait: 'arun',
  subsystemSlugs: ["mechanical-design"],
  crop: { x: 844, y: 0, w: 262, h: 288 },
  contributions: [
   'Overall Mechanical Design of FOD Argus Prototype',
   'Component Placement and CG Analysis',
   'Motor Calculations (Thrust)',
   'Propeller Arm Calculations (CF Tube Selection)',
   'Prototyping and Testing',
   'Secondary Research'
  ]
 },
 {
  name: 'Talitha Kummarikunta', initials: 'TK', role: 'Electrical Design & Navigation', detail: '', color: '#48b4e5', portrait: 'talitha',
  subsystemSlugs: ["electrical-design","navigation-obstacle-avoidance"],
  crop: { x: 1673, y: 8, w: 367, h: 279 },
  contributions: [
   'Wiring and Sensor Communication',
   'Power Calculations',
   'Survey Method Optimisation',
   'Navigation and Obstacle Avoidance',
   'Emergency Failsafe Measures',
   'Stress Testing of Flight Kinematics for Limit Determination',
   'Simulation (Gazebo)',
   'Secondary Research'
  ]
 }
]

export default {
 watch: ['public/team/*'],
 load() {
  const directory = resolve(process.cwd(), 'docs/public/team')
  const files = existsSync(directory) ? readdirSync(directory) : []
  const findImage = (stem: string) => files.find(file =>
   ['png', 'jpg', 'jpeg', 'webp'].some(extension => file.toLowerCase() === `${stem}.${extension}`)
  )
  const sheet = findImage('portraits')
  return {
   // Crop positions are expressed against the displayed 2048 x 579 portrait sheet.
   sheet: sheet ? '/team/' + sheet : null,
   members: members.map(member => {
    const photo = findImage(member.portrait)
    return { ...member, photo: photo ? '/team/' + photo : null }
   })
  }
 }
}