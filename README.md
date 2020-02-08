# Odoo Template Project

This repository is a template repository meant to be copied for your Odoo project.
It contains:

* Dockerfile: The Docker file to build the Odoo image
* docker-compose.yml: The composition to run Odoo and PostgreSQL
* helm: The structure to generate the Helm package
* openshift: The structure with the OpenShift templates

## Process

### New Project

* Create a new repository `odoo-project` on Github or Gitlab
* Clone this repository and push it to `odoo-project`
* Create the project in your cluster
```shell script
helm install odoo-project ./helm
```

###  New version

* Add new repositories

```shell script
git submodule add --name web -b 13.0 https://github.com/OCA/web.git src/web
```
* Make changes to the modules in `/src`
* Test locally with:

```shell script
docker-compose up
```

* Commit your changes
* Push them to the repository
* Create a pull/merge request to the master branch

## Roadmap

* Add a BuildConfig, ImageStream, etc. to monitor the repository, run tests and build a test instance in the cluster
* Add an Operator to upgrade the production instance
