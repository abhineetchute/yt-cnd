# Start with a lightweight Python environment
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies: FFmpeg (for video processing) and Node.js (for the JS bot bypass)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy your requirements and code into the container
COPY requirements.txt .
COPY . .

# Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit uses
EXPOSE 8501

# Command to run the web app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
