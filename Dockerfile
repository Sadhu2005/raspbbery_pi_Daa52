# Use Python 3.10 slim base image
FROM python:3.10-slim

# Install necessary system tools and libraries
RUN apt-get update && apt-get install -y \
    bluez \
    alsa-utils \
    mpg123 \
    && apt-get clean

# Set the working directory
WORKDIR /Daa5.2

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY Audio /Daa5.2/Audio
COPY Code /Daa5.2/Code

# Set the command to run the main script
CMD ["python3", "/Daa5.2/osSetting/auto_shutdown.py"]
