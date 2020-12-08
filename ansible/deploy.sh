#!/bin/bash

if [ ! -n "$3" ]; then
  cat << EOF
    Usage:
        $0 {database} {version} [rollback]
    where:
        - database is the database to copy to and/or upgrade: DEV
        - version is the target version
        - rollback is optional
    Examples:
        $0 DB 14.0 false     # to upgrade to 14.0
        $0 DB 14.0 true      # to rollback to 14.0
EOF
  exit 1
fi

OLD_PWD=$PWD
DATABASE=$1
VERSION=$2
ROLLBACK=$3

cd `dirname $0`

if [ "$ROLLBACK" == 'false' ]; then
  echo "Upgrade to $VERSION..."
  ansible-playbook deploy.yml \
    --extra-vars "database=$DATABASE db_version=$VERSION"
else
  echo "Rollback to $VERSION..."
  ansible-playbook deploy.yml \
    --extra-vars "database=$DATABASE git_tag=$VERSION"
fi

cd $OLD_PWD

exit 0
