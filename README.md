# Odoo Template Project

## Table of Contents
* [Prerequisites](#Prerequisites)
* [Configuration](#Configuration)
* [Build your development environment](#Build-your-development-environment)
	* [For custom module](#For-custom-module)
	* [For contributed module](#For-contributed-module)
* [Deploy to an environment](#Deploy-to-an-environment)
* [Tests](#Tests)
* [Docker Compose environment variables](#Docker-Compose-environment-variables)
* [Issues](#Issues)
* [Roadmap](#Roadmap)

## Prerequisites

For Ursa employees, run the `Install` Job on Jenkins.
Otherwise look at the [INSTALL](./INSTALL.md) file.

## Configuration

* Add your version of Odoo, modules and Python dependencies in `requirements.txt`

## Build your development environment

Change the working directory to the cloned Github repository and run:

```shell script
$ ./build.sh`
```

To start an Odoo server:

```shell script
$ ./env/bin/odoo -c odoo.conf
```

### For custom module

* Create a new branch and add your module in src/custom-addons
* Add your module as a dependency of the customer module
* Push your branch and create a pull request against develop

### For contributed module

* Create a new branch in src/<repo> and add your module
* Create the setup directory

```
$ cd src/<repo>/setup
$ mkdir -p module_name/odoo/addons
$ ln -s ../module_name module_name/odoo/addons/.
$ vi module_name/setup.py
import setuptools

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    odoo_addon=True,
)
$ vi module_name/odoo/__init__.py
__import__('pkg_resources').declare_namespace(__name__)
$ cp module_name/odoo/__init__.py module_name/odoo/addons/__init__.py
```

* Commit your changes and push your module to Github
* In Github (http://github.com/ursais/repo), create a pull request against the corresponding OCA repository
* Add your module as a dependency of the customer module
* Push your branch and create a pull request against develop

## Deploy to an environment

For Ursa employees, run the `<Project>_Deploy` Job on Jenkins. Otherwise:

* Pull the repo

`$ git pull`

* Update the environment

`$ . env/bin/activate && pip install -r requirements.txt`

* Restart Odoo

`# service odoo restart`

## Tests

* For functional tests using Selenium, please go to [tests/selenium](./tests/selenium).
* For performance tests using Locust, please go to [tests/locust](./tests/locust).

### Docker Compose environment variables
Description: A list of variables that have default values when not set in docker-compose.yml.
These Environment variables can be altered to directly impact configurations of the build when using docker-compose up

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


Description: Environment variables that are related to configuring the Odoo filestore
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `AWS_ACCESS_KEY_ID`           | Access key set for connection to AWS cloud filestore bucket  |               |
| `AWS_SECRET_ACCESS_KEY`       | Secret key set for connection to AWS cloud filtestore bucket |               |
| `PLATFORM`                    | Used to identify the cloud provider: aws, azure, do or anything else for local filestore | `do`|
| `AZURE_STORAGE_ACCOUNT_URL`   | Set value if using azure platform for cloud filestore        |               |
| `AWS_REGION`                  | Set value if using AWS platform for cloud filestore          |               |

Description: Environment variables that are related to Additional database
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `AWS_HOST`                    | Value for Aws host URL                             | `false` |
| `AZURE_STORAGE_CONNECTION_STRING` | Value for Azure connection string              | `false` |
| `AZURE_STORAGE_ACCOUNT_KEY`   | Value for Azure storage account key                | `false` |

Description: Environment variabls related to Marabunta migrations (migration.yml)
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `RUNNING_ENV` | Set to replicate what type of migration will occur options are production(create, migrate), qa(upgrade_existing,duplicate), test(upgrade_existing,duplicate), dev(drop latest, create, migrate), anything else for not triggering migration | `dev` |
| `APP_IMAGE_VERSION`           | Used to set a custom database name on migration    | `latest` |
| `MARABUNTA_MODE`              | The mode controls what operations should occur based off its value of external(serverside) or base(General) | `base` |
| `MARABUNTA_ALLOW_SERIE`       | Allows multiple versions to upgrade                | `false`  |
| `MARABUNTA_FORCE_VERSION`     | Force a specific version to be re-ran              |          |


## Issues

Report any issue to this
[Github project](https://github.com/ursais/odoo-template/issues).

## Roadmap

* Update helm/odoo/templates/ingress.yaml rules and redirect
