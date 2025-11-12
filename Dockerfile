# Multi-stage Dockerfile with security best practices
# Stage 1: Build stage
FROM python:3.11-slim as builder

# Set build arguments
ARG APP_USER=appuser
ARG APP_UID=1000

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.11-slim

# Security: Create non-root user
ARG APP_USER=appuser
ARG APP_UID=1000
RUN groupadd -g ${APP_UID} ${APP_USER} && \
    useradd -m -u ${APP_UID} -g ${APP_USER} -s /bin/bash ${APP_USER}

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=${APP_USER}:${APP_USER} . .

# Security: Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_ENV=production \
    PORT=5000

# Security: Remove setuid/setgid bits
RUN find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Security: Switch to non-root user
USER ${APP_USER}

# Expose port
EXPOSE ${PORT}

# Use exec form for CMD to ensure proper signal handling
CMD ["python", "app.py"]
