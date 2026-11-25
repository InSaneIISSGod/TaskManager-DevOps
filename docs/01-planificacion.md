# Fase 1. Planificación (Plan)

## 1.1 Repositorio

- **Nombre:** `TaskManager-DevOps`
- **Descripción:** Sistema web para la gestión de tareas.
- **Visibilidad:** Public
- **README:** inicializado al crear el repositorio.

## 1.2 Tablero de GitHub Projects

Proyecto **TaskManager DevOps**, vista **Board**, agrupado por el campo *Status* con las columnas:

| Columna | Significado |
|---|---|
| Backlog | Actividades pendientes de realizar |
| To Do | Actividades que se realizarán en la iteración |
| In Progress | Actividades en desarrollo |
| Review | Actividades en revisión (Pull Request abierto) |
| Done | Actividades terminadas |

Campos personalizados del proyecto:

| Propiedad | Tipo de campo | Valores |
|---|---|---|
| Tarea | Título | Nombre de la actividad |
| Responsable | Assignees | Persona asignada |
| Estado | Status | Backlog, To Do, In Progress, Review, Done |
| Prioridad | Single select | Crítica, Alta, Media, Baja |
| Estimación | Number | Horas de trabajo estimadas |
| Fase DevOps | Single select | Plan, Code, Build, Test, Release, Deploy, Operate, Monitor |
| Fecha límite | Date | Fecha de entrega |

## 1.3 Distribución de responsabilidades

El proyecto se realizó de forma **individual**, por lo que una sola persona desempeñó los cuatro roles propuestos. Para mantener el orden, el trabajo se dividió por rol y cada rol tuvo sus propias ramas e Issues:

| Rol | Responsabilidades | Issues |
|---|---|---|
| Product Owner | Requerimientos, prioridades, historias de usuario y tablero | #1–#10, #22 |
| Desarrollador 1 (backend) | API Flask y base de datos SQLite | #11, #29 |
| Desarrollador 2 (interfaz) | HTML, CSS y JavaScript; registro, edición, eliminación y cambio de estado | #12–#15 |
| Ingeniero DevOps / QA | Pruebas unitarias y funcionales, GitHub Actions, release, despliegue y monitoreo | #16–#21 |

Todos los Issues están asignados a **Emiliano Vega**. Como GitHub no permite aprobar un Pull Request propio, cada PR se revisó con una **auto-revisión** (comentario con la lista de verificación) y con la ejecución de GitHub Actions en verde antes de combinarlo a `main`.

## 1.4 Historias de usuario

### HU-01: Registrar tareas (RF01)
**Como** usuario del sistema, **quiero** registrar nuevas tareas **para** organizar mis actividades.

Criterios de aceptación:
- El sistema debe permitir ingresar el nombre de la tarea.
- El sistema debe permitir agregar una descripción (opcional).
- El sistema debe permitir seleccionar una prioridad.
- El sistema debe guardar la tarea.
- El sistema debe mostrar un mensaje de confirmación.
- Si el nombre está vacío, el sistema debe mostrar una validación y no guardar.

### HU-02: Consultar tareas (RF02)
**Como** usuario, **quiero** ver todas las tareas registradas **para** saber qué actividades existen y en qué situación están.

Criterios de aceptación:
- El sistema debe mostrar el listado de todas las tareas al abrir la página.
- Cada tarea debe mostrar nombre, descripción, prioridad, estado, responsable y fecha de creación.
- Debe mostrarse un resumen con el total de tareas pendientes, en proceso y terminadas.
- Debe poder filtrarse el listado por estado y por prioridad.
- Si no hay tareas, debe mostrarse el mensaje "No hay tareas registradas".

### HU-03: Editar tareas (RF03)
**Como** usuario, **quiero** modificar la información de una tarea **para** corregir datos o actualizar su contenido.

Criterios de aceptación:
- Cada tarea debe tener un botón **Editar**.
- Debe abrirse un formulario con los datos actuales de la tarea.
- Debe permitir modificar nombre, descripción, responsable, prioridad y estado.
- No debe permitir dejar el nombre vacío.
- Al guardar, el listado debe mostrar la información actualizada y un mensaje de confirmación.

### HU-04: Eliminar tareas (RF04)
**Como** usuario, **quiero** eliminar tareas **para** quitar actividades duplicadas o que ya no aplican.

Criterios de aceptación:
- Cada tarea debe tener un botón **Eliminar**.
- El sistema debe pedir confirmación antes de eliminar.
- La tarea eliminada debe desaparecer del listado.
- Debe mostrarse un mensaje de confirmación.

### HU-05: Cambiar estado de tareas (RF05)
**Como** usuario, **quiero** cambiar el estado de una tarea **para** conocer su progreso.

Criterios de aceptación:
- Debe permitir seleccionar *Pendiente*.
- Debe permitir seleccionar *En proceso*.
- Debe permitir seleccionar *Terminada*.
- El cambio debe reflejarse en el listado de tareas y en el resumen.

### HU-06: Asignar prioridad (RF06)
**Como** usuario, **quiero** clasificar las tareas como alta, media o baja **para** atender primero lo más importante.

Criterios de aceptación:
- Debe permitir elegir *Alta*, *Media* o *Baja* al registrar y al editar.
- Si no se elige, la prioridad por defecto es *Media*.
- La prioridad debe mostrarse con un color distinto en el listado.
- El listado debe ordenarse de mayor a menor prioridad.

### HU-07: Verificar la calidad antes de publicar (requerimiento del cliente)
**Como** responsable de TechSolutions, **quiero** que cada cambio se pruebe automáticamente **para** no publicar versiones con errores.

Criterios de aceptación:
- Cada push y Pull Request hacia `main` debe ejecutar las pruebas en GitHub Actions.
- Un Pull Request con pruebas fallidas no debe combinarse.
- Cada versión publicada debe generar un artefacto descargable.

### HU-08: Consultar el sistema en línea
**Como** empleado de TechSolutions, **quiero** acceder al sistema desde una URL pública **para** usarlo sin instalar nada.

Criterios de aceptación:
- La aplicación debe estar desplegada en un servicio en la nube.
- La URL debe cargar la página principal y permitir registrar, editar, eliminar y cambiar estado.
- Debe existir un punto de verificación de salud (`/health`) para monitoreo.

## 1.5 Issues registrados

Fecha de inicio: 24/11/2026 · Fecha límite general: 25/11/2026.

Las historias de usuario HU-01…HU-08 se registraron como Issues **#1–#8** (etiqueta `historia de usuario`). Las actividades son los Issues **#9–#25**:

| # | Tarea | Responsable | Prioridad | Estimación (h) | Fase DevOps | Historia |
|---|---|---|---|---|---|---|
| 9 | Crear la estructura inicial del proyecto | Emiliano Vega | Alta | 1 | Plan | — |
| 10 | Configurar el tablero y distribuir responsabilidades | Emiliano Vega | Alta | 1 | Plan | Todas |
| 11 | Implementar la API y base de datos (RF01–RF06) | Emiliano Vega | Crítica | 4 | Code | #1–#6 |
| 12 | Diseñar la interfaz del sistema | Emiliano Vega | Alta | 3 | Code | #2 |
| 13 | Implementar el registro de tareas en la interfaz | Emiliano Vega | Crítica | 1 | Code | #1, #6 |
| 14 | Implementar la edición de tareas | Emiliano Vega | Alta | 1 | Code | #3 |
| 15 | Implementar eliminación y cambio de estado | Emiliano Vega | Alta | 1 | Code | #4, #5 |
| 16 | Implementar las pruebas unitarias | Emiliano Vega | Alta | 2 | Test | #7 |
| 17 | Configurar integración continua con GitHub Actions | Emiliano Vega | Alta | 1 | Build | #7 |
| 18 | Ejecutar pruebas funcionales CP01–CP07 | Emiliano Vega | Alta | 1 | Test | #1–#6 |
| 19 | Crear release v1.0.0 y workflow de entrega | Emiliano Vega | Media | 1 | Release | #7 |
| 20 | Desplegar la aplicación en Render | Emiliano Vega | Alta | 1 | Deploy | #8 |
| 21 | Monitorear la aplicación publicada | Emiliano Vega | Media | 1 | Monitor | #8 |
| 22 | Documentación, resultados y conclusiones | Emiliano Vega | Media | 2 | Operate | — |
| 23 | [Mejora v1.1] Autenticación de usuarios | Emiliano Vega | Media | 6 | Plan | — |
| 24 | [Mejora v1.1] Búsqueda por texto y filtro por responsable | Emiliano Vega | Baja | 3 | Plan | — |
| 25 | [Mejora v1.1] Base de datos persistente (PostgreSQL) | Emiliano Vega | Alta | 3 | Plan | — |

Issues creados en fases posteriores:

| # | Tarea | Fase | Origen |
|---|---|---|---|
| 29 | [Error] Error al guardar tareas sin descripción | Test | Pruebas funcionales (Fase 4) |
| 32 | [Incidencia] Las tareas desaparecen tras reiniciar el servicio | Operate | Monitoreo (Fase 7) |
| 33 | [Incidencia] La primera carga tarda cerca de un minuto | Monitor | Monitoreo (Fase 7) |

Los Issues 23–25 permanecen en **Backlog** como planeación de la siguiente versión.