"""
tests/test_app.py — Pruebas unitarias para el servicio de diagnóstico
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app, diagnosticar, estadisticas, ultimas_predicciones

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

# ── Prueba 1: Categorías correctas ──────────────────────────────────────────
def test_no_enfermo():
    assert diagnosticar(1, 2, 1) == "NO ENFERMO"

def test_enfermedad_leve():
    assert diagnosticar(4, 10, 2) == "ENFERMEDAD LEVE"

def test_enfermedad_aguda():
    assert diagnosticar(8, 7, 4) == "ENFERMEDAD AGUDA"

def test_enfermedad_cronica():
    assert diagnosticar(5, 120, 3) == "ENFERMEDAD CRÓNICA"

def test_enfermedad_terminal():
    assert diagnosticar(10, 100, 5) == "ENFERMEDAD TERMINAL"

# ── Prueba 2: Estadísticas se actualizan ────────────────────────────────────
def test_estadisticas_se_actualizan(client):
    from app import estadisticas, ultimas_predicciones
    antes = estadisticas["NO ENFERMO"]
    client.post("/api/predecir",
                json={"intensidad_sintomas": 1, "duracion_dias": 1, "num_sintomas": 1})
    assert estadisticas["NO ENFERMO"] == antes + 1

# ── Prueba 3: Estadísticas inician vacías ────────────────────────────────────
def test_estadisticas_iniciales():
    # Verifica que todas las claves esperadas existen
    claves = ["NO ENFERMO","ENFERMEDAD LEVE","ENFERMEDAD AGUDA",
              "ENFERMEDAD CRÓNICA","ENFERMEDAD TERMINAL"]
    for c in claves:
        assert c in estadisticas

# ── Prueba 4: Existen las 5 categorías distintas ─────────────────────────────
def test_cinco_categorias():
    resultados = {
        diagnosticar(1, 2, 1),
        diagnosticar(4, 10, 2),
        diagnosticar(8, 7, 4),
        diagnosticar(5, 120, 3),
        diagnosticar(10, 100, 5),
    }
<<<<<<< HEAD
    assert len(resultados) == 5
=======
    assert len(resultados) == 5
>>>>>>> añadir-githup-actions
