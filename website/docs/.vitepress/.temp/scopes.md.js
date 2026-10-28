import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Project Scope","description":"","frontmatter":{"title":"Project Scope"},"headers":[],"relativePath":"scopes.md","filePath":"scopes.md"}');
const _sfc_main = { name: "scopes.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><p class="chapter-kicker">FOD ARGUS / PROJECT REPORT</p><h1 id="project-scope" tabindex="-1">Project Scope <a class="header-anchor" href="#project-scope" aria-label="Permalink to &quot;Project Scope&quot;">​</a></h1><div class="info custom-block"><p class="custom-block-title">Documentation pending</p><p>Project scope, boundaries, and individual responsibilities will be added here.</p></div></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("scopes.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const scopes = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  scopes as default
};
