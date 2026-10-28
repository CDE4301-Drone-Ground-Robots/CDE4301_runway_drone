import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Future Works","description":"","frontmatter":{"title":"Future Works"},"headers":[],"relativePath":"report/future-works.md","filePath":"report/future-works.md"}');
const _sfc_main = { name: "report/future-works.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><p class="chapter-kicker">FOD ARGUS / PROJECT REPORT</p><h1 id="future-works" tabindex="-1">Future Works <a class="header-anchor" href="#future-works" aria-label="Permalink to &quot;Future Works&quot;">​</a></h1><div class="info custom-block"><p class="custom-block-title">Documentation pending</p><p>Project-level future work and integration plans will be added here.</p></div></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("report/future-works.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const futureWorks = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  futureWorks as default
};
