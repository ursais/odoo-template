# Template Project

## Table of Contents
* [Prerequisites](#Prerequisites)
* [Configuration](#Configuration)
* [Build your development environment](#Build-your-development-environment)
	* [For custom module](#For-custom-module)
	* [For contributed module](#For-contributed-module)
* [Release](#Release)
	* [Init](#Init)
	* [New DB](#New-db)
	* [Deploy](#Deploy)
* [Tests](#Tests)
* [Issues](#Issues)


## Prerequisites

Look at the [INSTALL](./INSTALL.md) file.

## Configuration

* Add your version of Odoo, modules and Python dependencies in `requirements.txt`

## Build your development environment

`$ ./build.sh`

and start Odoo

`$ ./env/bin/odoo -c odoo.conf`

### For private module

* Create a new branch and add your module in src/custom-addons
* Add your module as a dependency of the customer module
* Push your branch and create a pull request against develop

### For public module

* Create a new branch in src/<repo> and add your module
* Commit your changes and push your module to Github
* In Github (http://github.com/ursais/repo), create a pull request against the corresponding public/OCA repository
* Update `repos.yml` with your pull request
* Run
```shell script
gitaggregate -c repos.yml -p -j 10
```
* Add your module as a dependency of the customer module
* Commit your changes, push your branch and create a pull request against develop

## Release

### Init

You can pass extra variables to the Ansible playbook in their corresponding script by.

new-db.sh:

* service: Name of the service to find the configuration file. By default "odoo".
* archives: Absolute path to find the backups (db dump and filestore tarball). By default "/home/odoo/archives".
* tarpath: Structure of the filestore tarball. By default "home/odoo/.local/share/Odoo/filestore/MASTER".

deploy.sh:

* odoodir: Odoo directory. By default "/opt/odoo".
* database: Database to upgrade/rollback. By default "MASTER".
* git_tag: Tag to rollback the source code to. By default "none".
* db_version: Version to upgrade to. Must match a filename in /ansible. By default "none".
* service: Name of the service to start/stop and to find the configuration file. By default "odoo".

### New DB

* Load a new backup from production
```shell script
/opt/odoo/ansible/new-db.sh
```

### Deploy

* Deploy a new version
```shell script
/opt/odoo/ansible/deploy.sh <DB> <VERSION> <ROLLBACK>
```
where

* <DB> is the database to copy to and/or upgrade: 20201027, 12.0-RC1
* <VERSION> is the target version: 12.0
* <ROLLBACK> whether to rollback or not: true, false

Examples:
```shell script
/opt/odoo/ansible/deploy.sh 20201027 12.0 false     # to upgrade to 12.0
/opt/odoo/ansible/deploy.sh 12.0-RC1 12.0 true      # to rollback to 12.0
```

## Tests

* For functional tests using Selenium, please go to [tests/selenium](./tests/selenium).
* For performance tests using Locust, please go to [tests/locust](./tests/locust).

## Issues

Report any issue to this
[Github project](https://github.com/ursais/odoo-template/issues).
