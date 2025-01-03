# Use the official lightweight Python image
FROM python:3.9-slim

# Install system dependencies, including FLAC
RUN apt-get update && apt-get install -y flac && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "health.py", "--server.port=8501", "--server.address=0.0.0.0"]
