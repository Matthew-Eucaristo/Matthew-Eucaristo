# GitHub profile README

`README.md` renders on github.com/Matthew-Eucaristo. Terminal style: `$ command` headings, plain tables, no emoji walls, badge grids, stat cards, typing SVGs or invented numbers. Every claim and description comes from the real repo.

- `assets/header-{dark,light}.svg`: hand-written header, switched with `<picture>`.
- `graph/graph.json` + `graph/build.py` (stdlib Python) → `assets/graph-{dark,light}.svg` and `docs/graph.json`. The script drops every node the GitHub API does not report as public and adds tap edges from `homebrew-tap`. Never put a private or unreleased repo's name in `graph.json`. `.github/workflows/graph.yml` reruns it on push to `graph/**` and weekly, and commits only when output changes.
- `docs/index.html`: interactive graph, served by GitHub Pages from `main /docs` at matthew-eucaristo.github.io/Matthew-Eucaristo (vanilla JS, reads `docs/graph.json`).
- `demo/tour.tape` + `demo/tour.sh` → `assets/tour.gif`. Render locally with `vhs demo/tour.tape` from the repo root, with the tool repos in `../dev-tools/`. Each tool builds from its committed HEAD and runs in a child shell set up by its own `demo/setup.sh` (synthetic HOME, dummy data); never record the real machine. Keep the GIF well under 1 MB.
- No PII beyond what the profile already shows. Commit with the GitHub noreply identity. Ask before pushing or enabling Pages.
