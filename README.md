# Odoo Template Project

## Table of Contents
* [Prerequisites](#Prerequisites)
* [Build your environment](#Build-your-environment)
	* [For private modules](#For-private-modules)
	* [For existing public modules](#For-existing-public-modules)
	* [For new public modules](#For-new-public-modules)
* [Deploy](#Deploy)
* [Tests](#Tests)
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
* Add the repo as a submodule:
```shell
git submodule add --name repo -b 14.0 https://github.com/ursais/repo.git odoo/src/repo
```
* Create a new branch in odoo/src/<repo> and add your module
* Commit your changes and push your module to Github
* In Github (https://github.com/ursais), create a pull request against the corresponding OCA repository
* Add a section (1 per repo) in `repos.yml` and include your pull request
* Run Git Aggregator:
```shell
gitaggregate -c repos.yml -p -j 10
```
* Add your module as a dependency of the customer module
* Add your module in `odoo/Dockerfile`
* Commit, push your branch and create a pull request against `master`

## Deploy

Look at the [helm/README.md](./helm/README.md) file.

## Tests

* For functional tests using Selenium, please go to [odoo/tests/selenium](./odoo/tests/selenium).
* For performance tests using Locust, please go to [odoo/tests/locust](./odoo/tests/locust).

## Issues

Report any issue to this
[Github project](https://github.com/ursais/odoo-template/issues).
