# Odoo project template: structure, CI, tests, and pre-commit

This note describes how GML Odoo project repositories are laid out after the template update, and how GitHub Actions, Odoo unit tests, and pre-commit fit together. The same model is used on the versioned templates (14.0–20.0). Branch names, Docker base images, and Python language pins differ by version; the layout does not.

---

## What a project repo is

Each customer/project repo is an **Odoo deployment**, not a copy of Odoo itself.

- **Odoo core** is either the base Docker image (containers) or the `odoo/odoo` git submodule (standalone/host installs).
- **Our code** lives mainly under `odoo/src/private-addons/`.
- **Third-party / OCA / GML** code is checked out as git submodules and **copied** into addon farms. We do not point `addons_path` at whole OCA repositories.

The `customer` module is the **dependency anchor**: every private addon this project uses should be listed in `customer`’s `depends`. Installing `customer` installs the rest of the graph.

---

## Repository structure

```
<project>/
├── .github/workflows/          # CI (see below)
├── .pre-commit-config.yaml     # What pre-commit runs
├── .pylintrc                   # Optional pylint-odoo checks (IDE / --exit-zero)
├── .pylintrc-mandatory         # Blocking pylint-odoo checks
├── docker-compose.yml          # Local stack: db + app (+ mail)
├── repos.yml                   # Git Aggregator (optional, for pending OCA PRs)
└── odoo/
    ├── Dockerfile              # Multi-stage image build
    ├── .dockerignore
    ├── requirements.txt        # Extra Python packages (not Odoo core)
    ├── migration.yml           # Marabunta
    ├── songs/                  # Initial data load (Anthem)
    ├── odoo/                   # Git submodule: Odoo core (standalone only)
    └── src/
        ├── addons.manifest.yml # Which modules to copy from submodules
        ├── sync-addons.sh      # Copies modules; never symlinks
        ├── private-addons/     # This project's modules (git-tracked)
        ├── paid-addons/        # Purchased modules (always included if present)
        ├── enterprise/         # Optional submodule; not in the template
        ├── public-submodules/  # OCA / ursais checkouts (whole repos)
        ├── gml-submodules/     # GML checkouts (whole repos)
        ├── public-addons/      # Generated; gitignored
        └── gml-addons/         # Generated; gitignored
```

### Addon farms (the important idea)

| Path | Role |
|---|---|
| `private-addons/` | Modules we own. Lint and unit-test these. |
| `public-submodules/` / `gml-submodules/` | Full git checkouts. **Not** on `addons_path`. |
| `addons.manifest.yml` | Include list: `public-submodules/repo/module_name` (or `gml-submodules/...`). |
| `public-addons/` / `gml-addons/` | **Copies** of the modules listed in the manifest. Gitignored. |
| `enterprise/`, `paid-addons/`, `private-addons/` | Always included if the directory exists. Not listed in the manifest. |

After clone, submodule update, or a manifest change, run:

```shell
odoo/src/sync-addons.sh
```

**Containers:** the Dockerfile runs `sync-addons.sh --dest /odoo/addons` in a builder stage, then copies only that folder into the runtime image. Adding a module is a manifest (or private-addons) change, not a Dockerfile edit.

**Standalone:** run the sync script, then set `addons_path` to `odoo/odoo/addons`, `src/enterprise` (if present), `src/paid-addons`, `src/private-addons`, `src/public-addons`, and `src/gml-addons`. Run `odoo/odoo/odoo-bin`.

**Enterprise** is optional. The template does not ship it (it is a private repo and would break CI checkout). A project that is entitled to it adds:

```shell
git submodule add --name enterprise -b <version> https://github.com/ursais/enterprise.git \
  odoo/src/enterprise
```

**`odoo/odoo`** is for host installs. Docker images already contain Odoo; `.dockerignore` excludes `odoo/odoo` from the image build.

### How to add a module (short)

- **Private:** put it in `odoo/src/private-addons/`, add it to `customer`’s `depends`.
- **PyPI:** add the package to `odoo/requirements.txt`, add the Odoo module name to `customer`.
- **OCA / GML git:** submodule under `public-submodules/` or `gml-submodules/`, list the module in `addons.manifest.yml`, run `sync-addons.sh`, add the dependency on `customer`.

---

## GitHub workflows

Templates ship three workflows. They do **not** deploy to a customer server (there is no cluster in the template).

### 1. Test (`.github/workflows/test.yml`)

- **When:** every pull request.
- **What:**
  1. Checkout with **public** submodules (`submodules: true`, default `GITHUB_TOKEN`).
  2. `docker compose build`.
  3. Collect test tags from directory names under `odoo/src/private-addons/` (e.g. `/customer,/elearning_content`).
  4. Run Odoo in the `app` service with tests enabled (see next section).

Private submodules such as `enterprise` are **not** in the template on purpose: the default GitHub token cannot clone them.

### 2. Code Quality Checks (`.github/workflows/code-quality-checks.yml`)

- **When:** pull requests, and pushes to the version branch (`14.0` … `20.0`), `main`, `master`, or `production`.
- **What:** `pre-commit` on the **changed files only** (`--from-ref` … `--to-ref`), not the whole history.
- Uses Python 3.11 to *run* the tools. Generated code still targets that Odoo version’s Python (Black `--target-version` / pyupgrade `--pyXX-plus`).

### 3. Docker Build (`.github/workflows/build.yml`)

- **When:** push to the version branch / `main` / `master`, or **manual** “Run workflow”.
- **What:** `docker build odoo` (prove the image builds).
- **Optional:** on a manual run, “Reset PGDATABASE to YYYYMMDD” sets `PGDATABASE` to today’s date. That is only `db_name`; it does **not** require `queue_job`. On the template it no-ops unless the repo variable `DEPLOY_NAMESPACE` is set (real projects with kubectl can use it to point at a fresh database).

---

## Odoo unit tests — what they are

Odoo ships a test runner inside the server process. Tests are Python classes (usually `TransactionCase`, `SavepointCase`, or `HttpCase`) in each module’s `tests/` folder. They run **against a real database**: modules are installed, XML/CSV data is loaded, then test methods execute.

They are **not** pytest by default, and they are **not** Selenium/Locust (those live under `odoo/tests/` for functional/performance work).

### What CI runs

```text
docker compose run app \
  --test-enable \
  --test-tags=/customer,/elearning_content \
  --workers=0 \
  --stop-after-init \
  -d test \
  -i customer
```

| Flag | Meaning |
|---|---|
| `--test-enable` | Turn on the test runner. |
| `-i customer` | Install `customer` (and thus everything it depends on) into database `test`. |
| `--test-tags=/…` | Only run tests whose tag matches those **module names**. `/customer` means “tests from the `customer` addon”. Stops Odoo’s own `website_slides` (etc.) tests from running. |
| `--workers=0` | One process; required for tests. |
| `--stop-after-init` | Install, run tests, exit. Do not leave a server running. |

If a private addon has **no** `tests/` folder, CI can still succeed with `0 failed, 0 error(s) of 0 tests` as long as the modules **install** (data files load). That is still useful: broken XML/CSV fails this job.

Tags are collected automatically from `private-addons/*` directory names, so a new private addon is included without editing the workflow.

### Running the same thing locally

```shell
docker compose build
docker compose run --rm app \
  --test-enable \
  --test-tags=/customer,/your_module \
  --workers=0 \
  --stop-after-init \
  -d test \
  -i customer
```

On Windows Git Bash, `/customer` can be mangled into a path. Prefix the command with `MSYS_NO_PATHCONV=1` or run it from a Linux/macOS shell.

---

## Pre-commit — what it is and how it works

[pre-commit](https://pre-commit.com/) is a framework that runs **small checkers and formatters** on git files. The list of tools is `.pre-commit-config.yaml`. It does **not** start Odoo and does **not** install modules.

### What it checks (this template)

Only files under **`odoo/src/private-addons/`** (the `exclude` pattern skips everything else). Submodules and generated farms are not linted here.

Typical hooks:

| Hook | Role |
|---|---|
| **black** | Python formatting. `--target-version` matches that Odoo’s Python (e.g. py36 on 14, py38 on 15, py310 on 16+). |
| **pyupgrade** | Modernize syntax for that Python. `--keep-percent-format` so `_("%s") % x` translations are not rewritten. |
| **isort** / **autoflake** / **flake8** | Import order, unused imports, style. |
| **prettier** / **eslint** | XML/JS (Odoo web). |
| **pylint-odoo** | Odoo-specific rules (manifest version `16.0.x.y.z`, licenses, security patterns). **Mandatory** file can fail the job; **optional** file is `--exit-zero` (warnings). |
| **en.po** | English `.po` files must not exist in private addons (Odoo uses the source language). |

Manifest **author** must be **Open Source Integrators** or **Gray Matter Logic**, not OCA. Licenses may include `OPL-1` / `OEEL-1` for enterprise-style modules.

### Local vs GitHub

Install once per clone:

```shell
pip install pre-commit
pre-commit install
```

- **`pre-commit install`:** runs on `git commit` for staged files (fast feedback).
- **CI:** runs on the diff of the PR/push, same config, so a laptop and GitHub agree if hook versions match.

Useful commands:

```shell
pre-commit run --all-files                          # whole private-addons tree
pre-commit run --files odoo/src/private-addons/foo/models/bar.py
```

If a hook **auto-fixes** (black, prettier), it fails once, writes the file, and you restage and commit again.

---

## How this hangs together on a PR

1. Open a PR against the version branch (or `master` / `main`).
2. **Code Quality Checks** lints the private-addon diff.
3. **Test** builds the image and installs `customer` with tests enabled for private addons.
4. **Docker Build** is mainly for pushes to the long-lived branches (or a manual run), not every PR.

A green PR means: the image builds, our modules install, our tagged tests (if any) passed, and the changed private-addon files meet the formatter and pylint-odoo rules for that Odoo version.
