export type MechanicalSection = {
 slug: string
 title: string
 sections?: MechanicalSection[]
}

import { subsystemRubricSections } from './rubric-sections'

export const mechanicalSubsystemSections: MechanicalSection[] = subsystemRubricSections('mechanical-design')

type MechanicalSidebarItem = { text: string; link: string }

export function numberedMechanicalSections(): MechanicalSidebarItem[] {
 return mechanicalSubsystemSections.map(section => {
  return {
   text: section.title,
   link: '/subsystems/mechanical-design#' + section.slug
  }
 })
}

export function flattenMechanicalSections(sections = mechanicalSubsystemSections): MechanicalSection[] {
 return sections.flatMap(section => [section, ...flattenMechanicalSections(section.sections ?? [])])
}
