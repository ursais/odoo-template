# Installation of OSI - PM System

## Table of Contents
* [Requirements](#Requirements)
* [Dev environment](#Dev-environment)
  * [On Github](#On-Github)
* [Test environment](#Test-environment)
* [QA environment](#QA-environment)
* [Production environment](#Production-environment)


## Requirements

Create a new repository `odoo-project` on Github or Gitlab

Clone this repository and push it to `odoo-project`

## Dev environment

Create the project:
```shell script
oc new-project odoo-project-dev --display-name="Odoo Project Dev"
```
Add permissions to the default Service Account of the project:
```shell script
oc adm policy add-scc-to-user anyuid -z default
oc adm policy add-scc-to-user privileged -z default
```
Edit the variables in helm/odoo/values.yaml

Run
```shell script
helm dependency update helm/odoo
helm install odoo helm/odoo
```
Go to the Build Config `odoo` on the [console](https://console-openshift-console.apps.do1.ursasys.net)

Click on `Copy URL with Secret`.

### On Github

Go to the repository, then Settings > Webhooks > Add webhook.

Paste the URL into `Payload URL`.

Change the `Content Type` to `application/json`.

Click `Add webhook`.

## Test environment

Create the project:
```shell script
oc new-project odoo-project-test --display-name="Odoo Project Test"
```
Add permissions to the default Service Account of the project:
```shell script
oc adm policy add-scc-to-user anyuid -z default
oc adm policy add-scc-to-user privileged -z default
oc policy add-role-to-user \
    system:image-puller system:serviceaccount:odoo-project-test:default \
    --namespace=odoo-project-dev
```
Edit the variables in helm/odoo/values.test.yaml

Run
```shell script
helm install odoo -f helm/odoo/values.test.yaml helm/odoo
```

## QA environment

Create the project:
```shell script
oc new-project odoo-project-qa --display-name="Odoo Project QA"
```
Add permissions to the default Service Account of the project:
```shell script
oc adm policy add-scc-to-user anyuid -z default
oc adm policy add-scc-to-user privileged -z default
oc policy add-role-to-user \
    system:image-puller system:serviceaccount:odoo-project-qa:default \
    --namespace=odoo-project-dev
```
Edit the variables in helm/odoo/values.qa.yaml

Run
```shell script
helm install odoo -f helm/odoo/values.qa.yaml helm/odoo
```

## Production environment

Create the project:
```shell script
oc new-project odoo-project --display-name="Odoo Project Production"
```
Add permissions to the default Service Account of the project:
```shell script
oc adm policy add-scc-to-user anyuid -z default
oc adm policy add-scc-to-user privileged -z default
oc policy add-role-to-user \
    system:image-puller system:serviceaccount:odoo-project:default \
    --namespace=odoo-project-dev
```
Edit the variables in helm/odoo/values.production.yaml

Run
```shell script
helm install odoo -f helm/odoo/values.production.yaml helm/odoo
```
