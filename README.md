# Template for an Odoo 14 Project

## Table of Contents
* [Prerequisites](#Prerequisites)
* [Build your environment](#Build-your-environment)
	* [Addon farms](#Addon-farms)
	* [For private modules](#For-private-modules)
	* [For existing public modules](#For-existing-public-modules)
	* [For new public modules](#For-new-public-modules)
* [Deploy](#Deploy)
* [Tests](#Tests)
* [Environment Variables](#Environment-Variables)
* [Issues](#Issues)

## Prerequisites

Look at the [INSTALL](./INSTALL.md) file.

## Build your environment

Go to the root directory of the cloned Github repository and run:
```shell script
docker-compose build
```

To start Odoo:
```shell script
docker-compose up
```

### Addon farms

`odoo/src/addons.manifest.yml` is the include list for modules copied from larger checkouts. `odoo/src/sync-addons.sh` is the only script that materializes it; it copies modules and never creates symlinks.

* Odoo core is included at `odoo/odoo` for standalone installs (`odoo/odoo/odoo-bin` and `odoo/odoo/addons` on `addons_path`). Docker images already ship Odoo, so containers do not use this tree.
* `enterprise/`, `paid-addons/`, and `private-addons/` are always included and are not listed in the manifest. The sync script skips any of these trees that are absent, so a project without Enterprise still builds. Projects entitled to Enterprise add it as a submodule:
```shell
git submodule add --name enterprise -b 14.0 https://github.com/ursais/enterprise.git \
  odoo/src/enterprise
```
* OCA checkouts live under `odoo/src/public-submodules/` and are listed under `public:` in the manifest.
* GML checkouts live under `odoo/src/gml-submodules/` and are listed under `gml:` in the manifest.
* `public-addons/` and `gml-addons/` are generated copies and are gitignored. Run the sync script after cloning, updating submodules, or changing the manifest.

For a standalone environment, run `odoo/src/sync-addons.sh`, then include `odoo/odoo/addons`, `src/enterprise`, `src/paid-addons`, `src/private-addons`, `src/public-addons`, and `src/gml-addons` in `addons_path`.

For containers, the Dockerfile runs `sync-addons.sh --dest /odoo/addons`. Adding a module does not require a Dockerfile change.

### For private modules

* Create a new branch and add your module in odoo/src/private-addons
* Add your module as a dependency of the customer module
* Commit, push your branch and create a pull request against `master`

### For existing public modules

Modules must be available on [Pypi](https://pypi.org), otherwise look at [the next section](#For-new-public-modules).

* Create a new branch
* Add the module in `odoo/requirements.txt`
* Add the module as a dependency of the customer module
* Commit, push your branch and create a pull request against `master`

### For new public modules

* In Github, fork the repo in the `ursais` organization
* Add the repo as a submodule under `odoo/src/public-submodules/` (or `odoo/src/gml-submodules/` for GML):
```shell
git submodule add --name repo -b 14.0 https://github.com/ursais/repo.git \
  odoo/src/public-submodules/repo
```
* Create a new branch in the submodule and add your module
* Commit your changes and push your module to Github
* In Github (https://github.com/ursais), create a pull request against the corresponding OCA repository
* Add a section (1 per repo) in `repos.yml` and include your pull request
* Run Git Aggregator:
```shell
gitaggregate -c repos.yml -p -j 10
```
* Add your module path to `odoo/src/addons.manifest.yml` (`public:` or `gml:`)
* Add your module as a dependency of the customer module
* Run `odoo/src/sync-addons.sh`
* Commit, push your branch and create a pull request against `master`

## Deploy

Look at the [helm/README.md](./helm/README.md) file.

## Tests

* For functional tests using Selenium, please go to [odoo/tests/selenium](./odoo/tests/selenium).
* For performance tests using Locust, please go to [odoo/tests/locust](./odoo/tests/locust).

## Environment Variables

Description: Environment variables
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `RUNNING_ENV` | Set to replicate what type of migration will occur options are production(create, migrate), qa(upgrade_existing,duplicate), test(upgrade_existing,duplicate), dev(drop latest, create, migrate), anything else for not triggering migration | `dev` |
| `PLATFORM`                    | Used to identify the cloud provider: aws, azure, do or local | `do`          |
| `APP_IMAGE_VERSION`           | Used to set the version of the image               | `latest` |
| `DEBUG`                       | Display debugging information if set to 1          |          |

Description: A list of variables that have default values when not set in docker-compose.yml.
These environment variables can be altered to directly impact configurations of the build when using docker-compose up

| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `ODOO_ADDONS_PATH`            | Value set in odoo.conf for: addons_path            | `/odoo/addons`                        |
| `ODOO_ADMIN_PASSWD`           | Value set in odoo.conf for: admin_passwd           | `admin`                               |
| `ODOO_CSV_INTERNAL_SEP`       | Value set in odoo.conf for: csv_internal_sep       | `,`                                   |
| `ODOO_DATA_DIR`               | Value set in odoo.conf for: data_dir               | `/odoo/data`                          |
| `ODOO_DBFILTER`               | Value set in odoo.conf for: dbfilter               | `^[^backup\|defaultdb].*$`            |
| `PGHOST`                      | Value set in odoo.conf for: db_host                | `db`                                  |
| `ODOO_DB_MAXCONN`             | Value set in odoo.conf for: db_maxconn             | `64`                                  |
| `PGDATABASE`                  | Value set in odoo.conf for: db_name                | `False`                               |
| `PGPASSWORD`                  | Value set in odoo.conf for: db_password            | `odoo`                                |
| `PGPORT`                      | Value set in odoo.conf for: db_port                | `5432`                                |
| `PGSSLMODE`                   | Value set in odoo.conf for: db_sslmode             | `prefer`                              |
| `ODOO_DB_TEMPLATE`            | Value set in odoo.conf for: db_template            | `template0`                           |
| `PGUSER`                      | Value set in odoo.conf for: db_user                | `odoo`                                |
| `ODOO_DEMO`                   | Value set in odoo.conf for: demo                   | `{}`                                  |
| `ODOO_EMAIL_FROM`             | Value set in odoo.conf for: email_from             | `False`                               |
| `ODOO_GEOIP_DATABASE`         | Value set in odoo.conf for: geoip_database         | `/usr/share/GeoIP/GeoLite2-City.mmdb` |
| `ODOO_HTTP_ENABLE`            | Value set in odoo.conf for: http_enable            | `True`                                |
| `ODOO_HTTP_INTERFACE`         | Value set in odoo.conf for: http_interface         |                                       |
| `ODOO_IMPORT_PARTIAL`         | Value set in odoo.conf for: import_partial         |                                       |
| `ODOO_LIMIT_MEMORY_HARD`      | Value set in odoo.conf for: limit_memory_hard      | `4294967296`                          |
| `ODOO_LIMIT_MEMORY_SOFT`      | Value set in odoo.conf for: limit_memory_soft      | `2147483648`                          |
| `ODOO_LIMIT_REQUEST`          | Value set in odoo.conf for: limit_request          | `8192`                                |
| `ODOO_LIMIT_TIME_CPU`         | Value set in odoo.conf for: limit_time_cpu         | `1800`                                |
| `ODOO_LIMIT_TIME_REAL_CRON`   | Value set in odoo.conf for: limit_time_real_cron   | `120`                                 |
| `ODOO_LIMIT_TIME_REAL`        | Value set in odoo.conf for: limit_time_real        | `1800`                                |
| `ODOO_LIST_DB`                | Value set in odoo.conf for: list_db                | `False`                               |
| `ODOO_LOG_DB`                 | Value set in odoo.conf for: log_db                 | `False`                               |
| `ODOO_LOG_DB_LEVEL`           | Value set in odoo.conf for: log_db_level           | `warning`                             |
| `ODOO_LOGFILE`                | Value set in odoo.conf for: logfile                | `None`                                |
| `ODOO_LOG_HANDLER`            | Value set in odoo.conf for: log_handler            | `:INFO`                               |
| `ODOO_LOG_LEVEL`              | Value set in odoo.conf for: log_level              | `info`                                |
| `ODOO_LOGROTATE`              | Value set in odoo.conf for: logrotate              | `False`                               |
| `ODOO_MAX_CRON_THREADS`       | Value set in odoo.conf for: max_cron_threads       | `1`                                   |
| `ODOO_OSV_MEMORY_COUNT_LIMIT` | Value set in odoo.conf for: osv_memory_count_limit | `False`                               |
| `ODOO_PG_PATH`                | Value set in odoo.conf for: pg_path                |                                       |
| `ODOO_PIDFILE`                | Value set in odoo.conf for: pidfile                |                                       |
| `ODOO_PROXY_MODE`             | Value set in odoo.conf for: proxy_mode             | `True`                                |
| `ODOO_REPORTGZ`               | Value set in odoo.conf for: reportgz               | `False`                               |
| `ODOO_SCREENCASTS`            | Value set in odoo.conf for: screencasts            | `False`                               |
| `ODOO_SCREENSHOTS`            | Value set in odoo.conf for: screenshots            | `/tmp/odoo_tests`                     |
| `ODOO_SERVER_WIDE_MODULES`    | Value set in odoo.conf for: server_wide_modules    | `web,monitoring_status`               |
| `ODOO_SMTP_PASSWORD`          | Value set in odoo.conf for: smtp_password          | `False`                               |
| `ODOO_SMTP_PORT`              | Value set in odoo.conf for: smtp_port              | `25`                                  |
| `ODOO_SMTP_SERVER`            | Value set in odoo.conf for: smtp_server            | `localhost`                           |
| `ODOO_SMTP_SSL`               | Value set in odoo.conf for: smtp_ssl               | `False`                               |
| `ODOO_SMTP_USER`              | Value set in odoo.conf for: smtp_user              | `False`                               |
| `ODOO_SYSLOG`                 | Value set in odoo.conf for: syslog                 | `False`                               |
| `ODOO_TEST_ENABLE`            | Value set in odoo.conf for: test_enable            | `False`                               |
| `ODOO_TEST_FILE`              | Value set in odoo.conf for: test_file              |                                       |
| `ODOO_TEST_TAGS`              | Value set in odoo.conf for: test_tags              | `None`                                |
| `ODOO_TRANSLATE_MODULES`      | Value set in odoo.conf for: translate_modules      | `['all']`                             |
| `ODOO_TRANSIENT_AGE_LIMIT`    | Value set in odoo.conf for: transient_age_limit    | `1.0`                                 |
| `ODOO_UNACCENT`               | Value set in odoo.conf for: unaccent               | `False`                               |
| `ODOO_UPGRADE_PATH`           | Value set in odoo.conf for: upgrade_path           |                                       |
| `ODOO_WITHOUT_DEMO`           | Value set in odoo.conf for: without_demo           | `all`                                 |
| `ODOO_WORKERS`                | Value set in odoo.conf for: workers                | `3`                                   |
| `ODOO_XMLRPC_INTERFACE`       | Value set in odoo.conf for: xmlrpc_interface       |                                       |

Description: Environment variables related to the Odoo filestore and Rclone
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `PLATFORM`                    | Used to identify the cloud provider: aws, azure, do or local | `do`|
| `AWS_HOST`                    | Value for Aws host URL                             | `false` |
| `AWS_REGION`                  | Set value if using AWS platform for cloud filestore          |               |
| `AWS_ACCESS_KEY_ID`           | Access key set for connection to AWS cloud filestore bucket  |               |
| `AWS_SECRET_ACCESS_KEY`       | Secret key set for connection to AWS cloud filtestore bucket |               |
| `AZURE_STORAGE_CONNECTION_STRING` | Value for Azure connection string              | `false` |
| `AZURE_STORAGE_ACCOUNT_URL`   | Set value if using azure platform for cloud filestore        |               |
| `AZURE_STORAGE_ACCOUNT_KEY`   | Value for Azure storage account key                | `false` |
| `AWS_DUPLICATE`               | Set value to true to duplicate filestore with database       |               |
| `AWS_EMPTY_ON_DBDROP`         | Set value to true to remove contents from filestore bucket when dropping db |              |

Description: Environment variables related to PostgreSQL client
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `PGHOST`                      | Value set in odoo.conf for: db_host                | `db`                                  |
| `PGPORT`                      | Value set in odoo.conf for: db_port                | `5432`                                |
| `PGUSER`                      | Value set in odoo.conf for: db_user                | `odoo`                                |
| `PGPASSWORD`                  | Value set in odoo.conf for: db_password            | `odoo`                                |
| `PGDATABASE`                  | Value set in odoo.conf for: db_name                | `False`                               |
| `PGSSLMODE`                   | Value set in odoo.conf for: db_sslmode             | `prefer`                              |

Description: Environment variables related to Marabunta (migration.yml)
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `RUNNING_ENV` | Set to replicate what type of migration will occur options are production(create, migrate), qa(upgrade_existing,duplicate), test(upgrade_existing,duplicate), dev(drop latest, create, migrate), anything else for not triggering migration | `dev` |
| `APP_IMAGE_VERSION`           | Used to set a custom database name on migration    | `latest` |
| `MARABUNTA_MODE`              | The mode controls what operations should occur based off its value of external(serverside) or base(General) | `base` |
| `MARABUNTA_ALLOW_SERIE`       | Allows multiple versions to upgrade                | `false`  |
| `MARABUNTA_FORCE_VERSION`     | Force a specific version to be re-ran              |          |

Description: Environment variables related to Anthem (songs)
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `ODOO_DATA_PATH`              | Set the path to the csv files                      | `/odoo/songs/data`                    |

## Issues

Report any issue to this
[Github project](https://github.com/ursais/odoo-template/issues).
