FROM thraxil/django.base:2017-09-27-98304b84ac68
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
