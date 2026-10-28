import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Executive Summary | Electrical Design","description":"","frontmatter":{"title":"Executive Summary | Electrical Design"},"headers":[],"relativePath":"subsystems/electrical-design/executive-summary.md","filePath":"subsystems/electrical-design/executive-summary.md"}');
const _sfc_main = { name: "subsystems/electrical-design/executive-summary.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><p class="chapter-kicker">Electrical Design</p><h1 id="executive-summary" tabindex="-1">Executive Summary <a class="header-anchor" href="#executive-summary" aria-label="Permalink to &quot;Executive Summary&quot;">​</a></h1><p><strong>Subsystem lead:</strong> Kummarikunta Talitha<br><strong>Matriculation number:</strong> A0286653R</p><div class="info custom-block"><p class="custom-block-title">Documentation pending</p><p>This section is ready for the subsystem report content.</p></div><h2 id="purpose" tabindex="-1">Purpose <a class="header-anchor" href="#purpose" aria-label="Permalink to &quot;Purpose&quot;">​</a></h2><p><em>To be added.</em></p><h2 id="main-engineering-problem" tabindex="-1">Main Engineering Problem <a class="header-anchor" href="#main-engineering-problem" aria-label="Permalink to &quot;Main Engineering Problem&quot;">​</a></h2><p><em>To be added.</em></p><h2 id="selected-approach" tabindex="-1">Selected Approach <a class="header-anchor" href="#selected-approach" aria-label="Permalink to &quot;Selected Approach&quot;">​</a></h2><p><em>To be added.</em></p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("subsystems/electrical-design/executive-summary.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const executiveSummary = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  executiveSummary as default
};
