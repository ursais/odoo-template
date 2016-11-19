# Template Project

Template for an Odoo project

# Prerequisites

For Ursa employees, run the `Install` Job on Jenkins. Otherwise look at the INSTALL file.

# Build your development environment

`$ ./dev.sh`

and start Odoo

`$ ./env/bin/odoo -c dev.conf`

# Deploy to an environment

For Ursa employees, run the `<Project>_Deploy` Job on Jenkins. Otherwise:

* Pull the repo

`$ git pull`

* Update the environment

`$ . env/bin/activate && pip install -r requirements.txt`

* Restart Odoo

`# service odoo restart`