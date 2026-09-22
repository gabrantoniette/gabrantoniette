"""Marker-anchored replacement, and the rule that keeps the README quiet.

Everything outside the markers is hand-written and never touched.
"""

from __future__ import annotations

import re

HEADING = re.compile(r"^#### \[[^\]]*\]\(https://github\.com/[^/)]+/([^/)]+)\)", re.MULTILINE)


def _pattern(name: str) -> re.Pattern[str]:
    return re.compile(
        rf"(<!-- {name}:start -->\n).*?(\n<!-- {name}:end -->)",
        re.DOTALL,
    )


def block(text: str, name: str) -> str:
    """What currently sits between the markers."""
    found = _pattern(name).search(text)
    if not found:
        raise ValueError(f"markers <!-- {name}:start --> / <!-- {name}:end --> not found")
    return found.group(0)[len(found.group(1)) : -len(found.group(2))]


def replace(text: str, name: str, body: str) -> str:
    pattern = _pattern(name)
    if not pattern.search(text):
        raise ValueError(f"markers <!-- {name}:start --> / <!-- {name}:end --> not found")
    return pattern.sub(lambda m: m.group(1) + body + m.group(2), text)


def repos_in(text: str) -> list[str]:
    """The repositories the projects block links to, in the order shown."""
    return HEADING.findall(text)


def preserve_order(desired: list[str], current: list[str]) -> list[str]:
    """Keep the order on the page while the cast is unchanged.

    This is what stops the section behaving like a feed. Committing to an
    existing project reshuffles nothing, because the order only gets
    recomputed at the moment a different project joins the three. The dates
    on the page stay honest regardless: they come from live badges, which
    refresh without anyone committing anything.
    """
    if set(desired) == set(current):
        return current
    return desired
