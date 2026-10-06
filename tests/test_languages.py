"""Every language counts, by its share, and no single repository decides the chart."""

from __future__ import annotations

import pytest

from conftest import make_repo
from profilegen import github, languages

LINGUIST = '''---
1C Enterprise:
  type: programming
  color: "#814CCC"
JavaScript:
  type: programming
  color: "#f1e05a"
  aliases:
  - js
Jinja:
  type: markup
  color: "#a52a22"
Text:
  type: prose
Python:
  type: programming
  color: "#3572A5"
  extensions:
  - ".py"
'''


def test_colours_are_read_from_linguist():
    colors = languages.parse_colors(LINGUIST)
    assert colors == {
        "1C Enterprise": "#814CCC",
        "JavaScript": "#f1e05a",
        "Jinja": "#a52a22",
        "Python": "#3572A5",
    }


def test_a_language_linguist_gives_no_colour_still_gets_one():
    assert languages.color_of("Text", languages.parse_colors(LINGUIST)) == languages.FALLBACK_COLOR


def test_shares_match_the_languages_tab():
    repo = make_repo(languages={"Python": 8000, "JavaScript": 2000})
    assert repo.language_shares() == {"Python": 0.8, "JavaScript": 0.2}


def test_by_repo_weighs_every_repository_the_same():
    """A huge Python repository must not drown a small JavaScript one."""
    big = make_repo(languages={"Python": 1_000_000})
    small = make_repo(languages={"JavaScript": 1_000})
    assert languages.by_repo([big, small]) == [("JavaScript", 0.5), ("Python", 0.5)]


def test_by_repo_keeps_the_minor_languages():
    """The old card counted one language per repository. These count in full."""
    repo = make_repo(languages={"Python": 80, "JavaScript": 15, "CSS": 5})
    names = [name for name, _ in languages.by_repo([repo])]
    assert names == ["Python", "JavaScript", "CSS"]


def test_by_commit_weighs_each_repository_by_its_commits():
    python = make_repo(languages={"Python": 100}, commits=30)
    javascript = make_repo(languages={"JavaScript": 100}, commits=10)
    shares = dict(languages.by_commit([python, javascript]))
    assert shares == {"Python": 0.75, "JavaScript": 0.25}


def test_by_commit_splits_a_commit_across_the_repository_languages():
    repo = make_repo(languages={"Python": 60, "TypeScript": 40}, commits=10)
    assert languages.by_commit([repo]) == [("Python", 0.6), ("TypeScript", 0.4)]


def test_empty_input_draws_nothing():
    assert languages.by_repo([make_repo(languages={})]) == []
    assert languages.by_commit([make_repo(languages={"Python": 1}, commits=0)]) == []


def test_fold_keeps_the_limit_and_sums_the_rest_into_other():
    shares = [(f"L{i}", 0.1) for i in range(10)]
    folded = languages.fold(shares, 8)
    assert len(folded) == 8
    assert folded[-1][0] == "Other"
    assert folded[-1][1] == pytest.approx(0.3)


def test_fold_leaves_a_short_list_alone():
    shares = [("Python", 0.7), ("JavaScript", 0.3)]
    assert languages.fold(shares, 8) == shares


def test_percent_reads_like_the_languages_tab():
    assert languages.percent(0.8) == "80.0%"
    assert languages.percent(0.0041) == "0.4%"
    assert languages.percent(0.0003) == "<0.1%"


def test_commit_count_comes_from_the_last_page_link():
    """One commit per page, so the number of the last page is the count."""
    link = (
        '<https://api.github.com/repositories/1/commits?author=x&per_page=1&page=2>; rel="next", '
        '<https://api.github.com/repositories/1/commits?author=x&per_page=1&page=187>; rel="last"'
    )
    assert github.count_from([{}], link) == 187


def test_commit_count_without_a_link_is_the_page_itself():
    assert github.count_from([{}], "") == 1
    assert github.count_from([], "") == 0
