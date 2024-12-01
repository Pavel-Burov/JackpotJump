# Dockerfile

# Use the official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install

# Set the command to run the automation
CMD ["python", "main.py"]
