FROM ursa/odoo-15.0:latest AS addons_builder

# Materialize addons from addons.manifest.yml plus always-included trees.
# This stage is not part of the final runtime image.
COPY --chown=odoo src /src
RUN chmod +x /src/sync-addons.sh \
    && /src/sync-addons.sh --dest /odoo/addons \
    && chown -R odoo:odoo /odoo/addons

FROM ursa/odoo-15.0:latest
MAINTAINER Open Source Integrators <support@opensourceintegrators.com>

# Copy files
COPY --chown=odoo setup.py /odoo/
COPY --chown=odoo migration.yml /odoo/
COPY --chown=odoo requirements.txt /odoo/
COPY --chown=odoo songs /odoo/songs

COPY --from=addons_builder --chown=odoo /odoo/addons /odoo/addons

RUN cd /odoo && pip3 install -r requirements.txt
