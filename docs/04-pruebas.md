# Fase 4. Pruebas (Test)

## 4.1 Matriz de casos de prueba

| ID | Prueba | Datos de entrada | Resultado esperado | Prueba automatizada | Resultado |
|---|---|---|---|---|---|
| CP01 | Registrar una tarea | Nombre "Elaborar documentación", descripción, prioridad Alta | La tarea se guarda y aparece en el listado con mensaje de confirmación | `test_cp01_*` | ✅ Aprobada (tras corregir Issue #29) |
| CP02 | Registrar una tarea sin nombre | Nombre vacío | El sistema muestra "El nombre de la tarea es obligatorio." y no guarda | `test_cp02_*` | ✅ Aprobada |
| CP03 | Consultar tareas | Abrir el sistema con tareas registradas | Se muestra el listado ordenado por prioridad y el resumen por estado | `test_cp03_*` | ✅ Aprobada |
| CP04 | Editar una tarea | Cambiar nombre y descripción | Se actualiza la información en el listado | `test_cp04_*` | ✅ Aprobada |
| CP05 | Eliminar una tarea | Botón Eliminar → Aceptar | La tarea desaparece del listado | `test_cp05_*` | ✅ Aprobada |
| CP06 | Cambiar estado | Pendiente → En proceso → Terminada | Se actualiza el estado y el resumen | `test_cp06_*` | ✅ Aprobada |
| CP07 | Seleccionar prioridad | Alta / Media / Baja | Se guarda la prioridad elegida y se muestra con su color | `test_cp07_*` | ✅ Aprobada |
| CP08 | Filtrar tareas | Filtro estado = Terminada | Solo se muestran tareas terminadas | `test_filtrar_*` | ✅ Aprobada |
| CP09 | Registrar tarea sin descripción | Solo nombre | La tarea se guarda con descripción vacía | `test_cp01_registrar_tarea_sin_descripcion` | ❌ → ✅ (Issue #29) |

## 4.2 Pruebas funcionales (manuales)

Ambiente: navegador Chrome/Edge, aplicación local (`python app.py`) y posteriormente la URL pública.

### CP01: Registrar una tarea
1. Abrir el sistema.
2. Ir al formulario **Nueva tarea**.
3. Escribir el nombre: *Elaborar documentación*.
4. Agregar una descripción.
5. Seleccionar prioridad **Alta**.
6. Presionar **Guardar tarea**.
7. Verificar que aparezca en el listado y el mensaje "Tarea registrada correctamente."

### CP02: Registrar una tarea sin nombre
1. Dejar el nombre vacío y presionar **Guardar tarea**.
2. Verificar el mensaje en rojo "El nombre de la tarea es obligatorio." y que no se agregue nada al listado.

### CP03: Consultar tareas
1. Registrar 3 tareas con prioridades distintas.
2. Recargar la página.
3. Verificar que aparecen las 3, ordenadas Alta → Media → Baja, y que el resumen muestra Total = 3.

### CP04: Editar una tarea
1. Presionar **Editar** en una tarea.
2. Cambiar el nombre y la descripción y presionar **Guardar cambios**.
3. Verificar los nuevos datos en el listado.

### CP05: Eliminar una tarea
1. Presionar **Eliminar** y aceptar la confirmación.
2. Verificar que la tarea desaparece y el total disminuye.

### CP06: Cambiar estado
1. En el selector de estado de una tarea elegir **En proceso**, luego **Terminada**.
2. Verificar el mensaje de confirmación, que el nombre aparece tachado al terminar y que el resumen se actualiza.

### CP07: Seleccionar prioridad
1. Registrar una tarea con prioridad **Baja**.
2. Verificar la etiqueta verde "Baja" y que la tarea aparece al final del listado.

### CP09: Registrar tarea sin descripción
1. Escribir solo el nombre *Tarea sin descripción* y guardar.
2. **Resultado obtenido en la primera versión:** mensaje rojo "Error inesperado." → se reportó el Issue #29.
3. **Resultado tras la corrección:** la tarea se guarda correctamente.

## 4.3 Error reportado mediante GitHub Issues

**Título:** Error al guardar tareas sin descripción

- **Funcionalidad afectada:** Registro de tareas (RF01).
- **Pasos para reproducir:** Abrir el sistema → escribir solo el nombre → Guardar tarea.
- **Resultado obtenido:** El sistema muestra "Error inesperado." (HTTP 500, `KeyError: 'descripcion'`).
- **Resultado esperado:** La descripción es opcional; la tarea debe guardarse.
- **Prioridad:** Alta.
- **Corrección:** rama `fix/validacion-descripcion`, Pull Request que agrega la prueba de regresión y la validación.

## 4.4 Evidencias

- [ ] Esta matriz de casos de prueba.
- [ ] Capturas de cada prueba funcional CP01–CP07.
- [ ] Captura del Issue #29 (error) cerrado por el PR.
- [ ] Captura del PR de corrección con la ejecución ❌ y luego ✅.
- [ ] Captura de la nueva ejecución exitosa de GitHub Actions en `main`.
