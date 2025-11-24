#official Python 3.11 base image
FROM python:3.11-slim

# Install Java
RUN apt-get update && apt-get install -y openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application code into the container
COPY ./app ./app
COPY ./data ./data

# Expose the port the app will run on
EXPOSE 10000

# The command to run when the container starts
# Note: We use the app/main.py path directly now
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]