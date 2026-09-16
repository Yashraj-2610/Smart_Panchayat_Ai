# Multi-stage build for Smart Panchayat AI
FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create database directory
RUN mkdir -p /app/backend

# Expose ports
# 8000 - FastAPI backend
# 8501 - Family Portal
# 8502 - Sarpanch Dashboard
EXPOSE 8000 8501 8502

# Initialize database on startup
RUN python backend/init_db.py || true

# Default command (can be overridden)
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
