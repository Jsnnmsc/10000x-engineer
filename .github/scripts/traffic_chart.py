#!/usr/bin/env python3
"""Record daily clone traffic and render it as light/dark SVG charts.

GitHub's traffic API only exposes the last 14 days, so this appends each day's
numbers to a JSON file in the repo. Clone count is the closest thing to an
install count for a Claude Code plugin: `/plugin install` clones the repo.
"""

import json
import math
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

REPO = os.environ.get("GITHUB_REPOSITORY", "Jsnnmsc/10000x-engineer")
TOKEN = os.environ.get("GH_TRAFFIC_TOKEN") or os.environ.get("GITHUB_TOKEN")
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / ".github" / "traffic" / "clones.json"

# From the dataviz reference palette.
THEMES = {
    "light": {
        "surface": "#fcfcfb", "primary": "#0b0b0b", "secondary": "#52514e",
        "muted": "#898781", "grid": "#e1e0d9", "axis": "#c3c2b7",
        "accent": "#2a78d6",
    },
    "dark": {
        "surface": "#1a1a19", "primary": "#ffffff", "secondary": "#c3c2b7",
        "muted": "#898781", "grid": "#2c2c2a", "axis": "#383835",
        "accent": "#3987e5",
    },
}


def fetch_clones():
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/traffic/clones?per=day",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "traffic-chart",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp).get("clones", [])
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            sys.exit(
                f"HTTP {e.code} from the traffic API, which needs push access to "
                f"{REPO}. The default GITHUB_TOKEN may not reach traffic even with "
                "administration:read. Fix: create a fine-grained personal access "
                "token limited to this repository with Administration: Read-only "
                "(a classic token needs the broader repo scope), and add it as the "
                "GH_TRAFFIC_TOKEN repository secret."
            )
        raise


def load():
    if not DATA.exists():
        return {}
    return json.loads(DATA.read_text(encoding="utf-8")).get("days", {})


def save(days):
    """Keep every recorded day. Pruning old days would shrink a running total."""
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(
        json.dumps(
            {
                "note": (
                    "Daily git clones of this repo. `/plugin install` clones the "
                    "repo, so this tracks installs — but it also counts CI, "
                    "mirrors, and plain browsing clones. Trend, not headcount."
                ),
                "repo": REPO,
                "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "days": dict(sorted(days.items())),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return days


def series(days):
    """Every recorded day, oldest first.

    Days never recorded are left out rather than zero-filled — a workflow
    outage longer than the API's 14-day window would otherwise be drawn as a
    run of genuine zeros, which is a claim the data cannot support. The x
    axis is positioned by date, so a gap reads as a gap.
    """
    return [
        (d, v.get("count", 0), v.get("uniques", 0)) for d, v in sorted(days.items())
    ]


def nice_max(v):
    """Round up to a tidy, even axis maximum.

    Even, so the midpoint gridline lands on a whole number instead of being
    labelled 7 while sitting at 7.5.
    """
    if v <= 4:
        return 4
    mag = 10 ** math.floor(math.log10(v))
    for mult in (1, 2, 5, 10):
        step = mag * mult
        top = int(math.ceil(v / step) * step)
        if top <= step * 4:
            return top if top % 2 == 0 else top + int(step)
    return int(math.ceil(v / mag) * mag)


def path_for(points):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points)


def render(rows, theme_name, out_path):
    """One cumulative series: install events, summed over every recorded day.

    Each day contributes GitHub's unique-cloner count for that day, so this
    counts installs, not distinct people: the same machine cloning again a
    week later is another install event and is counted again.

    A single series needs no legend — the headline names it. Cumulative and
    monotonic, so area reads it better than a bare line.
    """
    t = THEMES[theme_name]
    W, H = 840, 268
    L, R, TOP, BOT = 56, 40, 84, 34
    pw, ph = W - L - R, H - TOP - BOT

    running = 0
    cumulative = []
    for _, _, uniq in rows:
        running += uniq
        cumulative.append(running)

    # Recorded zeros are data. Only an empty record means nothing was collected.
    has_data = bool(rows)
    ymax = nice_max(max(cumulative or [1]))

    if has_data:
        first = date.fromisoformat(rows[0][0])
        span = (date.fromisoformat(rows[-1][0]) - first).days or 1

    def xy(i, v):
        offset = (date.fromisoformat(rows[i][0]) - first).days
        return L + pw * offset / span, TOP + ph - (ph * v / ymax)

    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="system-ui,-apple-system,Segoe UI,sans-serif">',
        f'<rect width="{W}" height="{H}" rx="8" fill="{t["surface"]}"/>',
    ]

    s.append(
        f'<text x="{L}" y="34" font-size="11" font-weight="600" '
        f'letter-spacing="1.6" fill="{t["muted"]}">TOTAL INSTALLS</text>'
    )
    if has_data:
        # One <text> with two <tspan>s: the flourish flows from the end of the
        # number, so it lands beside it without measuring glyph widths.
        s.append(
            f'<text x="{L}" y="68">'
            f'<tspan font-size="32" font-weight="700" fill="{t["primary"]}">'
            f'{running:,}</tspan>'
            f'<tspan dx="12" font-size="14" font-weight="600" '
            f'fill="{t["accent"]}">productivity granted!!</tspan>'
            f'</text>'
        )

    for frac in (0, 0.5, 1):
        y = TOP + ph - ph * frac
        s.append(
            f'<line x1="{L}" y1="{y:.1f}" x2="{L + pw}" y2="{y:.1f}" '
            f'stroke="{t["grid"] if frac else t["axis"]}" stroke-width="1"/>'
        )
        s.append(
            f'<text x="{L - 8}" y="{y + 4:.1f}" font-size="10" text-anchor="end" '
            f'fill="{t["muted"]}" font-variant-numeric="tabular-nums">'
            f'{int(ymax * frac)}</text>'
        )

    if has_data:
        pts = [xy(i, v) for i, v in enumerate(cumulative)]
        base = TOP + ph
        s.append(
            f'<path d="{path_for(pts)} L{pts[-1][0]:.1f},{base:.1f} '
            f'L{pts[0][0]:.1f},{base:.1f} Z" fill="{t["accent"]}" fill-opacity="0.13"/>'
        )
        s.append(
            f'<path d="{path_for(pts)}" fill="none" stroke="{t["accent"]}" '
            f'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
        )
        ex, ey = pts[-1]
        s.append(
            f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.5" fill="{t["accent"]}" '
            f'stroke="{t["surface"]}" stroke-width="2"/>'
        )
        for i, anchor in ((0, "start"), (len(rows) - 1, "end")):
            x, _ = xy(i, 0)
            s.append(
                f'<text x="{x:.0f}" y="{TOP + ph + 20}" font-size="10" '
                f'text-anchor="{anchor}" fill="{t["muted"]}">{rows[i][0]}</text>'
            )
    else:
        s.append(
            f'<text x="{L + pw / 2:.0f}" y="{TOP + ph / 2:.0f}" font-size="12" '
            f'text-anchor="middle" fill="{t["muted"]}">collecting &#8212; first data '
            f'lands after the next daily run</text>'
        )

    s.append("</svg>")
    out_path.write_text("\n".join(s) + "\n", encoding="utf-8")


def main():
    days = load()
    if "--render-only" not in sys.argv:
        if not TOKEN:
            sys.exit("No token. Set GH_TRAFFIC_TOKEN or GITHUB_TOKEN.")
        for entry in fetch_clones():
            d = entry["timestamp"][:10]
            # A later fetch is authoritative for a day it still covers.
            days[d] = {"count": entry["count"], "uniques": entry["uniques"]}
        days = save(days)

    rows = series(days)
    for name in THEMES:
        render(rows, name, DATA.parent / f"clones-{name}.svg")
    print(f"{len(days)} days recorded; charts written to {DATA.parent}")


if __name__ == "__main__":
    main()
