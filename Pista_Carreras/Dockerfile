FROM python:3.11-slim

LABEL maintainer="didierposse@gmail.com"

# Instalar dependencias del sistema incluyendo tkinter y X11
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    python3-tk \
    tk-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libx11-6 \
    libxcb1 \
    libxau6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /pista_carreras

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY pista_carreras.py .

# Configurar display para X11
ENV DISPLAY=:0

CMD ["python", "pista_carreras.py"]
