"""Pruebas unitarias de TaskManager (Pytest).

Cada prueba usa una base de datos SQLite temporal, por lo que no afecta los
datos reales. Los identificadores CPxx corresponden a la matriz de casos de
prueba documentada en docs/04-pruebas.md.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  # noqa: E402


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    with app.test_client() as client:
        yield client


def crear(client, **datos):
    base = {"nombre": "Realizar actividad DevOps", "descripcion": "Fase de planificacion",
            "prioridad": "Alta"}
    base.update(datos)
    return client.post("/api/tareas", json=base)


# Ejemplo base del documento
def test_registro_tarea():
    tarea = {"nombre": "Realizar actividad DevOps", "estado": "Pendiente"}
    assert tarea["nombre"] == "Realizar actividad DevOps"
    assert tarea["estado"] == "Pendiente"


# ---------------------------------------------------------------- general
def test_pagina_principal_carga(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "TaskManager" in resp.get_data(as_text=True)


def test_health_check(client):
    resp = client.get("/health")
    datos = resp.get_json()
    assert resp.status_code == 200
    assert datos["status"] == "ok"
    assert datos["base_de_datos"] == "ok"


# ------------------------------------------------- CP01 Registrar una tarea
def test_cp01_registrar_tarea(client):
    resp = crear(client)
    datos = resp.get_json()
    assert resp.status_code == 201
    assert datos["mensaje"] == "Tarea registrada correctamente."
    assert datos["tarea"]["nombre"] == "Realizar actividad DevOps"
    assert datos["tarea"]["estado"] == "Pendiente"  # estado por defecto
    assert datos["tarea"]["id"] > 0


def test_cp01_registrar_tarea_sin_descripcion(client):
    """Regresion del Issue 'Error al guardar tareas sin descripcion'."""
    resp = client.post("/api/tareas", json={"nombre": "Sin descripcion"})
    assert resp.status_code == 201
    assert resp.get_json()["tarea"]["descripcion"] == ""


# ----------------------------------------- CP02 Registrar tarea sin nombre
def test_cp02_registrar_sin_nombre(client):
    resp = client.post("/api/tareas", json={"descripcion": "algo"})
    assert resp.status_code == 400
    assert "El nombre de la tarea es obligatorio." in resp.get_json()["errores"]


def test_cp02_nombre_solo_espacios(client):
    resp = client.post("/api/tareas", json={"nombre": "    ", "descripcion": ""})
    assert resp.status_code == 400


def test_cp02_cuerpo_invalido(client):
    resp = client.post("/api/tareas", data="no es json", content_type="text/plain")
    assert resp.status_code == 400


def test_nombre_demasiado_largo(client):
    resp = client.post("/api/tareas", json={"nombre": "x" * 101, "descripcion": ""})
    assert resp.status_code == 400


# --------------------------------------------------- CP03 Consultar tareas
def test_cp03_consultar_tareas(client):
    crear(client, nombre="Tarea A")
    crear(client, nombre="Tarea B")
    resp = client.get("/api/tareas")
    nombres = [t["nombre"] for t in resp.get_json()]
    assert resp.status_code == 200
    assert len(nombres) == 2
    assert {"Tarea A", "Tarea B"} == set(nombres)


def test_cp03_consultar_vacio(client):
    assert client.get("/api/tareas").get_json() == []


def test_consultar_una_tarea(client):
    tid = crear(client).get_json()["tarea"]["id"]
    resp = client.get(f"/api/tareas/{tid}")
    assert resp.status_code == 200
    assert resp.get_json()["id"] == tid


def test_consultar_tarea_inexistente(client):
    assert client.get("/api/tareas/999").status_code == 404


def test_filtrar_por_estado_y_prioridad(client):
    crear(client, nombre="A", prioridad="Alta")
    crear(client, nombre="B", prioridad="Baja", estado="Terminada")
    assert [t["nombre"] for t in client.get("/api/tareas?prioridad=Baja").get_json()] == ["B"]
    assert [t["nombre"] for t in client.get("/api/tareas?estado=Pendiente").get_json()] == ["A"]


def test_orden_por_prioridad(client):
    crear(client, nombre="baja", prioridad="Baja")
    crear(client, nombre="alta", prioridad="Alta")
    crear(client, nombre="media", prioridad="Media")
    nombres = [t["nombre"] for t in client.get("/api/tareas").get_json()]
    assert nombres == ["alta", "media", "baja"]


# ------------------------------------------------------ CP04 Editar tarea
def test_cp04_editar_tarea(client):
    tid = crear(client).get_json()["tarea"]["id"]
    resp = client.put(f"/api/tareas/{tid}",
                      json={"nombre": "Nombre editado", "descripcion": "Nueva desc"})
    tarea = resp.get_json()["tarea"]
    assert resp.status_code == 200
    assert tarea["nombre"] == "Nombre editado"
    assert tarea["descripcion"] == "Nueva desc"
    assert tarea["prioridad"] == "Alta"  # no cambia lo que no se envio


def test_cp04_editar_con_nombre_vacio(client):
    tid = crear(client).get_json()["tarea"]["id"]
    resp = client.put(f"/api/tareas/{tid}", json={"nombre": ""})
    assert resp.status_code == 400


def test_cp04_editar_inexistente(client):
    assert client.put("/api/tareas/999", json={"nombre": "x"}).status_code == 404


def test_cp04_editar_sin_campos(client):
    tid = crear(client).get_json()["tarea"]["id"]
    assert client.put(f"/api/tareas/{tid}", json={}).status_code == 400


# ---------------------------------------------------- CP05 Eliminar tarea
def test_cp05_eliminar_tarea(client):
    tid = crear(client).get_json()["tarea"]["id"]
    resp = client.delete(f"/api/tareas/{tid}")
    assert resp.status_code == 200
    assert client.get(f"/api/tareas/{tid}").status_code == 404
    assert client.get("/api/tareas").get_json() == []


def test_cp05_eliminar_inexistente(client):
    assert client.delete("/api/tareas/999").status_code == 404


# ----------------------------------------------------- CP06 Cambiar estado
@pytest.mark.parametrize("estado", ["Pendiente", "En proceso", "Terminada"])
def test_cp06_cambiar_estado(client, estado):
    tid = crear(client).get_json()["tarea"]["id"]
    resp = client.patch(f"/api/tareas/{tid}/estado", json={"estado": estado})
    assert resp.status_code == 200
    # El cambio se refleja en el listado
    listado = client.get("/api/tareas").get_json()
    assert listado[0]["estado"] == estado


def test_cp06_estado_invalido(client):
    tid = crear(client).get_json()["tarea"]["id"]
    resp = client.patch(f"/api/tareas/{tid}/estado", json={"estado": "Cancelada"})
    assert resp.status_code == 400


def test_cp06_estado_tarea_inexistente(client):
    resp = client.patch("/api/tareas/999/estado", json={"estado": "Terminada"})
    assert resp.status_code == 404


# ------------------------------------------------ CP07 Seleccionar prioridad
@pytest.mark.parametrize("prioridad", ["Alta", "Media", "Baja"])
def test_cp07_guardar_prioridad(client, prioridad):
    resp = crear(client, prioridad=prioridad)
    assert resp.get_json()["tarea"]["prioridad"] == prioridad


def test_cp07_prioridad_por_defecto(client):
    resp = client.post("/api/tareas", json={"nombre": "Sin prioridad", "descripcion": ""})
    assert resp.get_json()["tarea"]["prioridad"] == "Media"


def test_cp07_prioridad_invalida(client):
    resp = crear(client, prioridad="Urgentisima")
    assert resp.status_code == 400


# ------------------------------------------------------------------ resumen
def test_resumen_por_estado(client):
    crear(client, nombre="a")
    crear(client, nombre="b", estado="Terminada")
    datos = client.get("/api/resumen").get_json()
    assert datos["Total"] == 2
    assert datos["Pendiente"] == 1
    assert datos["Terminada"] == 1


def test_api_ruta_inexistente_regresa_json(client):
    resp = client.get("/api/no-existe")
    assert resp.status_code == 404
    assert resp.get_json()["error"]
