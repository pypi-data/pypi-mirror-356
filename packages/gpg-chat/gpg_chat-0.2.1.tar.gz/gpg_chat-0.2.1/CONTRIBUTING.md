# 🛡️ gpg-chat

[![Release](https://img.shields.io/gitlab/v/release/Diabeul/gpg-chat)](https://img.shields.io/gitlab/v/release/Diabeul/gpg-chat)
[![Build status](https://img.shields.io/gitlab/actions/workflow/status/Diabeul/gpg-chat/main.yml?branch=main)](https://gitlab.com/Diabeul/gpg-chat/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/Diabeul/gpg-chat/branch/main/graph/badge.svg)](https://codecov.io/gh/Diabeul/gpg-chat)
[![Commit activity](https://img.shields.io/gitlab/commit-activity/m/Diabeul/gpg-chat)](https://img.shields.io/gitlab/commit-activity/m/Diabeul/gpg-chat)
[![License](https://img.shields.io/gitlab/license/Diabeul/gpg-chat)](https://img.shields.io/gitlab/license/Diabeul/gpg-chat)

Some gpg chat tui

- **Gitlab repository**: <https://gitlab.com/Diabeul/gpg-chat/>
- **Documentation** <https://Diabeul.gitlab.io/gpg-chat/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on gitlab with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@gitlab.com:Diabeul/gpg-chat.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.gitlab.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.gitlab.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-gitlab).
To enable the code coverage reports, see [here](https://fpgmaas.gitlab.io/cookiecutter-uv/features/codecov/).

## Releasing a new version

- Create an API Token on [PyPI](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://gitlab.com/Diabeul/gpg-chat/settings/secrets/actions/new).
- Create a [new release](https://gitlab.com/Diabeul/gpg-chat/releases/new) on gitlab.
- Create a new tag in the form `*.*.*`.

For more details, see [here](https://fpgmaas.gitlab.io/cookiecutter-uv/features/cicd/#how-to-trigger-a-release).

---

Repository initiated with [diabeul/bakeplate](https://gitlab.com/Diabeul/bakeplate).

