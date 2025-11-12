FROM python:3.11-slim

RUN groupadd -r orderservice && useradd -r -g orderservice orderservice

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --chown=orderservice:orderservice ../shared /app/shared

COPY --chown=orderservice:orderservice requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=orderservice:orderservice . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    SERVICE_NAME=order-service \
    PORT=5003

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

USER orderservice
EXPOSE 5003
CMD ["python", "app.py"]
