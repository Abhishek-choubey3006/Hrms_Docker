
If you Want to Run on localmachine follow step:
1. setting.py -> Database{ HOST = "localhost"} change host = db to localhost it will run


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

Project Overview:
Designed and developed a complete HRMS platform to manage employee data, attendance, leave requests, salary processing, and project allocation.
Implemented Agile methodology using Jira for sprint planning, backlog management, and tracking development progress.

Key Contributions

Agile Project Management: Managed the project using Jira Agile boards, tracking sprints, tasks, and user stories efficiently.

Jira-GitHub Integration: Linked Jira issues with GitHub commits & pull requests for real-time development visibility.

API Development: Built secure REST APIs for employee onboarding, leave management, and attendance tracking.

Database Management: Designed and optimized database schemas in MySQL for efficient HR data storage.

Dockerized Deployment: Set up Docker Compose to run Django, MySQL, and Nginx in containerized environments.

Interactive Calendar: Integrated FullCalendar.js for company-wide event & leave visualization.

Project Links

🔗 GitHub Repository: https://github.com/Abhishek-choubey3006/container

🔗 Jira Agile Board (View Only): (Make Public First)
https://abhishekchoubey.atlassian.net/jira/software/projects/HRMS/boards/34
