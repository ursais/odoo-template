FROM odoo:12
MAINTAINER Open Source Integrators <contact@opensourceintegrators.com>

COPY odoo.conf /etc/odoo/
COPY requirements.txt /tmp/
COPY src/private-addons /mnt/extra-addons/
# COPY src/enterprise /mnt/extra-addons/
# Add your module to the list below. Please respect the alphabetic order
# COPY src/l10n-usa/l10n_us_form_1099 /mnt/extra-addons/l10n_us_form_1099

RUN pip3 install -r /tmp/requirements.txt

USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]
