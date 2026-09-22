"""Render the three most recent projects as cards.

The shape is the one the README already had by hand. What changes is where
the writing comes from: projects.toml when it exists, the repository's own
metadata when it does not. A project that nobody has written about yet still
gets a card, a description and a link -- it just gets a plainer one.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

REPO_BADGE = (
    "https://img.shields.io/badge/Repository-{label}-1F3864"
    "?style=flat-square&logo=github&logoColor=white"
)
TOP_LANGUAGE = "https://img.shields.io/github/languages/top/{user}/{name}?style=flat-square&color=4A7DBF"
LAST_COMMIT = "https://img.shields.io/github/last-commit/{user}/{name}?style=flat-square&color=4A7DBF"


def load_content(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def escape(label: str) -> str:
    """shields.io reads `-` as a separator and `_` as a space."""
    return label.replace("-", "--").replace("_", "__").replace(" ", "_")


def card(repo, user: str, entry: dict, chips: list[str]) -> str:
    title = entry.get("title") or repo.name
    headline = entry.get("headline", "")
    heading = f"#### [{title}]({repo.url})"
    if headline:
        heading += f": {headline}"

    badges = (
        "<p>\n"
        f'  <a href="{repo.url}">\n'
        f'    <img src="{REPO_BADGE.format(label=escape(repo.name))}" alt="{repo.name} repository">\n'
        "  </a>\n"
        f'  <img src="{TOP_LANGUAGE.format(user=user, name=repo.name)}" alt="Primary language of the project">\n'
        f'  <img src="{LAST_COMMIT.format(user=user, name=repo.name)}" alt="Date of the last commit">\n'
        "</p>"
    )

    parts = [heading, badges]

    body = (entry.get("body") or repo.description or "").strip()
    if body:
        parts.append(body)

    decisions = entry.get("decisions") or []
    if decisions:
        items = "\n".join(f"- {line}" for line in decisions)
        parts.append(
            "<details>\n"
            "<summary><b>Decisions worth the click</b></summary>\n\n"
            "<br>\n\n"
            f"{items}\n\n"
            "</details>"
        )

    if chips:
        rendered = " ".join(f"<code>{chip}</code>" for chip in chips)
        parts.append(f"<p>\n  {rendered}\n</p>")

    return "\n\n".join(parts)


def chips_for(repo, entry: dict, resolve) -> list[str]:
    """Curated chips when they exist, otherwise whatever the topics prove."""
    curated = entry.get("chips")
    if curated:
        return list(curated)

    found: list[str] = []
    for term in repo.topics:
        hit = resolve(term)
        if hit and hit.name not in found:
            found.append(hit.name)
    return found


def render(repos, user: str, content: dict, resolve) -> str:
    cards = [
        card(repo, user, content.get(repo.name, {}), chips_for(repo, content.get(repo.name, {}), resolve))
        for repo in repos
    ]
    return "\n\n<br>\n\n".join(cards)
