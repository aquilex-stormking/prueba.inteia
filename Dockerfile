# Usar una imagen base de Python
FROM python:3.8

# Establecer una carpeta de trabajo
WORKDIR /app

# Copiar los requerimientos e instalar dependencias
COPY requirements.txt .
run pip install pydantic[dotenv]
RUN pip install  -r requirements.txt

# Copiar el código fuente
COPY . .

# Ejecutar la app
CMD [ "uvicorn","main:app","--reload","--host","0.0.0.0","--port","8000"]
