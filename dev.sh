#!/bin/bash

# Create the virtuale env if it doesn not exist
[ ! -d env ] && virtualenv env
[ ! -d src ] && mkdir src

# Activate the env and get the requirements
. env/bin/activate
pip install -r requirements.txt

# Get Odoo version
BRANCH=`grep -v "^#" requirements.txt | grep "nightly\.odoo\.com" | cut -d / -f 4`

# Clone repositories and build ADDONS_PATH
ADDONS_PATH=$PWD/custom-addons
cd src
for REPO in `grep -v "^#" ../repo.list`
do
    [ ! -d $REPO ] && git clone $REPO -b $BRANCH
    ADDONS_PATH=$ADDONS_PATH,$PWD/`echo $REPO | cut -d "/" -f 2`
done
cd ..
[ -d enterprise ] && ADDONS_PATH=$PWD/enterprise,$ADDONS_PATH

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