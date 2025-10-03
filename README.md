STEP TO CONVERT THE ANY PROJECT IN DOKCER CONTAINER


1. CREATE A DOCKER FILE
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

2. CREATE DOCKER-COMPOSE FILE
   version: "3.9"

services:
  db:
    image: mysql:8.0
    container_name: hrms_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: Abhi@7050
      MYSQL_DATABASE: new_hrms
    volumes:
      - db_data:/var/lib/mysql
    ports:
      - "3307:3306"
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-pAbhi@7050"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: hrms_container
    command: >
      sh -c "until nc -z db 3306;
             do echo '⏳ Waiting for DB...';
             sleep 2;
             done;
             python manage.py makemigrations &&
             python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/app
    environment:
      DB_HOST: db
      DB_NAME: DB NAME
      DB_USER: ROOT USER
      DB_PASSWORD: YOUR DB PASSWORD
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8000:8000"

volumes:
  db_data:

# Wait for DB to be ready before starting Django
CMD ["sh", "-c", "until nc -z db 3306; do echo '⏳ Waiting for MySQL...'; sleep 2; done; python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

3. CREATE DOCKER .DOCKERIGNORE FILE
   db.sqlite3

COMMAND - > DOKCER-COMPOSE UP --BUILD 















