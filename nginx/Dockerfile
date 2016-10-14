FROM ursa/nginx:20161012

MAINTAINER "Ursa"

# Copy Odoo file
COPY ./odoo.nginx /etc/nginx/sites-available/odoo

RUN mkdir /etc/nginx/ssl \
    && chown www-data:www-data /etc/nginx/ssl \
    && chmod 0700 /etc/nginx/ssl

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
      -subj "/C=US/ST=CA/L=Los Angeles/O=IT/CN={{ fqdn }}" \
      -keyout /etc/nginx/ssl/odoo.key \
      -out /etc/nginx/ssl/odoo.crt \
     && chmod 600 /etc/nginx/ssl/odoo.key

RUN ln -s /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled/odoo \
    && chown www-data:www-data /etc/nginx/sites-enabled/odoo

RUN nginx -t