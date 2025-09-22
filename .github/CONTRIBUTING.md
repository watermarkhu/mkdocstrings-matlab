# Contributing to mkdocstrings-matlab

Thank you for considering contributing! Please follow these steps to get started:

## 1. Environment Setup

Install all dependencies using [uv](https://github.com/astral-sh/uv):

```sh
uv sync --all-groups
```

Learn more about uv: [uv documentation](https://github.com/astral-sh/uv)

## 2. Pre-commit Hooks using prek

Set up [prek](https://github.com/j178/prek) hooks to ensure code quality:

```sh
uv run prek install
```

See: [prek documentation](https://prek.j178.dev/)

## 3. Running Tests

Run tests with [pytest](https://docs.pytest.org/en/stable/):

```sh
uv run pytest
```

See: [pytest documentation](https://docs.pytest.org/en/stable/)

## 4. Pull Request Guidelines

- Pull requests should target the `main` branch.
- Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages.

See: [Conventional Commits Spec](https://www.conventionalcommits.org/en/v1.0.0/)
