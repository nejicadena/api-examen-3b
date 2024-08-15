# Usa una imagen base oficial de Python
FROM python:3.11-slim

ENV TZ="America/Mexico_City"

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos y el resto del proyecto al contenedor
COPY requirements.txt requirements.txt
COPY . .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Ejecuta makemigrations y migrate al construir la imagen
RUN python manage.py makemigrations && python manage.py migrate

# Expone el puerto 8000 en el contenedor
EXPOSE 8000

# Ejecuta comandos para aplicar migraciones y correr el servidor de desarrollo
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]