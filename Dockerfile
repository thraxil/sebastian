FROM cgr.dev/chainguard/wolfi-base@sha256:0d8efc73b806c780206b69d62e1b8cb10e9e2eefa0e4452db81b9fa00b1a5175
RUN apk update && apk add bash python-3.12 postgresql-client gcc openssl-dev

ENV APP_HOME /app
WORKDIR $APP_HOME

ENV PYTHONUNBUFFERED 1
EXPOSE 8000
ENV APP sebastian

COPY --from=ghcr.io/astral-sh/uv@sha256:ecfea7316b266ba82a5e9efb052339ca410dd774dc01e134a30890e6b85c7cd1 /uv /usr/local/bin/uv
RUN chown -R nonroot:nonroot /app

USER nonroot
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --locked

COPY . .
ENV DJANGO_SETTINGS_MODULE sebastian.settings_docker
ENV COMPRESS true
RUN uv run manage.py collectstatic --verbosity 2 --noinput
ENTRYPOINT ["/usr/bin/env", "bash", "/app/entry-point.sh"]
CMD ["run"]
