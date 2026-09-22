"""Detect the stack from public repositories and render its badge block.

Detection only ever adds. Every entry in stack.toml renders whether or not a
scan confirms it, because plenty of real experience leaves no trace in a
public repository -- Pydantic, SQL, Git and the whole "From the data years"
group are true and undetectable.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from .icons import Icon, Resolver, logo_color, slug

BADGE = "https://img.shields.io/badge/{label}-{color}?style=flat-square&logo={logo}&logoColor={logo_color}"


@dataclass(frozen=True)
class Tech:
    name: str
    group: str
    color: str
    logo: str
    logo_color: str
    alt: str = ""

    def label(self) -> str:
        """What a screen reader announces. Longer than the badge when the
        badge is abbreviated: the Azure badge reads "Azure" and says
        "Microsoft Azure"."""
        return self.alt or self.name

    def badge(self) -> str:
        return BADGE.format(
            label=escape(self.name),
            color=self.color,
            logo=self.logo,
            logo_color=self.logo_color,
        )


@dataclass
class Catalog:
    tech: list[Tech]
    aliases: dict[str, str]
    order: list[str]
    frozen: set[str]
    new_group: str
    language_threshold: float
    suffixes: list[str]

    def names(self) -> dict[str, str]:
        return {entry.name: entry.group for entry in self.tech}


@dataclass
class Report:
    added: list[tuple[str, str]]   # (technology, how it was found)
    unresolved: list[str]


def escape(label: str) -> str:
    """shields.io reads `-` as a separator and `_` as a space."""
    return label.replace("-", "--").replace("_", "__").replace(" ", "_")


def load_catalog(path: Path) -> Catalog:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    settings = data.get("settings", {})
    return Catalog(
        tech=[
            Tech(
                name=entry["name"],
                group=entry["group"],
                color=entry["color"],
                logo=entry["logo"],
                logo_color=entry.get("logo_color", "white"),
                alt=entry.get("alt", ""),
            )
            for entry in data.get("tech", [])
        ],
        aliases=data.get("aliases", {}),
        order=settings.get("order", []),
        frozen=set(settings.get("frozen", [])),
        new_group=settings.get("new_group", "Recently picked up"),
        language_threshold=settings.get("language_threshold", 0.05),
        suffixes=settings.get("suffixes", []),
    )


def resolver_for(catalog: Catalog, icons: dict[str, Icon]) -> Resolver:
    return Resolver(icons, catalog.names(), catalog.aliases, catalog.suffixes)


def detect(repos, catalog: Catalog, resolver: Resolver) -> tuple[dict[str, str], list[str]]:
    """Every technology the repositories can vouch for.

    Returns the resolved technologies mapped to how each was found, plus the
    terms that resolved to nothing. The second list is the report's job, not
    the README's: it is how a real tool with no brand icon gets noticed.
    """
    found: dict[str, str] = {}
    unresolved: list[str] = []

    for repo in repos:
        terms = list(repo.significant_languages(catalog.language_threshold))
        terms.extend(repo.topics)
        for term in terms:
            hit = resolver.resolve(term)
            if hit is None:
                if term not in unresolved:
                    unresolved.append(term)
            elif hit.name not in found:
                found[hit.name] = hit.via

    return found, sorted(unresolved)


def build(catalog: Catalog, found: dict[str, str], icons: dict[str, Icon]) -> tuple[dict[str, list[Tech]], Report]:
    """Lay the catalog out by group, then append what detection turned up."""
    groups: dict[str, list[Tech]] = {name: [] for name in catalog.order}
    for entry in catalog.tech:
        groups.setdefault(entry.group, []).append(entry)

    known = set(catalog.names())
    added: list[tuple[str, str]] = []

    for name in sorted(found):
        if name in known:
            continue
        icon = icons.get(slug(name))
        if icon is None:
            continue
        if catalog.new_group in catalog.frozen:
            raise ValueError(f"new_group {catalog.new_group!r} cannot also be frozen")
        groups.setdefault(catalog.new_group, []).append(
            Tech(
                name=icon.title,
                group=catalog.new_group,
                color=icon.hex,
                logo=icon.logo,
                logo_color=logo_color(icon.hex),
            )
        )
        added.append((icon.title, found[name]))

    return groups, Report(added=added, unresolved=[])


def render(catalog: Catalog, groups: dict[str, list[Tech]]) -> str:
    """The badge block, in the shape the README already uses."""
    names = catalog.order + [name for name in groups if name not in catalog.order]
    blocks: list[str] = []

    for name in names:
        entries = groups.get(name) or []
        if not entries:
            continue
        badges = "\n".join(
            f'  <img src="{entry.badge()}" alt="{entry.label()}">' for entry in entries
        )
        blocks.append(f"**{name}**\n\n<p>\n{badges}\n</p>")

    return "\n\n".join(blocks)
