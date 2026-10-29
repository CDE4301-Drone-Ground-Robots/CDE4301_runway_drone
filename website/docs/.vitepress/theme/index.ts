import SubsystemLead from './components/SubsystemLead.vue'
import ReportScrollSync from './components/ReportScrollSync.vue'
import CvFigure from './components/CvFigure.vue'
import CursorSpotlight from './components/CursorSpotlight.vue'
import SubsystemNav from './components/SubsystemNav.vue'
import SubsystemOverview from './components/SubsystemOverview.vue'
import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import { h } from 'vue'
import RunwayHome from './components/RunwayHome.vue'
import ThemeToggle from './components/ThemeToggle.vue'
import HeaderIdentity from './components/HeaderIdentity.vue'
import './style.css'
import './team.css'
import TeamCarousel from './components/TeamCarousel.vue'
export default {
 extends: DefaultTheme,
 Layout: () => h(DefaultTheme.Layout, null, {
  'layout-bottom': () => [h(CursorSpotlight), h(ReportScrollSync)],
  'sidebar-nav-before': () => h('div', { class: 'report-sidebar-identity' }, [
   h('span', 'FOD ARGUS'), h('small', 'ENGINEERING REPORT / AIS-407')
  ]),
  'nav-bar-content-after': () => h(ThemeToggle),
  'nav-bar-title-before': () => h(HeaderIdentity)
 }),
 enhanceApp({ app }) {
  app.component('SubsystemLead', SubsystemLead)
  app.component('CvFigure', CvFigure)
  app.component('SubsystemNav', SubsystemNav)
  app.component('SubsystemOverview', SubsystemOverview)
  app.component('RunwayHome', RunwayHome)
  app.component('TeamCarousel', TeamCarousel)
 }
} satisfies Theme
