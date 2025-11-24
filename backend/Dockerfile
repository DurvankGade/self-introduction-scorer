# Start with a modern, slim Python base image
FROM python:3.11-slim

# Install the Java Runtime Environment
RUN apt-get update && apt-get install -y openjdk-17-jre-headless

# Set a working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the application code into the container
# CORRECTED: Removed the leading "./"
COPY app ./app

# Expose the port that Uvicorn will run on
EXPOSE 10000

# The command that will be executed when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]