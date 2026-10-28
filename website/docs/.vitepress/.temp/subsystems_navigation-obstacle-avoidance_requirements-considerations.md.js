import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Requirements and Considerations | Navigation & Obstacle Avoidance","description":"","frontmatter":{"title":"Requirements and Considerations | Navigation & Obstacle Avoidance"},"headers":[],"relativePath":"subsystems/navigation-obstacle-avoidance/requirements-considerations.md","filePath":"subsystems/navigation-obstacle-avoidance/requirements-considerations.md"}');
const _sfc_main = { name: "subsystems/navigation-obstacle-avoidance/requirements-considerations.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><p class="chapter-kicker">Navigation &amp; Obstacle Avoidance</p><h1 id="requirements-and-considerations" tabindex="-1">Requirements and Considerations <a class="header-anchor" href="#requirements-and-considerations" aria-label="Permalink to &quot;Requirements and Considerations&quot;">​</a></h1><p><strong>Subsystem lead:</strong> Kummarikunta Talitha<br><strong>Matriculation number:</strong> A0286653R</p><div class="info custom-block"><p class="custom-block-title">Documentation pending</p><p>This section is ready for the subsystem report content.</p></div><h2 id="subsystem-requirements" tabindex="-1">Subsystem Requirements <a class="header-anchor" href="#subsystem-requirements" aria-label="Permalink to &quot;Subsystem Requirements&quot;">​</a></h2><p><em>To be added.</em></p><h2 id="constraints-and-design-considerations" tabindex="-1">Constraints and Design Considerations <a class="header-anchor" href="#constraints-and-design-considerations" aria-label="Permalink to &quot;Constraints and Design Considerations&quot;">​</a></h2><p><em>To be added.</em></p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("subsystems/navigation-obstacle-avoidance/requirements-considerations.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const requirementsConsiderations = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  requirementsConsiderations as default
};
