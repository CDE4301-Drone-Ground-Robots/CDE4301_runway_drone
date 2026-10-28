import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Team portraits","description":"","frontmatter":{},"headers":[],"relativePath":"public/team/README.md","filePath":"public/team/README.md"}');
const _sfc_main = { name: "public/team/README.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="team-portraits" tabindex="-1">Team portraits <a class="header-anchor" href="#team-portraits" aria-label="Permalink to &quot;Team portraits&quot;">​</a></h1><p>The current portraits are Charan.png, Arun.png, and Talitha.jpg. Filenames are matched without regard to case, and their exact casing is preserved in site URLs for GitHub Pages. To replace them, use either:</p><ul><li>The latest combined portrait image as portraits.png (also accepts .jpg, .jpeg, or .webp). Keep the full original canvas and photo positions; it is automatically cropped into the three cards.</li><li>Individual photographs named charan.png, arun.png, and talitha.png (also accepts .jpg, .jpeg, or .webp). Individual files take priority over the combined image.</li></ul><p>Rebuild with npm run docs:build and restart the preview after adding files. The development server watches this directory. Portraits are loaded only when present, so pending images cause no broken requests.</p><p>Names, roles and Semester 1 contribution descriptions were transcribed from the user&#39;s team-card reference. The combined portrait crop uses normalized positions from the 2048 x 579 displayed reference and scales with the original 2407 x 681 image.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("public/team/README.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const README = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  README as default
};
