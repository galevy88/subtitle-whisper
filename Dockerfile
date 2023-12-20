# Start from an NVIDIA CUDA image
FROM nvidia/cuda:12.3.1-base-ubuntu22.04

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3-pip python3-dev build-essential ffmpeg

COPY . /usr/src/app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["python3", "handler.py"]

