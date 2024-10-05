# Use the official Python slim image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 instead of the default 8501
EXPOSE 80

# Run Streamlit when the container starts, listening on port 80
CMD ["streamlit", "run", "main.py", "--server.enableXsrfProtection=false", "--server.port=80", "--server.address=0.0.0.0"]

