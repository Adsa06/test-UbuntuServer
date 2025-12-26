# Usamos la imagen oficial de Python como base
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo requirements.txt al contenedor
COPY requirements.txt /app/

# Instalamos las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código fuente al contenedor
COPY . /app/

# Exponemos el puerto que FastAPI usará (8000 por defecto)
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
