import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"System Architecture","description":"","frontmatter":{"title":"System Architecture"},"headers":[],"relativePath":"report/system-architecture.md","filePath":"report/system-architecture.md"}');
const _sfc_main = { name: "report/system-architecture.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><p class="chapter-kicker">FOD ARGUS / PROJECT REPORT</p><h1 id="system-architecture" tabindex="-1">System Architecture <a class="header-anchor" href="#system-architecture" aria-label="Permalink to &quot;System Architecture&quot;">​</a></h1><p>The project is organised into five subsystem reports. Each report documents its operation, requirements, design development, implementation, testing, evaluation, lessons learned, and Semester 2 plan.</p><h2 id="subsystem-responsibilities" tabindex="-1">Subsystem Responsibilities <a class="header-anchor" href="#subsystem-responsibilities" aria-label="Permalink to &quot;Subsystem Responsibilities&quot;">​</a></h2><table tabindex="0"><thead><tr><th>Subsystem</th><th>Lead</th></tr></thead><tbody><tr><td><a href="./../subsystems/mechanical-design">Mechanical Design</a></td><td>Muruganantham Arun</td></tr><tr><td><a href="./../subsystems/electrical-design">Electrical Design</a></td><td>Kummarikunta Talitha</td></tr><tr><td><a href="./../subsystems/navigation-obstacle-avoidance">Navigation &amp; Obstacle Avoidance</a></td><td>Kummarikunta Talitha</td></tr><tr><td><a href="./../subsystems/computer-vision">Computer Vision Based Inspection and Safety System</a></td><td>Charansagar Ramanujam</td></tr><tr><td><a href="./../subsystems/communication-system">Communication System</a></td><td>Charansagar Ramanujam</td></tr></tbody></table><h2 id="integrated-architecture-and-interfaces" tabindex="-1">Integrated Architecture and Interfaces <a class="header-anchor" href="#integrated-architecture-and-interfaces" aria-label="Permalink to &quot;Integrated Architecture and Interfaces&quot;">​</a></h2><div class="info custom-block"><p class="custom-block-title">Documentation pending</p><p>The system architecture diagram and interface descriptions will be added with the approved engineering documentation.</p></div></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("report/system-architecture.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const systemArchitecture = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  systemArchitecture as default
};
