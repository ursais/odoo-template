#!/bin/bash

# Create the virtual environment if it does not exist
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
    REPO_DIR=`echo $REPO | cut -d "/" -f 2 | sed -e 's/\.git//g'`
    [ ! -d $REPO_DIR ] && git clone $REPO -b $BRANCH
    ADDONS_PATH=$ADDONS_PATH,$PWD/`echo $REPO_DIR`
done
cd ..
[ -d enterprise ] && ADDONS_PATH=$PWD/enterprise,$ADDONS_PATH

# Create the Odoo configuration file for the dev environment
cat > dev.conf << EOF
[options]
addons_path=$ADDONS_PATH
db_user=odoo10
EOF

exit 0
