# Sistema de Predicción de Enfermedades — Docker

> También disponible en formato **PDF** (`README.pdf`) con presentación más visual.

## Finalidad del sistema

Este servicio permite a un médico ingresar datos clínicos de un paciente y obtener
una predicción automática del estado de salud. El sistema simula un modelo de ML
que clasifica al paciente en uno de cuatro estados:

| Estado             | Descripción                                              |
|--------------------|----------------------------------------------------------|
| `NO ENFERMO`       | Los síntomas no indican enfermedad significativa         |
| `ENFERMEDAD LEVE`  | Síntomas leves y recientes, manejo ambulatorio           |
| `ENFERMEDAD AGUDA` | Síntomas intensos o múltiples, requiere atención pronta  |
| `ENFERMEDAD CRÓNICA` | Síntomas presentes por 90 días o más                  |

El médico puede usar el sistema de **dos formas**:
1. **Página web** — accesible desde cualquier navegador
2. **API REST** — para integraciones con otros sistemas

---

## Estructura del proyecto

```
diagnostico_docker/
├── app.py              ← Función de diagnóstico + servidor Flask
├── Dockerfile          ← Instrucciones para construir la imagen
├── requirements.txt    ← Dependencias de Python
├── README.md           ← Este archivo
└── templates/
    └── index.html      ← Interfaz web para el médico
```

---

## Requisitos previos

- Tener instalado **Docker** ([descargar aquí](https://docs.docker.com/get-docker/))
- No se necesita Python ni ningún otro software adicional

Verificar que Docker está instalado:
```bash
docker --version
# Debe mostrar algo como: Docker version 25.0.0, build ...
```

---

## 1. Construir la imagen Docker

Desde la carpeta raíz del proyecto (donde está el `Dockerfile`):

```bash
docker build -t diagnostico-medico .
```

**¿Qué hace este comando?**
- `docker build` — construye una imagen
- `-t diagnostico-medico` — le asigna el nombre `diagnostico-medico`
- `.` — usa el `Dockerfile` del directorio actual

La primera vez tarda unos minutos porque descarga la imagen base de Python.
Las veces siguientes es mucho más rápido gracias al caché de Docker.

---

## 2. Ejecutar el contenedor

```bash
docker run -d -p 5000:5000 --name diagnostico diagnostico-medico
```

**¿Qué hace cada parte?**

| Parte            | Significado                                                  |
|------------------|--------------------------------------------------------------|
| `docker run`     | Ejecuta un contenedor a partir de una imagen                |
| `-d`             | Modo "detached" — corre en segundo plano                    |
| `-p 5000:5000`   | Mapea el puerto 5000 del contenedor al puerto 5000 de tu PC |
| `--name diagnostico` | Nombre amigable para el contenedor                     |
| `diagnostico-medico` | Nombre de la imagen construida en el paso anterior     |

---

## 3. Usar el sistema

### Opción A — Página web (recomendada para médicos)

Abrir el navegador y visitar:

```
http://localhost:5000
```

Verás un formulario donde ingresar:
- **Intensidad de síntomas** (0 a 10)
- **Duración en días**
- **Número de síntomas distintos**

Al hacer clic en *Obtener diagnóstico*, el sistema responde en la misma página.

---

### Opción B — API REST (para integraciones técnicas)

Enviar una petición `POST` a `http://localhost:5000/api/predecir` con un JSON:

**Con curl:**
```bash
curl -X POST http://localhost:5000/api/predecir \
     -H "Content-Type: application/json" \
     -d '{"intensidad_sintomas": 7, "duracion_dias": 5, "num_sintomas": 3}'
```

**Respuesta esperada:**
```json
{
  "diagnostico": "ENFERMEDAD AGUDA",
  "parametros_recibidos": {
    "intensidad_sintomas": 7,
    "duracion_dias": 5,
    "num_sintomas": 3
  }
}
```

**Ejemplos de casos de prueba:**

| intensidad_sintomas | duracion_dias | num_sintomas | Resultado esperado    |
|---------------------|---------------|--------------|----------------------|
| 1                   | 2             | 1            | NO ENFERMO           |
| 4                   | 10            | 2            | ENFERMEDAD LEVE      |
| 8                   | 7             | 4            | ENFERMEDAD AGUDA     |
| 5                   | 120           | 3            | ENFERMEDAD CRÓNICA   |

---

## 4. Detener y eliminar el contenedor

```bash
# Detener el contenedor (sin eliminarlo)
docker stop diagnostico

# Volver a iniciarlo
docker start diagnostico

# Eliminarlo completamente
docker rm -f diagnostico
```

---

## 5. Ver los logs del servicio

```bash
docker logs diagnostico
```

---

## Lógica de la función `diagnosticar()`

La función recibe tres parámetros y aplica reglas basadas en evidencia clínica simplificada:

```
puntuacion = (intensidad_sintomas × 0.5) + (num_sintomas × 0.8)

SI duracion_dias >= 90  →  ENFERMEDAD CRÓNICA
SI puntuacion  <  2.0   →  NO ENFERMO
SI puntuacion  <  5.5   →  ENFERMEDAD LEVE
SI puntuacion  >= 5.5   →  ENFERMEDAD AGUDA
```

En un sistema real, la función invocaría un modelo de ML entrenado (XGBoost,
red neuronal, etc.) almacenado como archivo `.pkl` o `.onnx`.

---

## Solución de problemas comunes

| Problema | Solución |
|----------|----------|
| `Port 5000 already in use` | Cambiar el puerto: `-p 5001:5000` y acceder a `localhost:5001` |
| `Cannot connect to Docker daemon` | Asegurarse de que Docker Desktop está abierto |
| La página no carga | Esperar 5 segundos y recargar; el servidor tarda un momento en iniciar |
