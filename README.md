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

| Member | Working documents | Website chapters |
| --- | --- | --- |
| Muruganantham Arun | [interim/mechanical-design/](interim/mechanical-design/) | [website/docs/subsystems/mechanical-design/](website/docs/subsystems/mechanical-design/) |
| Kummarikunta Talitha | [interim/electrical-design/](interim/electrical-design/) | [website/docs/subsystems/electrical-design/](website/docs/subsystems/electrical-design/) |
| Kummarikunta Talitha | [interim/navigation-obstacle-avoidance/](interim/navigation-obstacle-avoidance/) | [website/docs/subsystems/navigation-obstacle-avoidance/](website/docs/subsystems/navigation-obstacle-avoidance/) |
| Charansagar Ramanujam | [interim/computer-vision/](interim/computer-vision/) | [website/docs/subsystems/computer-vision/](website/docs/subsystems/computer-vision/) |
| Charansagar Ramanujam | [interim/communication-system/](interim/communication-system/) | [website/docs/subsystems/communication-system/](website/docs/subsystems/communication-system/) |

Shared draft folders: [Research](interim/research/) and [Notes](interim/notes/). The corresponding visible website pages are under **website/docs/research/** and **website/docs/notes.md**.

## Nine report chapters per subsystem

1. **executive-summary.md** - Short purpose, main engineering problem, selected approach.
2. **subsystem-overview.md** - Operation and interfaces.
3. **requirements-considerations.md** - Requirements, acceptance criteria, constraints.
4. **design-iterations-selection.md** - Alternatives, comparison, selection.
5. **detailed-design-implementation.md** - Development and implementation.
6. **testing-methodology-results.md** - What was tested, why, methods, results.
7. **evaluation-discussion.md** - Results against requirements, limitations, uncertainties, trade-offs.
8. **improvements-lessons-learned.md** - Challenges, improvements, lessons.
9. **semester-2-development-plan.md** - Next objectives, tasks, milestones, validation.

The matching file directly inside **website/docs/subsystems/**, such as **mechanical-design.md**, is the subsystem report landing page. Keep chapter filenames so navigation continues to work.

## Edit individually using GitHub

1. Open the repository on GitHub and select **main**.
2. Open your website chapter folder from the table above. Select a Markdown chapter, then click the **pencil / Edit this file** button.
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
git add website/docs/subsystems/mechanical-design.md website/docs/subsystems/mechanical-design/ interim/mechanical-design/
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
| Chapter order | **docs/.vitepress/subsystem-sections.ts** |

See [website modifying instructions.md](<website modifying instructions.md>) for implementation details. Generated builds, dependencies, and local caches remain excluded by **.gitignore**.
