FROM public.ecr.aws/t4c3a5h0/odoo-base:19.0-20250918
LABEL MAINTAINER="Gray Matter Logic <support@graymatterlogic.com>"

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

# Patch anthem for Odoo 19: odoo.service is not auto-imported, and db_name may be a list
RUN sed -i 's/^    import odoo$/    import odoo\n    import odoo.service.server/' /usr/local/lib/python3.12/dist-packages/anthem/cli.py && \
    sed -i 's/        dbname = odoo.tools.config\["db_name"\]/        dbname = odoo.tools.config["db_name"]\n        if isinstance(dbname, list):\n            dbname = dbname[0] if dbname else None/' /usr/local/lib/python3.12/dist-packages/anthem/cli.py
