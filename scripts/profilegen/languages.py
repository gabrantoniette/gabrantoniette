"""Every language in the public repositories, not just the main one.

The third-party cards this replaces counted one language per repository, the
primary one, so a project that is 20% JavaScript added nothing to
JavaScript. Here every language GitHub detects counts by its share of the
repository's bytes, which is what the repository's own Languages tab shows.

Colours come from GitHub's linguist, so Python is the same blue here as it
is on every repository page.
"""

from __future__ import annotations

import re
import urllib.request

LINGUIST_URL = "https://raw.githubusercontent.com/github-linguist/linguist/main/lib/linguist/languages.yml"
TIMEOUT = 45
FALLBACK_COLOR = "#8b949e"   # what GitHub paints a language linguist gives no colour
OTHER = "Other"

_NAME = re.compile(r"^([^\s#-][^:]*):\s*$")
_COLOR = re.compile(r'^  color:\s*"(#[0-9a-fA-F]{6})"')


def parse_colors(text: str) -> dict[str, str]:
    """Language name -> hex colour, read straight from linguist's YAML.

    Two line shapes are all it takes: a top-level `Name:` and an indented
    `color: "#rrggbb"` under it. Reading them by hand keeps the scripts on
    the standard library, which is the property they already had.
    """
    colors: dict[str, str] = {}
    current = None
    for line in text.splitlines():
        name = _NAME.match(line)
        if name:
            current = name.group(1).strip().strip('"')
            continue
        color = _COLOR.match(line)
        if color and current:
            colors[current] = color.group(1)
    return colors


def fetch_colors(url: str = LINGUIST_URL, timeout: int = TIMEOUT) -> dict[str, str]:
    """Raises on failure: a chart in the wrong colours is worse than no update."""
    request = urllib.request.Request(url, headers={"User-Agent": "profile-readme-updater"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        colors = parse_colors(response.read().decode("utf-8"))
    if not colors:
        raise RuntimeError("linguist returned no language colours")
    return colors


def color_of(language: str, colors: dict[str, str]) -> str:
    return colors.get(language, FALLBACK_COLOR)


def ranked(totals: dict[str, float]) -> list[tuple[str, float]]:
    """Largest share first, name as the tie-breaker so runs agree."""
    whole = sum(totals.values())
    if not whole:
        return []
    return sorted(((name, value / whole) for name, value in totals.items()), key=lambda item: (-item[1], item[0]))


def by_repo(repos) -> list[tuple[str, float]]:
    """Each repository counts once, split by its own language mix.

    Summing raw bytes instead would let the largest repository decide the
    chart on its own. Weighting every project the same answers the question
    the title asks: across my projects, what do I write?
    """
    totals: dict[str, float] = {}
    for repo in repos:
        for name, share in repo.language_shares().items():
            totals[name] = totals.get(name, 0.0) + share
    return ranked(totals)


def by_commit(repos) -> list[tuple[str, float]]:
    """Each repository weighs as many commits as its owner made there.

    A commit is attributed to the repository's languages in proportion to
    their bytes. Attributing it to the files it actually touched would cost
    one API call per commit; this costs one per repository and still counts
    every language, which the card it replaces did not.
    """
    totals: dict[str, float] = {}
    for repo in repos:
        for name, share in repo.language_shares().items():
            totals[name] = totals.get(name, 0.0) + share * repo.commits
    return ranked(totals)


def fold(shares: list[tuple[str, float]], limit: int) -> list[tuple[str, float]]:
    """Keep `limit` entries, folding the smallest into "Other" past that."""
    if len(shares) <= limit:
        return shares
    kept = shares[: limit - 1]
    return kept + [(OTHER, sum(share for _, share in shares[limit - 1 :]))]


def percent(share: float) -> str:
    """One decimal, like the Languages tab, without ever printing a 0.0%."""
    value = share * 100
    if 0 < value < 0.1:
        return "<0.1%"
    return f"{value:.1f}%"
