import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Navigation & Obstacle Avoidance","description":"","frontmatter":{"title":"Navigation & Obstacle Avoidance","outline":false},"headers":[],"relativePath":"subsystems/navigation-obstacle-avoidance.md","filePath":"subsystems/navigation-obstacle-avoidance.md"}');
const _sfc_main = { name: "subsystems/navigation-obstacle-avoidance.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="navigation-obstacle-avoidance" tabindex="-1">Navigation &amp; Obstacle Avoidance <a class="header-anchor" href="#navigation-obstacle-avoidance" aria-label="Permalink to &quot;Navigation &amp; Obstacle Avoidance&quot;">​</a></h1><p><strong>Subsystem lead:</strong> Kummarikunta Talitha<br><strong>Matriculation number:</strong> A0286653R</p><h2 id="subsystem-report" tabindex="-1">Subsystem Report <a class="header-anchor" href="#subsystem-report" aria-label="Permalink to &quot;Subsystem Report&quot;">​</a></h2><p>Select a section to read this subsystem&#39;s report. Documentation will be added as the project develops.</p><ol><li><a href="./navigation-obstacle-avoidance/executive-summary">Executive Summary</a> - Purpose, main engineering problem, and selected approach.</li><li><a href="./navigation-obstacle-avoidance/subsystem-overview">Subsystem Overview</a> - Operation and interfaces with the rest of FOD ARGUS.</li><li><a href="./navigation-obstacle-avoidance/requirements-considerations">Requirements and Considerations</a> - Required performance, constraints, and design considerations.</li><li><a href="./navigation-obstacle-avoidance/design-iterations-selection">Design Iterations and Selection</a> - Alternatives explored and reasons for selecting the final design.</li><li><a href="./navigation-obstacle-avoidance/detailed-design-implementation">Detailed Design and Implementation</a> - Development and implementation of the selected solution.</li><li><a href="./navigation-obstacle-avoidance/testing-methodology-results">Testing Methodology &amp; Results</a> - What was tested, why, how, and the measured results.</li><li><a href="./navigation-obstacle-avoidance/evaluation-discussion">Evaluation &amp; Discussion</a> - Performance against requirements, limitations, uncertainties, and trade-offs.</li><li><a href="./navigation-obstacle-avoidance/improvements-lessons-learned">Improvements &amp; Lessons Learned</a> - Development challenges, improvements, and engineering lessons.</li><li><a href="./navigation-obstacle-avoidance/semester-2-development-plan">Semester 2 Development Plan</a> - Next-stage objectives, tasks, milestones, and validation.</li></ol></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("subsystems/navigation-obstacle-avoidance.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const navigationObstacleAvoidance = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  navigationObstacleAvoidance as default
};
