FROM ursa/nginx:20161012

MAINTAINER "Ursa"

ENV FQDN localhost

# Remove the default Nginx configuration file
RUN rm -v /etc/nginx/nginx.conf

# Copy a configuration file from the current directory
ADD  ./nginx.conf /etc/nginx/nginx.conf

RUN sed -i "s/fqdn/${FQDN}/g" /etc/nginx/nginx.conf

RUN mkdir /etc/nginx/ssl \
    && chown www-data:www-data /etc/nginx/ssl \
    && chmod 0700 /etc/nginx/ssl

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
      -subj "/C=US/ST=CA/L=Los Angeles/O=IT/CN=${FQDN}" \
      -keyout /etc/nginx/ssl/odoo.key \
      -out /etc/nginx/ssl/odoo.crt \
     && chmod 600 /etc/nginx/ssl/odoo.key

CMD ["nginx"]