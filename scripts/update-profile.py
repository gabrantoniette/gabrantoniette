#!/usr/bin/env python3
"""Regenerate the automated sections of the profile README.

Usage:
    python scripts/update-profile.py            # dry run, prints the report
    python scripts/update-profile.py --write    # apply it

Rewrites two marker-anchored blocks and nothing else: the three most recently
worked-on public projects, and the stack detected from those repositories.

It stays silent on purpose. When the cast of three and the set of
technologies are both unchanged, it writes nothing, so an ordinary commit to
an ordinary project never produces a commit here. The dates on the page do
not need one: they come from live badges.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from profilegen import github, icons, projects, readme, stack  # noqa: E402

USER = "gabrantoniette"
TOP_N = 3

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CONTENT = ROOT / "content"


def report_for(entered, left, added, unresolved) -> str:
    lines: list[str] = []

    if entered or left:
        lines.append("**Projects**")
        for name in entered:
            lines.append(f"- `{name}` entered the three most recent")
        for name in left:
            lines.append(f"- `{name}` dropped out")
        lines.append("")

    if added:
        lines.append("**New in the stack**")
        for name, via in added:
            lines.append(f"- `{name}` — matched by {via}, filed under *Recently picked up*")
        lines.append("")
        lines.append("Move any of these into a real group by editing its `group` in `content/stack.toml`.")
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="apply the changes to README.md")
    parser.add_argument("--report", type=Path, help="also write the report to this file")
    args = parser.parse_args()

    catalog = stack.load_catalog(CONTENT / "stack.toml")
    content = projects.load_content(CONTENT / "projects.toml")
    icon_catalog = icons.fetch_catalog()
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
    changed = updated != text

    report = report_for(
        entered=[name for name in desired if name not in current],
        left=[name for name in current if name not in desired],
        added=stack_report.added,
        unresolved=unresolved,
    )

    print(f"projects: {', '.join(order)}")
    print(f"stack: {len(found)} detected, {len(stack_report.added)} new")
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
        README.write_text(updated, encoding="utf-8", newline="\n")
        print("\nREADME.md written")

    return 0


if __name__ == "__main__":
    sys.exit(main())
