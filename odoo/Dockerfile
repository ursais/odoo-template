FROM public.ecr.aws/t4c3a5h0/odoo-base:20.0-20261009 AS addons_builder

# Materialize addons from addons.manifest.yml plus always-included trees.
# This stage is not part of the final runtime image.
COPY --chown=odoo src /src
RUN chmod +x /src/sync-addons.sh \
    && /src/sync-addons.sh --dest /odoo/addons \
    && chown -R odoo:odoo /odoo/addons

FROM public.ecr.aws/t4c3a5h0/odoo-base:20.0-20261009
LABEL MAINTAINER="Gray Matter Logic <support@graymatterlogic.com>"

# Must match the k8s readiness/liveness probe path so the pod stays Ready and
# serves Marabunta's maintenance page during migrations instead of an ingress 503.
ENV MARABUNTA_WEB_HEALTHCHECK_PATH=/monitoring/status

# Copy files
COPY --chown=odoo setup.py /odoo/
COPY --chown=odoo migration.yml /odoo/
COPY --chown=odoo requirements.txt /odoo/
COPY --chown=odoo songs /odoo/songs

#Copy Enterprise
COPY src/enterprise /odoo/addons/

COPY --from=addons_builder --chown=odoo /odoo/addons /odoo/addons

RUN cd /odoo && pip3 install -r requirements.txt --break-system-packages
