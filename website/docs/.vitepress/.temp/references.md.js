import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"References","description":"","frontmatter":{"title":"References"},"headers":[],"relativePath":"references.md","filePath":"references.md"}');
const _sfc_main = { name: "references.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><p class="chapter-kicker">FOD ARGUS / PROJECT REPORT</p><h1 id="references" tabindex="-1">References <a class="header-anchor" href="#references" aria-label="Permalink to &quot;References&quot;">​</a></h1><div class="info custom-block"><p class="custom-block-title">Documentation pending</p><p>Project references will be added here alongside citations in the report chapters.</p></div></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("references.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const references = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  references as default
};
