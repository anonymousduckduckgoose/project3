# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the Docker image
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

WORKDIR /usr/src/app/favicon-fetcher

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set environment variables for python service
ENV host=0.0.0.0
ENV port=8000

# Start python service
ENTRYPOINT ["python3", "main.py"]