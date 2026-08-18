# uv Guide — Cohort Management System

This project uses [uv](https://docs.astral.sh/uv/) for Python dependency management and virtual environments. This guide covers everything from setup to daily usage.

## What is uv?

uv is a fast Python package and project manager (written in Rust, from the Astral team — makers of Ruff). It replaces:

| pip | uv equivalent |
|---|---|
| `pip install` | `uv add` / `uv sync` |
| `python -m venv` | automatic (uv does it for you) |
| `pip freeze > requirements.txt` | `uv export` |
| `requirements.txt` | `pyproject.toml` + `uv.lock` |

The core idea: **you never manage the venv or packages by hand**. uv creates and updates `.venv` automatically.

## 1. Installing uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or check if it's already installed:

```bash
uv --version
```

## 2. Initializing a project

For a brand-new empty project:

```bash
mkdir my-project && cd my-project
uv init --bare
```

For an **existing** project that already has code (like this one), run `uv init --bare` inside the project directory — it won't touch your code.

`--bare` means "just create config files, no sample code". Files uv creates:

| File | Purpose | Commit? |
|---|---|---|
| `pyproject.toml` | Declared dependencies (what *you* ask for) | yes |
| `uv.lock` | Exact resolved versions + hashes (the source of truth) | yes |
| `.python-version` | Pins which Python interpreter to use | yes |
| `.venv/` | The virtual environment (auto-created, auto-updated) | no (gitignored) |

### Which Python version?

`uv init` may pick a newer Python than you want. Pin it explicitly:

```bash
echo "3.12" > .python-version
```

uv will then use Python 3.12 for everything. Make sure `requires-python` in `pyproject.toml` matches (e.g. `>=3.12`).

## 3. Migrating from pip to uv

If you have an existing `requirements.txt`, import all packages into `pyproject.toml` in one shot:

```bash
uv add -r requirements.txt
```

This resolves everything, creates `.venv`, installs the packages, and writes `uv.lock`.

**Note:** if your shell has the old pip venv activated (`VIRTUAL_ENV` set), uv warns that it will ignore it and use `.venv` instead. Run `deactivate` or close the terminal. The old `venv/` folder is now dead weight — it's gitignored, so you can delete it anytime.

Once you're comfortable, delete `requirements.txt` — `pyproject.toml` + `uv.lock` fully replace it.

## 4. Running the project

```bash
uv run python manage.py runserver
```

`uv run` checks the lockfile, syncs `.venv` if anything changed (dependency drift is impossible), then runs your command inside it. No activation needed.

If you prefer "activating" a venv like before:

```bash
source .venv/bin/activate
python manage.py runserver
```

## 5. Managing packages

```bash
# Add a new package
uv add django-cors-headers

# Add a dev-only package (not deployed with the app)
uv add --dev pytest

# Add a package in a specific version
uv add "django==6.0"

# Remove a package
uv remove django-api-readme

# Reinstall everything exactly as in the lockfile
uv sync

# Upgrade all packages to latest allowed versions
uv sync --upgrade

# Upgrade just one package
uv lock --upgrade-package django
uv sync
```

The golden rule: **`pyproject.toml` says what you want, `uv.lock` says what you get.** Both contain the same version you asked for — pyproject.toml holds the constraint (e.g. `django==6.0.4`), uv.lock pins the exact wheel with a hash for reproducibility.

## 6. Installing everything on a fresh machine

```bash
git clone <repo-url>
cd cohort-management-system
uv sync
```

That's it. No venv creation, no `pip install -r requirements.txt`. `uv sync` reads `uv.lock`, creates `.venv`, installs the exact same versions.

## 7. Day-to-day cheat sheet

| Task | Command |
|---|---|
| Run server | `uv run python manage.py runserver` |
| Run a management command | `uv run python manage.py migrate` |
| Run Django check | `uv run python manage.py check` |
| Add a package | `uv add <package>` |
| Remove a package | `uv remove <package>` |
| Sync env to lockfile | `uv sync` |
| Upgrade everything | `uv sync --upgrade` |
| Activate venv | `source .venv/bin/activate` |
| Export lockfile as requirements.txt | `uv export -o requirements.txt` |
| Run a CLI tool without installing it | `uvx ruff check .` |

## 8. Bonus: one-off tools with `uvx`

Don't want to install a CLI tool into your project? `uvx` runs it in a temporary environment:

```bash
uvx ruff check .          # lint
uvx django-admin --help   # any tool, ephemeral
```

## 9. Common gotchas

- **`VIRTUAL_ENV=venv does not match ... .venv` warning** — stale pip venv is still active in your shell. `deactivate` it.
- **Editor/IDE can't see packages** — point your interpreter at `.venv/bin/python`.
- **Mixing pip and uv** — don't. Once on uv, install everything through `uv add` so `pyproject.toml` and `uv.lock` stay in sync.
- **Docker** — the app now runs in Docker via the `Dockerfile` + `compose.yaml` (`docker compose up -d --build`). The image uses `uv sync --frozen` for reproducible installs. Note `[tool.uv] package = false` in `pyproject.toml` tells uv this is an application, not a package to build — without it `uv sync` fails on the missing build backend.