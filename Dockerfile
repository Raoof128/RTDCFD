# Multi-stage Docker build for Autonomous Multi-Agent Red/Blue Team Simulation System
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs reports storage data && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port for dashboard
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "from utils.validation_standalone import check_system_health; check_system_health()" || \
    curl -f http://localhost:8501/health || exit 1

# Default command
CMD ["python", "main.py", "--scenario", "soci_energy_grid", "--dashboard"]
