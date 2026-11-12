# Publishing the translation (run by the owner)

Claude does not push. Run these steps yourself, in order, from the repository root.
The site goes to `https://duypham9895.github.io/dive-into-llms/` (vi at the root, en under `/en/`).

## 0. Before anything leaves this machine

Commit the working tree on `content/i18n`, then run every check, including the slide checks
that CI cannot run (they read the git-ignored pdftotext cache in `i18n/.cache/slides/`):

```sh
git switch content/i18n
git status --short                         # must be empty
P=.venv/bin/python
$P scripts/test_i18n_normalize.py && $P scripts/test_i18n_links.py && $P scripts/test_i18n_check.py \
  && $P scripts/test_i18n_slides_check.py && $P scripts/i18n_check.py && $P scripts/i18n_slides_check.py \
  && $P scripts/assemble_docs.py && .venv/bin/mkdocs build --strict \
  && $P scripts/i18n_render_check.py site docs
```

## 1. Create the fork and the removal-request channel

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
git remote add origin git@github.com:duypham9895/dive-into-llms.git
git push origin content/i18n
```

## 3. Enable Pages BEFORE merging

The workflow deploys on every push to `main`; Pages must already be set to build from Actions.

```sh
gh api -X POST repos/duypham9895/dive-into-llms/pages -f build_type=workflow
gh api repos/duypham9895/dive-into-llms/pages --jq '.build_type, .html_url'   # expect: workflow
```

## 4. Merge and push main

One merge commit, so a take-down can revert it in one step.

```sh
git switch main
git merge --no-ff content/i18n -m "Publish the Vietnamese and English translation"
git push origin main
```

## 5. Watch the Actions run

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

## 6. Live checks

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
- **Unpublish:**

  ```sh
  gh api -X DELETE repos/duypham9895/dive-into-llms/pages
  gh workflow disable pages.yml -R duypham9895/dive-into-llms
  git switch main
  git revert -m 1 --no-edit "$(git log --merges -1 --format=%H)"   # the publish merge
  git push origin main
  ```

  This removes the website, but the translation stays public on the `content/i18n` branch and in
  `main`'s history. When the request is about the translation itself, also run:

  ```sh
  git push origin --delete content/i18n
  gh repo delete duypham9895/dive-into-llms --yes   # removes the fork and all its history
  ```

  Then reply on the issue (or to GitHub) with what was removed and when.
