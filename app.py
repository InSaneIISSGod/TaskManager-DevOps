"""TaskManager - Sistema web para la gestion de tareas (TechSolutions).

Backend en Flask + SQLite. Expone una API REST en /api/tareas y sirve la
interfaz web en "/".
"""
import os
import sqlite3
import time
from datetime import datetime

from flask import Flask, g, jsonify, render_template, request

ESTADOS = ("Pendiente", "En proceso", "Terminada")
PRIORIDADES = ("Alta", "Media", "Baja")
MAX_NOMBRE = 100
MAX_DESCRIPCION = 500

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_VERSION = "1.0.0"


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        DATABASE=os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "taskmanager.db")),
        JSON_AS_ASCII=False,
    )
    if config:
        app.config.update(config)
    app.json.ensure_ascii = False
    app.config["START_TIME"] = time.time()

    # ------------------------------------------------------------------ BD
    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        db = sqlite3.connect(app.config["DATABASE"])
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL DEFAULT '',
                prioridad TEXT NOT NULL DEFAULT 'Media',
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                responsable TEXT NOT NULL DEFAULT '',
                fecha_creacion TEXT NOT NULL,
                fecha_actualizacion TEXT NOT NULL
            )
            """
        )
        db.commit()
        db.close()

    init_db()

    # ----------------------------------------------------------- helpers
    def ahora():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def a_dict(row):
        return dict(row) if row else None

    def validar(datos, parcial=False):
        """Valida y normaliza los datos de una tarea.

        Regresa (datos_limpios, errores).
        """
        errores = []
        limpio = {}

        if not isinstance(datos, dict):
            return {}, ["El cuerpo de la peticion debe ser un objeto JSON."]

        if "nombre" in datos or not parcial:
            nombre = datos.get("nombre")
            nombre = nombre.strip() if isinstance(nombre, str) else ""
            if not nombre:
                errores.append("El nombre de la tarea es obligatorio.")
            elif len(nombre) > MAX_NOMBRE:
                errores.append(f"El nombre no debe superar {MAX_NOMBRE} caracteres.")
            limpio["nombre"] = nombre

        if "descripcion" in datos or not parcial:
            descripcion = datos["descripcion"].strip()
            if len(descripcion) > MAX_DESCRIPCION:
                errores.append(f"La descripcion no debe superar {MAX_DESCRIPCION} caracteres.")
            limpio["descripcion"] = descripcion

        if "prioridad" in datos or not parcial:
            prioridad = datos.get("prioridad") or "Media"
            if prioridad not in PRIORIDADES:
                errores.append("La prioridad debe ser: " + ", ".join(PRIORIDADES) + ".")
            limpio["prioridad"] = prioridad

        if "estado" in datos or not parcial:
            estado = datos.get("estado") or "Pendiente"
            if estado not in ESTADOS:
                errores.append("El estado debe ser: " + ", ".join(ESTADOS) + ".")
            limpio["estado"] = estado

        if "responsable" in datos or not parcial:
            responsable = datos.get("responsable") or ""
            if not isinstance(responsable, str):
                responsable = ""
            limpio["responsable"] = responsable.strip()[:MAX_NOMBRE]

        return limpio, errores

    def buscar(tarea_id):
        return get_db().execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,)).fetchone()

    def no_encontrada():
        return jsonify({"error": "Tarea no encontrada."}), 404

    # ------------------------------------------------------------ rutas
    @app.route("/")
    def index():
        return render_template(
            "index.html", estados=ESTADOS, prioridades=PRIORIDADES, version=APP_VERSION
        )

    # RF02 - Consultar tareas (con filtros opcionales)
    @app.get("/api/tareas")
    def listar_tareas():
        sql = "SELECT * FROM tareas WHERE 1=1"
        params = []
        estado = request.args.get("estado")
        prioridad = request.args.get("prioridad")
        if estado:
            sql += " AND estado = ?"
            params.append(estado)
        if prioridad:
            sql += " AND prioridad = ?"
            params.append(prioridad)
        sql += (
            " ORDER BY CASE prioridad WHEN 'Alta' THEN 1 WHEN 'Media' THEN 2 ELSE 3 END,"
            " id DESC"
        )
        filas = get_db().execute(sql, params).fetchall()
        return jsonify([a_dict(f) for f in filas])

    @app.get("/api/tareas/<int:tarea_id>")
    def obtener_tarea(tarea_id):
        fila = buscar(tarea_id)
        return jsonify(a_dict(fila)) if fila else no_encontrada()

    # RF01 - Registrar tareas
    @app.post("/api/tareas")
    def crear_tarea():
        datos, errores = validar(request.get_json(silent=True))
        if errores:
            return jsonify({"errores": errores}), 400
        fecha = ahora()
        db = get_db()
        cur = db.execute(
            "INSERT INTO tareas (nombre, descripcion, prioridad, estado, responsable,"
            " fecha_creacion, fecha_actualizacion) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                datos["nombre"],
                datos["descripcion"],
                datos["prioridad"],
                datos["estado"],
                datos["responsable"],
                fecha,
                fecha,
            ),
        )
        db.commit()
        tarea = a_dict(buscar(cur.lastrowid))
        return jsonify({"mensaje": "Tarea registrada correctamente.", "tarea": tarea}), 201

    # RF03 - Editar tareas
    @app.put("/api/tareas/<int:tarea_id>")
    def editar_tarea(tarea_id):
        if not buscar(tarea_id):
            return no_encontrada()
        datos, errores = validar(request.get_json(silent=True), parcial=True)
        if errores:
            return jsonify({"errores": errores}), 400
        if not datos:
            return jsonify({"errores": ["No se enviaron campos para actualizar."]}), 400
        datos["fecha_actualizacion"] = ahora()
        columnas = ", ".join(f"{k} = ?" for k in datos)
        db = get_db()
        db.execute(f"UPDATE tareas SET {columnas} WHERE id = ?", (*datos.values(), tarea_id))
        db.commit()
        return jsonify(
            {"mensaje": "Tarea actualizada correctamente.", "tarea": a_dict(buscar(tarea_id))}
        )

    # RF05 - Cambiar estado
    @app.patch("/api/tareas/<int:tarea_id>/estado")
    def cambiar_estado(tarea_id):
        if not buscar(tarea_id):
            return no_encontrada()
        cuerpo = request.get_json(silent=True) or {}
        estado = cuerpo.get("estado") if isinstance(cuerpo, dict) else None
        if estado not in ESTADOS:
            return jsonify({"errores": ["El estado debe ser: " + ", ".join(ESTADOS) + "."]}), 400
        db = get_db()
        db.execute(
            "UPDATE tareas SET estado = ?, fecha_actualizacion = ? WHERE id = ?",
            (estado, ahora(), tarea_id),
        )
        db.commit()
        return jsonify({"mensaje": f"Estado cambiado a {estado}.", "tarea": a_dict(buscar(tarea_id))})

    # RF04 - Eliminar tareas
    @app.delete("/api/tareas/<int:tarea_id>")
    def eliminar_tarea(tarea_id):
        if not buscar(tarea_id):
            return no_encontrada()
        db = get_db()
        db.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
        db.commit()
        return jsonify({"mensaje": "Tarea eliminada correctamente."})

    # Resumen para la interfaz
    @app.get("/api/resumen")
    def resumen():
        db = get_db()
        conteo = {e: 0 for e in ESTADOS}
        for fila in db.execute("SELECT estado, COUNT(*) AS n FROM tareas GROUP BY estado"):
            conteo[fila["estado"]] = fila["n"]
        conteo["Total"] = sum(conteo.values())
        return jsonify(conteo)

    # Fase 7 - Monitoreo: verificacion de salud del servicio
    @app.get("/health")
    def health():
        inicio = time.perf_counter()
        try:
            total = get_db().execute("SELECT COUNT(*) FROM tareas").fetchone()[0]
            bd = "ok"
        except sqlite3.Error as exc:  # pragma: no cover - solo ante fallas reales
            total, bd = None, f"error: {exc}"
        return (
            jsonify(
                {
                    "status": "ok" if bd == "ok" else "error",
                    "version": APP_VERSION,
                    "base_de_datos": bd,
                    "total_tareas": total,
                    "uptime_segundos": round(time.time() - app.config["START_TIME"], 1),
                    "tiempo_respuesta_ms": round((time.perf_counter() - inicio) * 1000, 2),
                }
            ),
            200 if bd == "ok" else 503,
        )

    @app.errorhandler(404)
    def error_404(_e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Recurso no encontrado."}), 404
        return render_template("index.html", estados=ESTADOS, prioridades=PRIORIDADES, version=APP_VERSION), 404

    @app.errorhandler(500)
    def error_500(_e):
        app.logger.exception("Error interno")
        return jsonify({"error": "Error interno del servidor."}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
