# Weather ETL Pipeline Dockerfile

# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p db logs docs

# Copy source code
COPY src/ src/
COPY .env.template .

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Set environment variables
ENV SQLITE_DB=/app/db/weather.db
ENV LOG_FILE=/app/logs/pipeline.log

# Default command
CMD ["python", "-m", "src.main", "run"]