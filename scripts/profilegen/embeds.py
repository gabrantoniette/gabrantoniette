"""Where the generated charts live, and the HTML that shows them.

The profile README points at them by relative path. A project's own README
cannot, so it points at the raw file on this repository's `main`. Either
way the HTML never changes: the workflow redraws the file behind it, so a
project's README shows its current languages without anyone committing to
that project.
"""

from __future__ import annotations

GENERATED = "assets/generated"
RAW = "https://raw.githubusercontent.com/{user}/{user}/main/{path}"


def bar_path(name: str, theme: str) -> str:
    return f"{GENERATED}/languages/{name}-{theme}.svg"


def chart_path(kind: str, theme: str) -> str:
    return f"{GENERATED}/languages-by-{kind}-{theme}.svg"


def picture(light: str, dark: str, alt: str, indent: str = "") -> str:
    return (
        f"{indent}<picture>\n"
        f'{indent}  <source media="(prefers-color-scheme: dark)" srcset="{dark}">\n'
        f'{indent}  <img src="{light}" alt="{alt}">\n'
        f"{indent}</picture>"
    )


def language_bar(name: str, user: str, absolute: bool, indent: str = "") -> str:
    """The language bar for one repository.

    `absolute` is for the project's own README, which lives in another
    repository and needs the full raw URL.
    """
    def where(theme: str) -> str:
        path = bar_path(name, theme)
        return RAW.format(user=user, path=path) if absolute else path

    return picture(where("light"), where("dark"), f"Languages in {name}, by share of code", indent)


def has_language_bar(readme: str, name: str) -> bool:
    """Whether a project's README already embeds its own bar, in either form.

    The whole file name is matched, so `demo-two`'s bar does not count as
    `demo`'s.
    """
    return any(bar_path(name, theme) in readme for theme in ("light", "dark"))
