# User Service Dockerfile
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r userservice && useradd -r -g userservice userservice

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy shared library first
COPY --chown=userservice:userservice ../shared /app/shared

# Copy service code
COPY --chown=userservice:userservice requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=userservice:userservice . .

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    SERVICE_NAME=user-service \
    PORT=5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

USER userservice
EXPOSE ${PORT}

CMD ["python", "app.py"]
