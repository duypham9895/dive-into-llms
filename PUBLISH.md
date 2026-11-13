# Publishing the translation (run by the owner)

Claude does not push. Run these steps yourself, in order, from the repository root.
The site goes to `https://duypham9895.github.io/dive-into-llms/` (vi at the root, en under `/en/`).

## 0. Before anything leaves this machine

Commit the working tree on `content/i18n`, then run every check, including the slide checks
that CI cannot run (they read the git-ignored pdftotext cache in `i18n/.cache/slides/`, or the
upstream PDF blobs through `pdfinfo`):

```sh
git switch content/i18n
git status --short                         # must be empty
P=.venv/bin/python
$P scripts/test_i18n_normalize.py && $P scripts/test_i18n_links.py && $P scripts/test_i18n_check.py \
  && $P scripts/test_i18n_slides_check.py && $P scripts/test_build_github_readme.py \
  && $P scripts/i18n_check.py && $P scripts/i18n_slides_check.py \
  && $P scripts/slide_decks.py --check \
  && $P scripts/assemble_docs.py && .venv/bin/mkdocs build --strict \
  && $P scripts/i18n_render_check.py site docs \
  && $P scripts/build_github_readme.py --check
```

`build_github_readme.py --check` runs last because its own live-URL check reads `site/`,
built by the `mkdocs build` just above it.

`overrides/main.html`'s `site_meta` block is Material 9.7.1's own block, copied in by hand
minus its `config.extra.alternate` hreflang loop (item D': that loop makes the browser fetch
a wrong, 404ing `sitemap.xml` on every page). Bumping `mkdocs-material` in
`requirements-docs.lock` means re-copying that block from the new version's
`material/templates/base.html` and re-applying the same one-line removal, or the override
can silently fall behind Material's own `<head>` (a missing `<meta>`/`<link>` future versions
add there).

## 1. Create the fork and the removal-request channel

First publish only (done 2026-11-12: the fork exists, Issues and Actions are on). Later publishes
start at step 0, then step 2.

```sh
gh repo fork Lordog/dive-into-llms --clone=false
gh repo edit duypham9895/dive-into-llms --enable-issues      # forks start with Issues off
gh api repos/duypham9895/dive-into-llms --jq .has_issues      # expect: true
gh api repos/duypham9895/dive-into-llms/actions/permissions   # expect "enabled": true
```

If `enabled` is false: `gh api -X PUT repos/duypham9895/dive-into-llms/actions/permissions -F enabled=true`.
If the Actions tab of the fork shows a banner asking to enable workflows on a fork, click it.

## 2. Push the branch

SSH, because the gh token lacks the `workflow` scope and an HTTPS push of
`.github/workflows/pages.yml` would be refused.

```sh
git remote get-url origin 2>/dev/null \
  || git remote add origin git@github.com:duypham9895/dive-into-llms.git   # only if origin is missing
git push origin content/i18n
```

## 3. Enable Pages BEFORE merging

The workflow deploys on every push to `main`; Pages must already be set to build from Actions.

```sh
gh api -X POST repos/duypham9895/dive-into-llms/pages -f build_type=workflow
gh api repos/duypham9895/dive-into-llms/pages --jq '.build_type, .html_url'   # expect: workflow
```

## 4. Render-check the GitHub README at the pushed ref

The branch is on GitHub now, `main` is not yet: this is the only chance to check the real
file before it can show on the repo's default page. `POST /markdown` cannot be used for
this (it does not add heading ids at all); a GET of the file at the ref, rendered, does:

```sh
for f in README.md README.en.md; do
  gh api -H 'Accept: application/vnd.github.html' \
    "repos/duypham9895/dive-into-llms/contents/.github/$f?ref=content/i18n" > "/tmp/$f.html"
  echo "$f: $(grep -c 'id="user-content-' "/tmp/$f.html") heading ids"
done
```

Every `#fragment` the file links to must match an `id="user-content-<fragment>"` in that
render (3 per language: motivation, contents, contributors). A mismatch means the slug
rule and GitHub's real renderer disagree; fix `scripts/build_github_readme.py`, push the
fix to `content/i18n`, and check again before merging.

## 5. Merge and push main

One merge commit, so a take-down can revert it in one step.

```sh
git switch main
git merge --no-ff content/i18n -m "Publish the Vietnamese and English translation"
git push origin main
```

## 6. Watch the Actions run

If the fork says workflows are disabled, enable them, and if the list below is empty, start a run:

```sh
gh api -X PUT repos/duypham9895/dive-into-llms/actions/permissions -F enabled=true
gh workflow run pages.yml --ref main -R duypham9895/dive-into-llms
```

```sh
gh run list -R duypham9895/dive-into-llms --workflow pages.yml --limit 1
gh run watch -R duypham9895/dive-into-llms --exit-status "$(gh run list -R duypham9895/dive-into-llms --workflow pages.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
```

Both jobs (`build`, `deploy`) must succeed. A failed run deploys nothing.

## 7. Live checks

Every page answers 200 (52 pages: home, 11 chapters, 3 notebooks, 11 slide notes, in vi and en):

```sh
B=https://duypham9895.github.io/dive-into-llms
for L in "" en/; do
  for u in "" chapter{1..11}/ chapter{1..11}/slides/ chapter4/sft_math/ chapter9/GUIagent/ chapter11/RLHF/; do
    printf '%s %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$B/$L$u")" "$L$u"
  done
done | grep -v '^200 ' || echo "all 200"
```

Every image answers 200 (the images are hotlinked from upstream at f84c042, never copied):

```sh
grep -rhoE '<img[^>]+src="https://[^"]+"' site | sed -E 's/.*src="([^"]+)".*/\1/' | sort -u \
  | while read -r u; do printf '%s %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "$u")" "$u"; done \
  | grep -v '^200 ' || echo "all images 200"
```

Banner with the Issues link on a vi and an en page:

```sh
for u in "" en/chapter8/; do curl -s "$B/$u" | grep -c 'https://github.com/duypham9895/dive-into-llms/issues'; done   # expect >= 1 each
```

In a normal browser: open a chapter, check that the images load, that the language switcher goes
to the same page in the other language, and that the banner and its Issues link show on top.

## Take-down procedure

- **Who watches:** the owner (duypham9895). Issues are the removal-request channel named in the
  banner and in FORK.md. Make sure GitHub notifies you:
  `gh api repos/duypham9895/dive-into-llms/subscription` (404 = not watching), and if needed
  `gh api -X PUT repos/duypham9895/dive-into-llms/subscription -F subscribed=true`.
  A DMCA notice from GitHub arrives by email to the account address.
- **Answer time:** about 1 business day for a DMCA notice or a removal request.
- **Unpublish:** `main` already has several publish merges (42ad6f5, 849d208, f7f65ff,
  0a6e7b4, and any later one `git log --merges main` shows above them) -- `git log --merges
  -1` alone only reverts the newest. Revert every one of them, newest first, and remove the
  two GitHub-README files separately: a `git revert` of the merge that added them only
  undoes that merge's own changes, not a later commit that also touched them.

  ```sh
  gh api -X DELETE repos/duypham9895/dive-into-llms/pages
  gh workflow disable pages.yml -R duypham9895/dive-into-llms
  git switch main
  for sha in 0a6e7b4 f7f65ff 849d208 42ad6f5; do
    git revert -m 1 --no-edit "$sha"
  done
  git rm .github/README.md .github/README.en.md
  git commit -m "Take down the GitHub README pair with the rest of the site"
  git push origin main
  ```

  This removes the website, but the translation stays public on the `content/i18n` branch and in
  `main`'s history. When the request is about the translation itself, also run:

  ```sh
  git push origin --delete content/i18n
  gh repo delete duypham9895/dive-into-llms --yes   # removes the fork and all its history
  ```

  Then reply on the issue (or to GitHub) with what was removed and when.
