# Fase 3. Integración continua (CI)

## 3.1 Pruebas unitarias

Archivo: `tests/test_app.py` — **33 pruebas** con Pytest. Cada prueba crea una base de datos SQLite temporal, así no se modifican datos reales, y llama a la API real de la aplicación mediante el cliente de pruebas de Flask.

| Grupo | Qué verifica |
|---|---|
| General | La página principal carga; `/health` responde `ok` |
| CP01 | Registro de tarea, estado por defecto, registro sin descripción |
| CP02 | Validación de nombre vacío, solo espacios, cuerpo inválido y nombre > 100 caracteres |
| CP03 | Listado, listado vacío, consulta por id, filtros, orden por prioridad |
| CP04 | Edición, nombre vacío, tarea inexistente, petición sin campos |
| CP05 | Eliminación y tarea inexistente |
| CP06 | Cambio a los 3 estados, estado inválido, tarea inexistente |
| CP07 | Guardado de las 3 prioridades, prioridad por defecto, prioridad inválida |

Ejecución local:

```bash
pytest -v
```

## 3.2 Workflow `.github/workflows/ci.yml`

Se ejecuta en cada `push` y `pull_request` hacia `main` (y manualmente con *Run workflow*):

1. Descarga el código (`actions/checkout@v4`).
2. Configura Python 3.12 (`actions/setup-python@v5`).
3. Instala dependencias de `requirements.txt`.
4. Ejecuta `pytest -v` y genera un reporte JUnit.
5. Sube el reporte como artefacto `reporte-pruebas`.

## 3.3 Registro de errores detectados y corregidos

| Fecha | Ejecución | Error detectado | Causa | Corrección | Resultado |
|---|---|---|---|---|---|
| 25/11/2026 | Integracion Continua #3 — PR #30 (1er commit) | `test_cp01_registrar_tarea_sin_descripcion` falla con `KeyError: 'descripcion'` | El backend accedía a `datos["descripcion"]` sin verificar que existiera | Tratar la descripción como opcional: `datos.get("descripcion") or ""` (Issue #29) | ✅ Integracion Continua #4 (PR) y #5 (main) en verde |

## 3.4 Evidencias

- [ ] Captura del archivo `ci.yml` en GitHub.
- [ ] Captura de la pestaña **Actions** con el workflow *Integracion Continua*.
- [ ] Captura de una ejecución **fallida** (❌) con el detalle del error.
- [ ] Captura de una ejecución **exitosa** (✅) con las 33 pruebas aprobadas.
