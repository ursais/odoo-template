# OSI - PM System

## Table of Contents
* [Installation](#Installation)
* [Setup your development environment](#Setup-your-development-environment)
* [How to make changes](#How-to-make-changes)
	* [Add a submodule](#Add-a-submodule)
	* [Add an open pull request](#Add-an-open-pull-request)
* [How to build](#How-to-build)
* [How to test](#How-to-test)
* [How to publish](#How-to-publish)
* [How to release](#How-to-release)
* [Issues](#Issues)
* [Roadmap](#Roadmap)

## Installation

See [INSTALL](./INSTALL.md).

## Setup your development environment

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

## How to make changes

### Add a submodule

Add a new repository
```shell script
git submodule add --name web -b 12.0 https://github.com/OCA/web.git odoo/src/web
```
Add your module in `Dockerfile`

Add the modules in the `__manifest__.py` of one of the modules in `odoo/src/private-addons`

### Add an open pull request

Update the URL of the submodule `.gitmodules` to point to the `ursais` repository

Add your open pull requests in the file `repos.yml`

Update the target branch for each submodule

Run the following command to build a consolidated branch:
```shell script
gitaggregate -c repos.yml -p -j 5
```

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

## Issues

Report any issue to this [Github project](https://github.com/ursais/template-project/issues).

## Roadmap

* Create the database and load the data
* Upgrade an instance
* Push the production database to the other environments
