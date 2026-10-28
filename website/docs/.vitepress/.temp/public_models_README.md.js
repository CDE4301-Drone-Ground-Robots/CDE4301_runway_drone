import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"FOD ARGUS 3D model","description":"","frontmatter":{},"headers":[],"relativePath":"public/models/README.md","filePath":"public/models/README.md"}');
const _sfc_main = { name: "public/models/README.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="fod-argus-3d-model" tabindex="-1">FOD ARGUS 3D model <a class="header-anchor" href="#fod-argus-3d-model" aria-label="Permalink to &quot;FOD ARGUS 3D model&quot;">​</a></h1><p>FOD_Argus.glb is the user-provided SolidWorks assembly, preserved unchanged. The filename is case-sensitive on GitHub Pages.</p><p>The overview embeds it using docs/.vitepress/theme/components/DroneModel.vue. Drag to orbit, scroll/pinch to zoom, pause/resume automatic rotation, or reset the view. Automatic rotation is initially disabled for reduced-motion preferences. Mobile vertical swiping still scrolls the page.</p><p>The GLB embeds its textures and uses KHR_draco_mesh_compression. Its Draco decoder is served locally from /decoders/draco/; the original model and decoder do not depend on an external 3D hosting service. model-viewer is dynamically loaded in the browser, preserving VitePress server rendering.</p><p>To replace the assembly, keep the same filename or update the src in DroneModel.vue. Rebuild and restart the production preview after changes. Lighting and the initial camera angle are configured in that component.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("public/models/README.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const README = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  README as default
};
