"""A project is never missing and never broken: either rich or plain."""

from __future__ import annotations

from conftest import make_repo
from profilegen import projects

RICH = {
    "demo": {
        "title": "Demo",
        "headline": "does a thing",
        "body": "One paragraph.\n\nAnother paragraph.",
        "decisions": ["**First.** Because.", "**Second.** Also because."],
        "chips": ["Python", "FastAPI"],
    }
}


def test_a_written_project_renders_the_full_card(resolver):
    repo = make_repo(name="demo")
    card = projects.render([repo], "gabrantoniette", RICH, resolver.resolve)

    assert "#### [Demo](https://github.com/gabrantoniette/demo): does a thing" in card
    assert "Another paragraph." in card
    assert "<summary><b>Decisions worth the click</b></summary>" in card
    assert "<code>Python</code> <code>FastAPI</code>" in card


def test_an_unwritten_project_still_gets_a_card(resolver):
    """The point of the fallback: a new repository is never a hole."""
    repo = make_repo(
        name="students-categorization",
        description="A neural network in JavaScript.",
        topics=("tensorflowjs", "one-hot-encoding"),
    )
    card = projects.render([repo], "gabrantoniette", {}, resolver.resolve)

    assert "#### [students-categorization](https://github.com/gabrantoniette/students-categorization)" in card
    assert "A neural network in JavaScript." in card
    assert "<code>TensorFlow</code>" in card
    assert "one-hot-encoding" not in card
    assert "Decisions worth the click" not in card


def test_every_card_is_clickable(resolver):
    repo = make_repo(name="demo")
    card = projects.render([repo], "gabrantoniette", {}, resolver.resolve)
    assert '<a href="https://github.com/gabrantoniette/demo">' in card


def test_repository_badge_escapes_hyphens(resolver):
    repo = make_repo(name="halcyon-goods-product-control")
    card = projects.render([repo], "gabrantoniette", {}, resolver.resolve)
    assert "Repository-halcyon--goods--product--control-1F3864" in card


def test_the_live_badges_carry_the_dates(resolver):
    """Why no commit is needed when only a date changes."""
    repo = make_repo(name="demo")
    card = projects.render([repo], "gabrantoniette", {}, resolver.resolve)
    assert "img.shields.io/github/last-commit/gabrantoniette/demo" in card
    assert "2026" not in card


def test_cards_are_separated(resolver):
    repos = [make_repo(name="one"), make_repo(name="two")]
    card = projects.render(repos, "gabrantoniette", {}, resolver.resolve)
    assert card.count("<br>") == 1
