"""Read the public repositories that count as recent work.

Ranking uses the last commit on the default branch, not `pushed_at`.
`pushed_at` moves for a push to any branch: halcyon-goods-product-control
reported 2026-09-01 from a side branch while its `main` had not moved since
2026-08-18. The default-branch date is also what the `last-commit` badge
renders, so the prose and the badge cannot disagree.
"""

from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass, field

API = "https://api.github.com"
TIMEOUT = 45


@dataclass(frozen=True)
class Repo:
    name: str
    url: str
    description: str
    topics: tuple[str, ...]
    default_branch: str
    last_commit: str
    languages: dict[str, int] = field(default_factory=dict)

    def significant_languages(self, threshold: float) -> list[str]:
        """Languages holding at least `threshold` of the repository's bytes.

        Below the line sit Alembic's Mako templates, the CSS a Next.js
        starter emits and the 491-byte JavaScript file that rides along with
        a Python project. None of those are stack.
        """
        total = sum(self.languages.values())
        if not total:
            return []
        return [name for name, count in self.languages.items() if count / total >= threshold]


def _get(path: str, token: str | None) -> object:
    headers = {
        "User-Agent": "profile-readme-updater",
        "Accept": "application/vnd.github+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"{API}{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8"))


def eligible(raw: dict, user: str) -> bool:
    """A repository a visitor can actually open and that is not this page.

    Excluding the profile repository is load-bearing, not tidiness: the
    workflow commits to it, which would otherwise hold it at first place
    forever.
    """
    return (
        not raw.get("private")
        and not raw.get("fork")
        and not raw.get("archived")
        and raw["name"].lower() != user.lower()
    )


def fetch_repos(user: str, token: str | None = None) -> list[Repo]:
    """Every eligible public repository, most recently committed to first."""
    token = token or os.environ.get("GITHUB_TOKEN") or None
    listing = _get(f"/users/{user}/repos?type=owner&per_page=100&sort=pushed", token)

    repos: list[Repo] = []
    for raw in listing:
        if not eligible(raw, user):
            continue
        name = raw["name"]
        branch = raw.get("default_branch") or "main"
        head = _get(f"/repos/{user}/{name}/commits/{branch}", token)
        repos.append(
            Repo(
                name=name,
                url=raw["html_url"],
                description=(raw.get("description") or "").strip(),
                topics=tuple(raw.get("topics") or ()),
                default_branch=branch,
                last_commit=head["commit"]["committer"]["date"],
                languages=_get(f"/repos/{user}/{name}/languages", token),
            )
        )

    return rank(repos)


def rank(repos: list[Repo]) -> list[Repo]:
    """Most recent commit first, name as the tie-breaker so runs agree."""
    return sorted(repos, key=lambda repo: (repo.last_commit, repo.name), reverse=True)
