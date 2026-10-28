import { ssrRenderAttrs, ssrRenderStyle } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Optional still renders","description":"","frontmatter":{},"headers":[],"relativePath":"public/renders/README.md","filePath":"public/renders/README.md"}');
const _sfc_main = { name: "public/renders/README.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="optional-still-renders" tabindex="-1">Optional still renders <a class="header-anchor" href="#optional-still-renders" aria-label="Permalink to &quot;Optional still renders&quot;">​</a></h1><p>The overview now displays the actual user-provided SolidWorks assembly at docs/public/models/FOD_Argus.glb through DroneModel.vue. See docs/public/models/README.md for model-viewer instructions.</p><p>This directory is available for optional transparent PNG/WebP renders used in later report chapters, for example:</p><div class="language-md vp-adaptive-theme line-numbers-mode"><button title="Copy Code" class="copy"></button><span class="lang">md</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">![</span><span style="${ssrRenderStyle({ "--shiki-light": "#032F62", "--shiki-light-text-decoration": "underline", "--shiki-dark": "#DBEDFF", "--shiki-dark-text-decoration": "underline" })}">FOD ARGUS SolidWorks assembly</span><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">](</span><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-light-text-decoration": "underline", "--shiki-dark": "#E1E4E8", "--shiki-dark-text-decoration": "underline" })}">/renders/uav-render.webp</span><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">)</span></span></code></pre><div class="line-numbers-wrapper" aria-hidden="true"><span class="line-number">1</span><br></div></div><p>The old conceptual SVG drone has been removed from the overview.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("public/renders/README.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const README = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  README as default
};
