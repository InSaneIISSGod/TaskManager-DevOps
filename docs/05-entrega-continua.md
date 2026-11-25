# Fase 5. Entrega continua (Continuous Delivery)

## 5.1 Revisión de la versión estable

| Verificación | Estado |
|---|---|
| Todas las funcionalidades RF01–RF06 implementadas | ✅ |
| Pruebas aprobadas en GitHub Actions (33/33) | ✅ |
| Sin errores críticos conocidos (Issue #29 cerrado) | ✅ |
| Código integrado en `main` mediante Pull Requests | ✅ |
| Documentación del sistema (`README.md` y `docs/`) | ✅ |

## 5.2 Release

- **Etiqueta:** `v1.0.0`
- **Título:** Primera versión estable de TaskManager
- **Rama:** `main`

### Notas de versión (texto para el Release)

```markdown
## TaskManager v1.0.0 — Primera versión estable

Sistema web para la gestión de tareas de TechSolutions.

### Funcionalidades
- RF01 Registrar tareas con nombre, descripción, responsable, prioridad y estado.
- RF02 Consultar tareas con resumen por estado y filtros por estado y prioridad.
- RF03 Editar tareas.
- RF04 Eliminar tareas con confirmación.
- RF05 Cambiar estado: Pendiente, En proceso, Terminada.
- RF06 Asignar prioridad: Alta, Media, Baja (el listado se ordena por prioridad).

### Calidad
- 33 pruebas unitarias automatizadas con Pytest ejecutadas en GitHub Actions.
- Corrección: el registro de tareas sin descripción ya no genera error (#29).

### Operación
- Endpoint `/health` para monitoreo de disponibilidad y tiempo de respuesta.
- Despliegue en Render con Gunicorn.
```

## 5.3 Workflow de entrega `.github/workflows/cd.yml`

Se ejecuta al **publicar un Release**: vuelve a correr las pruebas y genera el artefacto descargable `TaskManager-v1.0.0` con `app.py`, `requirements.txt`, `render.yaml`, `README.md`, `templates/` y `static/`.

Este workflow prepara un paquete; la publicación en el servidor la hace Render (Fase 6).

## 5.4 Evidencias

- [ ] Captura del Release `v1.0.0` publicado con sus notas.
- [ ] Captura de la ejecución del workflow *Entrega Continua*.
- [ ] Captura de la sección **Artifacts** con `TaskManager-v1.0.0`.
