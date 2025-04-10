# Imagen base
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto de Streamlit
EXPOSE 8501

# Comando para ejecutar la app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
