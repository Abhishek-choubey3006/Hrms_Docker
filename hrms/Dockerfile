# -------------------------------
# Stage 1: Use official Python image
# -------------------------------
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory inside the container
WORKDIR /hrms

# Install system dependencies (updated for Debian Trixie)
RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev pkg-config netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire Django project into container
COPY . .

# Expose Django's default port
EXPOSE 8000

# Wait for DB to be ready before starting Django
CMD ["sh", "-c", "until nc -z db 3306; do echo '⏳ Waiting for MySQL...'; sleep 2; done; python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
