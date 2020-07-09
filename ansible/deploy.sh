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
        $0 DB 12.0-RC9 false     # to upgrade to 12.0-RC9
        $0 DB 12.0-RC9 true      # to rollback to 12.0-RC9
EOF
  exit 1
fi

DATABASE=$1
VERSION=$2
ROLLBACK=$3

if [ "$ROLLBACK" == 'false' ]; then
  echo "Upgrade to $VERSION..."
  ansible-playbook deploy.yml \
    --limit $CUSTOMER-$ENVIRONMENT \
    --extra-vars "database=$DATABASE db_version=$VERSION"
else
  echo "Rollback to $VERSION..."
  ansible-playbook deploy.yml \
    --extra-vars "database=$DATABASE git_tag=$VERSION"
fi

exit 0
