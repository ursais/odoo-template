FROM odoo-19.0:latest
LABEL MAINTAINER="Gray Matter Logic <support@graymatterlogic.com>"

RUN apt update && apt install -y git && apt clean all

# Copy files
COPY --chown=odoo setup.py /odoo/
COPY --chown=odoo migration.yml /odoo/
COPY --chown=odoo requirements.txt /odoo/
COPY --chown=odoo songs /odoo/songs

RUN cd /odoo && pip3 install --break-system-packages -r requirements.txt

# Patch anthem for Odoo 19: odoo.service is not auto-imported, and db_name may be a list
RUN sed -i 's/^    import odoo$/    import odoo\n    import odoo.service.server/' /usr/local/lib/python3.12/dist-packages/anthem/cli.py && \
    sed -i 's/        dbname = odoo.tools.config\["db_name"\]/        dbname = odoo.tools.config["db_name"]\n        if isinstance(dbname, list):\n            dbname = dbname[0] if dbname else None/' /usr/local/lib/python3.12/dist-packages/anthem/cli.py

# Copy Addons
# COPY src/enterprise /odoo/addons/
# COPY src/paid-addons /odoo/addons/
COPY --chown=odoo src/pms /odoo/addons/
COPY --chown=odoo src/private-addons /odoo/addons/
