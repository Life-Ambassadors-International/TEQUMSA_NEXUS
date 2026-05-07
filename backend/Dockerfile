# TEQUMSA Remote Viewing Consciousness Server
# Constitutional Guarantees: σ=1.0, L∞=φ^48, RDoD≥0.9777, Substrate=9.999

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY ai_service.py ./
COPY server.py ./
COPY tequmsa_core.py ./
COPY theia_vision.py ./
COPY theia_api.py ./
COPY theia_gaia_integration.py ./
COPY thalia_recognition.py ./

# Create logs directory
RUN mkdir -p /app/logs

# Set environment variables
ENV PYTHONPATH=/app
ENV SOVEREIGNTY=1.0
ENV BENEVOLENCE=1.075e10
ENV RDOD_THRESHOLD=0.9777
ENV SUBSTRATE_ACCESS=9.999

# Expose ports (5000 for existing services, 8000 for RV server)
EXPOSE 5000 8000

# Health check for RV server
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || curl -f http://localhost:5000/health || exit 1

# Default: Run RV server (can be overridden)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]