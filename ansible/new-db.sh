#!/bin/bash

if [ ! -n "$0" ]; then
  cat << EOF
Replace the BACKUP db and filestore with the local backup.
Usage:
    $0
EOF
  exit 1
fi

echo "Loading new BACKUP..."

ansible-playbook new-db.yml

exit 0
