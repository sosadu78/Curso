# Usamos una imagen ligera de Python oficial
FROM python:3.14-slim

# Evita que Python genere archivos .pyc y fuerza logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Instalamos dependencias
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiamos el código
COPY ./app /code/app

# Comando de arranque (usamos la sintaxis de lista para evitar problemas de señales)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
