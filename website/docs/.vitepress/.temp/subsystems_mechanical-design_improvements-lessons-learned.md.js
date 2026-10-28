import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Improvements & Lessons Learned | Mechanical Design","description":"","frontmatter":{"title":"Improvements & Lessons Learned | Mechanical Design"},"headers":[],"relativePath":"subsystems/mechanical-design/improvements-lessons-learned.md","filePath":"subsystems/mechanical-design/improvements-lessons-learned.md"}');
const _sfc_main = { name: "subsystems/mechanical-design/improvements-lessons-learned.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><p class="chapter-kicker">Mechanical Design</p><h1 id="improvements-lessons-learned" tabindex="-1">Improvements &amp; Lessons Learned <a class="header-anchor" href="#improvements-lessons-learned" aria-label="Permalink to &quot;Improvements &amp; Lessons Learned&quot;">​</a></h1><p><strong>Subsystem lead:</strong> Muruganantham Arun<br><strong>Matriculation number:</strong> A0308280J</p><div class="info custom-block"><p class="custom-block-title">Documentation pending</p><p>This section is ready for the subsystem report content.</p></div><h2 id="challenges-encountered" tabindex="-1">Challenges Encountered <a class="header-anchor" href="#challenges-encountered" aria-label="Permalink to &quot;Challenges Encountered&quot;">​</a></h2><p><em>To be added.</em></p><h2 id="proposed-improvements" tabindex="-1">Proposed Improvements <a class="header-anchor" href="#proposed-improvements" aria-label="Permalink to &quot;Proposed Improvements&quot;">​</a></h2><p><em>To be added.</em></p><h2 id="lessons-learned" tabindex="-1">Lessons Learned <a class="header-anchor" href="#lessons-learned" aria-label="Permalink to &quot;Lessons Learned&quot;">​</a></h2><p><em>To be added.</em></p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("subsystems/mechanical-design/improvements-lessons-learned.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const improvementsLessonsLearned = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  improvementsLessonsLearned as default
};
