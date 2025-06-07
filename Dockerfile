FROM python:3.12-slim
RUN apt-get update \
    && apt-get -y install libpq-dev gcc python3-dev

ENV APP_HOME /app
WORKDIR $APP_HOME

ENV PYTHONUNBUFFERED 1
EXPOSE 8000
ENV APP sebastian

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --locked

COPY . .
ENV DJANGO_SETTINGS_MODULE sebastian.settings_docker
ENV COMPRESS true
RUN uv run manage.py collectstatic --verbosity 2 --noinput
ENTRYPOINT ["/usr/bin/env", "bash", "/app/entry-point.sh"]
CMD ["run"]
