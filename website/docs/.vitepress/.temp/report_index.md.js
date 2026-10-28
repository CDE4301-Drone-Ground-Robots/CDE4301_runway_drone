import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"FOD ARGUS Engineering Report","description":"","frontmatter":{"title":"FOD ARGUS Engineering Report","outline":false},"headers":[],"relativePath":"report/index.md","filePath":"report/index.md"}');
const _sfc_main = { name: "report/index.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><div class="report-cover"><p class="report-cover-kicker">NUS CDE4301 / AIS-407</p><h1>FOD ARGUS<span>Engineering Report</span></h1><p class="report-cover-subtitle">Autonomous Runway Inspection UAV</p><p class="report-cover-note">Innovation &amp; Design Programme<br>College of Design and Engineering<br>National University of Singapore</p></div><h2 id="about-this-report" tabindex="-1">About This Report <a class="header-anchor" href="#about-this-report" aria-label="Permalink to &quot;About This Report&quot;">​</a></h2><p>This report brings together the project scope, system architecture, and the five subsystem reports. Use the contents panel to navigate between chapters and expand a subsystem to explore its nine report sections.</p><div class="info custom-block"><p class="custom-block-title">Report in development</p><p>The chapter structure is ready. Engineering content, test evidence, and results will be integrated when available.</p></div><h2 id="report-contents" tabindex="-1">Report Contents <a class="header-anchor" href="#report-contents" aria-label="Permalink to &quot;Report Contents&quot;">​</a></h2><ol><li><a href="./../scopes">Project scope</a></li><li><a href="./system-architecture">System architecture</a></li><li><a href="./../subsystems/mechanical-design">Mechanical Design</a> - Muruganantham Arun</li><li><a href="./../subsystems/electrical-design">Electrical Design</a> - Kummarikunta Talitha</li><li><a href="./../subsystems/navigation-obstacle-avoidance">Navigation &amp; Obstacle Avoidance</a> - Kummarikunta Talitha</li><li><a href="./../subsystems/computer-vision">Computer Vision Based Inspection and Safety System</a> - Charansagar Ramanujam</li><li><a href="./../subsystems/communication-system">Communication System</a> - Charansagar Ramanujam</li><li><a href="./../timeline">Timeline</a></li><li><a href="./future-works">Future works</a></li><li><a href="./../references">References</a></li></ol></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("report/index.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const index = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  index as default
};
