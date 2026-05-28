# LOAD-SPAN Dockerfile
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml setup.cfg VERSION ./
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    libopenblas0 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY load_span/ ./load_span/
COPY simulation/ ./simulation/
COPY configs/ ./configs/
COPY README.md LICENSE VERSION ./

# Create necessary directories
RUN mkdir -p /data /logs /models

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV LOG_LEVEL=INFO

# Expose ports
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import load_span; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "load_span.pipeline", "--config", "configs/default.yaml"]
