# Fork notice

This repository is a fork of **[Lordog/dive-into-llms](https://github.com/Lordog/dive-into-llms)**: 《动手学大模型》 Dive into LLMs, by 张倬胜, 袁童鑫 et al. (Shanghai Jiao Tong University, National University of Singapore, Huawei Ascend community).

- Forked at upstream commit `f84c04268794ef94f8949808bbc14ab8636763a0` (2025-10-10).
- Branch `main` is identical to upstream `main` at that commit. The Vietnamese and English translation is developed on branch `content/i18n`.
- The upstream repository has **no licence**. Copyright remains with the original authors. This fork adds an unofficial Vietnamese and English translation. It is not affiliated with or endorsed by the authors. Removal requests are honoured.

## Remotes

- `upstream` points to the original repository. Pushing to it is disabled in this checkout.
- There is no `origin` yet. The owner adds it and pushes manually.

## Publishing (run by the owner)

GitHub shows the "forked from Lordog/dive-into-llms" label only when the GitHub repository is created as a fork. Create it that way first, then push:

```sh
gh repo fork Lordog/dive-into-llms --clone=false
git remote add origin git@github.com:duypham9895/dive-into-llms.git
git push origin content/i18n
```
