# What updates itself, and what you still write

Two blocks of `README.md` and everything under `assets/generated/` are
generated. Everything else on the page is hand-written and no script
touches it.

| What | Holds | Owner |
|---|---|---|
| `<!-- projects:start -->` | the three most recently worked-on public projects, and only those three | `scripts/update-profile.py` |
| `<!-- stack:start -->` | the badge groups | `scripts/update-profile.py` |
| `assets/generated/languages-by-*.svg` | the two language donuts in *GitHub at a glance* | `scripts/update-profile.py` |
| `assets/generated/languages/<repo>-*.svg` | one language bar per public repository | `scripts/update-profile.py` |
| `<!-- cards:start -->` | the stats card | `scripts/use-self-hosted-stats.py` |

## When it runs, and when it stays quiet

`.github/workflows/update-profile.yml` runs every hour, on demand, and on any
push to `main` that touches `content/`, `scripts/` or the workflow itself. It
opens a pull request **only when something on the page actually changed**,
and keeps one open: a later run updates that pull request instead of
stacking another beside it. The pull request's description says what moved.

What counts as a change:

- a different project joins the three most recent
- a technology shows up that the stack does not have yet
- a repository's languages or the number of commits you made to it change,
  which redraws its language bar and the donuts

The dates you see are live badges from shields.io, which re-render every
time someone loads the page, so keeping them honest costs no commit at all.

Order inside the projects block is frozen between changes too. It gets
recomputed at the moment a different project joins the three, not every time
one of them moves.

## Adding the writing for a new project

A repository with nothing written about it still gets a card: its name, its
GitHub description, its language bar, a link, and chips built from whatever
topics resolve to a real technology. It just gets a plainer one.

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

## The language charts

Every language GitHub detects counts, by its share of the repository's
bytes, which is what the repository's own *Languages* tab shows. The
third-party cards these replaced counted one language per repository, the
primary one, so a project that is 20% JavaScript added nothing to
JavaScript.

- **Top Languages by Repo** weighs every public project the same, split by
  its own language mix. Summing raw bytes instead would let the largest
  repository decide the chart on its own.
- **Top Languages by Commit** weighs each project by the commits you made to
  its default branch, split across its languages in proportion to their
  bytes. Attributing each commit to the files it touched would cost one API
  call per commit; this costs one per repository.

Each donut shows up to eight languages, every one named in the legend with
its share, so a slice too thin to see still says what it is. A ninth and
beyond fold into *Other*. Colours are GitHub's own, from
[linguist](https://github.com/github-linguist/linguist).

## The language bar in each project's README

Each public repository gets a bar drawn like its *Languages* tab, in light
and dark, at `assets/generated/languages/<repo>-light.svg` and `-dark.svg`.
The profile cards use it, and each project's own README embeds it from the
raw URL on this repository's `main`:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gabrantoniette/gabrantoniette/main/assets/generated/languages/REPO-dark.svg">
  <img src="https://raw.githubusercontent.com/gabrantoniette/gabrantoniette/main/assets/generated/languages/REPO-light.svg" alt="Languages in REPO, by share of code">
</picture>
```

The project's README is edited once and never again: when its languages
change, the file behind that URL is redrawn here.

A new public project gets its bar drawn on the first run. Its README still
needs the snippet pasted once, and the workflow says so: drawing that bar is
a change, so the run opens the pull request, and its description lists every
project whose README lacks the bar, with the snippet ready to paste.

## When a new technology shows up

Detection reads two things from each eligible repository: the languages
GitHub reports, above 5% of the repository's bytes, and the topics.

Both are matched against [simple-icons](https://simple-icons.org), which
doubles as the filter. A topic is free text, so `fastapi` sits beside
`one-hot-encoding` and `portfolio` — and nobody draws a logo for a concept,
so a term with no icon never reaches the page. `tensorflowjs` does reach it,
because the resolver strips the `js` and finds TensorFlow.

A technology found that is not already a `[[tech]]` entry in
`content/stack.toml` goes to the group `[placement]` names for it: HTML
lands in the frontend group, pandas in *Backend and data*, the way Python
sits in *AI and Python*. Only a technology `[placement]` does not mention
falls through to *Recently picked up*, and the pull request says so. To give
it a home, add its simple-icons title to the right list in `[placement]`, or
give it a full entry:

```toml
[[tech]]
name  = "TensorFlow"
group = "AI and Python"
color = "FF6F00"
logo  = "tensorflow"
```

`logo` is the simple-icons slug, which spells out punctuation: Node.js is
`nodedotjs`, not `nodejs`.

Detection only ever adds. Nothing in that file is removed because a scan
failed to confirm it, which is why Pydantic, SQL and the whole **From the
data years** group survive — that group is marked `frozen`, because
professional experience leaves no trace in a public repository, and
`[placement]` cannot point into it.

## Repositories that never appear

Private ones (they 404 for a visitor), forks, archived repositories, and
this one. Excluding this one matters: the workflow commits here, so
including it would hold it at first place forever.

When a repository stops being eligible, its language bar is deleted on the
next run.

## Running it yourself

```bash
python scripts/update-profile.py            # dry run, prints the report
python scripts/update-profile.py --write    # apply it
python -m pytest tests/ -q                  # 68 tests, no network
python scripts/check-readme-links.py        # every image still responds
```
