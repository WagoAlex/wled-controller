# Multi-stage build to ensure smaller final image

# Stage 1: Build dependencies
FROM python:3.10-alpine AS builder

# Install build dependencies
RUN apk add --no-cache gcc libffi-dev musl-dev

# Set working directory
WORKDIR /app

# Copy Python script to the container
COPY script.py /app/

# Install Python dependencies
RUN pip install --no-cache-dir requests

# Stage 2: Create minimal runtime image
FROM python:3.10-alpine

# Set working directory
WORKDIR /app

# Copy Python script to the container
COPY script.py /app/

# Copy installed Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Set executable permissions for the Python script
RUN chmod +x /app/script.py

# Set default environment variables for WLED IP and colors
ENV WLED_IP=192.168.2.200
ENV BLUE_COLOR="[0, 0, 255]"
ENV GREEN_COLOR="[0, 255, 0]"
ENV RED_COLOR="[255, 0, 0]"
ENV CUSTOM_COLOR="[a, b, c]"

# Run the Python script
CMD ["python", "script.py"]
