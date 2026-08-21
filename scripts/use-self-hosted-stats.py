#!/usr/bin/env python3
"""Aponta os cartoes de estatisticas do README para uma instancia propria
do github-readme-stats.

Uso:
    python scripts/use-self-hosted-stats.py github-readme-stats-seunome.vercel.app

Troca o conteudo entre os marcadores <!-- cards:start --> / <!-- cards:end -->
e <!-- pin:start --> / <!-- pin:end -->. Salva README.bak.md antes de escrever.

Passo a passo do deploy: docs/self-host-stats.md
"""

from __future__ import annotations

import io
import re
import shutil
import sys
from pathlib import Path

USER = "gabrantoniette"
PIN_REPO = "halcyon-goods-product-control"

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
BACKUP = ROOT / "README.bak.md"

# Identidade visual do perfil.
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


def build_stats(host: str) -> str:
    stats = picture(
        host,
        "/api",
        {
            "username": USER,
            "show_icons": "true",
            "count_private": "true",
            "include_all_commits": "true",
        },
        "Resumo de estatisticas do GitHub de " + USER,
    )
    langs = picture(
        host,
        "/api/top-langs/",
        {"username": USER, "layout": "compact", "langs_count": "8"},
        "Linguagens mais usadas por " + USER,
    )
    return '<p align="center">\n' + stats + "\n" + langs + "\n</p>"


def build_pin(host: str) -> str:
    pin = picture(
        host,
        "/api/pin/",
        {"username": USER, "repo": PIN_REPO},
        f"Cartao do repositorio {PIN_REPO}",
        height="",
    ).replace(' height=""', "")
    return (
        "<p>\n"
        f'  <a href="https://github.com/{USER}/{PIN_REPO}">\n'
        + "\n".join("  " + line for line in pin.splitlines())
        + "\n  </a>\n</p>"
    )


def replace_block(text: str, name: str, new_body: str) -> str:
    pattern = re.compile(
        rf"(<!-- {name}:start -->\n).*?(\n<!-- {name}:end -->)",
        re.DOTALL,
    )
    if not pattern.search(text):
        sys.exit(f"erro: marcadores <!-- {name}:start --> / <!-- {name}:end --> nao encontrados em README.md")
    return pattern.sub(lambda m: m.group(1) + new_body + m.group(2), text)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)

    host = sys.argv[1].strip().rstrip("/")
    host = re.sub(r"^https?://", "", host)
    if not re.fullmatch(r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}", host):
        sys.exit(f"erro: '{host}' nao parece um dominio. Exemplo: github-readme-stats-seunome.vercel.app")

    text = io.open(README, encoding="utf-8").read()
    text = replace_block(text, "cards", build_stats(host))
    text = replace_block(text, "pin", build_pin(host))

    shutil.copyfile(README, BACKUP)
    io.open(README, "w", encoding="utf-8", newline="\n").write(text)

    print(f"README.md aponta agora para https://{host}")
    print(f"backup em {BACKUP.name}")
    print("confira com: python scripts/check-readme-links.py")


if __name__ == "__main__":
    main()
