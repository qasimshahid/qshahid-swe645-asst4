# Qasim Shahid SWE 645 - Assignment 4
# Dockerfile: Docker configuration for building the Python Survey application image.

# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install packages specified in requirements.txt (we need fastapi and uvicorn and peewee)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the FastAPI application runs on
EXPOSE 8080

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]