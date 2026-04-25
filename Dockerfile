# Sermon Pro — production Dockerfile (all-in-one for Railway)
# Stage 1: build React frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /frontend

COPY dashboard/package.json dashboard/package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY dashboard/ ./
RUN npm run build

# Stage 2: Python deps builder
FROM python:3.11-slim AS py-builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Stage 3: runtime
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    nodejs \
    && ln -sf /usr/bin/nodejs /usr/bin/node \
    && rm -rf /var/lib/apt/lists/*

COPY --from=py-builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade --no-cache-dir yt-dlp

# Application code
COPY . .

# Built frontend from stage 1
COPY --from=frontend-builder /frontend/dist ./dashboard/dist

# Non-root user + cache dirs
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser \
    && mkdir -p /app/uploads /app/output /tmp/Ultralytics \
    && chown -R appuser:appuser /app /tmp/Ultralytics

USER appuser

# Pre-download YOLO model at build time
RUN python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Railway sets $PORT; default to 8000 locally
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
