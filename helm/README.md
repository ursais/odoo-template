# Odoo Deployment

## Table of Contents
* [Environment Variables](#Environment-Variables)
* [Development environment](#Development-environment)
* [Test environment](#Test-environment)
* [QA environment](#QA-environment)
* [Production environment](#Production-environment)
* [Secrets](#Secrets)
* [Release](#Release)
* [Known issues](#Known-issues)

## Environment Variables

Description: Environment variables
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `RUNNING_ENV` | Set to replicate what type of migration will occur options are production(create, migrate), qa(upgrade_existing,duplicate), test(upgrade_existing,duplicate), dev(drop latest, create, migrate), anything else for not triggering migration | `dev` |
| `PLATFORM`                    | Used to identify the cloud provider: aws, azure, do or local | `do`          |
| `APP_IMAGE_VERSION`           | Used to set the version of the image               | `latest` |

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


Description: Environment variables that are related to configuring Odoo filestore and Rclone
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `PLATFORM`                    | Used to identify the cloud provider: aws, azure, do or anything else for local filestore | `do`          |
| `AWS_HOST`                    | Set value if using S3 storage for cloud filestore          |               |
| `AWS_REGION`                  | Set value if using S3 storage for cloud filestore          |               |
| `AWS_ACCESS_KEY_ID`           | Access key set for connection to S3 bucket                 |               |
| `AWS_SECRET_ACCESS_KEY`       | Secret key set for connection to S3 bucket                 |               |
| `AWS_BUCKETNAME`              | Set value if using S3 storage for cloud filestore          |               |
| `AZURE_STORAGE_CONNECTION_STRING` | Value for Azure connection string              | `false` |
| `AZURE_STORAGE_ACCOUNT_URL`   | Set value if using Azure Blob Storage for cloud filestore  |               |
| `AZURE_STORAGE_ACCOUNT_KEY`   | Value for Azure storage account key                | `false` |

Description: Environment variables related to PostgreSQL client
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `PGHOST`                      | Value set in odoo.conf for: db_host                | `db`                                  |
| `PGPORT`                      | Value set in odoo.conf for: db_port                | `5432`                                |
| `PGUSER`                      | Value set in odoo.conf for: db_user                | `odoo`                                |
| `PGPASSWORD`                  | Value set in odoo.conf for: db_password            | `odoo`                                |
| `PGDATABASE`                  | Value set in odoo.conf for: db_name                | `False`                               |
| `PGSSLMODE`                   | Value set in odoo.conf for: db_sslmode             | `prefer`                              |

Description: Environment variables related to Marabunta
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `MARABUNTA_MODE`              | The mode controls what operations should occur based off its value of external(serverside) or base(General) | `base` |
| `MARABUNTA_ALLOW_SERIE`       | Allows multiple versions to upgrade                | `false`  |
| `MARABUNTA_FORCE_VERSION`     | Force a specific version to be re-ran              |          |

Description: Environment variables related to Anthem
| Name                          | Description                                        | Default Value                         |
| ----------------------------- | -------------------------------------------------- | ------------------------------------- |
| `ODOO_DATA_PATH`              | Path to the folder containing csv files            | `/odoo/songs/data` |


## Development environment

Create the project:
```shell script
kubectl create namespace odoo-dev
```
Edit the variables in helm/odoo/values.yaml

Run
```shell script
helm dependency update helm/odoo
helm upgrade --install odoo helm/odoo
```

## Test environment

Create the project:
```shell script
kubectl create namespace odoo-test
```
Edit the variables in helm/odoo/values.test.yaml

Run
```shell script
helm upgrade --install odoo -f helm/odoo/values.test.yaml helm/odoo
```

## QA environment

Create the project:
```shell script
kubectl create namespace odoo-qa
```
Edit the variables in helm/odoo/values.qa.yaml

Run
```shell script
helm upgrade --install odoo -f helm/odoo/values.qa.yaml helm/odoo
```

## Production environment

Create the project:
```shell script
kubectl create namespace odoo
```
Edit the variables in helm/odoo/values.production.yaml

Run
```shell script
helm upgrade --install odoo -f helm/odoo/values.production.yaml helm/odoo
```

## Secrets

The installation generates random values for confidential information like passwords,
tokens, keys, etc. You need to replace them with the value from the provider.

### External database

```shell
SECRET=`echo -n "PASSWORD" | base64`
kubectl edit secret odoo-externaldb
  data:
    db-password: $SECRET
```

### Storage

```shell
SECRET1=`echo -n "Account URL" | base64`
SECRET2=`echo -n "Connection string" | base64`
kubectl edit secret odoo
  data:
    azure-storage-account-url: $SECRET1
    azure-storage-connection-string: $SECRET2
```

## Release

Create a new release in the repository:
https://github.com/ursais/odoo-template/releases

Update the deployment:
```shell script
TAG=20210527
NAMESPACE=odoo-test
kubectl set image deploy odoo \
    odoo=docker.pkg.github.com/ursais/odoo-template/odoo-template:$TAG \
    --namespace $NAMESPACE
```

## Backup

Install Velero:
```shell
export BUCKET=velerobackup-<name>
export REGION=us-east-2
velero install \
    --provider aws \
    --use-restic \
    --plugins velero/velero-plugin-for-aws:v1.2.0 \
    --bucket $BUCKET \
    --backup-location-config region=$REGION \
    --snapshot-location-config region=$REGION \
    --secret-file ./helm/credentials-velero
```

Create schedules:
```shell
velero create schedule full-daily --schedule="@every 24h"
velero create schedule odoo-daily --schedule="@every 24h" --include-namespaces <name>-odoo
velero create schedule odoo-qa-daily --schedule="@every 24h" --include-namespaces <name>-odoo-qa
velero create schedule odoo-test-daily --schedule="@every 24h" --include-namespaces <name>-odoo-test
velero create schedule odoo-dev-daily --schedule="@every 24h" --include-namespaces <name>-odoo-dev
```

## Known issues

* https://github.com/bitnami/charts/issues/6121
  Upgrading the PostgreSQL helm chart regenerates the password in the secret and causes
  Odoo's connections to fail.
