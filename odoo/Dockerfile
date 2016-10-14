FROM ursa/odoo:10.0-20161012

MAINTAINER "Ursa"

# Set Odoo variables
ENV OPENERP_SERVER /etc/odoo/odoo.conf

# Install Odoo
RUN set -x; \
        export PIP_FIND_LINKS="https://wheelhouse.odoo-community.org/oca" \
        && pip install --upgrade pip \
        && pip install -r requirements.txt

# Copy entrypoint script and Odoo configuration file
COPY ./entrypoint.sh /
COPY ./odoo.conf /etc/odoo/
RUN chown odoo /etc/odoo/odoo.conf

# Copy /opt/odoo/custom-addons for users addons
COPY ./custom-addons /opt/odoo/

# Set default user when running the container
USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]
