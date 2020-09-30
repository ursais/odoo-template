#!/bin/bash

echo "Loading new backup..."

ansible-playbook new-db.yml \
  --extra-vars ""

exit 0
