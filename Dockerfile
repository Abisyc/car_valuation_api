# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables:
# - Prevents Python from writing .pyc files to disk
# - Ensures stdout and stderr streams are unbuffered for immediate container logging
# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies if required (e.g. curl for healthcheck)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages first for Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and model files
COPY . .

# Create a non-root user and switch to it for enhanced security
# RUN useradd -m -u 1000 appuser && \
#     chown -R appuser:appuser /app
# USER appuser

# Expose port for FastAPI
EXPOSE 8000

# # Health check to ensure the service is running properly
# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
#     CMD curl -f http://localhost:8000/health || exit 1

# Run the FastAPI server using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
