# Girokmoji

Changelog Generator for Gitmoji enthusiasts

_기록 + Gitmoji_

## Minimum Dependencies

We use minimum dependencies. Currently, only pygit2, which requires no runtime
`git` executable, good enough binary distributions, is used.

## Designed for General Use

### Pipeline as a trigger

Pipelines, such as SCM provided ones (e.g., GitHub Actions), dedicated solutions
(e.g., Jenkins) are best when you use it as a ***"trigger"***.

### Do a single thing

This only generates release note. This project has no interest in versioning
scheme, repository scheme (mono/poly war), even tag order. Just put two tags.

## Basic use case

Clone

```bash
git clone https://github.com/KMilhan/girokmoji.git
```

**Note**: Please change repository url with your repository url. Also, clone with enough depth, so `libgit2` can
traverse to the past tag.

### Installation

#### with `uv` (recommended for development)

Install [`uv`](https://github.com/astral-sh/uv) and create a virtual
environment:

```bash
uv pip install girokmoji
```

The last command installs this package together with development tools such as
`pytest`. Use `uv pip` inside the environment whenever you need to add more
packages.

#### with isolated `pip`

If you do not use `uv`, you can install the project with plain `pip` in an
already isolated environment:

```bash
pip install girokmoji
```

### Generate Release Note

#### with `uv` (recommended, especially for release pipelines)

```bash
uvx --from "girokmoji@latest" girokmoji TEST_PROJECT_NAME 2025-02-10 test_repository_dir v0.1.0 v0.5.2 > release_note.md
```

#### with isolated `pip`

```bash
python -m girokmoji TEST_PROJECT_NAME 2025-02-10 test_repository_dir v0.1.0 v0.5.2 > release_note.md
```

or

```bash
girokmoji TEST_PROJECT_NAME 2025-02-10 test_repository_dir v0.1.0 v0.5.2 > release_note.md
```

### Show version

```bash
girokmoji --version
```

### GitHub Release payload

To create JSON payload for GitHub Release:

```bash
girokmoji TEST_PROJECT_NAME 2025-02-10 test_repository_dir v0.1.0 v0.5.2 --github-payload > release.json
```

## Example

For generated release note, go [EXAMPLE.md](./EXAMPLE.md)

## Development and Testing

The recommended workflow for local development uses `uv` for dependency
management. `uv` creates an isolated virtual environment and installs the
required packages using its own resolver.

```bash
# create a virtual environment in `.venv`
uv venv

# install main and development dependencies
uv sync

# run the test suite
uv run pytest
```
See [multiline commit test](docs/multiline_commit_test.md) for multi-line commit examples and how commits are grouped in release notes.

## Publishing to PyPI

The "Publish Python Package to PyPI" workflow can be dispatched manually. Provide the
`tag` input to select which release tag should be built and uploaded. The workflow
checks out the chosen tag, runs tests, builds the package and then deploys it to PyPI.
