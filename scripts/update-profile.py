#!/usr/bin/env python3
"""Regenerate everything on the profile that comes from the repositories.

Usage:
    python scripts/update-profile.py            # dry run, prints the report
    python scripts/update-profile.py --write    # apply it

What it owns:
  * two marker-anchored blocks of README.md: the three most recently
    worked-on public projects, and the stack detected from them
  * assets/generated/: the two language donuts in "GitHub at a glance", and
    one language bar per public repository, which that repository's own
    README embeds

It writes only what changed. The README blocks move when a different
project joins the three or a new technology shows up; the charts move when
a repository's languages or commit count does. When nothing moved, it
writes nothing, and the workflow has nothing to commit.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from profilegen import charts, embeds, github, icons, languages, projects, readme, stack  # noqa: E402

USER = "gabrantoniette"
TOP_N = 3
CHART_LIMIT = 8   # legend rows a 340x200 card holds; past that, "Other"

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CONTENT = ROOT / "content"
BARS = ROOT / embeds.GENERATED / "languages"


def assets_for(repos, colors: dict[str, str]) -> dict[Path, str]:
    """Every generated file, keyed by where it goes."""
    files: dict[Path, str] = {}
    charts_by = {
        "repo": ("Top Languages by Repo", languages.by_repo(repos)),
        "commit": ("Top Languages by Commit", languages.by_commit(repos)),
    }
    for theme in charts.CARD_THEMES:
        for kind, (title, shares) in charts_by.items():
            files[ROOT / embeds.chart_path(kind, theme)] = charts.donut_card(
                title, languages.fold(shares, CHART_LIMIT), colors, theme
            )
        for repo in repos:
            if repo.languages:
                files[ROOT / embeds.bar_path(repo.name, theme)] = charts.language_bar(
                    repo.name, languages.ranked(repo.languages), colors, theme
                )
    return files


def stale_bars(files: dict[Path, str]) -> list[Path]:
    """Bars for repositories that went private, were archived or deleted."""
    if not BARS.exists():
        return []
    return sorted(path for path in BARS.glob("*.svg") if path not in files)


def differs(path: Path, text: str) -> bool:
    return not path.exists() or path.read_text(encoding="utf-8") != text


def report_for(entered, left, added, unresolved, redrawn, missing) -> str:
    lines: list[str] = []

    if missing:
        lines.append(missing_report(missing))
        lines.append("")

    if entered or left:
        lines.append("**Projects**")
        for name in entered:
            lines.append(f"- `{name}` entered the three most recent")
        for name in left:
            lines.append(f"- `{name}` dropped out")
        lines.append("")

    if added:
        lines.append("**New in the stack**")
        for name, via, group in added:
            lines.append(f"- `{name}` — matched by {via}, filed under *{group}*")
        lines.append("")

    if redrawn:
        lines.append("**Redrawn**")
        lines.extend(f"- `{name}`" for name in redrawn)
        lines.append("")

    if unresolved:
        lines.append("<details>")
        lines.append("<summary>Terms that matched no brand icon, and were skipped</summary>")
        lines.append("")
        lines.append(", ".join(f"`{term}`" for term in unresolved))
        lines.append("")
        lines.append(
            "Most are concepts rather than tools. If one is a real tool you want shown, "
            "add it to `content/stack.toml` with a colour and a logo."
        )
        lines.append("")
        lines.append("</details>")
        lines.append("")

    return "\n".join(lines).strip() or "Nothing moved."


def missing_report(names: list[str]) -> str:
    """Ask for the bar in each project README that lacks it, snippet included.

    A project that just went public always lands here, because its bar is
    drawn for the first time in the same run, so the pull request that
    announces it also carries what to paste.
    """
    lines = [
        "**READMEs without a language bar**",
        "",
        "The bar is already drawn and kept current here; each README only needs to "
        "point at it, once. Paste under the title:",
        "",
    ]
    for name in names:
        lines += [
            "<details>",
            f'<summary><a href="https://github.com/{USER}/{name}">{name}</a></summary>',
            "",
            "```html",
            embeds.language_bar(name, USER, absolute=True),
            "```",
            "",
            "</details>",
        ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="apply the changes")
    parser.add_argument("--report", type=Path, help="also write the report to this file")
    args = parser.parse_args()

    catalog = stack.load_catalog(CONTENT / "stack.toml")
    content = projects.load_content(CONTENT / "projects.toml")
    icon_catalog = icons.fetch_catalog()
    colors = languages.fetch_colors()
    resolver = stack.resolver_for(catalog, icon_catalog)

    repos = github.fetch_repos(USER)
    if len(repos) < TOP_N:
        print(f"only {len(repos)} eligible repositories, need {TOP_N}", file=sys.stderr)
        return 1

    text = README.read_text(encoding="utf-8")
    current = readme.repos_in(readme.block(text, "projects"))
    desired = [repo.name for repo in repos[:TOP_N]]
    order = readme.preserve_order(desired, current)

    by_name = {repo.name: repo for repo in repos}
    ordered = [by_name[name] for name in order if name in by_name]

    found, unresolved = stack.detect(repos, catalog, resolver)
    groups, stack_report = stack.build(catalog, found, icon_catalog)

    updated = readme.replace(text, "projects", projects.render(ordered, USER, content, resolver.resolve))
    updated = readme.replace(updated, "stack", stack.render(catalog, groups))

    files = assets_for(repos, colors)
    redrawn = [path for path, svg in files.items() if differs(path, svg)]
    stale = stale_bars(files)
    changed = updated != text or bool(redrawn) or bool(stale)

    missing = [repo.name for repo in repos if not embeds.has_language_bar(github.fetch_readme(USER, repo.name), repo.name)]

    report = report_for(
        entered=[name for name in desired if name not in current],
        left=[name for name in current if name not in desired],
        added=stack_report.added,
        unresolved=unresolved,
        redrawn=[path.relative_to(ROOT).as_posix() for path in redrawn + stale],
        missing=missing,
    )

    print(f"projects: {', '.join(order)}")
    print(f"stack: {len(found)} detected, {len(stack_report.added)} new")
    print(f"languages by repo: {', '.join(f'{n} {languages.percent(s)}' for n, s in languages.by_repo(repos))}")
    print(f"languages by commit: {', '.join(f'{n} {languages.percent(s)}' for n, s in languages.by_commit(repos))}")
    print(f"readmes without a language bar: {', '.join(missing) or 'none'}")
    print(f"changed: {changed}")
    print()
    print(report)

    if args.report:
        args.report.write_text(report + "\n", encoding="utf-8", newline="\n")

    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"changed={'true' if changed else 'false'}\n")

    if changed and args.write:
        if updated != text:
            README.write_text(updated, encoding="utf-8", newline="\n")
        for path in redrawn:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(files[path], encoding="utf-8", newline="\n")
        for path in stale:
            path.unlink()
        print(f"\nwritten: README {'updated' if updated != text else 'unchanged'}, "
              f"{len(redrawn)} charts drawn, {len(stale)} removed")

    return 0


if __name__ == "__main__":
    sys.exit(main())
