# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install allure-behave for reporting
RUN pip install --no-cache-dir allure-behave

# Copy the entire project
COPY . .

# Create reports directory
RUN mkdir -p reports/allure-report

# Set default command to run all tests
CMD ["behave"]
