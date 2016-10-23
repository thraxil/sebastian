FROM ccnmtl/django.base:latest
RUN apt-get update \
    && apt-get install -y \
                binutils \
                build-essential \
                curl \
                gcc \
                libffi-dev \
                libssl-dev \
                libexif-dev \
                libexif12 \
                libfontconfig1-dev \
                libfreetype6-dev \
                libldap2-dev \
                libpq-dev  \
                libsasl2-dev \
                libssl-dev \
                libxft-dev \
                libxml2-dev \
                libxslt-dev \
                libxslt1-dev \
                python-all-dev \
                python-dev \
                python-beautifulsoup \
                python-ldap \
                python-tk \
    && apt-get clean \
                && rm -rf /var/lib/apt/lists/* \
                && /ve/bin/pip install wheel
COPY requirements.txt /app/requirements.txt
RUN /ve/bin/pip install -r /app/requirements.txt && touch /ve/sentinal
WORKDIR /app
COPY . /app/
RUN VE=/ve/ MANAGE="/ve/bin/python manage.py" NODE_MODULES=/node/node_modules make all
EXPOSE 8000
ADD docker-run.sh /run.sh
ENV APP sebastian
ENTRYPOINT ["/run.sh"]
CMD ["run"]
