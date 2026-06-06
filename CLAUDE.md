# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an Odoo 19.0 project template maintained by Gray Matter Logic. It uses Docker for development, Marabunta for database migrations, Anthem (songs) for data initialization, and Helm for Kubernetes deployment.

## Development Commands

### Start the environment

```shell
docker-compose build
docker-compose up
```

Odoo is available at http://localhost:8069. MailHog (test email) at http://localhost:8025.

### Run pre-commit checks

```shell
pre-commit run --all-files
```

Pre-commit enforces: black (Python formatting), prettier (XML/JS/CSS/YAML), isort, flake8, pylint-odoo, and various file validators.

### Force a migration version to re-run

Set `MARABUNTA_FORCE_VERSION=setup` in docker-compose.yml (uncomment the line), then restart.

### Run Odoo tests for a module

```shell
docker-compose run --rm app odoo --test-enable --stop-after-init -d <dbname> -i <module_name>
```

Or set `ODOO_TEST_ENABLE=True` and `ODOO_TEST_TAGS=<tags>` as environment variables.

## Architecture

### Module organization

- **`odoo/src/private-addons/`** — Custom modules for this project. The `customer` module is the top-level dependency anchor; all other private modules should be listed as dependencies of `customer`.
- **`odoo/src/public-addons/`** — New OCA modules being contributed upstream; added as git submodules.
- **`odoo/src/osi-addons/`**, **`odoo/src/l10n-mexico/`**, **`odoo/src/pms/`** — External git submodules from OCA/ursais.
- **`odoo/src/amxodoo/`** — Additional addon directory (not a submodule).

### Adding modules

- **Private module**: Add to `odoo/src/private-addons/`, declare as dependency in `customer/__manifest__.py`.
- **Public module from PyPI**: Add to `odoo/requirements.txt`, add as dependency in `customer/__manifest__.py`.
- **New public module (not on PyPI)**: Fork repo into `ursais` org, `git submodule add` under `odoo/src/`, add to `odoo/Dockerfile`, add as dependency in `customer/__manifest__.py`. Use `repos.yml` + `gitaggregate` for merging pending PRs.

### Migration and data loading

- **`odoo/migration.yml`** — Marabunta configuration. Defines versioned migration steps. Each version can run pre/post shell commands and upgrade addon lists. The `setup` version runs Anthem songs for initial data load.
- **`odoo/songs/`** — Anthem data initialization scripts (Python). Entry points are `songs.setup.base::main` and `songs.setup.data::main`. Data CSV files go in `odoo/songs/data/`. These are packaged as `odoo-songs` via `odoo/setup.py`.

### Environment behavior

`RUNNING_ENV` controls migration behavior:
- `production`: creates DB and migrates; takes a backup snapshot before each version
- `qa`/`test`: upgrades existing DB and duplicates
- `dev`: drops latest DB, creates fresh, and migrates

`PLATFORM` sets the cloud filestore backend: `aws`, `azure`, `do`, or `local`.

### Helm / Kubernetes deployment

- **`helm/odoo/`** — Helm chart with per-environment values files (`values.yaml`, `values.test.yaml`, `values.qa.yaml`, `values.production.yaml`).
- Supports AWS, Azure, DigitalOcean, and local platforms for filestore.
- See `helm/README.md` for deployment instructions.

### Tests

- Functional/UI tests: `odoo/tests/selenium/`
- Performance tests: `odoo/tests/locust/`