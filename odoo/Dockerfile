FROM ursa/odoo-14.0:latest
MAINTAINER Open Source Integrators <support@opensourceintegrators.com>

# Copy files
COPY setup.py /odoo/
COPY migration.yml /odoo/
COPY requirements.txt /odoo/

# Copy Odoo
COPY odoo /odoo/odoo/
# Copy Addons
# COPY src/paid-addons /odoo/addons/
COPY src/private-addons /odoo/addons/
# COPY src/enterprise /odoo/addons/
COPY src/web/web_environment_ribbon /odoo/addons/web_environment_ribbon

COPY songs /odoo/songs

RUN cd /odoo && pip3 install -r requirements.txt
RUN chown -R odoo /odoo

USER odoo
