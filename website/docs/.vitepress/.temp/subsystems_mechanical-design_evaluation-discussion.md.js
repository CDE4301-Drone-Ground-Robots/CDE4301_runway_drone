import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Evaluation & Discussion | Mechanical Design","description":"","frontmatter":{"title":"Evaluation & Discussion | Mechanical Design"},"headers":[],"relativePath":"subsystems/mechanical-design/evaluation-discussion.md","filePath":"subsystems/mechanical-design/evaluation-discussion.md"}');
const _sfc_main = { name: "subsystems/mechanical-design/evaluation-discussion.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><p class="chapter-kicker">Mechanical Design</p><h1 id="evaluation-discussion" tabindex="-1">Evaluation &amp; Discussion <a class="header-anchor" href="#evaluation-discussion" aria-label="Permalink to &quot;Evaluation &amp; Discussion&quot;">​</a></h1><p><strong>Subsystem lead:</strong> Muruganantham Arun<br><strong>Matriculation number:</strong> A0308280J</p><div class="info custom-block"><p class="custom-block-title">Documentation pending</p><p>This section is ready for the subsystem report content.</p></div><h2 id="comparison-against-requirements" tabindex="-1">Comparison Against Requirements <a class="header-anchor" href="#comparison-against-requirements" aria-label="Permalink to &quot;Comparison Against Requirements&quot;">​</a></h2><p><em>To be added.</em></p><h2 id="performance-discussion" tabindex="-1">Performance Discussion <a class="header-anchor" href="#performance-discussion" aria-label="Permalink to &quot;Performance Discussion&quot;">​</a></h2><p><em>To be added.</em></p><h2 id="limitations-uncertainties-and-trade-offs" tabindex="-1">Limitations, Uncertainties and Trade-offs <a class="header-anchor" href="#limitations-uncertainties-and-trade-offs" aria-label="Permalink to &quot;Limitations, Uncertainties and Trade-offs&quot;">​</a></h2><p><em>To be added.</em></p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("subsystems/mechanical-design/evaluation-discussion.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const evaluationDiscussion = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  evaluationDiscussion as default
};
