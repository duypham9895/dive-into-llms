# Fork notice

This repository is a fork of **[Lordog/dive-into-llms](https://github.com/Lordog/dive-into-llms)**: 《动手学大模型》 Dive into LLMs, by 张倬胜, 袁童鑫 et al. (Shanghai Jiao Tong University, National University of Singapore), with support from the Huawei Ascend community.

- Forked at upstream commit `f84c04268794ef94f8949808bbc14ab8636763a0` (2025-10-10).
- Until publishing, branch `main` is identical to upstream `main` at that commit; publishing merges `content/i18n` into `main` (see [PUBLISH.md](PUBLISH.md)). The Vietnamese and English translation is developed on branch `content/i18n`.
- The upstream repository has **no licence**. Copyright remains with the original authors. This fork adds an unofficial Vietnamese and English translation. It is not affiliated with or endorsed by the authors. Removal requests are honoured: open an issue at https://github.com/duypham9895/dive-into-llms/issues.

## Remotes

- `upstream` points to the original repository. Pushing to it is disabled in this checkout.
- `origin` (github.com/duypham9895/dive-into-llms) is added by the owner when publishing; nothing is pushed from this checkout otherwise.

## Publishing (run by the owner)

The full sequence (checks, fork, push, Pages, merge, live checks) and the take-down procedure are in [PUBLISH.md](PUBLISH.md). The first steps:

GitHub shows the "forked from Lordog/dive-into-llms" label only when the GitHub repository is created as a fork. Create it that way first, then push:

```sh
gh repo fork Lordog/dive-into-llms --clone=false
gh repo edit duypham9895/dive-into-llms --enable-issues   # forks start with Issues off; Issues is the removal-request channel
git remote add origin git@github.com:duypham9895/dive-into-llms.git
git push origin content/i18n
```
