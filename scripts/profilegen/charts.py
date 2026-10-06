"""Draw the language charts as plain SVG, one file per theme.

Two shapes. The donut card sits in "GitHub at a glance" between cards from
github-profile-summary-cards, so it copies their frame: 340 by 200, the same
border, title and font, light and github_dark colours. The language bar
copies the Languages tab on a repository page, and goes in each project's
own README and in its card on the profile.

Coordinates are rounded to two places so an unchanged repository draws a
byte-identical file, and the workflow has nothing to commit.
"""

from __future__ import annotations

import math
from html import escape

from .languages import color_of, percent

FONT_CARD = "'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif"
FONT_BAR = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"

CARD_THEMES = {
    "light": {"bg": "#ffffff", "border": "#e4e2e2", "title": "#586e75", "text": "#586e75"},
    "dark": {"bg": "#0d1117", "border": "#2e343b", "title": "#0366d6", "text": "#77909c"},
}
BAR_THEMES = {
    "light": {"text": "#1f2328", "muted": "#59636e"},
    "dark": {"text": "#f0f6fc", "muted": "#9198a1"},
}

CARD_W, CARD_H = 340, 200
CENTER = (255, 120)
OUTER, INNER = 58, 34
LEGEND_X, LEGEND_TOP, LEGEND_ROOM = 30, 54, 140

BAR_W, BAR_H, GAP = 800, 8, 2
ITEM_GAP, ROW_H = 20, 24


def _point(radius: float, angle: float) -> str:
    x = CENTER[0] + radius * math.cos(angle)
    y = CENTER[1] + radius * math.sin(angle)
    return f"{x:.2f},{y:.2f}"


def _slice(start: float, end: float) -> str:
    """One ring segment, clockwise from `start` to `end` (radians)."""
    large = 1 if end - start > math.pi else 0
    return (
        f"M{_point(OUTER, start)}"
        f"A{OUTER},{OUTER},0,{large},1,{_point(OUTER, end)}"
        f"L{_point(INNER, end)}"
        f"A{INNER},{INNER},0,{large},0,{_point(INNER, start)}Z"
    )


def _summary(title: str, shares: list[tuple[str, float]]) -> str:
    return escape(f"{title}: " + ", ".join(f"{name} {percent(share)}" for name, share in shares))


def donut_card(title: str, shares: list[tuple[str, float]], colors: dict[str, str], theme: str) -> str:
    """A donut of every language, with a legend that names each one and its share.

    The legend carries the percentages so a sliver too thin to see still
    says what it is. Slices are separated by a 2px ring in the card's own
    background, never by an outline.
    """
    palette = CARD_THEMES[theme]
    many = len(shares) > 5
    size, swatch = (13, 11) if many else (14, 14)
    step = min(25.2, LEGEND_ROOM / max(len(shares), 1)) if many else 25.2

    legend = []
    for index, (name, share) in enumerate(shares):
        top = LEGEND_TOP + index * step
        legend.append(
            f'<rect x="{LEGEND_X}" y="{top:.2f}" width="{swatch}" height="{swatch}" '
            f'fill="{color_of(name, colors)}"/>'
            f'<text x="{LEGEND_X + swatch + 6}" y="{top + swatch - 2:.2f}" '
            f'style="font-size: {size}px; fill: {palette["text"]};">'
            f"{escape(name)} {escape(percent(share))}</text>"
        )

    if len(shares) == 1:
        middle = (OUTER + INNER) / 2
        ring = [
            f'<circle cx="{CENTER[0]}" cy="{CENTER[1]}" r="{middle}" fill="none" '
            f'stroke="{color_of(shares[0][0], colors)}" stroke-width="{OUTER - INNER}"/>'
        ]
    else:
        ring = []
        angle = -math.pi / 2
        for name, share in shares:
            end = angle + share * 2 * math.pi
            ring.append(
                f'<path d="{_slice(angle, end)}" fill="{color_of(name, colors)}" '
                f'stroke="{palette["bg"]}" stroke-width="2"/>'
            )
            angle = end

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" '
        f'viewBox="0 0 {CARD_W} {CARD_H}" role="img" aria-labelledby="title">'
        f'<title id="title">{_summary(title, shares)}</title>'
        f"<style>* {{ font-family: {FONT_CARD}; }}</style>"
        f'<rect x="1" y="1" rx="5" ry="5" width="{CARD_W - 2}" height="{CARD_H - 2}" '
        f'stroke="{palette["border"]}" stroke-width="1" fill="{palette["bg"]}"/>'
        f'<text x="30" y="40" style="font-size: 22px; fill: {palette["title"]};">{escape(title)}</text>'
        + "".join(legend)
        + "".join(ring)
        + "</svg>\n"
    )


def _item_width(name: str, share: float) -> float:
    """A slightly generous guess at a legend item's width, measured against
    14px Segoe UI. Guessing wide only adds air; ITEM_GAP absorbs a font
    that runs a little wider than this one."""
    return 14 + len(name) * 7.6 + 6 + len(percent(share)) * 7.8


def language_bar(repo_name: str, shares: list[tuple[str, float]], colors: dict[str, str], theme: str) -> str:
    """The Languages tab of a repository page, drawn to sit in its README.

    The background is transparent, so the 2px gaps between segments show the
    page itself, whichever theme the reader uses.
    """
    palette = BAR_THEMES[theme]

    usable = BAR_W - GAP * max(len(shares) - 1, 0)
    segments, x = [], 0.0
    for name, share in shares:
        width = max(share * usable, 1.0)
        segments.append(
            f'<rect x="{x:.2f}" y="0" width="{width:.2f}" height="{BAR_H}" fill="{color_of(name, colors)}"/>'
        )
        x += width + GAP

    items, x, row = [], 0.0, 0
    for name, share in shares:
        width = _item_width(name, share)
        if x and x + width > BAR_W:
            x, row = 0.0, row + 1
        y = BAR_H + 26 + row * ROW_H
        items.append(
            f'<circle cx="{x + 4:.2f}" cy="{y - 5}" r="4" fill="{color_of(name, colors)}"/>'
            f'<text x="{x + 14:.2f}" y="{y}" style="font-size: 14px;">'
            f'<tspan style="font-weight: 600; fill: {palette["text"]};">{escape(name)}</tspan>'
            f'<tspan dx="6" style="fill: {palette["muted"]};">{escape(percent(share))}</tspan></text>'
        )
        x += width + ITEM_GAP

    height = BAR_H + 26 + row * ROW_H + 8
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{BAR_W}" height="{height}" '
        f'viewBox="0 0 {BAR_W} {height}" role="img" aria-labelledby="title">'
        f'<title id="title">{_summary(f"Languages in {repo_name}", shares)}</title>'
        f"<style>* {{ font-family: {FONT_BAR}; }}</style>"
        f'<clipPath id="bar"><rect width="{BAR_W}" height="{BAR_H}" rx="{BAR_H / 2:g}"/></clipPath>'
        f'<g clip-path="url(#bar)">{"".join(segments)}</g>'
        + "".join(items)
        + "</svg>\n"
    )
