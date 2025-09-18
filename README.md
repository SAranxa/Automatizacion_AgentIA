# AI Agent Chat 
Automatización de Agendamiento de citas
## Descripción del proyecto

Este proyecto implementa un **asistente conversacional de agendamiento** que convierte mensajes de los usuarios en acciones concretas sobre un sistema de calendario. A través de diálogo natural, el asistente puede **crear, reprogramar y cancelar citas**, consultar **disponibilidad** y confirmar detalles con el usuario, respetando **horarios de atención** y **duraciones configurables por tipo de servicio**.

Está pensado para equipos que gestionan reservas de manera frecuente (servicios técnicos, talleres, clínicas, consultorías, educación, etc.) y buscan **reducir el intercambio manual**, **evitar choques de agenda** y **mejorar tiempos de respuesta**. El flujo usa un motor de IA para interpretar la intención del usuario y un conjunto de herramientas conectadas a un calendario para ejecutar las operaciones necesarias, manteniendo **contexto por conversación** para una experiencia continua.

**Objetivos principales**
- Automatizar el ciclo de reserva: consulta de disponibilidad → propuesta de horarios → confirmación → creación de la cita.
- Permitir **modificación** y **cancelación** guiadas por el usuario.
- Adaptar la duración de la cita según el servicio solicitado (configurable).
- Ajustarse a políticas de atención (p. ej., ventana horaria operativa, zona horaria, idioma/tono).

**Beneficios**
- Menos fricción y menor tiempo de respuesta frente a solicitudes repetitivas.
- Disminución de errores humanos en la programación.
- Escalabilidad operativa sin aumentar carga del equipo.
- Base extensible para recordatorios, validación de datos y handoff humano (opcional).

**Alcance**
- Interacción conversacional multicanal (mensajería/chat).
- Orquestación de acciones sobre un sistema de calendario.
- Configuración de reglas de negocio (horarios, duraciones, políticas).

**Fuera de alcance (por diseño)**
- Sustituir un CRM completo o facturación.
- Gestión avanzada de inventario/recursos más allá del calendario.
- Reportería analítica avanzada (se puede integrar externamente).

## Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/SAranxa/Automatizacion_AgentIA.git
```
### 2. Requisitos previos
- Docker y Docker Compose instalados
- Cuenta de Telegram Bot API configurada.
- Cuenta de Google Calendar API con credenciales OAuth.
- Cuenta de ngrok para exponer el webhook de Telegram.

### 3. Configuración de variables de entorno
Crea un archivo .env en la raíz del proyecto con lo siguiente:
```bash
# Puerto donde corre n8n
N8N_PORT=5678

# URL de ngrok (se actualiza en cada reinicio)
WEBHOOK_TUNNEL_URL=https://<tu-subdominio-ngrok>.ngrok-free.app
```
### 4. Levantar el entorno con Docker Compose
```bash
docker-compose up
```
Esto descargará las imágenes necesarias y levantará el contenedor con n8n.
### 5. Importar el flujo n8n
- Inicia sesión en n8n
- Importa el archivo JSON del flujo (AI agent chat.json).
- Reemplaza los IDs de credenciales por los tuyos.
- Activa el flujo.

----

## Tablero Kanban
Consulta el flujo de trabajo aquí:  
[GitHub Projects – Kanban](https://github.com/users/SAranxa/projects/4)
