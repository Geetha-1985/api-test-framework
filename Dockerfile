FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create reports directory
RUN mkdir -p reports logs

# Set environment variables
ENV PYTHONPATH=/app
ENV TEST_ENV=dev

# Default command
CMD ["pytest", "tests/", "--html=reports/report.html", "--allure-dir=reports/allure-results"]