import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Subsystem Overview | Navigation & Obstacle Avoidance","description":"","frontmatter":{"title":"Subsystem Overview | Navigation & Obstacle Avoidance"},"headers":[],"relativePath":"subsystems/navigation-obstacle-avoidance/subsystem-overview.md","filePath":"subsystems/navigation-obstacle-avoidance/subsystem-overview.md"}');
const _sfc_main = { name: "subsystems/navigation-obstacle-avoidance/subsystem-overview.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><p class="chapter-kicker">Navigation &amp; Obstacle Avoidance</p><h1 id="subsystem-overview" tabindex="-1">Subsystem Overview <a class="header-anchor" href="#subsystem-overview" aria-label="Permalink to &quot;Subsystem Overview&quot;">​</a></h1><p><strong>Subsystem lead:</strong> Kummarikunta Talitha<br><strong>Matriculation number:</strong> A0286653R</p><div class="info custom-block"><p class="custom-block-title">Documentation pending</p><p>This section is ready for the subsystem report content.</p></div><h2 id="how-the-subsystem-operates" tabindex="-1">How the Subsystem Operates <a class="header-anchor" href="#how-the-subsystem-operates" aria-label="Permalink to &quot;How the Subsystem Operates&quot;">​</a></h2><p><em>To be added.</em></p><h2 id="interfaces-with-other-subsystems" tabindex="-1">Interfaces with Other Subsystems <a class="header-anchor" href="#interfaces-with-other-subsystems" aria-label="Permalink to &quot;Interfaces with Other Subsystems&quot;">​</a></h2><p><em>To be added.</em></p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("subsystems/navigation-obstacle-avoidance/subsystem-overview.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const subsystemOverview = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  subsystemOverview as default
};
