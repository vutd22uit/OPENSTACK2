FROM python:3.11-slim

RUN groupadd -r gateway && useradd -r -g gateway gateway

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --chown=gateway:gateway ../shared /app/shared

COPY --chown=gateway:gateway requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=gateway:gateway . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    SERVICE_NAME=api-gateway \
    PORT=8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

USER gateway
EXPOSE 8080
CMD ["python", "app.py"]
