from profilegen import github

from conftest import make_repo


def test_newest_repository_comes_first_whatever_its_last_commit():
    old_but_busy = make_repo("old", created_at="2026-01-01T00:00:00Z", last_commit="2026-11-06T00:00:00Z")
    new_but_quiet = make_repo("new", created_at="2026-10-29T00:00:00Z", last_commit="2026-10-29T00:00:00Z")

    assert [r.name for r in github.rank([old_but_busy, new_but_quiet])] == ["new", "old"]


def test_same_creation_date_falls_back_to_the_name():
    a = make_repo("a", created_at="2026-10-29T00:00:00Z")
    b = make_repo("b", created_at="2026-10-29T00:00:00Z")

    assert [r.name for r in github.rank([a, b])] == ["b", "a"]
