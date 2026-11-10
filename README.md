<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/header-light.svg">
  <img alt="Matthew Eucaristo — AI agents, RL for games, playable things" src="assets/header-dark.svg" width="100%">
</picture>

I build **agents** that act, **RL** that plays games, and **games** people actually play.
Day job: CTO at [GeniusGrowthAI](https://geniusgrowth.ai), running the infra and AI agents behind an education platform.
Rule of thumb: keep it simple, measure it, ship it.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/spotlight-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/spotlight-light.svg">
  <img alt="Project spotlight, one at a time: Fotoin, a camera app that coaches you to match a reference pose; s1, a voice-first macOS agent; Mouse Maze Mayhem, an RL mouse escaping cats in the browser; mob-run, a 3D crowd-runner; decruft, one Storage screen for developer machines that brings all my cleaners with it; lately, a timeline of what just happened on a Mac; spoor.nvim, call bow-ties and traces in Neovim" src="assets/spotlight-dark.svg" width="100%">
</picture>

[**Fotoin**](https://matthew-eucaristo.github.io/fotoin/) · [**s1**](https://github.com/Matthew-Eucaristo/s1) · [**Mouse Maze Mayhem**](https://mouse-maze-mayhem-skripsi.web.app) · [**mob-run**](https://mob-run.pages.dev) · [**Flip10**](https://flip10.pages.dev) · [**solitaire-rl**](https://github.com/Matthew-Eucaristo/solitaire-rl) · [**crypto-cycle-signals**](https://github.com/Matthew-Eucaristo/crypto-cycle-signals)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/shipped-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/shipped-light.svg">
  <img alt="Latest releases of my public repos, newest first, refreshed weekly from the GitHub API" src="assets/shipped-dark.svg" width="100%">
</picture>

### `$ graph --public`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/graph-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/graph-light.svg">
  <img alt="Graph of public projects: fell, flutterkill, nodekill and rustkill ship through homebrew-tap and feed decruft, one TUI over all of them; lately sits beside them as a Go tool for macOS; s1 has its landing page and cask; spoor.nvim and jupynvim are Neovim plugins; the games form their own cluster; Fotoin and Plain Gallery are on-device phone apps" src="assets/graph-dark.svg" width="100%">
</picture>

<sub>Drawn by <a href="graph/build.py"><code>graph/build.py</code></a> on every change and once a week. It only draws repos the GitHub API reports as public. <a href="https://matthew-eucaristo.github.io/Matthew-Eucaristo/">Interactive version →</a></sub>

### `$ ls ~/dev-tools`

<img alt="A short tour on demo data: fell lists git worktrees left by AI coding agents, flutterkill lists Flutter build artifacts and caches, nodekill lists node_modules, caches and old Node versions, rustkill lists Rust target folders, Cargo caches and rustup toolchains, each with a safety label and in dry-run mode; decruft shows the whole disk by developer category with the official command for each Xcode item; then lately replays sample events as a classified timeline and opens one event card" src="assets/tour.gif" width="100%">

Terminal tools for a developer's Mac, recorded on demo data ([tape](demo/tour.tape)). **decruft** is the one to install: one scan of the whole machine, and it brings the family cleaners (fell, nodekill, rustkill, flutterkill) along, handing each removal to the tool that owns it. Evidence first, Trash by default.

```sh
brew install matthew-eucaristo/tap/{decruft,lately}   # decruft pulls in fell, nodekill, rustkill and flutterkill
```

<details>
<summary>what each tool does: decruft and its family, then the rest</summary>
<br>

| tool | what it does | install |
| :-- | :-- | :-- |
| [**decruft**](https://github.com/Matthew-Eucaristo/decruft) | **All in one.** A better "Storage" screen for programmers: one scan of Xcode, Go, Homebrew, Docker, Android and JS caches plus everything its family cleaners below find, reclaimed through each tool's own command. [Demo →](https://github.com/Matthew-Eucaristo/decruft#readme) | Homebrew |
| ↳ [**fell**](https://github.com/Matthew-Eucaristo/fell) | Finds git worktrees left behind by AI coding agents, shows the evidence, and cleans up without breaking the agent's own lifecycle. | with decruft |
| ↳ [**nodekill**](https://github.com/Matthew-Eucaristo/nodekill) | The Node.js footprint: `node_modules`, `.next` and framework caches, npm/pnpm/Yarn/Bun caches, npx, globals, old Node versions. | with decruft |
| ↳ [**rustkill**](https://github.com/Matthew-Eucaristo/rustkill) | The Rust footprint: `target` folders found by cargo's own tag, Cargo registry and git caches, sccache, `cargo install` tools, rustup toolchains and `rust-docs`. [Demo →](https://matthew-eucaristo.github.io/rustkill/) | with decruft |
| ↳ [**flutterkill**](https://github.com/Matthew-Eucaristo/flutterkill) | npkill for Flutter: `build/`, `.dart_tool`, Pods and Gradle leftovers plus pub, Gradle, FVM and Xcode caches. | with decruft |
| [**lately**](https://github.com/Matthew-Eucaristo/lately) | What just happened on my Mac? A classified timeline from the unified log, crash reports and persistence items, with a card per event. No root, no daemon. [Demo →](https://github.com/Matthew-Eucaristo/lately#readme) | Homebrew |
| [**spoor.nvim**](https://github.com/Matthew-Eucaristo/spoor.nvim) | Follow the trail through a codebase in Neovim: a call bow-tie on `K`, trace mode with notes, and what your agent changed. LSP first, tree-sitter where there is none. No AI, no index. [Demo →](https://github.com/Matthew-Eucaristo/spoor.nvim#readme) | lazy.nvim |
| [**jupynvim**](https://github.com/sheng-tse/jupynvim) | Jupyter notebooks in Neovim. I send fixes upstream: [HTML tables for pandas Styler](https://github.com/sheng-tse/jupynvim/pull/45), [docs](https://github.com/sheng-tse/jupynvim/pull/46). | upstream PRs |

</details>

<details>
<summary><code>$ ls -l ~/projects</code> — every project, with its stack</summary>
<br>

| project | what it is | built with |
| :-- | :-- | :-- |
| [**Fotoin**](https://github.com/Matthew-Eucaristo/fotoin) | Photograph someone exactly like a reference pose (Pinterest, IG, or an example shot): a ghost overlay and pose skeleton over the live camera, a match meter, one hint at a time, auto-capture. Bodies, faces and groups; on-device, free, no ads. [Site →](https://matthew-eucaristo.github.io/fotoin/) | Expo · React Native · VisionCamera · MediaPipe · Apple Vision |
| [**Plain Gallery**](https://github.com/Matthew-Eucaristo/plain-gallery) | A photo gallery for Android that just works: no ads, no backup nagging, no internet permission. Faces and text in photos are recognised on the phone, so search finds people and receipts. [APK →](https://github.com/Matthew-Eucaristo/plain-gallery/releases) | Kotlin · Jetpack Compose · LiteRT |
| [**s1**](https://github.com/Matthew-Eucaristo/s1) | Voice-first macOS agent. A fast local *System 1* acts; an LLM *System 2* is asked only when unsure. Every step gated and logged. [Site →](https://s1-mac.pages.dev) `brew install --cask matthew-eucaristo/tap/s1` | Swift 6 · AX API · ScreenCaptureKit |
| [**Mouse Maze Mayhem**](https://mouse-maze-mayhem-skripsi.web.app) | My thesis, playable. Four cats vs. one RL mouse in 3D mazes — a solver-distilled policy running in your browser via ONNX. | PyTorch · ONNX · React Three Fiber |
| [**solitaire-rl**](https://github.com/Matthew-Eucaristo/solitaire-rl) | Masked DQN and MaskablePPO learning Klondike, judged on a fixed 1000-deal benchmark. Honest result: the heuristic still wins. | Python · SB3 · Gymnasium |
| [**rl-2048**](https://github.com/Matthew-Eucaristo/rl-2048) | A 2048 agent that learns by self-play on one laptop in 20 minutes: an n-tuple network, no GPU, no human games. With a 3-move lookahead it reaches 16384 in 68% of games. | Go · TD learning |
| [**mob-run**](https://github.com/Matthew-Eucaristo/mob-run) | The game from those fake mobile ads, for real: a 3D crowd-runner where you pick multiplier gates and outgun mobs, walls and bosses across 5 zones. [Play →](https://mob-run.pages.dev) | Three.js |
| [**crypto-cycle-signals**](https://github.com/Matthew-Eucaristo/crypto-cycle-signals) | Futures indicator anchored to BTC's 4-year cycle; every parameter earned by backtest on 68 perps × 6 years. | Pine Script v6 |
| [**blockies**](https://github.com/Matthew-Eucaristo/blockies) | Organic living blocks: a whiteboard where every drawing is alive, with few enough pieces that humans and AI agents both draw valid boards. v0.1 engine; the web runtime is next. | Rust · WASM |
| [**Flip10**](https://github.com/Matthew-Eucaristo/Flip10) | Shut the Box, polished: hand-drawn SVG tiles, procedural audio, fully offline. [Play →](https://flip10.pages.dev) | Next.js · TypeScript |

</details>

<details>
<summary><code>$ ls ~/archive</code> — game jam + university game lab</summary>
<br>

| build | stack |
| :-- | :-- |
| [Poppp: Rocket Balloon](https://github.com/Matthew-Eucaristo/GMTKGameJam2024) · [play](https://mammamiaaaaa.itch.io/pop-rocket-balloon) | Unreal Engine · GMTK Game Jam 2024 |
| [FOCUS tower defense](https://github.com/Matthew-Eucaristo/FOCUS-Game) · [play](https://syntax-gamedev.itch.io/focus-td) | Unreal Engine 5 |
| [Sliding puzzle](https://github.com/Matthew-Eucaristo/Sliding-Puzzle-UnrealEngine) | Unreal Engine 5 |
| [Shoot The Ghost AR](https://github.com/Matthew-Eucaristo/Shoot-The-Ghost-AR-KelasARVR) · [play](https://syntax-gamedev.itch.io/shoot-the-ghost-ar) | Unreal Engine · AR |
| [Computer graphics final](https://github.com/Matthew-Eucaristo/GrafKom-Final-Project) · [VR sim](https://syntax-gamedev.itch.io/compgraphsimvr) | Java · LWJGL / OpenGL |
| [Solar system](https://github.com/Matthew-Eucaristo/SolarSystemProject-Grafkom) | Java · LWJGL |
| [Guess the Path](https://github.com/Matthew-Eucaristo/Guess-the-Path) | Java · graphs |

</details>

### `$ ping matthew`

[LinkedIn](https://www.linkedin.com/in/matthew-eucaristo-265127184/) · [X](https://x.com/0xZexy) · [itch.io](https://syntax-gamedev.itch.io/)

<sub>pytorch · stable-baselines3 · onnx · swift · typescript · react · three.js · go · bubble tea · lua · unreal engine · docker · cloudflare</sub>
