# TaskManager

Sistema web para la gestión de tareas de **TechSolutions**, desarrollado aplicando las fases del ciclo de vida DevOps con GitHub (Projects, Issues, Actions y Releases).

![CI](https://github.com/InSaneIISSGod/TaskManager-DevOps/actions/workflows/ci.yml/badge.svg)

- **Aplicación publicada:** https://taskmanager-devops-c3h2.onrender.com
- **Tablero:** GitHub Projects → *TaskManager DevOps* (público)
- **Versión estable:** [v1.0.0](https://github.com/InSaneIISSGod/TaskManager-DevOps/releases/tag/v1.0.0)

## Funcionalidades

| Código | Funcionalidad | Cómo se usa |
|---|---|---|
| RF01 | Registrar tareas | Formulario "Nueva tarea" (nombre obligatorio, descripción, responsable) |
| RF02 | Consultar tareas | Listado con resumen por estado y filtros por estado/prioridad |
| RF03 | Editar tareas | Botón **Editar** en cada tarea |
| RF04 | Eliminar tareas | Botón **Eliminar** (pide confirmación) |
| RF05 | Cambiar estado | Selector *Pendiente / En proceso / Terminada* en cada tarea |
| RF06 | Asignar prioridad | *Alta / Media / Baja*; el listado se ordena por prioridad |

## Tecnologías

Python 3.12 · Flask · SQLite · HTML/CSS/JavaScript · Pytest · GitHub Actions · Gunicorn · Render

## Estructura

```text
TaskManager-DevOps/
├── app.py                  # Backend Flask + API REST
├── requirements.txt
├── render.yaml             # Configuración de despliegue (Render)
├── templates/index.html    # Interfaz
├── static/css/style.css
├── static/js/app.js
├── tests/test_app.py       # Pruebas unitarias (Pytest)
├── docs/                   # Documentación por fase DevOps
└── .github/
    ├── workflows/ci.yml       # Integración continua
    ├── workflows/cd.yml       # Entrega continua (artefacto en cada release)
    ├── workflows/monitor.yml  # Monitoreo programado del sitio publicado
    └── ISSUE_TEMPLATE/        # Plantillas: tarea, error, incidencia
```

## Ejecutar localmente

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python app.py            # http://127.0.0.1:5000
pytest -v                # pruebas
```

## API REST

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/tareas?estado=&prioridad=` | Lista tareas (filtros opcionales) |
| GET | `/api/tareas/<id>` | Consulta una tarea |
| POST | `/api/tareas` | Registra una tarea |
| PUT | `/api/tareas/<id>` | Edita campos de una tarea |
| PATCH | `/api/tareas/<id>/estado` | Cambia el estado |
| DELETE | `/api/tareas/<id>` | Elimina una tarea |
| GET | `/api/resumen` | Conteo por estado |
| GET | `/health` | Salud del servicio (monitoreo) |

## Documentación DevOps

1. [Planificación](docs/01-planificacion.md)
2. [Desarrollo](docs/02-desarrollo.md)
3. [Integración continua](docs/03-integracion-continua.md)
4. [Pruebas](docs/04-pruebas.md)
5. [Entrega continua](docs/05-entrega-continua.md)
6. [Despliegue](docs/06-despliegue.md)
7. [Operación y monitoreo](docs/07-operacion-monitoreo.md)
8. [Resultados, conclusiones y preguntas de análisis](docs/08-resultados-conclusiones.md)

## Autor

**Emiliano Vega** — proyecto individual. Desempeñé todos los roles: Product Owner, desarrollo backend, desarrollo de interfaz e Ingeniería DevOps / QA.
