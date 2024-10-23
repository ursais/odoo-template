FROM public.ecr.aws/t4c3a5h0/odoo-base:18.0-test-20241022
MAINTAINER Open Source Integrators <support@opensourceintegrators.com>

# Copy files
COPY --chown=odoo setup.py /odoo/
COPY --chown=odoo migration.yml /odoo/
COPY --chown=odoo requirements.txt /odoo/
COPY --chown=odoo songs /odoo/songs

# Copy Addons
# COPY src/paid-addons /odoo/addons/
# COPY --chown=odoo src/l10n-mexico /odoo/addons/
COPY src/enterprise /odoo/addons/

RUN cd /odoo && pip3 install -r requirements.txt --break-system-packages
