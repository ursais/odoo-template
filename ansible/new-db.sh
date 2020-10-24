#!/bin/bash

OLD_PWD=$PWD
cd `dirname $0`
echo "Loading new backup..."
ansible-playbook new-db.yml \
  --extra-vars ""
cd $OLD_PWD
exit 0
