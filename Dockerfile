FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY scripts/ scripts/
COPY models/ models/
COPY reports/ reports/
COPY data/ data/

# Ejecutar training y scoring en secuencia
CMD ["bash", "-c", "python scripts/training.py && python scripts/scoring.py"]
