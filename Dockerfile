# Imagen base ligera con Python
FROM python:3.11-slim

# Evitar pyc y buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para aprovechar caché)
COPY requirements.txt .

# Instalar dependencias del sistema (psycopg2 y gdal para PostGIS)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gdal-bin \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn uvicorn

# Copiar todo el código
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando de arranque con Gunicorn (usando UvicornWorker para ASGI)
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
