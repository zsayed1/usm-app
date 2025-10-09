# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY app.py .

# Install Flask
RUN pip install flask

# Expose port
EXPOSE 8080

# Run app
CMD ["python", "app.py"]
