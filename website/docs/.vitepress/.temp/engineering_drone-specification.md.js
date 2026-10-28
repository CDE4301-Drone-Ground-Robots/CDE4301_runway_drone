import { useSSRContext, unref } from "vue";
import { ssrRenderAttrs, ssrRenderAttr } from "vue/server-renderer";
import { w as withBase } from "./Content.CZ-n0PZT.js";
import "@vueuse/core";
const __pageData = JSON.parse('{"title":"Drone Specification","description":"","frontmatter":{"layout":"page","title":"Drone Specification","sidebar":false,"outline":false},"headers":[],"relativePath":"engineering/drone-specification.md","filePath":"engineering/drone-specification.md"}');
const __default__ = { name: "engineering/drone-specification.md" };
const _sfc_main = /* @__PURE__ */ Object.assign(__default__, {
  __ssrInlineRender: true,
  setup(__props) {
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<div${ssrRenderAttrs(_attrs)}><section class="holding-page"><p class="eyebrow">FOD ARGUS / ENGINEERING / 01</p><span class="holding-status"><span class="status-dot"></span> COMING SOON</span><h1>Drone Specification<span>.</span></h1><p class="holding-description">The FOD ARGUS drone specification will be added here.</p><a class="holding-back"${ssrRenderAttr("href", unref(withBase)("/"))}>← Back to overview</a><div class="holding-rule"></div><p class="holding-caption">AUTONOMOUS RUNWAY INSPECTION UAV <span>NUS / CDE4301</span></p></section></div>`);
    };
  }
});
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("engineering/drone-specification.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
export {
  __pageData,
  _sfc_main as default
};
