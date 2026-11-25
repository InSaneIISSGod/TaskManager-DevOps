# Resultados y conclusiones

## Resultados por fase

| Fase DevOps | Herramienta | Resultado obtenido |
|---|---|---|
| Planificación | GitHub Projects e Issues | Tablero con 5 columnas, 8 historias de usuario y 8 historias como Issues y 20 Issues de actividades con responsable, prioridad, estimación, fase y fecha límite |
| Desarrollo | Git y GitHub | Aplicación Flask + SQLite con RF01–RF06 al 100 %, 5 ramas y 5 Pull Requests revisados |
| Integración continua | GitHub Actions | Workflow `ci.yml` que ejecuta 33 pruebas en cada push y PR |
| Pruebas | Pytest y pruebas manuales | Matriz CP01–CP09; 1 error detectado (#29) y corregido con rama + PR |
| Entrega continua | GitHub Releases y Actions | Release `v1.0.0` y artefacto `TaskManager-v1.0.0` generado por `cd.yml` |
| Despliegue | Render | Aplicación pública con Gunicorn y despliegue automático desde `main` |
| Operación y monitoreo | `/health`, `monitor.yml`, Issues | Registro de monitoreo, 2 incidencias documentadas y plan de versión 1.1 |

## Conclusiones

1. TaskManager resuelve los problemas de TechSolutions con las hojas de cálculo: la información está centralizada en una base de datos, cada tarea tiene estado, prioridad y responsable, y el resumen muestra de inmediato qué está pendiente y qué está terminado.
2. Usar GitHub como plataforma única permitió unir la planificación (Projects, Issues), el código (ramas y Pull Requests), la calidad (Actions) y la entrega (Releases) en un solo lugar, con trazabilidad de cada cambio hasta su Issue.
3. La integración continua mostró su valor en la práctica: el error de la descripción vacía se detectó con una prueba automatizada antes de llegar a `main`, y el PR no se combinó hasta que la ejecución estuvo en verde.
4. Aunque el proyecto fue individual, trabajar con ramas y Pull Requests mantuvo `main` siempre estable, separó cada funcionalidad en un cambio revisable y dejó un historial claro de qué se hizo y por qué.
5. El despliegue con Render y el monitoreo con `/health` demostraron que DevOps no termina al publicar: el monitoreo reveló limitaciones del plan gratuito (disco efímero y arranque en frío) que se convirtieron en mejoras planificadas para la siguiente versión.

## Preguntas de análisis

**1. ¿Qué ventajas ofrece utilizar GitHub Projects para organizar un proyecto de software?**
Permite ver en un tablero el estado de todas las actividades, asignar responsables, prioridades, estimaciones y fechas, y vincular cada tarjeta con su Issue y su Pull Request. Así cualquier persona del proyecto sabe qué falta, quién lo hace y qué está bloqueado, sin depender de hojas de cálculo separadas del código.

**2. ¿Cuál es la diferencia entre Git y GitHub?**
Git es el sistema de control de versiones que se instala localmente y registra el historial de cambios (commits, ramas, merges). GitHub es una plataforma en la nube que aloja repositorios Git y agrega herramientas de colaboración: Pull Requests, Issues, Projects, Actions, Releases y control de acceso.

**3. ¿Por qué es importante utilizar ramas durante el desarrollo?**
Porque cada funcionalidad se desarrolla de forma aislada sin romper el código estable de `main`. Se pueden desarrollar varias funcionalidades en paralelo, probarlas y revisarlas por separado, y solo integrarlas cuando están listas.

**4. ¿Qué función cumple un Pull Request?**
Es la solicitud para integrar los cambios de una rama en otra. Muestra las diferencias, permite que otra persona revise y comente el código, ejecuta las pruebas automáticas y deja un registro de quién aprobó qué. Además puede cerrar automáticamente los Issues relacionados.

**5. ¿Qué problemas permite detectar la integración continua?**
Errores de lógica que rompen pruebas, errores de sintaxis, dependencias faltantes o incompatibles, conflictos entre cambios de distintas ramas o desarrolladores y regresiones (funcionalidades que dejan de funcionar al agregar código nuevo), todo antes de que lleguen a la rama principal.

**6. ¿Cuál es la diferencia entre integración continua y entrega continua?**
La integración continua combina y prueba automáticamente el código cada vez que hay cambios. La entrega continua va un paso más allá: deja una versión estable empaquetada y lista para publicarse en cualquier momento (en este proyecto, el Release `v1.0.0` y su artefacto), aunque la decisión de publicar sigue siendo manual.

**7. ¿Qué diferencia existe entre entrega continua y despliegue continuo?**
En la entrega continua el software queda listo para publicarse, pero una persona decide cuándo hacerlo. En el despliegue continuo cada cambio que pasa las pruebas se publica automáticamente en producción, sin intervención manual (como Render al recibir commits en `main`).

**8. ¿Por qué es importante automatizar las pruebas?**
Porque se ejecutan siempre, de la misma forma y en segundos, en cada cambio. Evitan olvidos, detectan regresiones de inmediato y dan confianza para modificar el código. Hacerlo a mano en cada cambio sería lento y propenso a errores.

**9. ¿Qué sucede si se integra código que contiene errores?**
El error llega a la rama principal y puede afectar a todos los que trabajan en el proyecto y, si se despliega, a los usuarios finales: pérdida de datos, funciones que dejan de servir o caídas del sistema. Corregirlo después cuesta más tiempo y dinero que detectarlo antes con CI y revisión de código.

**10. ¿Por qué DevOps requiere monitorear una aplicación después de publicarla?**
Porque en producción aparecen problemas que no se ven en desarrollo: caídas, lentitud, errores con datos reales o limitaciones de la infraestructura. El monitoreo permite detectarlos rápido, registrarlos como incidencias y convertirlos en mejoras, cerrando el ciclo DevOps de retroalimentación.

**11. ¿Qué beneficios obtiene una empresa al implementar DevOps?**
Entregas más rápidas y frecuentes, menos errores en producción, mejor colaboración entre desarrollo y operaciones, trazabilidad de cada cambio, recuperación más rápida ante fallas y la capacidad de responder pronto a las necesidades del cliente.

**12. ¿Cómo podrían mejorar el proceso de desarrollo en una segunda versión?**
Agregando revisión obligatoria y protección de la rama `main` (no permitir merge sin CI en verde), análisis de estilo y cobertura de código en el pipeline, un ambiente de *staging* antes de producción, base de datos PostgreSQL, alertas automáticas de monitoreo y sprints con fechas definidas en GitHub Projects (campo *Iteration*).
