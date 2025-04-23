FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app/

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    python3-dev

COPY . /app/

ENV UV_COMPILE_BYTECODE=1

RUN uv venv && \
    export PATH="/app/.venv/bin:$PATH" && \
    uv sync --frozen &&\
    uv build && \
    uv pip install dist/*.whl

FROM python:3.12-slim

RUN addgroup --system user && adduser --system --ingroup user user
COPY --from=builder --chown=user:user /app/.venv /app/.venv

WORKDIR /app

ENV PYTHONOPTIMIZE=1
ENV PATH="/app/.venv/bin:$PATH"
ENV GRANIAN_THREADS=2
ENV GRANIAN_WORKERS=2
ENV GRANIAN_BLOCKING_THREADS=4

USER user

EXPOSE 5006

CMD ["cybersec_survey", "--host", "0.0.0.0", "--port", "5006"]
