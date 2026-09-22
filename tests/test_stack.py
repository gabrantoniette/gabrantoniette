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


def test_new_technology_lands_in_the_entry_group(catalog, resolver, icon_catalog):
    repo = make_repo(topics=("tensorflowjs",), languages={"JavaScript": 1476})
    found, _ = stack.detect([repo], catalog, resolver)
    groups, report = stack.build(catalog, found, icon_catalog)

    placed = [entry.name for entry in groups[catalog.new_group]]
    assert placed == ["JavaScript", "TensorFlow"]
    assert [name for name, _ in report.added] == ["JavaScript", "TensorFlow"]


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
