# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

# Prevents Python from writing .pyc files & enables unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system deps (add build tools if your reqs need compiling)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . .

# Use a non-root user for security
RUN useradd -m appuser
USER appuser

EXPOSE 8000

# If your FastAPI instance is "app" inside app.py:
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
