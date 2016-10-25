FROM ursa/odoo:10.0-20161012

MAINTAINER "Ursa Information Systems"

# Copy files
COPY ./odoo.conf /etc/odoo/
COPY ./requirements.txt /tmp/
COPY ./custom-addons /opt/odoo/

RUN chown -R odoo /etc/odoo/odoo.conf /opt/odoo

# Install Odoo
RUN set -x; \
        export PIP_FIND_LINKS="https://wheelhouse.odoo-community.org/oca" \
        && pip install --upgrade pip \
        && pip install -r /tmp/requirements.txt

