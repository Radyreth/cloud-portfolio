# Slim Python image to reduce attack surface and image size
FROM python:3.11-slim

LABEL maintainer="Radyreth"
LABEL description="API Flask CI/CD Demo"

# No .pyc files + real-time logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install deps first (better layer caching)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

USER appuser

EXPOSE 5000

# Gunicorn for production (not Flask dev server)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
