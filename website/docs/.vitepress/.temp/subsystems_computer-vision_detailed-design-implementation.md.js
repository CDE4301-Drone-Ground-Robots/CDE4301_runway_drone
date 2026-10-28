import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Detailed Design and Implementation | Computer Vision Based Inspection and Safety System","description":"","frontmatter":{"title":"Detailed Design and Implementation | Computer Vision Based Inspection and Safety System"},"headers":[],"relativePath":"subsystems/computer-vision/detailed-design-implementation.md","filePath":"subsystems/computer-vision/detailed-design-implementation.md"}');
const _sfc_main = { name: "subsystems/computer-vision/detailed-design-implementation.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><p class="chapter-kicker">Computer Vision Based Inspection and Safety System</p><h1 id="detailed-design-and-implementation" tabindex="-1">Detailed Design and Implementation <a class="header-anchor" href="#detailed-design-and-implementation" aria-label="Permalink to &quot;Detailed Design and Implementation&quot;">​</a></h1><p><strong>Subsystem lead:</strong> Charansagar Ramanujam<br><strong>Matriculation number:</strong> A0301658E</p><div class="info custom-block"><p class="custom-block-title">Documentation pending</p><p>This section is ready for the subsystem report content.</p></div><h2 id="selected-design" tabindex="-1">Selected Design <a class="header-anchor" href="#selected-design" aria-label="Permalink to &quot;Selected Design&quot;">​</a></h2><p><em>To be added.</em></p><h2 id="implementation-and-integration" tabindex="-1">Implementation and Integration <a class="header-anchor" href="#implementation-and-integration" aria-label="Permalink to &quot;Implementation and Integration&quot;">​</a></h2><p><em>To be added.</em></p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("subsystems/computer-vision/detailed-design-implementation.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const detailedDesignImplementation = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  detailedDesignImplementation as default
};
