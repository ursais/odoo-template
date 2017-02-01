# Template Project

Template for an Odoo project

# Prerequisites

For Ursa employees, run the `Install` Job on Jenkins. Otherwise look at the INSTALL file.

# Build your development environment

`$ ./dev.sh`

and start Odoo

`$ ./env/bin/odoo -c dev.conf`

## For custom module

* Create a new branch and add your module in custom-addons
* Add your module as a dependency of the customer module

## For contributed module

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
* Add your module in the requirements.txt
* Add your module as a dependency of the customer module

# Deploy to an environment

For Ursa employees, run the `<Project>_Deploy` Job on Jenkins. Otherwise:

* Pull the repo

`$ git pull`

* Update the environment

`$ . env/bin/activate && pip install -r requirements.txt`

* Restart Odoo

`# service odoo restart`
