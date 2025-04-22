FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app/

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    git \
    curl \
    openssl \
    build-essential \
    python3-dev

COPY . /app/

ENV UV_COMPILE_BYTECODE=1

RUN uv venv && \
    export PATH="/app/.venv/bin:$PATH" && \
    uv sync --frozen &&\
    uv pip install -e .

FROM python:3.12-slim

COPY --from=builder --chown=user:user /app/.venv /app/.venv

ENV PYTHONOPTIMIZE=1
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV GRANIAN_THREADS=2
ENV GRANIAN_WORKERS=2
ENV GRANIAN_BLOCKING_THREADS=4


VOLUME ["/app/data"]
EXPOSE 8080

CMD ["cybersec_survey", "--host", "0.0.0.0", "--port", "5006"]
