# What updates itself, and what you still write

Two blocks of `README.md` are generated. Everything else on the page is
hand-written and no script touches it.

| Block | Holds | Owner |
|---|---|---|
| `<!-- projects:start -->` | the three most recently worked-on public projects | `scripts/update-profile.py` |
| `<!-- stack:start -->` | the badge groups | `scripts/update-profile.py` |
| `<!-- cards:start -->` | the stats cards | `scripts/use-self-hosted-stats.py` |

## When it runs, and when it stays quiet

`.github/workflows/update-profile.yml` runs daily and on demand. It opens a
pull request **only when the cast of three projects or the set of
technologies actually changed.**

Committing to a project already on the page changes nothing here. That is
deliberate: the dates you see are live badges from shields.io, which
re-render every time someone loads the page, so keeping them honest costs no
commit at all.

Order inside the projects block is frozen between changes too. It gets
recomputed at the moment a different project joins the three, not every time
one of them moves.

## Adding the writing for a new project

A repository with nothing written about it still gets a card: its name, its
GitHub description, a link, and chips built from whatever topics resolve to
a real technology. It just gets a plainer one.

To give it the full treatment, add a table to `content/projects.toml` keyed
by the repository name. Every field is optional:

```toml
[repository-name]
title    = "What you want it called"
headline = "the bit after the colon"
body     = """
First paragraph.

Second paragraph.
"""
decisions = ["**A decision.** Why it went that way."]
chips     = ["Python", "FastAPI"]
```

## When a new technology shows up

Detection reads two things from each eligible repository: the languages
GitHub reports, above 5% of the repository's bytes, and the topics.

Both are matched against [simple-icons](https://simple-icons.org), which
doubles as the filter. A topic is free text, so `fastapi` sits beside
`one-hot-encoding` and `portfolio` — and nobody draws a logo for a concept,
so a term with no icon never reaches the page. `tensorflowjs` does reach it,
because the resolver strips the `js` and finds TensorFlow.

Anything found that is not already in `content/stack.toml` lands in
**Recently picked up**, and the pull request says so. To move it into a real
group, add it to `content/stack.toml`:

```toml
[[tech]]
name  = "TensorFlow"
group = "AI and Python"
color = "FF6F00"
logo  = "tensorflow"
```

Detection only ever adds. Nothing in that file is removed because a scan
failed to confirm it, which is why Pydantic, SQL and the whole **From the
data years** group survive — that group is marked `frozen`, because
professional experience leaves no trace in a public repository.

## Repositories that never appear

Private ones (they 404 for a visitor), forks, archived repositories, and
this one. Excluding this one matters: the workflow commits here, so
including it would hold it at first place forever.

## Running it yourself

```bash
python scripts/update-profile.py            # dry run, prints the report
python scripts/update-profile.py --write    # apply it
python -m pytest tests/ -q                  # 32 tests, no network
python scripts/check-readme-links.py        # every image still responds
```
