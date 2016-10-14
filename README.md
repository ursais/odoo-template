# Template Project

Template for an Odoo project

# Prerequisites

On Ubuntu 16.04

* Install docker-engine and docker-compose: https://docs.docker.com/engine/installation/linux/ubuntulinux/

# Build your development environment

`$ ./dev.sh`

and Start Odoo

`$ ./env/bin/odoo -c dev.conf`

# Build your production environment

`$ docker build -t odoo .`

# Push your production environment to the production server

On the building system:

```
$ docker save odoo | gzip > odoo.tar.gz
$ scp odoo.tar.gz root@$SERVER:/tmp/.
```

On the production system:

`$ gzcat /tmp/odoo.tar.gz | docker load`

# Start PostgreSQL and Odoo

`$ docker-compose up`