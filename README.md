<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/header-light.svg">
  <img alt="matthew eucaristo — ai agents, rl for games, playable things" src="assets/header-dark.svg" width="100%">
</picture>

i build **agents** that act, **rl** that plays games, and **games** people actually play.
day job: cto at [geniusgrowthai](https://geniusgrowth.ai), running the infra and ai agents behind an education platform.
rule of thumb: keep it simple, measure it, ship it.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/spotlight-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/spotlight-light.svg">
  <img alt="project spotlight, one at a time: fotoin, a camera app that coaches you to match a reference pose; s1, a voice-first macos agent; mouse maze mayhem, an rl mouse escaping cats in the browser; mob-run, a 3d crowd-runner; decruft, one storage screen for developer machines that brings all my cleaners with it; lately, a timeline of what just happened on a mac; spoor.nvim, call bow-ties and traces in neovim" src="assets/spotlight-dark.svg" width="100%">
</picture>

[**fotoin**](https://matthew-eucaristo.github.io/fotoin/) · [**s1**](https://github.com/Matthew-Eucaristo/s1) · [**mouse maze mayhem**](https://mouse-maze-mayhem-skripsi.web.app) · [**mob-run**](https://mob-run.pages.dev) · [**flip10**](https://flip10.pages.dev) · [**solitaire-rl**](https://github.com/Matthew-Eucaristo/solitaire-rl) · [**crypto-cycle-signals**](https://github.com/Matthew-Eucaristo/crypto-cycle-signals)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/shipped-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/shipped-light.svg">
  <img alt="latest releases of my public repos, newest first, refreshed weekly from the github api" src="assets/shipped-dark.svg" width="100%">
</picture>

### `$ graph --public`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/graph-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/graph-light.svg">
  <img alt="graph of public projects: fell, flutterkill, nodekill and rustkill ship through homebrew-tap and feed decruft, one tui over all of them; lately sits beside them as a go tool for macos; s1 has its landing page and cask; spoor.nvim and jupynvim are neovim plugins; the games form their own cluster; fotoin and plain gallery are on-device phone apps" src="assets/graph-dark.svg" width="100%">
</picture>

<sub>drawn by <a href="graph/build.py"><code>graph/build.py</code></a> on every change and once a week. it only draws repos the github api reports as public. <a href="https://matthew-eucaristo.github.io/Matthew-Eucaristo/">interactive version →</a></sub>

### `$ ls ~/dev-tools`

<img alt="a short tour on demo data: fell lists git worktrees left by ai coding agents, flutterkill lists flutter build artifacts and caches, nodekill lists node_modules, caches and old node versions, rustkill lists rust target folders, cargo caches and rustup toolchains, each with a safety label and in dry-run mode; decruft shows the whole disk by developer category with the official command for each xcode item; then lately replays sample events as a classified timeline and opens one event card" src="assets/tour.gif" width="100%">

terminal tools for a developer's mac, recorded on demo data ([tape](demo/tour.tape)). **decruft** is the one to install: one scan of the whole machine, and it brings the family cleaners (fell, nodekill, rustkill, flutterkill) along, handing each removal to the tool that owns it. evidence first, trash by default.

```sh
brew install matthew-eucaristo/tap/{decruft,lately}   # decruft pulls in fell, nodekill, rustkill and flutterkill
```

<details>
<summary>what each tool does: decruft and its family, then the rest</summary>
<br>

| tool | what it does | install |
| :-- | :-- | :-- |
| [**decruft**](https://github.com/Matthew-Eucaristo/decruft) | **all in one.** a better "storage" screen for programmers: one scan of xcode, go, homebrew, docker, android and js caches plus everything its family cleaners below find, reclaimed through each tool's own command. [demo →](https://github.com/Matthew-Eucaristo/decruft#readme) | homebrew |
| ↳ [**fell**](https://github.com/Matthew-Eucaristo/fell) | finds git worktrees left behind by ai coding agents, shows the evidence, and cleans up without breaking the agent's own lifecycle. | with decruft |
| ↳ [**nodekill**](https://github.com/Matthew-Eucaristo/nodekill) | the node.js footprint: `node_modules`, `.next` and framework caches, npm/pnpm/yarn/bun caches, npx, globals, old node versions. | with decruft |
| ↳ [**rustkill**](https://github.com/Matthew-Eucaristo/rustkill) | the rust footprint: `target` folders found by cargo's own tag, cargo registry and git caches, sccache, `cargo install` tools, rustup toolchains and `rust-docs`. [demo →](https://matthew-eucaristo.github.io/rustkill/) | with decruft |
| ↳ [**flutterkill**](https://github.com/Matthew-Eucaristo/flutterkill) | npkill for flutter: `build/`, `.dart_tool`, pods and gradle leftovers plus pub, gradle, fvm and xcode caches. | with decruft |
| [**lately**](https://github.com/Matthew-Eucaristo/lately) | what just happened on my mac? a classified timeline from the unified log, crash reports and persistence items, with a card per event. no root, no daemon. [demo →](https://github.com/Matthew-Eucaristo/lately#readme) | homebrew |
| [**spoor.nvim**](https://github.com/Matthew-Eucaristo/spoor.nvim) | follow the trail through a codebase in neovim: a call bow-tie on `K`, trace mode with notes, and what your agent changed. lsp first, tree-sitter where there is none. no ai, no index. [demo →](https://github.com/Matthew-Eucaristo/spoor.nvim#readme) | lazy.nvim |
| [**jupynvim**](https://github.com/sheng-tse/jupynvim) | jupyter notebooks in neovim. i send fixes upstream: [html tables for pandas styler](https://github.com/sheng-tse/jupynvim/pull/45), [docs](https://github.com/sheng-tse/jupynvim/pull/46). | upstream prs |

</details>

<details>
<summary><code>$ ls -l ~/projects</code> — every project, with its stack</summary>
<br>

| project | what it is | built with |
| :-- | :-- | :-- |
| [**fotoin**](https://github.com/Matthew-Eucaristo/fotoin) | photograph someone exactly like a reference pose (pinterest, ig, or an example shot): a ghost overlay and pose skeleton over the live camera, a match meter, one hint at a time, auto-capture. bodies, faces and groups; on-device, free, no ads. [site →](https://matthew-eucaristo.github.io/fotoin/) | expo · react native · visioncamera · mediapipe · apple vision |
| [**plain gallery**](https://github.com/Matthew-Eucaristo/plain-gallery) | a photo gallery for android that just works: no ads, no backup nagging, no internet permission. faces and text in photos are recognised on the phone, so search finds people and receipts. [apk →](https://github.com/Matthew-Eucaristo/plain-gallery/releases) | kotlin · jetpack compose · litert |
| [**s1**](https://github.com/Matthew-Eucaristo/s1) | voice-first macos agent. a fast local *system 1* acts; an llm *system 2* is asked only when unsure. every step gated and logged. [site →](https://s1-mac.pages.dev) `brew install --cask matthew-eucaristo/tap/s1` | swift 6 · ax api · screencapturekit |
| [**mouse maze mayhem**](https://mouse-maze-mayhem-skripsi.web.app) | my thesis, playable. four cats vs. one rl mouse in 3d mazes — a solver-distilled policy running in your browser via onnx. | pytorch · onnx · react three fiber |
| [**solitaire-rl**](https://github.com/Matthew-Eucaristo/solitaire-rl) | masked dqn and maskableppo learning klondike, judged on a fixed 1000-deal benchmark. honest result: the heuristic still wins. | python · sb3 · gymnasium |
| [**rl-2048**](https://github.com/Matthew-Eucaristo/rl-2048) | a 2048 agent that learns by self-play on one laptop in 20 minutes: an n-tuple network, no gpu, no human games. with a 3-move lookahead it reaches 16384 in 68% of games. | go · td learning |
| [**mob-run**](https://github.com/Matthew-Eucaristo/mob-run) | the game from those fake mobile ads, for real: a 3d crowd-runner where you pick multiplier gates and outgun mobs, walls and bosses across 5 zones. [play →](https://mob-run.pages.dev) | three.js |
| [**crypto-cycle-signals**](https://github.com/Matthew-Eucaristo/crypto-cycle-signals) | futures indicator anchored to btc's 4-year cycle; every parameter earned by backtest on 68 perps × 6 years. | pine script v6 |
| [**blockies**](https://github.com/Matthew-Eucaristo/blockies) | organic living blocks: a whiteboard where every drawing is alive, with few enough pieces that humans and ai agents both draw valid boards. v0.1 engine; the web runtime is next. | rust · wasm |
| [**flip10**](https://github.com/Matthew-Eucaristo/Flip10) | shut the box, polished: hand-drawn svg tiles, procedural audio, fully offline. [play →](https://flip10.pages.dev) | next.js · typescript |

</details>

<details>
<summary><code>$ ls ~/archive</code> — game jam + university game lab</summary>
<br>

| build | stack |
| :-- | :-- |
| [poppp: rocket balloon](https://github.com/Matthew-Eucaristo/GMTKGameJam2024) · [play](https://mammamiaaaaa.itch.io/pop-rocket-balloon) | unreal engine · gmtk game jam 2024 |
| [focus tower defense](https://github.com/Matthew-Eucaristo/FOCUS-Game) · [play](https://syntax-gamedev.itch.io/focus-td) | unreal engine 5 |
| [sliding puzzle](https://github.com/Matthew-Eucaristo/Sliding-Puzzle-UnrealEngine) | unreal engine 5 |
| [shoot the ghost ar](https://github.com/Matthew-Eucaristo/Shoot-The-Ghost-AR-KelasARVR) · [play](https://syntax-gamedev.itch.io/shoot-the-ghost-ar) | unreal engine · ar |
| [computer graphics final](https://github.com/Matthew-Eucaristo/GrafKom-Final-Project) · [vr sim](https://syntax-gamedev.itch.io/compgraphsimvr) | java · lwjgl / opengl |
| [solar system](https://github.com/Matthew-Eucaristo/SolarSystemProject-Grafkom) | java · lwjgl |
| [guess the path](https://github.com/Matthew-Eucaristo/Guess-the-Path) | java · graphs |

</details>

### `$ ping matthew`

[linkedin](https://www.linkedin.com/in/matthew-eucaristo-265127184/) · [x](https://x.com/0xZexy) · [itch.io](https://syntax-gamedev.itch.io/)

<sub>pytorch · stable-baselines3 · onnx · swift · typescript · react · three.js · go · bubble tea · lua · unreal engine · docker · cloudflare</sub>
