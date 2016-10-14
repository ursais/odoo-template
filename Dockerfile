FROM ubuntu:16.04

MAINTAINER "Ursa"

# Set Odoo variables
ENV OPENERP_SERVER /etc/odoo/odoo.conf
ENV ODOO_VERSION 10.0
ENV ODOO_RELEASE 20161012

#  Fix http://stackoverflow.com/questions/22466255/is-it-possibe-to-answer-dialog-questions-when-installing-under-docker
ENV DEBIAN_FRONTEND noninteractive

#  Setting utf-8 to python encoding
ENV PYTHONIOENCODING utf-8

#  Disable Sources
RUN sed -i "s/^deb-src/# deb-src/g" /etc/apt/sources.list

#  Basic configuration for a CI image
RUN echo 'APT::Get::Assume-Yes "true";' >> /etc/apt/apt.conf \
    && echo 'APT::Get::force-yes "true";' >> /etc/apt/apt.conf

#  Update and upgrade
RUN apt-get update -q ; apt-get upgrade -q

#  Installing packages
RUN apt-get install --allow-unauthenticated -q \
    build-essential \
    nginx \
    postfix \
    python \
    python-dev \
    python-pip \
    python-setuptools \
    libffi-dev \
    libfreetype6-dev \
    libgeoip-dev \
    libjpeg-dev \
    libldap2-dev \
    libpq-dev \
    libqrencode-dev \
    libsasl2-dev \
    libssl-dev \
    libyaml-dev \
    libxml2-dev \
    libxslt1-dev \
    postgresql-server-dev-9.5 \
    zlib1g-dev

RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            ca-certificates \
            curl \
            node-less \
            node-clean-css \
            python-pyinotify \
            python-renderpm \
        && curl -o wkhtmltox.deb -SL http://nightly.odoo.com/extra/wkhtmltox-0.12.1.2_linux-jessie-amd64.deb \
        && echo '40e8b906de658a2221b15e4e8cd82565a47d7ee8 wkhtmltox.deb' | sha1sum -c - \
        && dpkg --force-depends -i wkhtmltox.deb \
        && apt-get -y install -f --no-install-recommends \
        && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false npm \
        && rm -rf /var/lib/apt/lists/* wkhtmltox.deb

# Install Odoo
RUN set -x; \
        export PIP_FIND_LINKS="https://wheelhouse.odoo-community.org/oca" \
        && pip install --upgrade pip \
        && pip install \ 
            http://nightly.odoo.com/${ODOO_VERSION}/nightly/src/odoo_${ODOO_VERSION}.${ODOO_RELEASE}.zip \
            odoo-autodiscover==1.0.3
#            odoo10-addon-base-export-manager==10.0.1.0.0

# Copy entrypoint script and Odoo configuration file
COPY ./entrypoint.sh /
COPY ./odoo.conf /etc/odoo/
RUN adduser odoo
RUN chown odoo /etc/odoo/odoo.conf

# Mount /var/lib/odoo to allow restoring filestore and /opt/odoo/custom-addons for users addons
COPY ./custom-addons /opt/odoo/
VOLUME ["/var/lib/odoo"]

# Expose Odoo services
EXPOSE 8069 8071

# Set default user when running the container
USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]
