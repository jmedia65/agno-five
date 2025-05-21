# Base Python image - this sets the foundation for our container
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies needed for building certain Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the application code
COPY . .

# Create directories for persistent data
RUN mkdir -p /app/tmp/lancedb

# Define volume for persistent storage
VOLUME ["/app/tmp"]

# Expose Streamlit's default port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]