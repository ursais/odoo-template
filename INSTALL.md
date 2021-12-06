# Installation

* Install the prerequisites
```shell
apt install git docker docker-compose python3-pip python3-venv
```
* Clone the repo
```shell
git clone git@github.com:opensourceintegrators/odoo-template.git
```
* Run
```shell
cd odoo-template
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
pre-commit install
```
