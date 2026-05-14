"""
app.py — Servicio de predicción de enfermedades (Versión 2)
Agrega: ENFERMEDAD TERMINAL + módulo de estadísticas
"""

from flask import Flask, request, jsonify, render_template
from datetime import datetime
from collections import deque

app = Flask(__name__)

# ── Estadísticas en memoria ──────────────────────────────────────────────────
estadisticas = {
    "NO ENFERMO": 0,
    "ENFERMEDAD LEVE": 0,
    "ENFERMEDAD AGUDA": 0,
    "ENFERMEDAD CRÓNICA": 0,
    "ENFERMEDAD TERMINAL": 0,
}
ultimas_predicciones = deque(maxlen=5)   # guarda las últimas 5
ultima_fecha = None


def diagnosticar(intensidad_sintomas: float,
                 duracion_dias: float,
                 num_sintomas: int) -> str:
    intensidad_sintomas = max(0.0, min(10.0, float(intensidad_sintomas)))
    duracion_dias       = max(0.0, float(duracion_dias))
    num_sintomas        = max(0, int(num_sintomas))

    puntuacion = (intensidad_sintomas * 0.5) + (num_sintomas * 0.8)

    # Reglas de decisión (ahora con 5 categorías)
    if duracion_dias >= 90 and puntuacion >= 7.0:
        return "ENFERMEDAD TERMINAL"
    elif duracion_dias >= 90:
        return "ENFERMEDAD CRÓNICA"
    elif puntuacion < 2.0:
        return "NO ENFERMO"
    elif puntuacion < 5.5:
        return "ENFERMEDAD LEVE"
    else:
        return "ENFERMEDAD AGUDA"


def registrar_prediccion(resultado, intensidad, duracion, num_sint):
    """Actualiza las estadísticas globales."""
    global ultima_fecha
    estadisticas[resultado] += 1
    ultima_fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ultimas_predicciones.append({
        "diagnostico": resultado,
        "intensidad": intensidad,
        "duracion": duracion,
        "num_sintomas": num_sint,
        "fecha": ultima_fecha
    })


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predecir", methods=["POST"])
def predecir_web():
    try:
        intensidad = request.form.get("intensidad", 0)
        duracion   = request.form.get("duracion", 0)
        num_sint   = request.form.get("num_sintomas", 0)
        resultado  = diagnosticar(intensidad, duracion, num_sint)
        registrar_prediccion(resultado, intensidad, duracion, num_sint)
        return render_template("index.html",
                               resultado=resultado,
                               intensidad=intensidad,
                               duracion=duracion,
                               num_sintomas=num_sint)
    except Exception as e:
        return render_template("index.html", error=str(e))


@app.route("/api/predecir", methods=["POST"])
def predecir_api():
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
        registrar_prediccion(resultado,
                             datos["intensidad_sintomas"],
                             datos["duracion_dias"],
                             datos["num_sintomas"])
        return jsonify({
            "diagnostico": resultado,
            "parametros_recibidos": datos
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/estadisticas", methods=["GET"])
def estadisticas_api():
    """Retorna estadísticas globales del servicio."""
    return jsonify({
        "total_por_categoria": estadisticas,
        "ultimas_5_predicciones": list(ultimas_predicciones),
        "fecha_ultima_prediccion": ultima_fecha
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)