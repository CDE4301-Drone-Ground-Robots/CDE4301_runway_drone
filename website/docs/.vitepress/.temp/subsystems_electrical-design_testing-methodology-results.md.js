import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Testing Methodology & Results | Electrical Design","description":"","frontmatter":{"title":"Testing Methodology & Results | Electrical Design"},"headers":[],"relativePath":"subsystems/electrical-design/testing-methodology-results.md","filePath":"subsystems/electrical-design/testing-methodology-results.md"}');
const _sfc_main = { name: "subsystems/electrical-design/testing-methodology-results.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><p class="chapter-kicker">Electrical Design</p><h1 id="testing-methodology-results" tabindex="-1">Testing Methodology &amp; Results <a class="header-anchor" href="#testing-methodology-results" aria-label="Permalink to &quot;Testing Methodology &amp; Results&quot;">​</a></h1><p><strong>Subsystem lead:</strong> Kummarikunta Talitha<br><strong>Matriculation number:</strong> A0286653R</p><div class="info custom-block"><p class="custom-block-title">Documentation pending</p><p>This section is ready for the subsystem report content.</p></div><h2 id="test-objectives" tabindex="-1">Test Objectives <a class="header-anchor" href="#test-objectives" aria-label="Permalink to &quot;Test Objectives&quot;">​</a></h2><p><em>To be added.</em></p><h2 id="methodology-and-setup" tabindex="-1">Methodology and Setup <a class="header-anchor" href="#methodology-and-setup" aria-label="Permalink to &quot;Methodology and Setup&quot;">​</a></h2><p><em>To be added.</em></p><h2 id="results" tabindex="-1">Results <a class="header-anchor" href="#results" aria-label="Permalink to &quot;Results&quot;">​</a></h2><p><em>To be added.</em></p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("subsystems/electrical-design/testing-methodology-results.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const testingMethodologyResults = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  testingMethodologyResults as default
};
