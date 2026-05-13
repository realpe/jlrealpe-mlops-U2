"""
app.py — Servicio de predicción de enfermedades
Expone la función diagnosticar() tanto por API REST como por página web.
"""

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL DE DIAGNÓSTICO
# Recibe tres parámetros clínicos numéricos (escala 0-10) y retorna uno de
# los cuatro estados posibles.
#
# Parámetros:
#   intensidad_sintomas  (float 0-10): qué tan intensos son los síntomas
#   duracion_dias        (float 0+):   cuántos días lleva con síntomas
#   num_sintomas         (int 1+):     cuántos síntomas distintos presenta
#
# Retorna (str): uno de los cuatro estados de diagnóstico
# ──────────────────────────────────────────────────────────────────────────────
def diagnosticar(intensidad_sintomas: float,
                 duracion_dias: float,
                 num_sintomas: int) -> str:
    """
    Modelo simulado de diagnóstico basado en reglas clínicas simples.
    En un sistema real, aquí se invocaría el modelo de ML entrenado.

    Retorna:
        "NO ENFERMO"        — sin signos relevantes
        "ENFERMEDAD LEVE"   — signos leves y recientes
        "ENFERMEDAD AGUDA"  — signos moderados/intensos y recientes
        "ENFERMEDAD CRÓNICA"— síntomas prolongados independientemente de intensidad
    """

    # Validación básica de rangos
    intensidad_sintomas = max(0.0, min(10.0, float(intensidad_sintomas)))
    duracion_dias       = max(0.0, float(duracion_dias))
    num_sintomas        = max(0, int(num_sintomas))

    # Calcular puntuación ponderada
    puntuacion = (intensidad_sintomas * 0.5) + (num_sintomas * 0.8)

    # Reglas de decisión
    if duracion_dias >= 90:
        return "ENFERMEDAD CRÓNICA"
    elif puntuacion < 2.0:
        return "NO ENFERMO"
    elif puntuacion < 5.5:
        return "ENFERMEDAD LEVE"
    else:
        return "ENFERMEDAD AGUDA"


# ──────────────────────────────────────────────────────────────────────────────
# RUTAS WEB
# ──────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Página principal con formulario para el médico."""
    return render_template("index.html")


@app.route("/predecir", methods=["POST"])
def predecir_web():
    """Recibe datos del formulario HTML y devuelve el diagnóstico."""
    try:
        intensidad = request.form.get("intensidad", 0)
        duracion   = request.form.get("duracion", 0)
        num_sint   = request.form.get("num_sintomas", 0)

        resultado = diagnosticar(intensidad, duracion, num_sint)

        return render_template("index.html",
                               resultado=resultado,
                               intensidad=intensidad,
                               duracion=duracion,
                               num_sintomas=num_sint)
    except Exception as e:
        return render_template("index.html", error=str(e))


# ──────────────────────────────────────────────────────────────────────────────
# PUNTO FINAL DE API REST (para integraciones programáticas)
# Ejemplo de llamada:
#   POST /api/predecir
#   Content-Type: application/json
#   {"intensidad_sintomas": 7, "duracion_dias": 5, "num_sintomas": 3}
# ──────────────────────────────────────────────────────────────────────────────

@app.route("/api/predecir", methods=["POST"])
def predecir_api():
    """Punto final REST que acepta JSON y retorna JSON."""
    datos = request.get_json(force=True)

    if not datos:
        return jsonify({"error": "Se requiere un cuerpo JSON"}), 400

    campos = ["intensidad_sintomas", "duracion_dias", "num_sintomas"]
    faltantes = [c for c in campos if c not in datos]
    if faltantes:
        return jsonify({"error": f"Faltan campos: {faltantes}"}), 400

    try:
        resultado = diagnosticar(
            datos["intensidad_sintomas"],
            datos["duracion_dias"],
            datos["num_sintomas"]
        )
        return jsonify({
            "diagnostico": resultado,
            "parametros_recibidos": {
                "intensidad_sintomas": datos["intensidad_sintomas"],
                "duracion_dias":       datos["duracion_dias"],
                "num_sintomas":        datos["num_sintomas"]
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
