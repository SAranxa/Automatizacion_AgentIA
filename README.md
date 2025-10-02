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

## Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/SAranxa/Automatizacion_AgentIA.git
```
### 2. Requisitos previos
- VPS (Hostinger, DigitalOcean, HostGator)
- Docker y Docker Compose instalados
- Cuenta de Telegram Bot API configurada.
- Cuenta de Google Calendar API con credenciales OAuth.
- Cuenta de ngrok para exponer el webhook de Telegram.

### 3. Configuración de variables de entorno
Crea un archivo .env en la raíz del proyecto con lo siguiente:
```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=tu_password_segura
N8N_HOST=tu-dominio.com
N8N_PORT=5678
```
### 4. Levantar el entorno con Docker Compose
```bash
docker-compose up
```
Esto descargará las imágenes necesarias y levantará el contenedor con n8n.

### 5. Acceder a n8n
Abre en tu navegador:
```bash
http://TU_IP_VPS:5678
```
----
### 6. Importar el flujo n8n
- Inicia sesión en n8n
- Importa el archivo JSON del flujo (AI agent chat.json).
- Reemplaza los IDs de credenciales por los tuyos.
- Activa el flujo.

----

### 7. Obtener credenciales y API keys
#### Telegram
1. Abre la app de Telegram (móvil o desktop).
2. Busca y abre @BotFather (cuenta oficial). 
Telegram
3. Envía el comando /newbot y sigue los pasos:
   - Elige un nombre para el bot (visible).
   - Elige un username único que termine en bot (ej. MiAgendaBot).
4. Al terminar, BotFather te devolverá el Bot Token (una cadena 12345:ABC...) — cópialo. Ese token es la credencial que usarás en n8n (nodo Telegram) o en tus servicios para llamar al Bot API.
#### Gemini
Google ofrece acceso a Gemini a través de Google AI Studio / Generative AI APIs; para usar Gemini necesitas un API key desde Google AI Studio o Google Cloud según la configuración. Pasos generales: 
Google AI for Developers
1. Entra a Google AI Studio (o a la consola de Google Cloud si usas Vertex/Generative AI).
2. Si aún no lo hiciste, acepta términos y activa el producto (puede pedir billing). 
3. Busca la sección API keys o “Credentials / API keys” (en AI Studio o Google Cloud → API & Services → Credentials).
4. Crea una nueva API key. Guarda la clave (string). Puedes limitar su uso por referrer, IP o servicios (recomendado). 
Google AI for Developers
5. Usa el API key en llamadas al SDK/HTTP (por ejemplo el SDK google-genai o petición HTTP con Authorization: Bearer <API_KEY> o parámetro key= según la API). Revisa la guía rápida / quickstart del SDK para ejemplos.

#### Google Calendar 
1. Ve a console.cloud.google.com y crea/selecciona un proyecto (p.ej. agenda-n8n).
2. Habilita la API: APIs & Services → Library → Google Calendar API → Enable.
3. Ve a APIs & Services → Credentials → Create Credentials → OAuth client ID.
   - Si no configuraste el consentimiento, te pedirá configurar el OAuth consent screen (datos de app, scopes solicitados - pide https://www.googleapis.com/auth/calendar o el scope mínimo que uses).
4. Crea un OAuth Client:
   - Tipo: Web application (si tu n8n usa redirect URIs) o Other según caso.
   - Añade Authorized redirect URIs (por ejemplo https://tu-dominio.com/oauth2callback o la URL que n8n requiera).
5. Al crear obtendrás Client ID y Client Secret.

## Tablero Kanban
Consulta el flujo de trabajo aquí:  
[GitHub Projects – Kanban](https://github.com/users/SAranxa/projects/4)
