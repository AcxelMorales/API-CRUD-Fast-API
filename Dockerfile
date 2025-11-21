# Usa una imagen base ligera de Python
FROM python:3.11-slim

# Configura el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto donde correrá FastAPI
EXPOSE 8000

# Comando por defecto: iniciar el servidor con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
