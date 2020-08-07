# Odoo Template

## Table of Contents
* [Installation](#Installation)
* [Setup your environment](#Setup-your-environment)
* [How to contribute](#How-to-contribute)
	* [New Version](#New-Version)
	* [Add a new private module](#Add-a-new-private-module)
	* [Add an existing public module](#Add-an-existing-public-module)
	* [Add a new public module](#Add-a-new-public-module)
	* [Update data or configuration](#Update-data-or-configuration)
* [How to build](#How-to-build)
* [How to test](#How-to-test)
* [How to publish](#How-to-publish)
* [How to release](#How-to-release)
* [Tests](#Tests)
* [Issues](#Issues)
* [Roadmap](#Roadmap)

## Installation

See [INSTALL](./INSTALL.md).

## Setup your environment

Run
```shell script
sudo apt install python3-venv
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
pre-commit install
git submodule sync
git submodule update --init
```

## How to contribute

### New Version

* Bump the version in `odoo/setup.py`
* Create a directory `odoo/data/<version>`
* Create a file `odoo/songs/<version>.py`
* Add a new version section in `odoo/migration.yml`

### Add a new private module

* Add your module in `odoo/src/private-addons`
* Add your library in `odoo/requirements.txt`
* Add your module in the `__manifest__.py` of an existing module in `odoo/src/private-addons` (`customer` for example)
* Add `customer` in the version section in `odoo/migration.yml`

### Add an existing public module

* Add a new submodule (if not already there)
```shell script
git submodule add --name web -b 13.0 https://github.com/OCA/web.git odoo/src/web
```
* Add the module in `Dockerfile`
* Add the module in the `__manifest__.py` of one of the modules in `odoo/src/private-addons` (`customer` for example)
* Add `customer` in the version section in `odoo/migration.yml`

### Add a new public module

* Add a new submodule (if not already there)
```shell script
git submodule add --name web -b 13.0 https://github.com/OCA/web.git odoo/src/web
```
* Update the URL of the submodule `.gitmodules` to point to the `ursais` repository
* Add your pull request in the file `repos.yml`
* Run the following command to build a consolidated branch:
```shell script
gitaggregate -c repos.yml -p -j 5
```
* Add the module in `Dockerfile`
* Add the module in the `__manifest__.py` of one of the modules in `odoo/src/private-addons` (`customer` for example)
* Add the module in the version section in `odoo/migration.yml`

### Update data or configuration

* Add the csv files to load in `odoo/data/<version>`
* Update `odoo/songs/<version>.py` to load the csv files and/or change the configuration

## How to build

Build locally with:
```shell script
docker-compose build
```

## How to test

Test locally with:
```shell script
docker-compose up
```
and go to http://localhost:8069

## How to publish

Commit your changes

Push them to the repository

Create a pull/merge request to the master branch

## How to release

Tag an image in the stream:
```shell script
oc project odoo-project-dev
oc tag odoo:lastest odoo:20200701
```

Update the DeploymentConfig to change the tag:
```shell script
oc project odoo-project-test
oc edit dc odoo
        [...]
        kind: ImageStreamTag
        name: odoo:20200701
```

## Tests

* For functional tests using Selenium, please go to [tests/selenium](./tests/selenium).
* For performance tests using Locust, please go to [tests/locust](./tests/locust).

## Issues

Report any issue to this
[Github project](https://github.com/ursais/odoo-template/issues).

## Roadmap

* Push the production database to the other environments
