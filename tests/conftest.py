"""Fixtures for the profile generator tests.

Everything here is local. The tests never reach the network and never need a
token, because every renderer takes plain data and returns a string.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from profilegen import github, icons, stack  # noqa: E402

CATALOG = ROOT / "content" / "stack.toml"


@pytest.fixture
def icon_catalog() -> dict[str, icons.Icon]:
    """A slice of simple-icons, big enough to exercise every resolution rule."""
    return {
        icons.slug(title): icons.Icon(title, hex_color)
        for title, hex_color in [
            ("Python", "3776AB"),
            ("JavaScript", "F7DF1E"),
            ("TypeScript", "3178C6"),
            ("TensorFlow", "FF6F00"),
            ("Docker", "2496ED"),
            ("FastAPI", "009688"),
            ("Node.js", "5FA04E"),
            ("React", "61DAFB"),
            ("Anthropic", "191919"),
            ("Claude", "D97757"),
        ]
    }


@pytest.fixture
def catalog() -> stack.Catalog:
    """The real catalog, so the tests fail when it drifts."""
    return stack.load_catalog(CATALOG)


@pytest.fixture
def resolver(catalog, icon_catalog) -> icons.Resolver:
    return stack.resolver_for(catalog, icon_catalog)


def make_repo(
    name: str = "demo",
    description: str = "",
    topics: tuple[str, ...] = (),
    languages: dict[str, int] | None = None,
    last_commit: str = "2026-09-22T00:00:00Z",
) -> github.Repo:
    return github.Repo(
        name=name,
        url=f"https://github.com/gabrantoniette/{name}",
        description=description,
        topics=topics,
        default_branch="main",
        last_commit=last_commit,
        languages=languages or {},
    )
