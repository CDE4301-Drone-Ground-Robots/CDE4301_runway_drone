# FOD ARGUS 3D model

FOD_Argus.glb is the user-provided SolidWorks assembly, preserved unchanged. The filename is case-sensitive on GitHub Pages.

The overview embeds it using docs/.vitepress/theme/components/DroneModel.vue. Drag to orbit, scroll/pinch to zoom, pause/resume automatic rotation, or reset the view. Automatic rotation is initially disabled for reduced-motion preferences. Mobile vertical swiping still scrolls the page.

The GLB embeds its textures and uses KHR_draco_mesh_compression. Its Draco decoder is served locally from /decoders/draco/; the original model and decoder do not depend on an external 3D hosting service. model-viewer is dynamically loaded in the browser, preserving VitePress server rendering.

To replace the assembly, keep the same filename or update the src in DroneModel.vue. Rebuild and restart the production preview after changes. Lighting and the initial camera angle are configured in that component.