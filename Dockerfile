FROM nvidia/cuda:12.3.1-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Working directory for the application
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        vim \
        lsof \
        python3-pip \
        python3-dev \
        python3-opencv \
        libglib2.0-0 \
        ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy only the requirements.txt to leverage Docker cache
COPY requirements.txt ./

# Upgrade pip and install Python dependencies
RUN python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --upgrade numpy

# Copy the rest of the application
COPY . .

# Expose port 3000 for the application
EXPOSE 3000

# Command to run the application
CMD ["python3", "handler.py"]

