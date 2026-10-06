"""The charts name every language, fit their frame, and draw the same bytes twice."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET

from profilegen import charts, embeds

COLORS = {"Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6"}
EIGHT = [
    ("Python", 0.502), ("JavaScript", 0.26), ("TypeScript", 0.174), ("HTML", 0.034),
    ("CSS", 0.022), ("Dockerfile", 0.005), ("Jinja", 0.003), ("Mako", 0.0003),
]


def test_the_donut_names_every_language_with_its_share():
    svg = charts.donut_card("Top Languages by Repo", EIGHT, COLORS, "light")
    for name, _ in EIGHT:
        assert f">{name} " in svg
    assert ">Mako &lt;0.1%<" in svg


def test_the_donut_is_valid_svg_in_both_themes():
    for theme in charts.CARD_THEMES:
        ET.fromstring(charts.donut_card("Top Languages by Commit", EIGHT, COLORS, theme))


def test_the_donut_copies_the_frame_of_the_cards_beside_it():
    """340 by 200, the github_dark background and border."""
    svg = charts.donut_card("Top Languages by Repo", EIGHT, COLORS, "dark")
    assert 'width="340" height="200"' in svg
    assert 'fill="#0d1117"' in svg
    assert 'stroke="#2e343b"' in svg


def test_eight_legend_rows_fit_inside_the_card():
    svg = charts.donut_card("Top Languages by Repo", EIGHT, COLORS, "light")
    bottoms = [float(y) + float(h) for y, h in re.findall(r'<rect x="30" y="([\d.]+)" width="\d+" height="(\d+)"', svg)]
    assert len(bottoms) == 8
    assert max(bottoms) < charts.CARD_H - 4


def test_one_slice_per_language():
    svg = charts.donut_card("Top Languages by Repo", EIGHT, COLORS, "light")
    assert svg.count("<path ") == 8


def test_a_single_language_is_a_whole_ring():
    """An arc from a point back to itself draws nothing, so one language is a circle."""
    svg = charts.donut_card("Top Languages by Repo", [("Python", 1.0)], COLORS, "light")
    assert "<path " not in svg
    assert '<circle cx="255" cy="120"' in svg


def test_the_chart_says_what_it_shows_to_a_screen_reader():
    svg = charts.donut_card("Top Languages by Repo", EIGHT[:2], COLORS, "light")
    assert "<title id=\"title\">Top Languages by Repo: Python 50.2%, JavaScript 26.0%</title>" in svg


def test_the_same_input_draws_the_same_bytes():
    """Otherwise the workflow would commit on every run for nothing."""
    first = charts.donut_card("Top Languages by Repo", EIGHT, COLORS, "light")
    assert charts.donut_card("Top Languages by Repo", EIGHT, COLORS, "light") == first
    assert charts.language_bar("demo", EIGHT, COLORS, "dark") == charts.language_bar("demo", EIGHT, COLORS, "dark")


def test_the_bar_names_every_language_and_is_valid_svg():
    for theme in charts.BAR_THEMES:
        svg = charts.language_bar("demo", EIGHT, COLORS, theme)
        ET.fromstring(svg)
        for name, _ in EIGHT:
            assert f">{name}</tspan>" in svg


def test_the_bar_has_no_background_of_its_own():
    """Transparent, so the gaps between segments show the reader's page."""
    svg = charts.language_bar("demo", EIGHT[:2], COLORS, "light")
    assert "<rect" in svg
    assert 'fill="#ffffff"' not in svg
    assert 'fill="#0d1117"' not in svg


def test_a_long_legend_wraps_onto_a_new_row():
    one_row = charts.language_bar("demo", EIGHT[:2], COLORS, "light")
    many = [(f"Language{i}", 1 / 12) for i in range(12)]
    wrapped = charts.language_bar("demo", many, COLORS, "light")

    height = lambda svg: int(re.search(r'height="(\d+)" viewBox', svg).group(1))
    assert height(wrapped) > height(one_row)


def test_a_projects_readme_points_at_the_raw_file_here():
    html = embeds.language_bar("students-categorization", "gabrantoniette", absolute=True)
    raw = "https://raw.githubusercontent.com/gabrantoniette/gabrantoniette/main/assets/generated/languages"
    assert f'srcset="{raw}/students-categorization-dark.svg"' in html
    assert f'src="{raw}/students-categorization-light.svg"' in html


def test_a_readme_with_the_bar_is_recognised_in_either_form():
    absolute = embeds.language_bar("demo", "gabrantoniette", absolute=True)
    relative = embeds.language_bar("demo", "gabrantoniette", absolute=False)
    assert embeds.has_language_bar(f"# Demo\n\n{absolute}\n", "demo")
    assert embeds.has_language_bar(relative, "demo")
    assert not embeds.has_language_bar("# Demo\n\nNo bar here.\n", "demo")
    assert not embeds.has_language_bar(absolute, "demo-two")
    assert not embeds.has_language_bar(embeds.language_bar("demo-two", "gabrantoniette", True), "demo")
