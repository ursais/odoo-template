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

Create SSH keys for the project to clone and pull the repository
```shell script
ssh-keygen -C "openshift-source-builder/osi-erp@github" -f github-osi-erp -N ''
```
Add the public key in the [Deploy Keys of the repository](https://github.com).

## Dev environment

Create the project:
```shell script
oc new-project osi-pm-dev --display-name="OSI PM Dev"
```
Add the private key
```shell script
oc create secret generic github-osi-erp \
    --from-file=ssh-privatekey=github-osi-erp \
    --type=kubernetes.io/ssh-auth
```
Allow the builder to use it:
```shell script
oc secrets link builder github-osi-erp
```
Add permissions to the default Service Account of the project:
```shell script
oc adm policy add-scc-to-user anyuid -z default
oc adm policy add-scc-to-user privileged -z default
```
Edit the variables in helm/odoo/values.yaml

Run
```shell script
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
oc new-project osi-pm-test --display-name="OSI PM Test"
```
Add permissions to the default Service Account of the project:
```shell script
oc adm policy add-scc-to-user anyuid -z default
oc adm policy add-scc-to-user privileged -z default
oc policy add-role-to-user \
    system:image-puller system:serviceaccount:osi-pm-test:default \
    --namespace=osi-pm-dev
```
Edit the variables in helm/odoo/values.test.yaml

Run
```shell script
helm install odoo -f values.test.yaml helm/odoo
```

## QA environment

Create the project:
```shell script
oc new-project osi-pm-qa --display-name="OSI PM QA"
```
Add permissions to the default Service Account of the project:
```shell script
oc adm policy add-scc-to-user anyuid -z default
oc adm policy add-scc-to-user privileged -z default
oc policy add-role-to-user \
    system:image-puller system:serviceaccount:osi-pm-qa:default \
    --namespace=osi-pm-dev
```
Edit the variables in helm/odoo/values.qa.yaml

Run
```shell script
helm install odoo -f values.qa.yaml helm/odoo
```

## Production environment

Create the project:
```shell script
oc new-project osi-pm --display-name="OSI PM Production"
```
Add permissions to the default Service Account of the project:
```shell script
oc adm policy add-scc-to-user anyuid -z default
oc adm policy add-scc-to-user privileged -z default
oc policy add-role-to-user \
    system:image-puller system:serviceaccount:osi-pm:default \
    --namespace=osi-pm-dev
```
Edit the variables in helm/odoo/values.production.yaml

Run
```shell script
helm install odoo -f values.production.yaml helm/odoo
```
