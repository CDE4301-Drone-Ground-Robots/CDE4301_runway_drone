# FOD ARGUS - Team Editing Guide

Autonomous Runway Inspection UAV | NUS CDE4301 | AIS-407

## Repository layout

```text
CDE4301_runway_drone/
|-- index.html                  Website launcher
|-- README.md                   This team guide
|-- website modifying instructions.md   Website maintenance guide
|-- .github/workflows/          GitHub Actions deployment
|-- interim/                    Working documents and research
|   |-- mechanical-design/
|   |-- electrical-design/
|   |-- navigation-obstacle-avoidance/
|   |-- computer-vision/
|   |-- communication-system/
|   |-- research/
|   |-- notes/
|-- website/                    Complete VitePress website project
    |-- package.json
    |-- package-lock.json
    |-- docs/
        |-- index.md            Cinematic homepage
        |-- subsystems/         Individual report chapters
        |-- public/             Images, drone model, and static assets
        |-- .vitepress/          Theme, configuration, and components
```

Use **interim/** for working documents, research, meeting notes, and draft material. These folders are tracked in Git but are not automatically published as website chapters.

Use **website/docs/** to edit the visible website. All website source code, assets, dependencies, and build configuration are inside **website/**. GitHub requires the deployment workflow to stay under the root **.github/workflows/** folder.

## Does the website run from GitHub?

Yes, once the repository is pushed and GitHub Pages is enabled. GitHub Actions builds the VitePress project in **website/** and publishes its generated pages. Your laptop does not need to remain switched on.

- Expected live website: https://cde4301-drone-ground-robots.github.io/CDE4301_runway_drone/
- Local preview: http://127.0.0.1:4173/CDE4301_runway_drone/
- Confirm publication under GitHub **Actions** and **Settings > Pages**. Local files alone are not published.

The root **index.html** is a launcher with links to the published website and local preview. The full production homepage is generated from **website/docs/index.md** during the VitePress build. Do not replace the root launcher with individual report chapters.

## Individual editing folders

| Member | Working documents | Website report |
| --- | --- | --- |
| Muruganantham Arun | [interim/mechanical-design/](interim/mechanical-design/) | [website/docs/subsystems/mechanical-design.md](website/docs/subsystems/mechanical-design.md) |
| Kummarikunta Talitha | [interim/electrical-design/](interim/electrical-design/) | [website/docs/subsystems/electrical-design.md](website/docs/subsystems/electrical-design.md) |
| Kummarikunta Talitha | [interim/navigation-obstacle-avoidance/](interim/navigation-obstacle-avoidance/) | [website/docs/subsystems/navigation-obstacle-avoidance.md](website/docs/subsystems/navigation-obstacle-avoidance.md) |
| Charansagar Ramanujam | [interim/computer-vision/](interim/computer-vision/) | [website/docs/subsystems/computer-vision.md](website/docs/subsystems/computer-vision.md) |
| Charansagar Ramanujam | [interim/communication-system/](interim/communication-system/) | [website/docs/subsystems/communication-system.md](website/docs/subsystems/communication-system.md) |

Shared draft folders: [Research](interim/research/) and [Notes](interim/notes/). The corresponding visible website pages are under **website/docs/research/** and **website/docs/notes.md**.

## Subsystem report editing

Each subsystem now uses one scrolling Markdown report:

- `website/docs/subsystems/mechanical-design.md`
- `website/docs/subsystems/electrical-design.md`
- `website/docs/subsystems/navigation-obstacle-avoidance.md`
- `website/docs/subsystems/computer-vision.md`
- `website/docs/subsystems/communication-system.md`

The Computer Vision report contains all nine pipeline-specific sections in the same file. Its sidebar entries jump to section anchors on that page. Edit this file to change the CV report; keep its explicit heading anchors so links continue to work.

The other four reports currently contain only their title, lead name, and matriculation number. Add each member's report beneath those details, using headings appropriate to the subsystem. The previous chapter lists and empty templates have been removed from the visible website.

Old files in the matching subfolders are compatibility redirects, not content to edit. Previous/next page buttons have been disabled.

## Edit individually using GitHub

1. Open the repository on GitHub and select **main**.
2. Open your subsystem Markdown report from the table above, then click the **pencil / Edit this file** button.
3. Replace **To be added** placeholders with your report content. Keep the initial metadata block between the first pair of **---** lines, the title, lead name, and matriculation number.
4. Remove the **Documentation pending** block when the chapter is ready. It begins with **::: info Documentation pending** and ends with **:::**.
5. Use **Preview** to check basic Markdown. VitePress applies the final website styling.
6. Select **Commit changes** and create a new branch with a clear name, such as **arun/mechanical-report**. Start a pull request targeting **main**.
7. Ask a teammate to review. Wait for the build check to pass, then merge the pull request.
8. Check **Actions > Build and deploy report**. After deployment succeeds, refresh the published site.

Continue related edits on the same branch before merging. Members can work simultaneously on separate branches and their own chapter folders. Coordinate changes to shared references, navigation, and theme files. If editing is unavailable, ask an administrator for **Write** access under **Settings > Collaborators & teams**.

Edits to draft files in **interim/** do not change the published report. Transfer approved content into the appropriate Markdown chapters under **website/docs/**.

## Add images, equations, and references

Upload subsystem images to **website/docs/public/report-assets/<subsystem>/** on the same working branch as your chapter. For example:

```text
website/docs/public/report-assets/mechanical-design/arm-design.png
```

In the Markdown chapter:

```md
## Selected Design

Explain the chosen design here.

![Selected arm design](/report-assets/mechanical-design/arm-design.png)

*Figure 1. Selected arm design. Add the relevant explanation or source.*

| Requirement | Target | Verification |
| --- | --- | --- |
| Add requirement | Add measurable target | Add test method |
```

Use **##** for main sections and **###** for subsections. LaTeX is supported with dollar signs for inline equations and double dollar signs for displayed equations. Add source links near claims and maintain the shared bibliography in **website/docs/references.md**.

Match image filenames and capitalisation exactly. Use short, lowercase names with hyphens. Do not put **website/docs/public/** into the image URL; VitePress handles the site base path.

## Preview locally

Install Node.js 22 or later and Git. From the repository root:

```sh
cd website
npm ci
npm run docs:dev
```

Open http://127.0.0.1:4173/CDE4301_runway_drone/ and keep the terminal running. Changes refresh automatically. Press **Ctrl+C** to stop.

To check a production build, run this inside **website/**:

```sh
npm run docs:build
```

## Local Git contribution workflow

From the repository root, with no uncommitted changes:

```sh
git switch main
git pull --ff-only origin main
git switch -c arun/mechanical-report
```

Edit your files, then build and commit. Example for Arun:

```sh
npm --prefix website run docs:build
git add website/docs/subsystems/mechanical-design.md interim/mechanical-design/
git commit -m "Add mechanical subsystem report content"
git push -u origin arun/mechanical-report
```

Replace branch names and paths with your own. Stage any new image files as well. Open a pull request into **main**. Resolve conflicts with the team; do not force-push **main**.

## First upload and GitHub Pages setup

From the repository root:

```sh
git add README.md "website modifying instructions.md" index.html .gitignore .github interim website
git commit -m "Organise interim documents and FOD ARGUS website"
git pull --rebase origin main
git push origin main
```

If a command reports a conflict, resolve it before continuing.

On GitHub, set **Settings > Pages > Build and deployment > Source** to **GitHub Actions**. Check the **Build and deploy report** workflow; run it manually on **main** if necessary after enabling Pages. The workflow builds from **website/** and publishes **website/docs/.vitepress/dist/**. Pull requests get a build check but no separate hosted preview.

Official guidance: [repository access](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-teams-and-people-with-access-to-your-repository) and [GitHub Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Shared website files

All paths below are relative to **website/**:

| Area | File |
| --- | --- |
| Homepage | **docs/index.md** and **docs/.vitepress/theme/components/RunwayHome.vue** |
| Team profiles | **docs/team.data.ts** |
| Scope | **docs/scopes.md** |
| Report cover | **docs/report/index.md** |
| Report architecture | **docs/report/system-architecture.md** |
| Timeline | **docs/timeline.md** |
| Future works | **docs/report/future-works.md** |
| References | **docs/references.md** |
| Navigation and report sidebar | **docs/.vitepress/config.mts** |
| Chapter order | **docs/.vitepress/cv-subsystem-sections.ts** |

See [website modifying instructions.md](<website modifying instructions.md>) for implementation details. Generated builds, dependencies, and local caches remain excluded by **.gitignore**.
