#!/usr/bin/env python3
"""Check that every image in the README still responds.

Usage:
    python scripts/check-readme-links.py

Exits 1 if any image is down. Free stats-card services disappear without
warning and the README breaks silently when they do -- this check exists so
you don't find out from someone else's screenshot.

It catches three shapes of failure:
  * an HTTP status other than 200
  * an error SVG served with status 200 (what github-readme-stats returns
    when the token is missing: "Something went wrong" / "Maximum retries
    exceeded")
  * a local path referenced by the README that isn't in the repository
"""

from __future__ import annotations

import io
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
TIMEOUT = 45
RETRIES = 3  # shared instances throw the occasional 503 under load

ERROR_MARKERS = (
    "something went wrong",
    "maximum retries exceeded",
    "user not found",
    "deployment_paused",
    "could not fetch",
)


def sources(text: str) -> list[str]:
    found = re.findall(r'(?:src|srcset)="([^"]+)"', text)
    seen: dict[str, None] = {}
    for url in found:
        seen.setdefault(url, None)
    return list(seen)


def check_remote(url: str) -> str | None:
    """Return None when healthy, or a description of the problem."""
    last = "no response"
    for _ in range(RETRIES):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "readme-link-check"})
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                body = response.read(20000).decode("utf-8", "replace").lower()
                for marker in ERROR_MARKERS:
                    if marker in body:
                        return f"status 200 but the SVG reads: {marker!r}"
                return None
        except urllib.error.HTTPError as exc:
            last = f"HTTP {exc.code}"
        except Exception as exc:  # timeout, DNS, TLS
            last = f"{type(exc).__name__}: {exc}"
    return f"{last} (after {RETRIES} attempts)"


def main() -> int:
    text = io.open(README, encoding="utf-8").read()
    urls = sources(text)
    if not urls:
        print("no images found in the README")
        return 1

    failures: list[tuple[str, str]] = []
    print(f"checking {len(urls)} images from the README\n")

    for url in urls:
        if url.startswith("http"):
            problem = check_remote(url)
        else:
            local = ROOT / url
            problem = None if local.exists() else "local file not found"

        label = url if len(url) <= 88 else url[:85] + "..."
        if problem:
            failures.append((url, problem))
            print(f"  FAIL  {label}\n        -> {problem}")
        else:
            print(f"  ok    {label}")

    print()
    if failures:
        print(f"{len(failures)} of {len(urls)} images are broken.")
        print("To host your own cards: docs/self-host-stats.md")
        return 1

    print(f"all {len(urls)} images responded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
