import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"NUS logo","description":"","frontmatter":{},"headers":[],"relativePath":"public/ASSETS.md","filePath":"public/ASSETS.md"}');
const _sfc_main = { name: "public/ASSETS.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="nus-logo" tabindex="-1">NUS logo <a class="header-anchor" href="#nus-logo" aria-label="Permalink to &quot;NUS logo&quot;">​</a></h1><p>The NUS header logo is stored locally at docs/public/nus-logo.png. Source: <a href="https://github.com/theflyingwolves/NUS-Slides-Latex-Template/blob/master/nus-logo.png" target="_blank" rel="noreferrer">https://github.com/theflyingwolves/NUS-Slides-Latex-Template/blob/master/nus-logo.png</a></p><p>The university mark remains the property of the National University of Singapore. It is displayed alongside AIS-407 as requested. FOD ARGUS remains the drone name in the overview and page metadata. The runway-night.svg hero background is an original vector illustration of a runway at night, created for this website.</p><h2 id="photorealistic-hero-backdrop" tabindex="-1">Photorealistic hero backdrop <a class="header-anchor" href="#photorealistic-hero-backdrop" aria-label="Permalink to &quot;Photorealistic hero backdrop&quot;">​</a></h2><p>runway-night-photo.png is an AI-generated photorealistic night runway created for this website. It is decorative artwork, not a photograph documenting a particular airport or a project test site. It contains no aircraft, so the actual UAV render can be overlaid separately. The earlier runway-night.svg is retained as an unused original illustration. Stock-photo candidates were not integrated into the website.</p><p>FOD_Argus.glb is the user&#39;s SolidWorks export. Draco decoder binaries are distributed with Three.js and originate from Google Draco (Apache 2.0); see <a href="https://github.com/google/draco" target="_blank" rel="noreferrer">https://github.com/google/draco</a>. The GLB is not modified by this website.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("public/ASSETS.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const ASSETS = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  ASSETS as default
};
