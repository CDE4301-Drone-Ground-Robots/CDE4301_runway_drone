export type MechanicalSection = {
 slug: string
 title: string
 sections?: MechanicalSection[]
}

// Mirror the report's heading hierarchy without adding numbers to its text.
export const mechanicalSubsystemSections: MechanicalSection[] = [
 {
  slug: 'overview-of-mechanical-design-of-the-uav',
  title: 'Overview of Mechanical Design of the UAV',
  sections: [
   { slug: 'initial-concept-sketch', title: 'Initial Concept Sketch' },
   { slug: 'plus-vs-x-vs-h-propeller-configuration', title: 'Plus vs X vs H Propeller Configuration' },
   { slug: 'pusher-vs-puller-configuration', title: 'Pusher vs Puller Configuration' }
  ]
 },
 {
  slug: 'design-iterations',
  title: 'Design Iterations',
  sections: [
   { slug: 'first-iteration', title: 'First Iteration', sections: [
    { slug: 'limitations', title: 'Limitations' },
    { slug: 'cfrp-sheets-tubes-vs-3d-printed-parts', title: 'CFRP Sheets & Tubes vs 3D-Printed Parts' }
   ] },
   { slug: 'second-iteration', title: 'Second Iteration', sections: [
    { slug: 'limitations-1', title: 'Limitations' }
   ] },
   { slug: 'final-prototype-design', title: 'Final Prototype Design' }
  ]
 },
 { slug: 'centre-of-gravity-cg-of-uav', title: 'Centre of Gravity (CG) of UAV', sections: [
  { slug: 'horizontal-cg-positioning', title: 'Horizontal CG Positioning' },
  { slug: 'vertical-cg-positioning', title: 'Vertical CG Positioning' }
 ] },
 { slug: 'placement-of-key-onboard-components', title: 'Placement of Key Onboard Components', sections: [
  { slug: 'central-alignment-of-gnss-antenna-and-rgb-camera', title: 'Central Alignment of GNSS Antenna and RGB Camera' },
  { slug: 'placement-of-the-pixhawk-flight-controller-near-centre-of-gravity', title: 'Placement of the Pixhawk Flight Controller near Centre of Gravity' },
  { slug: 'placement-of-the-360-lidar', title: 'Placement of the 360° LiDAR' },
  { slug: '45-degree-placement-of-the-thermal-camera', title: '45° Placement of the Thermal Camera' },
  { slug: 'placement-of-batteries-and-other-electrical-components-in-the-bottom-layer', title: 'Placement of Batteries and Other Electrical Components in the Bottom Layer' }
 ] },
 { slug: 'motor-propellers-selection', title: 'Motor & Propellers Selection', sections: [
  { slug: 'interactive-uav-attitude-thrust-simulator', title: 'Interactive UAV Attitude & Thrust Simulator' }
 ] },
 { slug: 'propeller-arm-selection', title: 'Propeller Arm Selection', sections: [
  { slug: 'bending-stress-calculation', title: 'Bending Stress Calculation' },
  { slug: 'beam-deflection-calculation', title: 'Beam Deflection Calculation' },
  { slug: 'natural-bending-frequency-calculation', title: 'Natural Bending Frequency Calculation' },
  { slug: 'evaluation-of-different-beam-configurations', title: 'Evaluation of Different Beam Configurations' }
 ] }
]

type MechanicalSidebarItem = { text: string; link: string }

export function numberedMechanicalSections(): MechanicalSidebarItem[] {
 return mechanicalSubsystemSections.map((section, index) => {
  const number = index + 1
  return {
   text: number + '. ' + section.title,
   link: '/subsystems/mechanical-design#' + section.slug
  }
 })
}

export function flattenMechanicalSections(sections = mechanicalSubsystemSections): MechanicalSection[] {
 return sections.flatMap(section => [section, ...flattenMechanicalSections(section.sections ?? [])])
}
