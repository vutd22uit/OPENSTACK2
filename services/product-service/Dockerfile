FROM python:3.11-slim

RUN groupadd -r prodservice && useradd -r -g prodservice prodservice

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --chown=prodservice:prodservice ../shared /app/shared

COPY --chown=prodservice:prodservice requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=prodservice:prodservice . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    SERVICE_NAME=product-service \
    PORT=5002

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

USER prodservice
EXPOSE 5002
CMD ["python", "app.py"]
