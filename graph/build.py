#!/usr/bin/env python3
"""Render graph/graph.json as an Obsidian-style SVG (dark + light) and docs/graph.json.

Every repo node is checked against the GitHub API first: anything that is not a
public repo is dropped, so a private name can never end up in the picture.
Tools found in the Homebrew tap get their tap edge (and node) automatically.

    python3 graph/build.py            # GITHUB_TOKEN is optional, it only lifts rate limits
"""

import json
import math
import os
import random
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H = 880, 400
TOP = 32  # title bar
PAD = 28

THEMES = {
    "dark": {
        "bg": "#0d1117", "bar": "#161b22", "border": "#30363d", "edge": "#30363d",
        "text": "#e6edf3", "muted": "#7d8590",
        "tools": "#3fb950", "s1": "#d29922", "nvim": "#a371f7", "games": "#58a6ff", "misc": "#db61a2",
        "red": "#f85149", "orange": "#db6d28",
    },
    "light": {
        "bg": "#ffffff", "bar": "#f6f8fa", "border": "#d0d7de", "edge": "#d0d7de",
        "text": "#1f2328", "muted": "#656d76",
        "tools": "#1a7f37", "s1": "#9a6700", "nvim": "#8250df", "games": "#0969da", "misc": "#bf3989",
        "red": "#cf222e", "orange": "#bc4c00",
    },
}


def api(path):
    req = urllib.request.Request(f"https://api.github.com/{path}", headers={"Accept": "application/vnd.github+json"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def public_repos(owner):
    repos, page = {}, 1
    while True:
        batch = api(f"users/{owner}/repos?type=owner&per_page=100&page={page}")
        for r in batch:
            if not r["private"]:
                repos[r["full_name"]] = r
        if len(batch) < 100:
            return repos
        page += 1


def tap_entries(owner, tap):
    out = []
    for folder, kind in (("Formula", "formula"), ("Casks", "cask")):
        try:
            files = api(f"repos/{owner}/{tap}/contents/{folder}")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            raise
        out += [(f["name"].removesuffix(".rb"), kind) for f in files if f["name"].endswith(".rb")]
    return out


def resolve(spec):
    owner = spec["owner"]
    repos = public_repos(owner)
    nodes = {}
    for n in spec["nodes"]:
        n = dict(n)
        if n.get("tag") or n.get("planned"):
            nodes[n["id"]] = n
            continue
        full = n.get("repo", f"{owner}/{n['id']}")
        r = repos.get(full)
        if r is None and not full.startswith(owner + "/"):  # someone else's repo the user contributes to
            try:
                r = api(f"repos/{full}")
                r = None if r.get("private") else r
            except urllib.error.HTTPError:
                r = None
        if r is None:
            print(f"skip {n['id']}: not a public repo", file=sys.stderr)
            continue
        n["url"] = n.get("url") or r["html_url"]
        n["desc"] = n.get("desc") or r.get("description") or ""
        nodes[n["id"]] = n

    edges = [tuple(e) for e in spec["edges"]]
    tap = spec.get("tap")
    if tap and tap in nodes:
        for name, kind in tap_entries(owner, tap):
            if name not in nodes and f"{owner}/{name}" in repos:
                r = repos[f"{owner}/{name}"]
                nodes[name] = {"id": name, "group": "tools", "url": r["html_url"], "desc": r.get("description") or ""}
            if name in nodes:
                edges.append((name, tap, kind))

    edges = [e for e in edges if e[0] in nodes and e[1] in nodes]
    linked = {x for e in edges for x in e[:2]}
    nodes = {k: v for k, v in nodes.items() if not v.get("tag") or k in linked}
    return nodes, edges


def layout(nodes, edges, seed=7, steps=900):
    ids = sorted(nodes)
    rnd = random.Random(seed)
    pos = {i: [rnd.uniform(-1, 1), rnd.uniform(-1, 1)] for i in ids}
    deg = {i: 0 for i in ids}
    for a, b, _ in edges:
        deg[a] += 1
        deg[b] += 1
    k = 0.42
    for step in range(steps):
        t = 0.08 * (1 - step / steps) + 0.002
        disp = {i: [0.0, 0.0] for i in ids}
        for x in range(len(ids)):
            for y in range(x + 1, len(ids)):
                a, b = ids[x], ids[y]
                dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
                d = max(math.hypot(dx, dy), 0.01)
                f = k * k / d if d < 3 * k else 0  # short range: clusters don't fling each other away
                disp[a][0] += dx / d * f; disp[a][1] += dy / d * f
                disp[b][0] -= dx / d * f; disp[b][1] -= dy / d * f
        for a, b, kind in edges:
            dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
            d = max(math.hypot(dx, dy), 0.01)
            f = d * d / k * (0.6 if kind == "tag" else 1.0)
            disp[a][0] -= dx / d * f; disp[a][1] -= dy / d * f
            disp[b][0] += dx / d * f; disp[b][1] += dy / d * f
        for i in ids:
            g = 0.6
            disp[i][0] -= pos[i][0] * g; disp[i][1] -= pos[i][1] * g * 2.4  # squash: the canvas is wide
            d = max(math.hypot(*disp[i]), 1e-9)
            pos[i][0] += disp[i][0] / d * min(d, t)
            pos[i][1] += disp[i][1] / d * min(d, t)
    return pos, deg


def radius(n, deg):
    if n.get("tag"):
        return 2.5
    return 3.5 + 1.5 * math.sqrt(deg)


def fit(nodes, pos, deg):
    """Scale the layout into the canvas, counting label widths so nothing is clipped."""
    def box(i, s, ox, oy):
        x, y = pos[i][0] * s + ox, pos[i][1] * s + oy
        half = len(i) * 3.3 + 2
        r = radius(nodes[i], deg[i])
        return x - half, y - r, x + half, y + r + 14

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    for i in pos:
        pos[i][0] -= cx; pos[i][1] -= cy
    s = 1000.0
    while s > 1:
        bs = [box(i, s, W / 2, (H + TOP) / 2) for i in pos]
        if (min(b[0] for b in bs) >= PAD and max(b[2] for b in bs) <= W - PAD
                and min(b[1] for b in bs) >= TOP + PAD and max(b[3] for b in bs) <= H - PAD - 10):
            break
        s *= 0.98
    xy = {i: [p[0] * s + W / 2, p[1] * s + (H + TOP) / 2] for i, p in pos.items()}
    return untangle(nodes, xy, deg)


def label(n):
    return n["id"] + (" (planned)" if n.get("planned") else "")


def untangle(nodes, xy, deg, gap=6):
    """Push apart nodes whose dot+label boxes overlap, staying inside the canvas."""
    def box(i):
        x, y = xy[i]
        half = max(len(label(nodes[i])) * 3.3, radius(nodes[i], deg[i])) + gap / 2
        return x - half, y - radius(nodes[i], deg[i]) - gap / 2, x + half, y + radius(nodes[i], deg[i]) + 15 + gap / 2

    ids = sorted(xy)
    for _ in range(400):
        moved = False
        for x in range(len(ids)):
            for y in range(x + 1, len(ids)):
                a, b = ids[x], ids[y]
                ax0, ay0, ax1, ay1 = box(a)
                bx0, by0, bx1, by1 = box(b)
                ox, oy = min(ax1, bx1) - max(ax0, bx0), min(ay1, by1) - max(ay0, by0)
                if ox <= 0 or oy <= 0:
                    continue
                moved = True
                if oy < ox:  # cheaper to separate vertically
                    d = (oy / 2 + 0.5) * (1 if xy[a][1] >= xy[b][1] else -1)
                    xy[a][1] += d; xy[b][1] -= d
                else:
                    d = (ox / 2 + 0.5) * (1 if xy[a][0] >= xy[b][0] else -1)
                    xy[a][0] += d; xy[b][0] -= d
        for i in ids:
            half = len(label(nodes[i])) * 3.3 + 2
            xy[i][0] = min(max(xy[i][0], PAD + half), W - PAD - half)
            xy[i][1] = min(max(xy[i][1], TOP + PAD), H - PAD - 24)
        if not moved:
            break
    return {i: (round(p[0], 1), round(p[1], 1)) for i, p in xy.items()}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(nodes, edges, xy, deg, c):
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Graph of public projects: dev tools, the Homebrew tap, s1, Neovim plugins and games">',
        "<style>text{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace}"
        ".n{opacity:0;animation:in .6s ease-out forwards}.flow{animation:flow 1.2s linear infinite}"
        "@keyframes in{to{opacity:1}}@keyframes flow{to{stroke-dashoffset:-8}}"
        "@media (prefers-reduced-motion:reduce){.n{animation:none;opacity:1}.flow{animation:none}.pulse{display:none}}</style>",
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>',
        f'<path d="M0.5 12.5 a12 12 0 0 1 12 -12 h{W - 25} a12 12 0 0 1 12 12 v19.5 h-{W - 1} z" fill="{c["bar"]}"/>',
        f'<line x1="0.5" y1="{TOP}" x2="{W - 0.5}" y2="{TOP}" stroke="{c["border"]}"/>',
        f'<text x="20" y="21" font-size="12" fill="{c["muted"]}"><tspan fill="{c["tools"]}">~</tspan> $ graph --public</text>',
        f'<text x="{W - 20}" y="21" text-anchor="end" font-size="12" fill="{c["muted"]}">{len([n for n in nodes.values() if not n.get("tag")])} nodes · {len(edges)} links</text>',
    ]
    for k, (a, b, kind) in enumerate(sorted(edges)):
        (x1, y1), (x2, y2) = xy[a], xy[b]
        dash = ' stroke-dasharray="4 4" class="flow"' if kind == "depends" else ""
        op = "0.6" if kind == "tag" else "1"
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["edge"]}" stroke-width="1.2" stroke-opacity="{op}"{dash}/>')
        if kind != "tag":  # a slow signal along real links (tap, depends, landing page)
            dur = 3.5 + (k * 7 % 5) * 0.5
            out.append(f'<circle class="pulse" r="1.8" fill="{c[nodes[a].get("group", "tools")]}" opacity="0.8">'
                       f'<animateMotion dur="{dur}s" begin="{k * 0.4:.1f}s" repeatCount="indefinite" path="M{x1} {y1} L{x2} {y2}"/></circle>')
    for k, i in enumerate(sorted(nodes, key=lambda i: (nodes[i].get("tag", False), -deg[i], i))):
        n, (x, y) = nodes[i], xy[i]
        r = round(radius(n, deg[i]), 1)
        out.append(f'<g class="n" style="animation-delay:{k * 0.06:.2f}s">')
        if n.get("tag"):
            out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["muted"]}"/>')
            fill, weight = c["muted"], ""
        elif n.get("planned"):
            out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["bg"]}" stroke="{c[n["group"]]}" stroke-width="1.5" stroke-dasharray="2.5 2"/>')
            fill, weight = c["muted"], ""
        else:
            out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c[n["group"]]}"/>')
            fill, weight = c["text"], ""
        text = esc(label(n))
        out.append(f'<text x="{x}" y="{round(y + r + 12, 1)}" text-anchor="middle" font-size="11" fill="{fill}"{weight}>{text}</text>')
        out.append("</g>")
    legend = [("tools", "dev tools"), ("s1", "s1"), ("nvim", "neovim"), ("games", "games")]
    lx = 20
    for g, name in legend:
        out.append(f'<circle cx="{lx + 4}" cy="{H - 16}" r="3.5" fill="{c[g]}"/>')
        out.append(f'<text x="{lx + 12}" y="{H - 12}" font-size="11" fill="{c["muted"]}">{name}</text>')
        lx += 24 + len(name) * 6.6
    out.append(f'<line x1="{lx}" y1="{H - 16}" x2="{lx + 18}" y2="{H - 16}" stroke="{c["muted"]}" stroke-dasharray="4 4"/>')
    out.append(f'<text x="{lx + 24}" y="{H - 12}" font-size="11" fill="{c["muted"]}">depends on</text>')
    out.append(f'<text x="{W - 20}" y="{H - 12}" text-anchor="end" font-size="11" fill="{c["muted"]}">public repos only · graph/build.py</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main():
    spec = json.loads((ROOT / "graph/graph.json").read_text())
    nodes, edges = resolve(spec)
    pos, deg = layout(nodes, edges)
    xy = fit(nodes, pos, deg)
    for name, c in THEMES.items():
        (ROOT / f"assets/graph-{name}.svg").write_text(svg(nodes, edges, xy, deg, c))
    data = {
        "nodes": [{k: v for k, v in nodes[i].items()} | {"x": xy[i][0], "y": xy[i][1]} for i in sorted(nodes)],
        "edges": [list(e) for e in sorted(edges)],
    }
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs/graph.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(nodes)} nodes, {len(edges)} edges")


if __name__ == "__main__":
    main()
