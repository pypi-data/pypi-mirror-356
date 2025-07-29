# Scripts for devops

- [Scripts for devops](#scripts-for-devops)
  - [Development](#development)
    - [Setup](#setup)
  - [Fixing Semantic Release](#fixing-semantic-release)
    - [Disclaimer](#disclaimer)
    - [Steps](#steps)

## Development

### Setup
1. poetry install
2. poetry shell

## Fixing Semantic Release

* [Source](https://github.com/relekang/python-semantic-release)
* [Action](https://python-semantic-release.readthedocs.io/en/latest/automatic-releases/github-actions.html)
* [Documentation](https://python-semantic-release.readthedocs.io/en/latest/#getting-started)
* [Configuration](https://python-semantic-release.readthedocs.io/en/latest/configuration.html)
  * These are being stored in the file `pyproject.toml` and its `tools.semantic_release` section

This is to resolve issues cuased by manually creating a version tag in conflict with what the CI process wants to create.

### Disclaimer

The below needs to be completed as an administrator of the git repo

This process is required because the semantic release action being used requires matching information

### Steps

1) Pull down the current main branch to your local
   1) Ensure that your git status shows no changes
2) Record the current tag without the `v` prefix
3) Update files:
   1) datateer_cli/\_\_init__.py
      1) set `__version__` to the currnet version
   2) CHANGELOG.md
      1) follow the format seen in the file adding the current version
4) git add .
5) git commit -m "<current version>"
   1) ensure that there isn't any other text other than the version for the commit message
6) git push

Now you have brought the repo back into a state where the semantic release can work as expected