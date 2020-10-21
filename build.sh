#!/bin/bash

# Clone submodules
git submodule sync
git submodule update --init --depth=1

# Create the virtual environment if it does not exist
[ ! -d env ] && python3 -m venv env

# Activate the env and get the requirements
. env/bin/activate
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt

# Get Odoo version
BRANCH=`grep branch .gitmodules | cut  -d '=' -f 2 | sed -e 's/ //'`
VERSION=`echo $BRANCH | cut -d . -f 1`

# Build ADDONS_PATH
ADDONS_PATH=$PWD/src/custom-addons,$PWD/odoo/addons
if [ -d src ]; then
	cd src
	for i in `ls -d */ | cut -f1 -d'/'`; do
		if [ $i == "enterprise" ] ; then
			export ADDONS_PATH=$PWD/enterprise,$ADDONS_PATH
		else
			export ADDONS_PATH=$ADDONS_PATH,$PWD/$i
		fi
	done
	cd ..
fi

# Create the Odoo configuration file for the dev environment
cat > odoo.conf << EOF
[options]
addons_path=$ADDONS_PATH
db_user=odoo$VERSION
EOF

exit 0
