# Usar una imagen base de Python
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Establecer una carpeta de trabajo
WORKDIR /app

# Copiar los requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install  -r requirements.txt

# Copiar el código fuente
COPY . .

# Ejecutar la app
CMD ["python", "main.py"]
