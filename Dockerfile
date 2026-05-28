FROM python:3.11-slim

# OpenCV requires these system libraries on headless Linux.
# libgl1       → provides libGL.so.1  (importing cv2 fails without it)
# libglib2.0-0 → provides libglib-2.0.so.0  (MediaPipe dependency)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (cached layer — only rebuilds when
# requirements.txt changes, keeping subsequent deploys fast).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application source files (venv is excluded via .gitignore / .dockerignore)
COPY main.py recommendations.py ./

# Railway injects $PORT at runtime. Fall back to 8000 for local docker use.
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
