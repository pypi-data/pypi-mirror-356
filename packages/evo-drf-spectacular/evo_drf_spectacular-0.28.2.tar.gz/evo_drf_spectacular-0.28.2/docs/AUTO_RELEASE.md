# Auto Release Documentation

This document describes how version management works in this repository.

## Overview

- Every push to `main` automatically bumps the patch version using `scripts/bump_version.py`.
- Only **major** releases are tagged. Pushing a tag triggers `release.yml` which uploads the package to PyPI.

## Workflows

### `auto-bump.yml`
Automatically runs on pushes to `main` and increments the patch version. The commit message is
`"Bump version to <version> [skip ci]"` so CI is skipped for the bump commit.

### `release.yml`
Builds and uploads the package when a tag is pushed. Tags should correspond to major
version bumps (e.g., `0.29.0`).

## Manual Version Bumps

Use `scripts/bump_version.py` locally when preparing a release:

```bash
# Bump patch version
python scripts/bump_version.py

# Bump minor version
python scripts/bump_version.py minor

# Bump major version
python scripts/bump_version.py major
```

Create a tag only for major versions. After pushing the tag, the `release.yml`
workflow publishes the package to PyPI.
