# FOD ARGUS - Website Modifying Instructions

This guide is stored at the repository root. **All file paths in this guide are relative to the repository root**, unless stated otherwise.

The complete VitePress + Vue website project lives inside `website/`. The root `index.html` is a launcher, not the full VitePress homepage. Working documents are kept separately inside `interim/`.

## 1. Start and stop the website

Requires Node.js 22 or newer.

From the repository root, install the locked dependencies when setting up a fresh checkout:

```powershell
npm --prefix website ci
```

Start the development server:

```powershell
npm --prefix website run docs:dev
```

Open **http://127.0.0.1:4173/CDE4301_runway_drone/** on the same computer. Keep the terminal running; changes refresh automatically. Press **Ctrl+C** in the server terminal to stop it.

Alternatively, run `cd website` and use `npm run docs:dev` from there. Do not run `npm run docs:dev` at the repository root without `--prefix website`, because the package file is inside `website/`.

The front page contains the breathing rose-gold FOD ARGUS wordmark, runway background, and interactive SolidWorks drone. **Report** in the top navigation opens the separate report cover and chapter layout.

## 2. Where to make changes

| What you want to change | File or folder |
| --- | --- |
| Homepage metadata | `website/docs/index.md` |
| Homepage text, sections, and layout | `website/docs/.vitepress/theme/components/RunwayHome.vue` |
| Top navigation, report sidebar, site title, and base URL | `website/docs/.vitepress/config.mts` |
| General styling, typography, search appearance, and report sidebar dimensions | `website/docs/.vitepress/theme/style.css` |
| Theme component registration and layout slots | `website/docs/.vitepress/theme/index.ts` |
| NUS identity and AIS-407 badge | `website/docs/.vitepress/theme/components/HeaderIdentity.vue` |
| Light/dark switch | `website/docs/.vitepress/theme/components/ThemeToggle.vue` |
| Rose-gold cursor spotlight | `website/docs/.vitepress/theme/components/CursorSpotlight.vue` |
| Team names, roles, contributions, and subsystem assignments | `website/docs/team.data.ts` |
| Team carousel layout and controls | `website/docs/.vitepress/theme/components/TeamCarousel.vue` |
| Team card styling | `website/docs/.vitepress/theme/team.css` |
| Team portraits | `website/docs/public/team/` |
| Research pages | `website/docs/research/primary.md` and `website/docs/research/secondary.md` |
| Notes page | `website/docs/notes.md` |
| Drone specification | `website/docs/engineering/drone-specification.md` |
| Runway subsystem overview page | `website/docs/engineering/subsystem.md` |
| Subsystem overview cards and background | `website/docs/.vitepress/theme/components/SubsystemOverview.vue` |
| Custom Subsystems top tab and dropdown | `website/docs/.vitepress/theme/components/SubsystemNav.vue` |
| Shared subsystem names, leads, colours, and slugs | `website/docs/.vitepress/theme/components/subsystems.ts` |
| Report cover | `website/docs/report/index.md` |
| System architecture chapter | `website/docs/report/system-architecture.md` |
| Project scope | `website/docs/scopes.md` |
| Timeline | `website/docs/timeline.md` |
| Future works | `website/docs/report/future-works.md` |
| References | `website/docs/references.md` |
| Chapter names and ordering | `website/docs/.vitepress/cv-subsystem-sections.ts` |

Dark mode is the default. The theme switch supports light mode. Check both themes after changing colours. Preserve touch controls and reduced-motion support when editing animations.

## 3. Edit individual subsystem reports

Each subsystem report is a single scrolling Markdown page. Paths are relative to the repository root:

| Member | Report file |
| --- | --- |
| Muruganantham Arun | `website/docs/subsystems/mechanical-design.md` |
| Kummarikunta Talitha | `website/docs/subsystems/electrical-design.md` |
| Kummarikunta Talitha | `website/docs/subsystems/navigation-obstacle-avoidance.md` |
| Charansagar Ramanujam | `website/docs/subsystems/computer-vision.md` |
| Charansagar Ramanujam | `website/docs/subsystems/communication-system.md` |

The CV report contains nine pipeline-specific sections on one page. Its sidebar links scroll to the explicit heading IDs such as `{#patchcore-anomaly-detection}`. Keep those IDs when editing headings. Section names and anchor slugs are configured in `website/docs/.vitepress/cv-subsystem-sections.ts`; sidebar links are generated in `website/docs/.vitepress/config.mts`.

The other four reports are intentionally empty beneath the subsystem title and lead details. Add original report content directly to the corresponding file. No generic chapter template is imposed. Introduce appropriate headings and add sidebar anchors when the content is ready.

Files in the old chapter subfolders are compatibility redirects. Do not edit those redirect files as if they were report chapters. The website no longer requires previous/next page buttons to read a subsystem report.

Preserve the frontmatter, lead name, matriculation number, and existing CV wording unless the author requests a change. Add calculations, diagrams, citations, and measured results where appropriate.

## 4. Add images and other assets

Put subsystem report images inside:

```text
website/docs/public/report-assets/<subsystem>/
```

For example, save `arm-design.png` inside `website/docs/public/report-assets/mechanical-design/`, then reference it in Markdown as:

```md
![Selected arm design](/report-assets/mechanical-design/arm-design.png)

*Figure 1. Selected arm design. Add an explanation and source where relevant.*
```

Do not include `website/docs/public/` in a website image URL. VitePress handles the repository base path. Match filename capitalisation exactly; GitHub Pages is case-sensitive. Use lowercase filenames with hyphens for new assets.

LaTeX equations are enabled. Use `$...$` for inline equations and `$$...$$` for displayed equations. Add citations beside claims and update `website/docs/references.md`.

## 5. Change the runway background or drone

### Runway image

The existing runway asset is:

```text
website/docs/public/runway-night-photo.png
```

The homepage and subsystem overview reuse this image. Their overlays are controlled separately in `style.css` and `SubsystemOverview.vue`. The team page backdrop is controlled in `team.css`.

The runway is a decorative generated image, not a photograph of the actual test site. Asset provenance is documented in `website/docs/public/ASSETS.md`.

### SolidWorks model

The current model is:

```text
website/docs/public/models/FOD_Argus.glb
```

Its exact filename matters on GitHub Pages. Rendering, camera framing, exposure, interaction hints, and rotation controls are in:

```text
website/docs/.vitepress/theme/components/DroneModel.vue
```

The model preserves the original material colours. Adjust viewer exposure if the rendering is too bright rather than recolouring the source model. The local Draco decoders are inside `website/docs/public/decoders/draco/`.

Keep the viewer browser-only initialization and local decoder setup. Check that the model loads, rotates, zooms, pauses, and resets after changing the GLB or viewer settings. See `website/docs/public/models/README.md` for model-specific details.

## 6. Working documents versus published chapters

`interim/` contains the five subsystem working folders plus `research/` and `notes/`. These files can be shared through GitHub, but they do not automatically appear on the website.

Transfer approved report material into `website/docs/` to publish it. Store website images in `website/docs/public/`. Keep drafts in the appropriate `interim/` folder when they are not ready for the report.

## 7. Check changes before sharing

From the repository root:

```powershell
npm --prefix website run docs:build
```

Check the relevant page in the browser, including mobile width and both themes when changing layout or colour. Confirm links, image paths, sidebar navigation, and report content still work.

For a production-style local preview:

```powershell
npm --prefix website run docs:preview
```

Use the address printed by that command; it may use a different port from the development server. Restart the production preview after rebuilding, because its asset list may otherwise refer to old generated filenames. Use the development server for routine editing.

Do not commit `node_modules/`, `.vitepress/dist/`, `.vitepress/cache/`, or local test caches. These paths are excluded by the root `.gitignore`.

## 8. GitHub contributions and deployment

Use individual branches and pull requests. Coordinate edits to shared files. See [README.md](README.md) for the step-by-step browser editing and local Git workflows.

The deployment workflow must remain at:

```text
.github/workflows/deploy.yml
```

GitHub discovers workflows at the repository root, so this is the intentional exception to storing website code under `website/`.

The workflow:

1. Installs dependencies and builds inside `website/`.
2. Checks pull requests for build errors.
3. Publishes `website/docs/.vitepress/dist/` after a successful update to `main`.

In GitHub **Settings > Pages**, choose **GitHub Actions** as the publishing source. Confirm successful deployment in **Actions** and the address shown in **Settings > Pages**. A pull request build does not create a separate hosted preview.

Expected live address:

https://cde4301-drone-ground-robots.github.io/CDE4301_runway_drone/

The website base path is `/CDE4301_runway_drone/`. If the repository or hosting location changes, update `base` and the favicon URL in `website/docs/.vitepress/config.mts`, and the published link in the root `index.html` launcher and documentation.

Once GitHub Pages has published the site, your laptop does not need to stay switched on. The `127.0.0.1` preview remains local to the computer running the development server.
