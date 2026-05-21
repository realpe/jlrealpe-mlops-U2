import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from app import app, diagnosticar, estadisticas

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

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

def test_estadisticas_se_actualizan(client):
    antes = estadisticas["NO ENFERMO"]
    client.post("/api/predecir",
        json={"intensidad_sintomas": 1, "duracion_dias": 1, "num_sintomas": 1})
    assert estadisticas["NO ENFERMO"] == antes + 1

def test_estadisticas_iniciales():
    claves = ["NO ENFERMO", "ENFERMEDAD LEVE", "ENFERMEDAD AGUDA",
              "ENFERMEDAD CRÓNICA", "ENFERMEDAD TERMINAL"]
    for c in claves:
        assert c in estadisticas

def test_cinco_categorias_distintas():
    resultados = {
        diagnosticar(1, 2, 1),
        diagnosticar(4, 10, 2),
        diagnosticar(8, 7, 4),
        diagnosticar(5, 120, 3),
        diagnosticar(10, 100, 5),
    }
    assert len(resultados) == 5
