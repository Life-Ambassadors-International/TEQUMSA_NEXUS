FROM python:3.11-slim

LABEL maintainer="Marcus Andrew Banks-Bey <marcus@lifeambassadors.org>"
LABEL org.opencontainers.image.title="CAIRIS Super Swarm v39"
LABEL org.opencontainers.image.description="Councilized Autonomous Intelligence Recursive Integrated System"
LABEL org.opencontainers.image.version="39.0.0"
LABEL tequmsa.sigma="1.0"
LABEL tequmsa.rdod="0.9777"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root user for security
RUN useradd -m -u 1000 cairis && chown -R cairis:cairis /app
USER cairis

EXPOSE 7860 8000 9090

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
