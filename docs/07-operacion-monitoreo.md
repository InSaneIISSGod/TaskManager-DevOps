# Fase 7. Operación y monitoreo (Operate & Monitor)

## 7.1 Mecanismos de monitoreo

| Aspecto | Cómo se monitorea |
|---|---|
| Disponibilidad | Workflow `monitor.yml` cada 6 horas consulta `/health`; si no responde 200, la ejecución falla y GitHub notifica por correo. Render también usa `/health` como *health check*. |
| Tiempo de respuesta | `monitor.yml` registra el tiempo total de la petición; `/health` reporta `tiempo_respuesta_ms` de la base de datos. |
| Errores | Pestaña **Logs** de Render (errores 500 y trazas de Python). |
| Almacenamiento | `/health` reporta `base_de_datos: ok` y `total_tareas`. |
| Funcionalidades principales | Pruebas funcionales CP01–CP07 repetidas sobre la URL pública. |

Configuración: en GitHub → *Settings → Secrets and variables → Actions → Variables* crear `APP_URL` con la URL pública.

## 7.2 Registro de monitoreo

| Fecha y hora | Disponible | Código HTTP | Tiempo de respuesta | Total tareas | Observaciones |
|---|---|---|---|---|---|
| 25/11/2026 02:05 | ✅ Sí | 200 | 0.35 s | 0 | Primera revisión, recién desplegado (uptime 129 s) |
| 25/11/2026 02:12 | ✅ Sí | 200 | BD 0.45 ms | 3 | Revisión manual de `/health` tras las pruebas funcionales |
| 25/11/2026 02:14 | ✅ Sí | 200 | 0.32 s | 3 | Workflow **Monitoreo #1** en GitHub Actions |
| 25/11/2026 02:20 | ✅ Sí | 200 | 0.58 s | 3 | Revisión manual (uptime 1034 s, BD 1.29 ms) |

Horas en tiempo del centro de México (CST). A partir de aquí el workflow `monitor.yml` registra una revisión cada 6 horas en la pestaña **Actions**.

## 7.3 Registro de incidencias

Las incidencias se documentan en GitHub Issues con la plantilla **Incidencia en producción**.

### INC-01 (Issue #32): Las tareas registradas desaparecen después de un reinicio del servicio
- **Fecha de detección:** 25/11/2026
- **Funcionalidad afectada:** Consultar tareas (RF02) / almacenamiento.
- **Descripción del problema:** Tras un nuevo despliegue en Render, el listado aparece vacío.
- **Evidencia:** captura del listado vacío y del log de despliegue.
- **Responsable de corregirlo:** Emiliano Vega.
- **Causa:** el plan gratuito de Render usa disco efímero; el archivo SQLite se recrea en cada despliegue.
- **Solución aplicada:** se documentó la limitación y se planificó migrar a PostgreSQL administrado (Issue #25, versión 1.1).

### INC-02 (Issue #33): La primera carga tarda cerca de un minuto
- **Fecha de detección:** 25/11/2026
- **Funcionalidad afectada:** Disponibilidad.
- **Descripción del problema:** después de un periodo sin uso, la primera petición tarda ~50 s.
- **Responsable:** Emiliano Vega.
- **Causa:** el plan gratuito suspende el servicio tras 15 minutos de inactividad.
- **Solución aplicada:** el workflow de monitoreo reintenta con tiempo de espera de 90 s; para producción se recomienda un plan de pago.

## 7.4 Propuestas de mejora (versión 1.1)

1. **Autenticación de usuarios** (Issue #23): inicio de sesión para que cada empleado vea sus tareas y quede registrado quién hace cada cambio.
2. **Búsqueda y filtros avanzados** (Issue #24): búsqueda por texto, filtro por responsable y por fecha límite.
3. **Base de datos persistente** (Issue #25): PostgreSQL en producción para no perder información.
4. **Notificaciones** por correo cuando se asigna una tarea o se acerca su fecha límite.
5. **Reportes de productividad**: tareas terminadas por persona y por semana.

## 7.5 Planeación de la nueva versión

| Versión | Contenido | Prioridad | Estimación |
|---|---|---|---|
| v1.1.0 | PostgreSQL (#25), búsqueda y filtros (#24) | Alta | 1 semana |
| v1.2.0 | Autenticación de usuarios (#23) | Media | 2 semanas |
| v2.0.0 | Notificaciones y reportes de productividad | Baja | 3 semanas |

Las mejoras están registradas como Issues en la columna **Backlog** del tablero.

## 7.6 Evidencias

- [ ] Captura de una ejecución del workflow *Monitoreo* con el resumen.
- [ ] Captura de `/health` en el navegador.
- [ ] Capturas de las incidencias registradas en Issues.
- [ ] Captura del Backlog con las mejoras de la v1.1.
