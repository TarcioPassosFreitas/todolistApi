# Use an official Python 3.10 base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies for building Python packages
RUN apt update && apt install -y --no-install-recommends \
    build-essential \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code into the container
COPY . .

RUN mkdir -p /opt/todolist/data/
# Expose the port FastAPI runs on
EXPOSE 8000

ENV API_VERSION=1.0.0
ENV APP_NAME=todolistApi
ENV DATABASE_DIALECT='sqlite'
ENV DATABASE_HOSTNAME=''
ENV DATABASE_NAME='/opt/todolist/data/todolist.db'
ENV DATABASE_PORT=0
ENV DATABASE_USERNAME=''
ENV DATABASE_PASSWORD=''
ENV DEBUG_MODE=false

# Command to run the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
