# Use official Python image as base
FROM python:3.13.5-slim-bullseye

# Set working directory
WORKDIR /app

# Copy requirements if present
COPY requirements.txt .env ./
# Copy application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


ARG SOURCE="./app/data/raw/daily_sales.csv"
# Default command (adjust as needed)
CMD ["python", "main.py", "--source", "$SOURCE"]