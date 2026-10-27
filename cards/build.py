#!/usr/bin/env python3
"""Render the animated profile cards (dark + light) from cards/cards.json and the GitHub API.

    assets/spotlight-*.svg  one project at a time, cross-fading, with a small live sketch of what it does
    assets/shipped-*.svg    the latest releases of public repos, newest first

Pure SVG + CSS animation, so they play inside a GitHub README (no JavaScript there) and stop
under prefers-reduced-motion. Releases come only from public repos, like the graph's nodes.

    python3 cards/build.py            # GITHUB_TOKEN is optional, it only lifts rate limits
"""

import json
import sys
import textwrap
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "graph"))
import build as graph  # noqa: E402  (shares the palette, the API helper and the public-repo check)

W = 880
TOP = 32
FONT = "font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
esc = graph.esc


def chrome(c, h, title, right=""):
    return [
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>',
        f'<path d="M0.5 12.5 a12 12 0 0 1 12 -12 h{W - 25} a12 12 0 0 1 12 12 v19.5 h-{W - 1} z" fill="{c["bar"]}"/>',
        f'<line x1="0.5" y1="{TOP}" x2="{W - 0.5}" y2="{TOP}" stroke="{c["border"]}"/>',
        f'<text x="20" y="21" font-size="12" fill="{c["muted"]}"><tspan fill="{c["tools"]}">~</tspan> $ {esc(title)}</text>',
        f'<text x="{W - 20}" y="21" text-anchor="end" font-size="12" fill="{c["muted"]}">{esc(right)}</text>' if right else "",
    ]


# ── the small sketches, one per kind of project; each draws in a 288 × 200 box ──

def voice(c, a):
    out = [f'<text x="144" y="26" text-anchor="middle" font-size="12" fill="{c["text"]}">“rename these screenshots by date”</text>']
    for i in range(29):
        h = 10 + (i * 37 % 23) + (14 if 9 < i < 20 else 0)
        out.append(f'<rect class="wave" style="animation-delay:{i * 0.06:.2f}s" x="{30 + i * 8}" y="{62 - h / 2:.1f}" '
                   f'width="4" height="{h}" rx="2" fill="{a}"/>')
    lanes = [("System 1 · local", "act", a, 2.2, 1, ""), ("System 2 · LLM", "ask", c["muted"], 6.6, 0.25, ' stroke-dasharray="3 4"')]
    for k, (name, verb, col, dur, end, dash) in enumerate(lanes):
        y = 118 + k * 40
        out += [
            f'<text x="16" y="{y + 4}" font-size="11" fill="{col}">{name}</text>',
            f'<line x1="136" y1="{y}" x2="236" y2="{y}" stroke="{c["border"]}" stroke-width="2"{dash}/>',
            f'<circle r="4" fill="{col}"><animateMotion dur="{dur}s" repeatCount="indefinite" keyPoints="0;1;1" '
            f'keyTimes="0;{end if k else 0.6};1" path="M136 {y} L236 {y}"/></circle>',
            f'<text x="246" y="{y + 4}" font-size="11" fill="{col}">{verb}</text>',
        ]
    out.append(f'<text x="144" y="196" text-anchor="middle" font-size="11" fill="{c["muted"]}">every step gated · logged</text>')
    return out


def maze(c, a):
    # 6 × 4 cells of 36px; the mouse's route and both patrols run only through open walls.
    walls = [(72, 132, 72, 168), (108, 96, 108, 132), (108, 24, 108, 60), (180, 60, 180, 96), (72, 96, 108, 96),
             (108, 132, 144, 132), (144, 132, 180, 132), (216, 60, 252, 60), (36, 60, 72, 60), (180, 132, 216, 132),
             (36, 24, 252, 24), (36, 168, 252, 168), (36, 24, 36, 132), (252, 60, 252, 168)]
    cell = lambda col, row: (54 + 36 * col, 42 + 36 * row)  # noqa: E731
    route = lambda cells: "M" + " L".join(f"{x} {y}" for x, y in (cell(*p) for p in cells))  # noqa: E731
    mouse = "M18 150 L" + route([(0, 3), (0, 2), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (4, 1), (4, 0), (5, 0)])[1:] + " L270 42"
    cat1 = route([(5, 3), (4, 3), (3, 3), (2, 3), (3, 3), (4, 3), (5, 3)])
    cat2 = route([(2, 0), (3, 0), (3, 1), (3, 0), (2, 0)])
    out = [f'<g stroke="{c["border"]}" stroke-width="2" stroke-linecap="round">']
    out += [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>' for x1, y1, x2, y2 in walls]
    out.append("</g>")
    out.append(f'<path class="trail" d="{mouse}" fill="none" stroke="{a}" stroke-opacity="0.45" stroke-width="2" '
               f'stroke-linejoin="round" pathLength="100"/>')
    out.append(f'<circle r="5" fill="{a}"><animateMotion dur="5s" repeatCount="indefinite" keyPoints="0;1;1" '
               f'keyTimes="0;0.85;1" path="{mouse}"/></circle>')
    for path, dur in ((cat1, 4), (cat2, 3)):
        out.append(f'<circle r="4.5" fill="{c["orange"]}"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{path}"/></circle>')
    out.append(f'<text x="144" y="196" text-anchor="middle" font-size="11" fill="{c["muted"]}">'
               f'<tspan fill="{a}">●</tspan> mouse · policy.onnx   <tspan fill="{c["orange"]}">●</tspan> cats</text>')
    return out


def crowd(c, a):
    out = [
        f'<line x1="8" y1="58" x2="280" y2="58" stroke="{c["border"]}"/>',
        f'<line x1="8" y1="142" x2="280" y2="142" stroke="{c["border"]}"/>',
        f'<rect x="112" y="54" width="4" height="92" fill="{a}" opacity="0.7"/>',
        f'<rect x="92" y="18" width="44" height="24" rx="5" fill="{a}"/>',
        f'<text x="114" y="35" text-anchor="middle" font-size="13" font-weight="700" fill="{c["bg"]}">×3</text>',
        f'<rect x="236" y="70" width="30" height="60" rx="4" fill="{c["red"]}" opacity="0.85"/>',
        f'<rect x="232" y="60" width="38" height="4" rx="2" fill="{c["border"]}"/>',
        f'<rect class="hp" x="232" y="60" width="38" height="4" rx="2" fill="{c["red"]}"/>',
    ]
    few = "".join(f'<circle cx="{18 + dx}" cy="{90 + dy}" r="5" fill="{c["text"]}"/>' for dx, dy in ((0, 0), (10, 14), (0, 28)))
    many = "".join(f'<circle cx="{124 + col * 11}" cy="{78 + row * 12}" r="4.5" fill="{a}"/>'
                   for col in range(3) for row in range(4))
    out += [f'<g class="few">{few}</g>', f'<g class="many">{many}</g>',
            f'<text x="144" y="196" text-anchor="middle" font-size="11" fill="{c["muted"]}">pick the gate · outgun the boss</text>']
    return out


def worktrees(c, a):
    rows = [("agent-a3f9…", "only here", c["red"], 0.9), ("codex/7c1e", "app-tracked", c["orange"], 0.75),
            ("cursor/q4k2", "safe", a, 0.6), ("shop-hotfix", "yours", c["muted"], 0.45)]
    out = [f'<line x1="22" y1="18" x2="22" y2="168" stroke="{c["muted"]}" stroke-width="2"/>',
           f'<text x="32" y="22" font-size="11" fill="{c["muted"]}">main</text>',
           f'<rect class="scan" x="4" y="38" width="280" height="26" rx="4" fill="{a}" opacity="0.10"/>']
    for i, (name, tag, col, size) in enumerate(rows):
        y = 51 + i * 33
        out += [
            f'<path d="M22 {y - 16} q0 16 16 16 h6" fill="none" stroke="{c["muted"]}" stroke-width="2"/>',
            f'<circle cx="48" cy="{y}" r="4" fill="{col}"/>',
            f'<text x="58" y="{y + 4}" font-size="11" fill="{c["text"]}">{name}</text>',
            f'<rect x="150" y="{y - 4}" width="{70 * size:.0f}" height="8" rx="3" fill="{c["border"]}"/>',
            f'<rect class="{"strip" if tag == "safe" else ""}" x="150" y="{y - 4}" width="{70 * size:.0f}" height="8" rx="3" fill="{col}" opacity="0.8"/>',
            f'<text x="282" y="{y + 4}" text-anchor="end" font-size="10" fill="{col}">{tag}</text>',
        ]
    out.append(f'<text x="144" y="196" text-anchor="middle" font-size="11" fill="{c["muted"]}">evidence first · Trash + rescue bundle</text>')
    return out


def timeline(c, a):
    rows = [("14:49", "▲", "HIGH", c["orange"], "Launch agent added"), ("14:52", "✖", "CRIT", c["red"], "System extension added"),
            ("14:53", "▲", "HIGH", c["orange"], "App crashed ×3"), ("14:58", "▲", "HIGH", c["orange"], "Screen Recording allowed"),
            ("15:01", "●", "MED", c["s1"], "Shell startup file changed")]
    out = []
    for i, (t, g, lvl, col, what) in enumerate(rows):
        y = 26 + i * 30
        out.append(f'<g class="row" style="animation-delay:{i * 0.45:.2f}s">'
                   f'<text x="8" y="{y}" font-size="11" fill="{c["muted"]}">{t}</text>'
                   f'<text x="52" y="{y}" font-size="11" fill="{col}">{g} {lvl}</text>'
                   f'<text x="110" y="{y}" font-size="11" fill="{c["text"]}">{esc(what)}</text></g>')
    out.append(f'<text x="144" y="196" text-anchor="middle" font-size="11" fill="{c["muted"]}">unified log → classified timeline</text>')
    return out


def bowtie(c, a):
    left, right, cx, cy = ["CartPage", "api/orders", "retry()"], ["validate()", "charge()", "receipt()"], 144, 92
    out = []
    for side, names in ((-1, left), (1, right)):
        for i, name in enumerate(names):
            y = 42 + i * 50
            x = cx + side * 104
            x0, x1 = (x + 34, cx - 40) if side < 0 else (cx + 40, x - 34)
            d = f"M{x0} {y} C{(x0 + x1) / 2} {y} {(x0 + x1) / 2} {cy} {x1} {cy}" if side < 0 else \
                f"M{x0} {cy} C{(x0 + x1) / 2} {cy} {(x0 + x1) / 2} {y} {x1} {y}"
            out += [
                f'<path class="flow" d="{d}" fill="none" stroke="{c["border"]}" stroke-width="1.5" stroke-dasharray="4 4"/>',
                f'<circle r="3" fill="{a}"><animateMotion dur="2.4s" begin="{i * 0.5 + (side > 0) * 1.2:.1f}s" repeatCount="indefinite" path="{d}"/></circle>',
                f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="11" fill="{c["text"]}">{name}</text>',
            ]
    out += [f'<rect x="{cx - 40}" y="{cy - 14}" width="80" height="28" rx="6" fill="{a}" opacity="0.15" stroke="{a}"/>',
            f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="12" font-weight="700" fill="{a}">checkout()</text>',
            f'<text x="144" y="196" text-anchor="middle" font-size="11" fill="{c["muted"]}">callers ← focus → callees</text>']
    return out


def storage(c, a):
    # The disk as one bar by developer category; the safe parts shrink as their own tool cleans them.
    rows = [("Xcode", "xcrun simctl delete unavailable", c["orange"], 70, True), ("Go", "go clean -cache", a, 46, True),
            ("node_modules", "via nodekill", c["nvim"], 58, False), ("Homebrew", "brew autoremove", c["games"], 34, True),
            ("Docker", "docker system prune", c["misc"], 40, True)]
    out = [f'<text x="8" y="14" font-size="10" fill="{c["muted"]}">disk</text>',
           f'<rect x="8" y="20" width="272" height="16" rx="4" fill="{c["border"]}" opacity="0.5"/>']
    x = 8
    for i, (_, _, col, w, safe) in enumerate(rows):
        cls = f' class="strip" style="animation-delay:{i * 0.35:.2f}s"' if safe else ""
        out.append(f'<rect{cls} x="{x}" y="20" width="{w}" height="16" fill="{col}" opacity="0.85"/>')
        x += w
    for i, (name, cmd, col, _, _) in enumerate(rows):
        y = 64 + i * 25
        out += [f'<circle cx="14" cy="{y - 4}" r="4" fill="{col}"/>',
                f'<text x="26" y="{y}" font-size="11" fill="{c["text"]}">{name}</text>',
                f'<text x="282" y="{y}" text-anchor="end" font-size="10" fill="{c["muted"]}">{esc(cmd)}</text>']
    out.append(f'<text x="144" y="196" text-anchor="middle" font-size="11" fill="{c["muted"]}">one scan · each tool cleans its own</text>')
    return out


VISUALS = {"voice": voice, "maze": maze, "crowd": crowd, "worktrees": worktrees, "timeline": timeline, "bowtie": bowtie,
           "storage": storage}

SKETCH_CSS = (
    ".wave{transform-box:fill-box;transform-origin:center;animation:wave 1.1s ease-in-out infinite}"
    "@keyframes wave{0%,100%{transform:scaleY(.35)}50%{transform:scaleY(1)}}"
    ".trail{stroke-dasharray:100;stroke-dashoffset:100;animation:trail 5s linear infinite}"
    "@keyframes trail{85%,100%{stroke-dashoffset:0}}"
    ".few{animation:few 3s linear infinite}.many{opacity:0;animation:many 3s linear infinite}"
    "@keyframes few{0%{transform:translateX(0);opacity:1}40%{transform:translateX(92px);opacity:1}45%,100%{transform:translateX(92px);opacity:0}}"
    "@keyframes many{0%,42%{transform:translateX(0);opacity:0}47%{opacity:1}85%{transform:translateX(70px);opacity:1}92%,100%{transform:translateX(70px);opacity:0}}"
    ".hp{transform-box:fill-box;transform-origin:left;animation:hp 3s linear infinite}"
    "@keyframes hp{0%,75%{transform:scaleX(1)}95%,100%{transform:scaleX(.25)}}"
    ".scan{animation:scan 4s steps(1) infinite}"
    "@keyframes scan{0%{transform:translateY(0)}25%{transform:translateY(33px)}50%{transform:translateY(66px)}75%{transform:translateY(99px)}}"
    ".strip{transform-box:fill-box;transform-origin:left;animation:strip 4s ease-in-out infinite}"
    "@keyframes strip{0%,45%{transform:scaleX(1)}60%,90%{transform:scaleX(.08)}100%{transform:scaleX(1)}}"
    ".row{opacity:0;animation:row 5s ease-out infinite}"
    "@keyframes row{0%{opacity:0;transform:translateX(-8px)}8%,88%{opacity:1;transform:none}100%{opacity:0}}"
    ".flow{animation:flow 1s linear infinite}@keyframes flow{to{stroke-dashoffset:-8}}"
)


def spotlight(spec, c):
    slides, t = spec["slides"], spec["seconds_per_slide"]
    n, h = len(slides), 300
    share = 100 / n
    fade = 1.6
    css = (
        f"text{{{FONT}}}"
        # Negative delays keep every slide's animation running from t=0, and each slide is fully visible at the
        # start of its own turn, so the first frame (and any renderer that ignores CSS animation) shows slide 0.
        f".s{{opacity:0;animation:slide {n * t}s infinite}}.s0{{opacity:1}}"
        f"@keyframes slide{{0%,{share - fade:.2f}%{{opacity:1;transform:none}}{share:.2f}%{{opacity:0}}"
        f"{100 - fade:.2f}%{{opacity:0;transform:translateY(6px)}}100%{{opacity:1;transform:none}}}}"
        f".bar{{transform-box:fill-box;transform-origin:left;animation:bar {n * t}s linear infinite}}"
        f"@keyframes bar{{0%{{transform:scaleX(0)}}{share:.2f}%,100%{{transform:scaleX(1)}}}}"
        + SKETCH_CSS +
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}.s{opacity:0}.s0{opacity:1}.many,.row{opacity:1}}"
    )
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" '
           f'aria-label="Project spotlight: {esc(", ".join(s["repo"] for s in slides))}">', f"<style>{css}</style>"]
    out += chrome(c, h, "spotlight --loop", f"{n} projects · {n * t}s")
    for k in range(n):  # the dots under every slide
        out.append(f'<circle cx="{W - 32 - (n - 1 - k) * 14}" cy="{h - 22}" r="3" fill="{c["border"]}"/>')
    for i, s in enumerate(slides):
        a = c[s["group"]]
        delay = f"animation-delay:{(i - n) * t}s"
        g = [f'<g class="s s{i}" style="{delay}">']
        g.append(f'<text x="32" y="70" font-size="11" letter-spacing="1.5" fill="{a}">{esc(s["kicker"].upper())}</text>')
        g.append(f'<text x="32" y="106" font-size="28" font-weight="700" fill="{c["text"]}">{esc(s["repo"])}</text>')
        for j, line in enumerate(textwrap.wrap(s["desc"], 54)[:3]):
            g.append(f'<text x="32" y="{136 + j * 21}" font-size="14" fill="{c["text"]}" opacity="0.88">{esc(line)}</text>')
        x = 32
        for chip in s["stack"]:
            w = len(chip) * 6.6 + 16
            g.append(f'<rect x="{x}" y="212" width="{w:.0f}" height="20" rx="10" fill="none" stroke="{c["border"]}"/>')
            g.append(f'<text x="{x + w / 2:.0f}" y="226" text-anchor="middle" font-size="11" fill="{c["muted"]}">{esc(chip)}</text>')
            x += w + 8
        g.append(f'<text x="32" y="{h - 18}" font-size="12" fill="{c["muted"]}"><tspan fill="{a}">→</tspan> {esc(s["where"])}</text>')
        g.append(f'<rect x="560" y="50" width="296" height="214" rx="8" fill="{c["bar"]}" stroke="{c["border"]}"/>')
        g.append('<g transform="translate(564,58)">')
        g += VISUALS[s["visual"]](c, a)
        g.append("</g>")
        g.append(f'<circle cx="{W - 32 - (n - 1 - i) * 14}" cy="{h - 22}" r="3.5" fill="{a}"/>')
        g.append(f'<rect class="bar" style="{delay}" x="1" y="{TOP}" width="{W - 2}" height="2" fill="{a}" opacity="0.7"/>')
        g.append("</g>")
        out += g
    out.append("</svg>")
    return "\n".join(x for x in out if x) + "\n"


def latest_releases(owner, groups, limit=5):
    rels = []
    for full, repo in sorted(graph.public_repos(owner).items()):
        if repo["fork"] or repo["archived"]:
            continue
        batch = graph.api(f"repos/{full}/releases?per_page=1")
        if batch and not batch[0]["draft"]:
            r = batch[0]
            rels.append({"repo": repo["name"], "tag": r["tag_name"], "date": r["published_at"],
                         "group": groups.get(repo["name"], "misc"), "desc": repo["description"] or ""})
    return sorted(rels, key=lambda r: r["date"], reverse=True)[:limit]


def shipped(rels, c):
    h, n = 112, max(len(rels), 1)
    css = (f"text{{{FONT}}}"
           ".new{animation:ping 2s ease-out infinite;transform-box:fill-box;transform-origin:center}"
           "@keyframes ping{0%{transform:scale(1);opacity:.8}100%{transform:scale(3);opacity:0}}"
           "@media (prefers-reduced-motion:reduce){*{animation:none!important}.new{display:none}}")
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" '
           f'aria-label="Latest releases: {esc(", ".join(r["repo"] + " " + r["tag"] for r in rels))}">', f"<style>{css}</style>"]
    out += chrome(c, h, "git tag --sort=-creatordate  # latest releases", "updated weekly")
    cw = (W - 40) / n
    for i, r in enumerate(rels):
        x, a = 20 + i * cw, c[r["group"]]
        day = datetime.fromisoformat(r["date"].replace("Z", "+00:00")).strftime("%b %-d")
        out.append('<g>')
        out.append(f'<rect x="{x + 4:.0f}" y="46" width="{cw - 8:.0f}" height="50" rx="8" fill="{c["bar"]}" stroke="{c["border"]}"/>')
        if i == 0:
            out.append(f'<circle class="new" cx="{x + 20:.0f}" cy="63" r="3.5" fill="{a}"/>')
        out.append(f'<circle cx="{x + 20:.0f}" cy="63" r="3.5" fill="{a}"/>')
        out.append(f'<text x="{x + 32:.0f}" y="67" font-size="13" font-weight="700" fill="{c["text"]}">{esc(r["repo"])}</text>')
        out.append(f'<text x="{x + 20:.0f}" y="87" font-size="11" fill="{a}">{esc(r["tag"])}<tspan fill="{c["muted"]}">  ·  {day}</tspan></text>')
        out.append("</g>")
    out.append("</svg>")
    return "\n".join(x for x in out if x) + "\n"


def main():
    spec = json.loads((ROOT / "cards/cards.json").read_text())
    gspec = json.loads((ROOT / "graph/graph.json").read_text())
    groups = {n["id"]: n["group"] for n in gspec["nodes"] if "group" in n}
    rels = latest_releases(gspec["owner"], groups)
    for theme, c in graph.THEMES.items():
        (ROOT / f"assets/spotlight-{theme}.svg").write_text(spotlight(spec, c))
        (ROOT / f"assets/shipped-{theme}.svg").write_text(shipped(rels, c))
    print(f"{len(spec['slides'])} slides, {len(rels)} releases: " + ", ".join(f"{r['repo']} {r['tag']}" for r in rels))


if __name__ == "__main__":
    main()
