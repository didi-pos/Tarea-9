FROM python:3.11-slim

LABEL maintainer="didierposse@gmail.com"

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libx11-6 \
    libxcb1 \
    libxau6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /brazo_robotico

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY brazo_robotico.py .

ENV DISPLAY=:0

CMD ["python", "brazo_robotico.py"]
