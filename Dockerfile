FROM python:3.9

# Crear usuario que ejecuta la app
RUN adduser --disabled-password --gecos '' api-user


COPY . /app

# Definir directorio de trabajo 
WORKDIR /app

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


USER api-user
# Puerto a exponer para la api 
EXPOSE 8001

# Comandos a ejecutar al correr el contenedor 
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
