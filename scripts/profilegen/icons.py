"""Resolve a language or a GitHub topic to a technology with a brand colour.

simple-icons doubles as the noise filter here. A topic is a free-text field,
so a repository mixes real tools with concepts: `fastapi` and `docker` sit
beside `one-hot-encoding`, `monorepo` and `portfolio`. No brand ships an icon
for a concept, so a term nobody has drawn a logo for is a term that does not
belong in a stack section.
"""

from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass

CATALOG_URL = "https://raw.githubusercontent.com/simple-icons/simple-icons/master/data/simple-icons.json"
TIMEOUT = 45


def slug(text: str) -> str:
    """Reduce a name to the form simple-icons uses to key its icons."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


@dataclass(frozen=True)
class Icon:
    title: str
    hex: str

    @property
    def logo(self) -> str:
        return slug(self.title)


@dataclass(frozen=True)
class Resolved:
    """A term that earned a badge.

    ``icon`` is None when the term matched an entry in stack.toml instead of
    simple-icons. Those entries carry their own colour and logo, which is how
    Agno, SQLModel and Alembic get a badge without a brand icon existing.
    """

    name: str
    icon: Icon | None
    via: str


def fetch_catalog(url: str = CATALOG_URL, timeout: int = TIMEOUT) -> dict[str, Icon]:
    """Download simple-icons and key it by slug.

    Raises on failure rather than returning an empty catalog: rendering the
    stack with no colours would be worse than leaving the README alone.
    """
    request = urllib.request.Request(url, headers={"User-Agent": "profile-readme-updater"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))

    icons = payload["icons"] if isinstance(payload, dict) else payload
    if not icons:
        raise RuntimeError("simple-icons returned an empty catalog")
    return {slug(icon["title"]): Icon(icon["title"], icon["hex"]) for icon in icons}


class Resolver:
    """Turn a raw term into a canonical technology name, or into nothing."""

    def __init__(
        self,
        catalog: dict[str, Icon],
        known: dict[str, str],
        aliases: dict[str, str],
        suffixes: list[str],
    ) -> None:
        self.catalog = catalog
        self.known = {slug(name): name for name in known}
        self.aliases = {slug(term): target for term, target in aliases.items()}
        self.suffixes = suffixes

    def resolve(self, term: str) -> Resolved | None:
        key = slug(term)

        target = self.aliases.get(key)
        if target:
            return Resolved(target, self.catalog.get(slug(target)), "alias")

        name = self.known.get(key)
        if name:
            return Resolved(name, self.catalog.get(key), "catalog")

        icon = self.catalog.get(key)
        if icon:
            return self._as_known(icon, "exact")

        for suffix in self.suffixes:
            if key.endswith(suffix) and len(key) > len(suffix):
                icon = self.catalog.get(key[: -len(suffix)])
                if icon:
                    return self._as_known(icon, f"suffix -{suffix}")

        head = re.split(r"[-_]", term, maxsplit=1)[0]
        if head != term:
            icon = self.catalog.get(slug(head))
            if icon:
                return self._as_known(icon, "prefix")

        return None

    def _as_known(self, icon: Icon, via: str) -> Resolved:
        """Prefer the catalog's own name when simple-icons resolves onto it."""
        return Resolved(self.known.get(slug(icon.title), icon.title), icon, via)


def logo_color(hex_color: str) -> str:
    """Pick the legible foreground for a badge background.

    Matches the two hand-made exceptions already in the README: React's cyan
    and Power BI's yellow carry black text, everything else carries white.
    """
    red, green, blue = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    brightness = (0.299 * red + 0.587 * green + 0.114 * blue) / 255
    return "black" if brightness > 0.65 else "white"
