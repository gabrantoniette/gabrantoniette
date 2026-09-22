"""The resolver decides what counts as a technology, and what is just a word."""

from __future__ import annotations

from profilegen.icons import logo_color


def test_the_catalog_is_consulted_before_simple_icons(resolver):
    """Docker exists in both. The catalog wins, so its curated colour does."""
    assert resolver.resolve("docker").name == "Docker"
    assert resolver.resolve("docker").via == "catalog"


def test_exact_match_against_simple_icons(resolver):
    """Node.js is in no catalog group yet, so it resolves on the icon alone."""
    hit = resolver.resolve("nodejs")
    assert hit.name == "Node.js"
    assert hit.via == "exact"


def test_alias_folds_a_topic_into_an_entry_you_already_have(resolver):
    """Without this, `anthropic` and `claude` each render a second badge."""
    assert resolver.resolve("anthropic").name == "Anthropic API"
    assert resolver.resolve("claude").name == "Anthropic API"


def test_catalog_entry_resolves_without_a_brand_icon(resolver):
    """Agno has no logo anywhere. It is still part of the stack."""
    hit = resolver.resolve("agno")
    assert hit.name == "Agno"
    assert hit.icon is None


def test_suffix_is_stripped_when_the_bare_name_exists(resolver):
    hit = resolver.resolve("tensorflowjs")
    assert hit.name == "TensorFlow"
    assert hit.via == "suffix -js"


def test_prefix_before_a_separator(resolver):
    assert resolver.resolve("docker-compose").name == "Docker"


def test_concepts_resolve_to_nothing(resolver):
    """The whole noise filter, in one assertion.

    These are all real topics on real repositories. None is a tool.
    """
    for term in [
        "one-hot-encoding",
        "machine-learning",
        "neural-network",
        "classification",
        "monorepo",
        "portfolio",
        "rest-api",
        "server-side-rendering",
        "inventory-management",
        "crud",
        "dashboard",
    ]:
        assert resolver.resolve(term) is None, term


def test_a_suffix_alone_is_not_a_match(resolver):
    """Stripping `js` off `js` would leave nothing and match nothing."""
    assert resolver.resolve("js") is None


def test_logo_colour_follows_brightness():
    assert logo_color("F7DF1E") == "black"   # JavaScript yellow
    assert logo_color("61DAFB") == "black"   # React cyan
    assert logo_color("F2C811") == "black"   # Power BI yellow
    assert logo_color("FF6F00") == "white"   # TensorFlow orange
    assert logo_color("000000") == "white"
