# ── Imagen base ──────────────────────────────────────────────────────────────
# Usamos Python 3.11 slim para mantener la imagen liviana
FROM python:3.11-slim

# ── Metadatos ────────────────────────────────────────────────────────────────
LABEL maintainer="Equipo MLOps"
LABEL description="Servicio de predicción de enfermedades — Maestría en IA Aplicada - JLRM"
LABEL version="1.0"

# ── Variables de entorno ─────────────────────────────────────────────────────
# PYTHONDONTWRITEBYTECODE: no genera archivos .pyc innecesarios
# PYTHONUNBUFFERED: los logs aparecen en tiempo real (importante para debug)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# ── Directorio de trabajo dentro del contenedor ───────────────────────────────
WORKDIR /app

# ── Instalar dependencias ─────────────────────────────────────────────────────
# Copiamos primero solo requirements.txt para aprovechar la caché de Docker:
# si el código cambia pero las dependencias no, Docker no reinstala paquetes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copiar el código fuente ───────────────────────────────────────────────────
COPY app.py .
COPY templates/ templates/

# ── Puerto expuesto ───────────────────────────────────────────────────────────
EXPOSE 5000

# ── Comando de inicio ─────────────────────────────────────────────────────────
# Usamos gunicorn (servidor WSGI de producción) en lugar de Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
