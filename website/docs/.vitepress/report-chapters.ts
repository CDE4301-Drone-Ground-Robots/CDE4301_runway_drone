export const reportChapters = [
 { id: 'project-scope', title: 'Project scope', path: '/scopes' },
 { id: 'research', title: 'Research', path: '/research' },
 { id: 'system-architecture', title: 'System architecture', path: '/report/system-architecture' },
 { id: 'mechanical-design', title: 'Mechanical Design', path: '/subsystems/mechanical-design' },
 { id: 'electrical-design', title: 'Electrical Design', path: '/subsystems/electrical-design' },
 { id: 'navigation-obstacle-avoidance', title: 'Navigation & Obstacle Avoidance', path: '/subsystems/navigation-obstacle-avoidance' },
 { id: 'computer-vision', title: 'Computer Vision Based Inspection and Safety System', path: '/subsystems/computer-vision' },
 { id: 'communication-system', title: 'Communication System', path: '/subsystems/communication-system' },
 { id: 'timeline', title: 'Timeline', path: '/timeline' },
 { id: 'references', title: 'References', path: '/references' },
 { id: 'appendices', title: 'Appendices', path: '/appendices' }
]

export function reportAnchor(chapter: string, heading?: string) {
 return 'report-' + chapter + (heading ? '--' + heading : '')
}

export function continuousReportLink(link: string) {
 const [pathname, hash] = link.split('#')
 const path = pathname.replace(/\.html$/, '').replace(/\/$/, '')
 if (path === '/report') return '/report/#report-overview'
 if (path === '/research/primary' || path === '/research/secondary') {
  const section = path.endsWith('/primary') ? 'primary-research' : 'secondary-research'
  return '/report/#' + reportAnchor('research', hash || section)
 }
 const chapter = reportChapters.find(chapter => chapter.path === path)
 return chapter ? '/report/#' + reportAnchor(chapter.id, hash) : link
}
