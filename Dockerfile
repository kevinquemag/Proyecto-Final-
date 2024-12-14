# Usa una imagen ligera de Python como base
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc libpq-dev && \
    apt-get clean

# Copiar los archivos del proyecto al contenedor
COPY . /app

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["python", "main.py"]

# Usa una imagen base ligera de Python
# FROM python:3.9-slim

# # Instala las dependencias del sistema necesarias para pymysql y psycopg2
# RUN apt-get update && apt-get install -y \
#     libpq-dev gcc && \
#     apt-get clean

# # Establece el directorio de trabajo en el contenedor
# WORKDIR /app

# # Copia los archivos de tu proyecto al contenedor
# COPY . /app

# # Copia el archivo requirements.txt y las dependencias
# COPY requirements.txt .

# # Instala las dependencias de Python
# RUN pip install --no-cache-dir -r requirements.txt

# # Copia el archivo .env al contenedor
# COPY .env /app/.env

# # Expone el puerto 5000 para Flask
# EXPOSE 5000

# # Comando para ejecutar la aplicación
# CMD ["python", "main.py"]


