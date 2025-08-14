# Use official Python image
FROM python:3.8-slim

# Set working directory
WORKDIR /application

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 5000

# Start the app with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "application:application"]
