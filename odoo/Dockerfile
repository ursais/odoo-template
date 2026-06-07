FROM ghcr.io/ursais/odoo-19.0:latest
LABEL MAINTAINER="Gray Matter Logic <support@graymatterlogic.com>"

# Copy files
COPY --chown=odoo setup.py /odoo/
COPY --chown=odoo migration.yml /odoo/
COPY --chown=odoo requirements.txt /odoo/
COPY --chown=odoo songs /odoo/songs

# Copy Addons
# COPY --chown=odoo src/enterprise /odoo/addons/
# COPY --chown=odoo src/paid-addons /odoo/addons/
# COPY --chown=odoo src/public-addons /odoo/addons/
# COPY --chown=odoo src/l10n-mexico /odoo/addons/
COPY --chown=odoo src/osi-addons /odoo/addons/
COPY --chown=odoo src/private-addons /odoo/addons/
COPY --chown=odoo src/pms /odoo/addons/

RUN cd /odoo && pip3 install -r requirements.txt --break-system-packages