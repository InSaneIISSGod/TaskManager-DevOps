# Fase 6. Despliegue continuo (Continuous Deployment)

## 6.1 Servicio seleccionado: Render

Se eligió **Render** porque tiene plan gratuito para servicios web Python, se conecta directamente con GitHub y vuelve a desplegar automáticamente cada vez que hay cambios en `main` (despliegue continuo).

## 6.2 Configuración

El repositorio incluye `render.yaml` (Infrastructure as Code):

| Parámetro | Valor |
|---|---|
| Tipo | Web Service |
| Runtime | Python 3.12 |
| Rama | `main` |
| Comando de instalación | `pip install -r requirements.txt` |
| Comando de inicio | `gunicorn app:app` |
| Health check | `/health` |
| Variables de entorno | `PYTHON_VERSION=3.12.7` |
| Auto-Deploy | Activado (cada commit en `main`) |

Pasos realizados:
1. Crear cuenta en https://render.com con la cuenta de GitHub.
2. **New → Blueprint** (o **New → Web Service**) y seleccionar el repositorio `TaskManager-DevOps`.
3. Render detecta `render.yaml` y aplica los comandos de instalación e inicio.
4. Seleccionar **Deploy** y esperar a que el estado sea **Live**.

Primer despliegue: 25/11/2026 02:01–02:02 (CST), commit `06f8198` (merge del PR #31), duración 1 min 2 s, resultado **Deploy succeeded / Live**. Cada merge posterior a `main` se despliega automáticamente.

## 6.3 Verificación de la aplicación publicada

URL pública: **https://taskmanager-devops-c3h2.onrender.com**

| Verificación | Resultado |
|---|---|
| La URL es accesible | ✅ |
| La página principal carga correctamente | ✅ |
| Se pueden registrar tareas | ✅ |
| Las tareas se pueden editar | ✅ |
| Las tareas se pueden eliminar | ✅ |
| Los estados se actualizan correctamente | ✅ |
| `/health` responde `{"status": "ok"}` | ✅ |

## 6.4 Consideración conocida

En el plan gratuito de Render el disco es efímero: la base SQLite se reinicia cuando el servicio se vuelve a desplegar o se reinicia. Para producción real se propone migrar a PostgreSQL (Issue #25). Además, el servicio se "duerme" tras 15 minutos sin uso y la primera petición tarda ~50 s.

## 6.5 Evidencias

- [ ] Captura del panel de Render con el servicio **Live**.
- [ ] Captura de los logs del despliegue (*Build successful*, *Your service is live*).
- [ ] Capturas de la aplicación funcionando en la URL pública.
