# Use the official Ubuntu image as a base
FROM ubuntu:22.04

# Update package list and install required packages
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python-is-python3 \
    python3-pip \
    python3-venv \
    redis-server \
    ffmpeg \
    curl \
    unzip \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Set up a working directory
WORKDIR /

# Expose the port for Redis (if needed)
EXPOSE 6379

# Start Redis server (if needed)
CMD ["redis-server"]
