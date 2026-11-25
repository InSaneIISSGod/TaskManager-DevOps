# Fase 2. Desarrollo (Code)

## 2.1 Flujo de trabajo con ramas

Se usa un flujo *feature branch*: `main` siempre contiene código estable y cada funcionalidad se desarrolla en su propia rama, que se integra mediante Pull Request revisado antes de combinarse.

| Rama | Rol | Contenido | Issues |
|---|---|---|---|
| `feature/backend-api` | Backend | `app.py`, `requirements.txt`, `.gitignore`, `render.yaml` | #9, #11 |
| `feature/interfaz` | Interfaz | `templates/`, `static/` (registro, edición, eliminación, estados) | #12, #13, #14, #15 |
| `feature/pruebas-ci` | DevOps / QA | `tests/`, `.github/workflows/`, plantillas de Issues | #16, #17 |
| `fix/validacion-descripcion` | Backend | Corrección del error de la descripción + prueba de regresión | #29 |
| `docs/documentacion` | Product Owner | `docs/`, `README.md` | #10, #22 |

## 2.2 Comandos utilizados

```bash
git clone https://github.com/InSaneIISSGod/TaskManager-DevOps.git
cd TaskManager-DevOps

git checkout -b feature/backend-api
git add .
git commit -m "Agregar API de tareas con Flask y SQLite (RF01-RF06)"
git push origin feature/backend-api
```

Convención de mensajes de commit: verbo en infinitivo + qué se hizo, y referencia al Issue (`Closes #11`) para que GitHub cierre el Issue al combinar el Pull Request.

## 2.3 Pull Requests

Cada Pull Request incluye:
1. Rama origen → `main`.
2. Descripción de los cambios y los Issues relacionados (`Closes #n`).
3. Auto-revisión: comentario en el PR con la lista de verificación (el código cumple la historia de usuario, las pruebas pasan, no hay archivos de más).
4. Ejecución de GitHub Actions en verde (a partir de que existe `ci.yml`).
5. Aprobación y *Merge*.

| PR | Rama | Revisión |
|---|---|---|
| #26 | `feature/backend-api` | Auto-revisión |
| #27 | `feature/interfaz` | Auto-revisión |
| #28 | `feature/pruebas-ci` | Auto-revisión + GitHub Actions |
| #30 | `fix/validacion-descripcion` | Auto-revisión + GitHub Actions (❌ → ✅) |
| #31 | `docs/documentacion` | Auto-revisión + GitHub Actions |

## 2.4 Cumplimiento funcional

Las 6 funcionalidades solicitadas (RF01–RF06) están implementadas (100 %), además de filtros, resumen por estado y punto de salud `/health`.

## 2.5 Evidencias

- [ ] Captura de la pestaña **Branches** con las ramas.
- [ ] Captura de **Commits** (historial).
- [ ] Captura de **Pull requests → Closed** con los PR combinados.
- [ ] Captura de un PR con su auto-revisión.
- [ ] Captura de **Insights → Network** (historial de modificaciones).
