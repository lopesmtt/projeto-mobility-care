FROM python:3.10-slim

WORKDIR /app

# Instala dependências do sistema para o Postgres
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# O Render injeta a porta automaticamente na variável $PORT
CMD uvicorn main:app --host 0.0.0.0 --port $PORT