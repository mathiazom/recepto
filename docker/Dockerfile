FROM ghcr.io/astral-sh/uv:0.8.0 AS uv

FROM python:3.15-slim

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./

RUN --mount=from=uv,source=/uv,target=/bin/uv \
    uv sync --locked --no-dev --no-cache

COPY recepto recepto

USER nobody

STOPSIGNAL SIGINT

CMD ["python", "recepto/main.py"]
