import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Electrical Design","description":"","frontmatter":{"title":"Electrical Design","outline":false},"headers":[],"relativePath":"subsystems/electrical-design.md","filePath":"subsystems/electrical-design.md"}');
const _sfc_main = { name: "subsystems/electrical-design.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="electrical-design" tabindex="-1">Electrical Design <a class="header-anchor" href="#electrical-design" aria-label="Permalink to &quot;Electrical Design&quot;">​</a></h1><p><strong>Subsystem lead:</strong> Kummarikunta Talitha<br><strong>Matriculation number:</strong> A0286653R</p><h2 id="subsystem-report" tabindex="-1">Subsystem Report <a class="header-anchor" href="#subsystem-report" aria-label="Permalink to &quot;Subsystem Report&quot;">​</a></h2><p>Select a section to read this subsystem&#39;s report. Documentation will be added as the project develops.</p><ol><li><a href="./electrical-design/executive-summary">Executive Summary</a> - Purpose, main engineering problem, and selected approach.</li><li><a href="./electrical-design/subsystem-overview">Subsystem Overview</a> - Operation and interfaces with the rest of FOD ARGUS.</li><li><a href="./electrical-design/requirements-considerations">Requirements and Considerations</a> - Required performance, constraints, and design considerations.</li><li><a href="./electrical-design/design-iterations-selection">Design Iterations and Selection</a> - Alternatives explored and reasons for selecting the final design.</li><li><a href="./electrical-design/detailed-design-implementation">Detailed Design and Implementation</a> - Development and implementation of the selected solution.</li><li><a href="./electrical-design/testing-methodology-results">Testing Methodology &amp; Results</a> - What was tested, why, how, and the measured results.</li><li><a href="./electrical-design/evaluation-discussion">Evaluation &amp; Discussion</a> - Performance against requirements, limitations, uncertainties, and trade-offs.</li><li><a href="./electrical-design/improvements-lessons-learned">Improvements &amp; Lessons Learned</a> - Development challenges, improvements, and engineering lessons.</li><li><a href="./electrical-design/semester-2-development-plan">Semester 2 Development Plan</a> - Next-stage objectives, tasks, milestones, and validation.</li></ol></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("subsystems/electrical-design.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const electricalDesign = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  electricalDesign as default
};
