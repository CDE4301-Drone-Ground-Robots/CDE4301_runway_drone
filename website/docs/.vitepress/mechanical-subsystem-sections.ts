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
   { slug: 'final-prototype-design', title: 'Final Prototype Design' },
   { slug: 'interactive-uav-attitude-thrust-simulator', title: 'Interactive UAV Attitude & Thrust Simulator' }
  ]
 }
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
