import { continuousReportLink } from './report-chapters'
import { communicationSubsystemSections } from './communication-subsystem-sections'
import { cvSubsystemSections } from './cv-subsystem-sections'
import { numberedMechanicalSections } from './mechanical-subsystem-sections'
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
  } : subsystem.slug === 'mechanical-design' ? {
   collapsed: false,
   items: numberedMechanicalSections()
  } : subsystem.slug === 'communication-system' ? {
   collapsed: false,
   items: communicationSubsystemSections.map((section, index) => ({
    text: (index + 1) + '. ' + section.title,
    link: '/subsystems/communication-system#' + section.slug
   }))
  } : {})
 })) },
 { text: 'DEVELOPMENT & SOURCES', items: [
  { text: 'Timeline', link: '/timeline' },
  { text: 'References', link: '/references' }
 ] }
]
type ReportSidebarItem = { text: string; link?: string; items?: ReportSidebarItem[]; collapsed?: boolean }
function continuousSidebar(items: ReportSidebarItem[]): ReportSidebarItem[] {
 return items.map(item => ({
  ...item,
  ...(item.link ? { link: continuousReportLink(item.link) } : {}),
  ...(item.items ? { items: continuousSidebar(item.items) } : {})
 }))
}
export default defineConfig({
 title: 'FOD ARGUS',
 description: 'FOD ARGUS - Autonomous Runway Inspection UAV. NUS CDE4301.',
 lang: 'en-SG', base: '/CDE4301_runway_drone/', cleanUrls: true,
 appearance: 'dark',
 head: [['meta', { name: 'theme-color', content: '#08090b' }], ['link', { rel: 'icon', href: '/CDE4301_runway_drone/favicon.svg', type: 'image/svg+xml' }]],
 markdown: {
  math: true, lineNumbers: true,
  config(md) {
   // Use MathJax's semantic MathML for selectable, numbered report equations.
   const renderMath = md.renderer.rules.math_block!
   md.renderer.rules.math_block = (tokens, index, options, env, renderer) => {
    if (env.relativePath !== 'subsystems/mechanical-design.md') {
     return renderMath(tokens, index, options, env, renderer)
    }
    const source = tokens[index].content
    const number = source.match(/\\tag\{(\d+)\}/)?.[1]
    if (!number) return renderMath(tokens, index, options, env, renderer)
    tokens[index].content = source.replace(/\\tag\{\d+\}/, '')
    let rendered: string
    try { rendered = renderMath(tokens, index, options, env, renderer) }
    finally { tokens[index].content = source }
    const math = rendered.match(/<math[\s\S]*?<\/math>/)?.[0]
    if (!math) throw new Error('Missing MathML for mechanical report equation ' + number)
    return '<div class="mechanical-equation" id="equation-md-' + number + '"><div class="mechanical-equation-math">' + math + '</div><span class="mechanical-equation-number">(' + number + ')</span></div>'
   }
  }
 },
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
   { text: 'Report', link: '/report/', activeMatch: '/(report/|scopes)' },
   { text: 'Timeline', link: '/timeline' },
   { text: 'References', link: '/references' }
  ],
  sidebar: Object.fromEntries(['/report/', '/subsystems/', '/research/', '/scopes', '/timeline', '/references'].map(path => [path, path === '/report/' ? continuousSidebar(reportSidebar) : reportSidebar])),
  docFooter: { prev: false, next: false },
  search: {
   provider: 'local',
   options: {
    detailedView: true,
    // Index the report chapters; each result uses its rendered heading anchor.
    _render(src, env, md) {
     const page = env.relativePath.replace(/\\/g, '/')
     const isReport = /^(report|subsystems|research)\//.test(page)
      || /^(scopes|timeline|references)\.md$/.test(page)
     if (!isReport) return ''
     const html = md.render(src, env)
     return env.frontmatter?.search === false ? '' : html
    }
   }
  },
  outline: { level: [2, 3], label: 'On this page' },
  footer: { message: 'NUS | College of Design and Engineering', copyright: 'FOD ARGUS / CDE4301' }
 }
})
