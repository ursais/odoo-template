# Odoo Template Project

## Table of Contents
* [Prerequisites](#Prerequisites)
* [Configuration](#Configuration)
* [Build your development environment](#Build-your-development-environment)
	* [For custom module](#For-custom-module)
	* [For contributed module](#For-contributed-module)
* [Deploy to an environment](#Deploy-to-an-environment)
* [Tests](#Tests)
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

## Issues

Report any issue to this
[Github project](https://github.com/ursais/odoo-template/issues).

## Roadmap

* Push the production database to the other environments
