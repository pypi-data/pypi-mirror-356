# Publishing Guide

This project supports both automated publishing via GitHub Actions and manual
publishing via script.

## Setup Requirements

### 1. PyPI Trusted Publisher

Since this project uses trusted publishing (no credentials in GitHub), you need
to:

1. Go to your PyPI project settings
2. Navigate to "Publishing" → "Trusted Publishers"
3. Add a new GitHub publisher with:
    - Owner: Your GitHub username/org
    - Repository: frost
    - Workflow: publish.yml
    - Environment: (leave blank)

### 2. GitHub Repository Settings

Ensure your repository has:

-   Actions enabled
-   Write permissions for workflows (Settings → Actions → General → Workflow
    permissions)

## How It Works

### Automatic Version Bumping

The project uses `python-semantic-release` which automatically bumps versions
based on your commit messages:

-   **PATCH** (0.1.0 → 0.1.1): Bug fixes

    -   Commit format: `fix: description`
    -   Example: `fix: resolve import error in utils module`

-   **MINOR** (0.1.0 → 0.2.0): New features

    -   Commit format: `feat: description`
    -   Example: `feat: add new monad implementations`

-   **MAJOR** (0.1.0 → 1.0.0): Breaking changes
    -   Commit format: `feat!: description` or include `BREAKING CHANGE:` in
        commit body
    -   Example: `feat!: redesign API interface`

### Other Commit Types

-   `docs:` - Documentation changes (no version bump)
-   `style:` - Code style changes (no version bump)
-   `refactor:` - Code refactoring (no version bump)
-   `perf:` - Performance improvements (PATCH)
-   `test:` - Test changes (no version bump)
-   `build:` - Build system changes (no version bump)
-   `ci:` - CI configuration (no version bump)
-   `chore:` - Other changes (no version bump)

## Publishing Process

The workflow automatically:

1. **On push to main branch**:

    - Analyzes commits since last release
    - Determines version bump type
    - Updates version in `pyproject.toml`
    - Creates git tag
    - Creates GitHub release
    - Builds package with `uv build`
    - Publishes to PyPI using trusted publisher

2. **Manual trigger**:
    - Use "Actions" tab → "Publish to PyPI" → "Run workflow"

## Example Workflow

```bash
# Make changes
git add .

# Commit with conventional format
git commit -m "feat: add new error handling utilities"

# Push to main
git push origin main

# GitHub Actions will:
# - Bump version from 0.1.0 → 0.2.0
# - Create tag v0.2.0
# - Build and publish to PyPI
```

## Troubleshooting

1. **No version bump**: Check commit message format
2. **Publishing fails**: Verify trusted publisher is configured on PyPI
3. **Permission errors**: Check GitHub repository settings

## Manual Publishing with Auto-Versioning

### Prerequisites

1. **Install uv** (if not installed):

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. **Set PyPI Token** (if not already set):

    ```bash
    export PYPI_TOKEN="pypi-YOUR_TOKEN_HERE"
    ```

### Publishing Steps

1. **Make commits with conventional format**:

    ```bash
    git commit -m "feat: add new functionality"    # Minor version bump
    git commit -m "fix: resolve bug"               # Patch version bump
    git commit -m "feat!: breaking change"        # Major version bump
    ```

2. **Run Publish Script**:

    ```bash
    ./scripts/publish.sh
    ```

3. **Follow Prompts**:
    - Script analyzes commits and suggests version bump
    - Type `y` to proceed with auto-versioning
    - Script handles version bump, build, and upload

## Testing Locally

```bash
# Check what version would be bumped to
uv run --with python-semantic-release -- semantic-release version --print

# Build package locally
uv build
```
