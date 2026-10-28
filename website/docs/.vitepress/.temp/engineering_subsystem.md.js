import { resolveComponent, useSSRContext } from "vue";
import { ssrRenderAttrs, ssrRenderComponent } from "vue/server-renderer";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Subsystems","description":"","frontmatter":{"layout":"page","title":"Subsystems","sidebar":false,"outline":false},"headers":[],"relativePath":"engineering/subsystem.md","filePath":"engineering/subsystem.md"}');
const _sfc_main = { name: "engineering/subsystem.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  const _component_SubsystemOverview = resolveComponent("SubsystemOverview");
  _push(`<div${ssrRenderAttrs(_attrs)}>`);
  _push(ssrRenderComponent(_component_SubsystemOverview, null, null, _parent));
  _push(`</div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("engineering/subsystem.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const subsystem = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  subsystem as default
};
