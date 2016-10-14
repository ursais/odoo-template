# Template Project

Template for an Odoo project

# Prerequisites

On Ubuntu 16.04

* Install docker-engine and docker-compose: https://docs.docker.com/engine/installation/linux/ubuntulinux/

# Build your development environment

`$ ./dev.sh`

and start Odoo

`$ ./env/bin/odoo -c dev.conf`

# Build your production environment

```
$ docker build -t odoo odoo
$ docker build -t nginx nginx
```

# Push your production environment to the production server

On the building system:

```
$ docker save odoo | gzip > odoo.tgz
$ docker save nginx | gzip > nginx.tgz
$ scp odoo.tgz nginx.tgz root@$SERVER:/tmp/.
```

On the production system:

```
$ gzcat /tmp/odoo.tgz | docker load
$ gzcat /tmp/nginx.tgz | docker load
```

# Start the production environment

`$ docker-compose up`