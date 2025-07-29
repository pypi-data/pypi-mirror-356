# Usar una imagen base de Python ligera
FROM python:3.9-slim-buster

# Establecer etiquetas OCI para metadatos
LABEL org.opencontainers.image.source="https://github.com/your-org/llmtrace"
LABEL org.opencontainers.image.description="LLMTrace Web Dashboard"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Your Name <your.email@example.com>"
LABEL org.opencontainers.image.version="0.1.0" # Se actualizará con el tag de la imagen

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar pyproject.toml y poetry.lock (si usas poetry) o requirements.txt
# para instalar dependencias antes de copiar el resto del código
COPY pyproject.toml ./
# Si usas poetry, descomenta la siguiente línea:
# COPY poetry.lock ./

# Instalar dependencias del proyecto
# Usamos el extra [web] para el dashboard y [all] para asegurar todas las dependencias necesarias
RUN pip install --no-cache-dir ".[web,all]"

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto por defecto de Flask (5000)
EXPOSE 5000

# HEALTHCHECK para verificar que el servicio está funcionando
# Asume que el dashboard tendrá un endpoint /health
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl --fail http://localhost:5000/health || exit 1

# Comando para ejecutar la aplicación Flask con Gunicorn
# Usar 0.0.0.0 para que sea accesible desde fuera del contenedor
# El módulo `llmtrace.dashboard.app:app` asume que `app` es la instancia de Flask/FastAPI
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "llmtrace.dashboard.app:app"]
