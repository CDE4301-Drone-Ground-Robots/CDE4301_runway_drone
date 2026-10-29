import { cvSubsystemSections } from './cv-subsystem-sections'
import { subsystems } from './theme/components/subsystems'
import { defineConfig } from 'vitepress'
const reportSidebar = [
 { text: 'PROJECT REPORT', items: [
  { text: 'Report overview', link: '/report/' },
  { text: 'Project scope', link: '/scopes' },
  { text: 'Primary Research', link: '/research/primary' },
  { text: 'Secondary Research', link: '/research/secondary' },
  { text: 'System architecture', link: '/report/system-architecture' }
 ] },
 { text: 'SUBSYSTEM REPORTS', items: subsystems.map(subsystem => ({
  text: subsystem.title,
  link: '/subsystems/' + subsystem.slug,
  ...(subsystem.slug === 'computer-vision' ? {
   collapsed: false,
   items: cvSubsystemSections.map((section, index) => ({
    text: (index + 1) + '. ' + section.title,
    link: '/subsystems/computer-vision#' + section.slug
   }))
  } : {})
 })) },
 { text: 'DEVELOPMENT & SOURCES', items: [
  { text: 'Timeline', link: '/timeline' },
  { text: 'Future works', link: '/report/future-works' },
  { text: 'References', link: '/references' }
 ] }
]
export default defineConfig({
 title: 'FOD ARGUS',
 description: 'FOD ARGUS - Autonomous Runway Inspection UAV. NUS CDE4301.',
 lang: 'en-SG', base: '/CDE4301_runway_drone/', cleanUrls: true,
 appearance: 'dark',
 head: [['meta', { name: 'theme-color', content: '#08090b' }], ['link', { rel: 'icon', href: '/CDE4301_runway_drone/favicon.svg', type: 'image/svg+xml' }]],
 markdown: { math: true, lineNumbers: true },
 vite: { server: { strictPort: true } },
 vue: { template: { compilerOptions: { isCustomElement: tag => tag === 'model-viewer' } } },
 themeConfig: {
  siteTitle: false,
  nav: [
   { text: 'Overview', link: '/' },
   { text: 'Meet the Team', link: '/team' },
   { text: 'Research', activeMatch: '/research/', items: [
    { text: 'Primary Research', link: '/research/primary' },
    { text: 'Secondary Research', link: '/research/secondary' }
   ] },
   { text: 'Drone Specification', link: '/engineering/drone-specification' },
   { component: 'SubsystemNav' },
   { text: 'Timeline', link: '/timeline' },
   { text: 'References', link: '/references' },
   { text: 'Report', link: '/report/', activeMatch: '/(report/|scopes)' }
  ],
  sidebar: Object.fromEntries(['/report/', '/subsystems/', '/research/', '/scopes', '/timeline', '/references'].map(path => [path, reportSidebar])),
  docFooter: { prev: false, next: false },
  search: { provider: 'local' },
  outline: { level: [2, 3], label: 'On this page' },
  footer: { message: 'NUS | College of Design and Engineering', copyright: 'FOD ARGUS / CDE4301' }
 }
})
