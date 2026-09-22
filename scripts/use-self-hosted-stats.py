#!/usr/bin/env python3
"""Point the README stats cards at your own github-readme-stats instance.

Usage:
    python scripts/use-self-hosted-stats.py github-readme-stats-yourname.vercel.app

Swaps whatever sits between the <!-- cards:start --> / <!-- cards:end -->
markers. Writes README.bak.md first.

It used to rewrite a pinned-repository card as well. That card is now part
of the generated projects block, which scripts/update-profile.py owns, so
this script stays out of it.

Deploy walkthrough: docs/self-host-stats.md
"""

from __future__ import annotations

import io
import re
import shutil
import sys
from pathlib import Path

USER = "gabrantoniette"

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
BACKUP = ROOT / "README.bak.md"

# Profile palette.
DARK = {
    "bg_color": "00000000",
    "title_color": "4A7DBF",
    "text_color": "E6EDF3",
    "icon_color": "4A7DBF",
    "border_color": "30363D",
}
LIGHT = {
    "bg_color": "00000000",
    "title_color": "1F3864",
    "text_color": "12233F",
    "icon_color": "1F3864",
    "border_color": "D0D7DE",
}


def card(host: str, path: str, params: dict[str, str], theme: dict[str, str]) -> str:
    query = {**params, **theme, "hide_border": "true"}
    return f"https://{host}{path}?" + "&".join(f"{k}={v}" for k, v in query.items())


def picture(host: str, path: str, params: dict[str, str], alt: str, height: str = "165") -> str:
    dark = card(host, path, params, DARK)
    light = card(host, path, params, LIGHT)
    return (
        "  <picture>\n"
        f'    <source media="(prefers-color-scheme: dark)" srcset="{dark}">\n'
        f'    <source media="(prefers-color-scheme: light)" srcset="{light}">\n'
        f'    <img height="{height}" src="{light}" alt="{alt}">\n'
        "  </picture>"
    )


def build_cards(host: str) -> str:
    stats = picture(
        host,
        "/api",
        {
            "username": USER,
            "show_icons": "true",
            "count_private": "true",
            "include_all_commits": "true",
        },
        f"GitHub stats summary for {USER}",
    )
    langs = picture(
        host,
        "/api/top-langs/",
        {"username": USER, "layout": "compact", "langs_count": "8"},
        f"Most used languages by {USER}",
    )
    return '<p align="center">\n' + stats + "\n" + langs + "\n</p>"


def replace_block(text: str, name: str, new_body: str) -> str:
    pattern = re.compile(
        rf"(<!-- {name}:start -->\n).*?(\n<!-- {name}:end -->)",
        re.DOTALL,
    )
    if not pattern.search(text):
        sys.exit(f"error: markers <!-- {name}:start --> / <!-- {name}:end --> not found in README.md")
    return pattern.sub(lambda m: m.group(1) + new_body + m.group(2), text)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)

    host = sys.argv[1].strip().rstrip("/")
    host = re.sub(r"^https?://", "", host)
    if not re.fullmatch(r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}", host):
        sys.exit(f"error: '{host}' doesn't look like a domain. Example: github-readme-stats-yourname.vercel.app")

    text = io.open(README, encoding="utf-8").read()
    text = replace_block(text, "cards", build_cards(host))

    shutil.copyfile(README, BACKUP)
    io.open(README, "w", encoding="utf-8", newline="\n").write(text)

    print(f"README.md now points at https://{host}")
    print(f"backup written to {BACKUP.name}")
    print("verify with: python scripts/check-readme-links.py")


if __name__ == "__main__":
    main()
