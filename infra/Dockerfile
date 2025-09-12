FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /project/

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --locked
RUN uv sync --locked --group speedups

COPY infra/startup.sh .
COPY src/ src/
COPY env/.env env/.env
COPY alembic/ alembic/
COPY alembic.ini .

ENTRYPOINT ["/bin/sh", "startup.sh"]
