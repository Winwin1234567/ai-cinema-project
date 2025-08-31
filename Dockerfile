# Use official Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt

# Add virtualenv bin to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy the rest of the app
COPY . .

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=aicinema.settings

# Collect static files (WhiteNoise)
RUN python manage.py collectstatic --noinput

# Expose the port Railway will use
EXPOSE 8080

# Run Gunicorn using $PORT from Railway

CMD gunicorn aicinema.wsgi:application --bind 0.0.0.0:$PORT --workers 3
