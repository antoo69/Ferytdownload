# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy the requirements.txt file into the working directory
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code into the working directory
COPY . /app/

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
CMD ["python", "main.py"]
