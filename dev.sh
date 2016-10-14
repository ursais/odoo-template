#!/bin/bash

# Create the virtuale env if it doesn not exist
[ ! -d env ] && virtualenv env
[ ! -d src ] && mkdir src

# Activate the env and get the requirements
. env/bin/activate
pip install -r odoo/requirements.txt

# Get Odoo version
BRANCH=`grep ursa/odoo odoo/Dockerfile | cut -d : -f 2 | cut -d - -f 1`

ADDONS_PATH=$PWD/odoo/custom-addons
cd src

# Clone repositories
for REPO in `cat ../repo.list`
do
    git clone $REPO -b $BRANCH
    ADDONS_PATH=$ADDONS_PATH,$PWD/`echo $REPO | cut -d "/" -f 2`
done

# Create the Odoo configuration file for the dev environment
cd ..
cat > dev.conf << EOF
[options]
addons_path=$ADDONS_PATH
db_host=localhost
db_port=5432
db_user=odoo10
EOF

exit 0