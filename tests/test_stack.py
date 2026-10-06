"""Detection adds; it never removes, and it never edits a frozen group."""

from __future__ import annotations

import pytest

from conftest import make_repo
from profilegen import stack


def test_language_below_the_threshold_is_not_stack():
    """Alembic ships Mako templates. That does not make Mako a skill."""
    repo = make_repo(languages={"Python": 91677, "Mako": 668, "CSS": 3681})
    assert repo.significant_languages(0.05) == ["Python"]


def test_language_above_the_threshold_counts():
    repo = make_repo(languages={"Python": 440850, "TypeScript": 237574})
    assert set(repo.significant_languages(0.05)) == {"Python", "TypeScript"}


def test_a_repository_with_no_code_yields_no_languages():
    assert make_repo(languages={}).significant_languages(0.05) == []


def test_detection_reports_what_it_could_not_place(catalog, resolver):
    repo = make_repo(topics=("fastapi", "one-hot-encoding", "tfjs-node"))
    found, unresolved = stack.detect([repo], catalog, resolver)

    assert "FastAPI" in found
    assert unresolved == ["one-hot-encoding", "tfjs-node"]


def test_a_new_technology_lands_in_its_placed_group(catalog, resolver, icon_catalog):
    """HTML joins the frontend group the way Python sits in "AI and Python"."""
    repo = make_repo(topics=("vuejs",), languages={"JavaScript": 8000, "HTML": 2000})
    found, _ = stack.detect([repo], catalog, resolver)
    groups, report = stack.build(catalog, found, icon_catalog)

    frontend = [entry.name for entry in groups["Frontend, when the project needs one"]]
    assert frontend[-2:] == ["HTML5", "Vue.js"]
    assert not groups[catalog.new_group]
    assert [(name, group) for name, _, group in report.added] == [
        ("HTML5", "Frontend, when the project needs one"),
        ("Vue.js", "Frontend, when the project needs one"),
    ]


def test_a_placed_technology_gets_the_logo_shields_knows(catalog, resolver, icon_catalog):
    found, _ = stack.detect([make_repo(topics=("vuejs",))], catalog, resolver)
    groups, _ = stack.build(catalog, found, icon_catalog)
    rendered = stack.render(catalog, groups)
    assert "logo=vuedotjs" in rendered


def test_only_an_unplaced_technology_falls_through_to_the_inbox(catalog, resolver, icon_catalog):
    found, _ = stack.detect([make_repo(topics=("elm",))], catalog, resolver)
    groups, report = stack.build(catalog, found, icon_catalog)

    assert [entry.name for entry in groups[catalog.new_group]] == ["Elm"]
    assert report.added[0][2] == catalog.new_group


def test_what_used_to_be_recently_picked_up_has_a_real_group(catalog):
    """The four badges that sat in the inbox, now where they belong."""
    groups = catalog.names()
    assert groups["TensorFlow"] == "AI and Python"
    assert groups["Node.js"] == "Backend and data"
    assert groups["pandas"] == "Backend and data"
    assert groups["JavaScript"] == "Frontend, when the project needs one"


def test_the_inbox_renders_nothing_for_what_the_repositories_hold_today(catalog, resolver, icon_catalog):
    """Every language and topic of the current projects has a real group."""
    repos = [
        make_repo(languages={"Python": 21010, "JavaScript": 5295},
                  topics=("javascript", "nodejs", "pandas", "python", "tensorflowjs")),
        make_repo(languages={"JavaScript": 29745, "HTML": 4886, "CSS": 1235},
                  topics=("javascript", "tensorflowjs", "tfjs-vis", "web-worker")),
        make_repo(languages={"Python": 506464, "TypeScript": 237574},
                  topics=("agno", "anthropic", "claude", "nextjs", "python")),
    ]
    found, _ = stack.detect(repos, catalog, resolver)
    groups, _ = stack.build(catalog, found, icon_catalog)
    assert "Recently picked up" not in stack.render(catalog, groups)


def test_placement_cannot_reach_into_a_frozen_group(catalog, icon_catalog):
    catalog.placement["elm"] = "From the data years"
    with pytest.raises(ValueError, match="frozen"):
        stack.build(catalog, {}, icon_catalog)


def test_detection_never_removes_an_undetectable_entry(catalog, resolver, icon_catalog):
    """Pydantic, SQL and Git appear in no repository and are still true."""
    groups, _ = stack.build(catalog, {}, icon_catalog)
    rendered = stack.render(catalog, groups)

    for name in ["Pydantic", "SQL", "Git", "Databricks", "Power BI"]:
        assert f'alt="{name}"' in rendered


def test_a_frozen_group_cannot_receive_new_technology(catalog, icon_catalog):
    """Professional experience is not something a scan gets to edit."""
    catalog.new_group = "From the data years"
    with pytest.raises(ValueError, match="cannot also be frozen"):
        stack.build(catalog, {"TensorFlow": "exact"}, icon_catalog)


def test_an_empty_group_is_not_rendered(catalog, icon_catalog):
    groups, _ = stack.build(catalog, {}, icon_catalog)
    assert "Recently picked up" not in stack.render(catalog, groups)


def test_badge_label_escaping():
    """shields.io reads `-` as a separator and `_` as a space."""
    assert stack.escape("halcyon-goods-product-control") == "halcyon--goods--product--control"
    assert stack.escape("Power BI") == "Power_BI"
    assert stack.escape("Next.js") == "Next.js"


def test_alt_text_may_be_longer_than_the_badge(catalog, icon_catalog):
    groups, _ = stack.build(catalog, {}, icon_catalog)
    rendered = stack.render(catalog, groups)
    assert 'badge/Azure-0078D4' in rendered
    assert 'alt="Microsoft Azure"' in rendered
