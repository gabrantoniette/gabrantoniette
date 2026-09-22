"""The rule that keeps the README from behaving like a feed."""

from __future__ import annotations

import pytest

from profilegen import readme

PAGE = """# Title

Hand-written, and not for a robot to touch.

<!-- projects:start -->
#### [Alpha](https://github.com/gabrantoniette/alpha): first

#### [Beta](https://github.com/gabrantoniette/beta): second
<!-- projects:end -->

Also hand-written.
"""


def test_block_reads_only_between_the_markers():
    body = readme.block(PAGE, "projects")
    assert "Alpha" in body
    assert "Hand-written" not in body


def test_replace_leaves_everything_else_alone():
    updated = readme.replace(PAGE, "projects", "REPLACED")
    assert "REPLACED" in updated
    assert "Hand-written, and not for a robot to touch." in updated
    assert "Also hand-written." in updated
    assert "Alpha" not in updated


def test_missing_markers_are_an_error_not_a_silent_no_op():
    with pytest.raises(ValueError, match="markers"):
        readme.replace("nothing here", "projects", "x")


def test_repos_are_read_in_the_order_shown():
    assert readme.repos_in(PAGE) == ["alpha", "beta"]


def test_order_is_frozen_while_the_cast_is_unchanged():
    """The requirement: committing to a project already listed changes nothing.

    `beta` is now the most recent, but the set is the same, so the page keeps
    the order it already had and the run produces no commit.
    """
    assert readme.preserve_order(["beta", "alpha"], ["alpha", "beta"]) == ["alpha", "beta"]


def test_order_is_recomputed_when_a_project_joins():
    assert readme.preserve_order(["gamma", "beta"], ["alpha", "beta"]) == ["gamma", "beta"]


def test_an_empty_block_accepts_the_first_render():
    page = "<!-- projects:start -->\n\n<!-- projects:end -->"
    assert readme.repos_in(readme.block(page, "projects")) == []
    assert readme.preserve_order(["alpha"], []) == ["alpha"]
