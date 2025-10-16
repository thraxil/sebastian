FROM python:3.12-slim@sha256:dc9e92fcdc085ad86dda976f4cfc58856dba33a438a16db37ff00151b285c8ca
RUN apt-get update \
    && apt-get -y install libpq-dev gcc python3-dev

ENV APP_HOME /app
WORKDIR $APP_HOME

ENV PYTHONUNBUFFERED 1
EXPOSE 8000
ENV APP sebastian

COPY --from=ghcr.io/astral-sh/uv@sha256:ecfea7316b266ba82a5e9efb052339ca410dd774dc01e134a30890e6b85c7cd1 /uv /usr/local/bin/uv
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --locked

COPY . .
ENV DJANGO_SETTINGS_MODULE sebastian.settings_docker
ENV COMPRESS true
RUN uv run manage.py collectstatic --verbosity 2 --noinput
ENTRYPOINT ["/usr/bin/env", "bash", "/app/entry-point.sh"]
CMD ["run"]
