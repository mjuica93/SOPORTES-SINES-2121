# Usar imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de la aplicación
COPY . .

# Instalar dependencias (aunque no hay externas, es buena práctica)
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usará Railway
EXPOSE $PORT

# Comando para ejecutar la aplicación
CMD ["python", "server_railway.py"] 