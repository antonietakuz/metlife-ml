FROM python:3.11-slim

WORKDIR /app

# Copiamos requirements
COPY requirements.txt .

# Instalamos dependencias (cryptography incluido)
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código
COPY . .

# Comando por defecto (docker-compose lo sobreescribe)
CMD ["python", "scripts/training.py"]
