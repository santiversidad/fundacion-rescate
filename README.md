# 🐾 Fundación Rescate Animal

Sistema web institucional para la gestión de adopciones, donaciones y eventos de una fundación de rescate animal. Construido con Django 6, PostgreSQL y Bootstrap 5.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0.3-092E20?style=flat&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=flat&logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat&logo=bootstrap&logoColor=white)

---

## Índice

- [Características](#características)
- [Stack tecnológico](#stack-tecnológico)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Módulos del sistema](#módulos-del-sistema)
- [Rutas principales](#rutas-principales)
- [Panel de administración](#panel-de-administración)
- [Contribución](#contribución)
- [Licencia](#licencia)

---

## Características

### Sitio público

- **Catálogo de mascotas** — listado filtrable por especie y sexo con buscador
- **Adopciones** — flujo completo de solicitud con gestión de estado y notificaciones por correo
- **Donaciones** — registro con comprobante, verificación manual y recibo descargable
- **Eventos** — inscripción en línea con control de cupos y barra de progreso en tiempo real
- **Testimonios** — envío de experiencias con moderación del equipo
- **Nosotros / Preguntas frecuentes / Contacto** — contenido institucional gestionable desde el dashboard
- **Inicio de sesión con Google** — OAuth 2.0 via django-allauth con PKCE habilitado

### Perfil de usuario

- Dashboard personal con tarjetas de resumen (solicitudes, donaciones, eventos, estado del perfil)
- Historial de actividad con timeline visual
- Edición de foto, nombre y biografía
- Panel de configuración de cuenta

### Panel de administración (staff)

- **Estadísticas** centralizadas al ingresar
- **CRUD completo** para mascotas (con galería de fotos), eventos, equipo, FAQ y contenido institucional
- **Gestión de adopciones** — cambio de estado con correo automático al solicitante
- **Gestión de donaciones** — verificación / rechazo con correo automático
- **Moderación de testimonios**
- **Bandeja de mensajes** de contacto con marcado de leído
- **Lista de usuarios registrados** con búsqueda y filtros
- **Registro de actividad** auditado (quién hizo qué y cuándo)

### Seguridad y rendimiento

- Rate limiting en formularios sensibles (adopciones, donaciones, login, testimonios)
- Cabeceras de seguridad personalizadas (Permissions-Policy, X-Frame-Options, HSTS en producción)
- Validación de contraseña con mínimo de 12 caracteres
- Logs rotativos de errores y eventos de seguridad
- Sitemaps XML y robots.txt para SEO

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Django 6.0.3 · Python 3.12+ |
| Base de datos | PostgreSQL 15+ |
| Autenticación | django-allauth 65 + Google OAuth 2.0 |
| Frontend | Bootstrap 5.3 · Bootstrap Icons 1.11 |
| Imágenes | Pillow 12 |
| Variables de entorno | python-decouple |
| Servidor de desarrollo | `manage.py runserver` |

---

## Requisitos previos

- Python **3.12 o superior**
- PostgreSQL **15 o superior**
- `pip` y `venv`
- Una cuenta de Google Cloud con un proyecto configurado (para OAuth)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/santiversidad/fundacion-rescate.git
cd fundacion-rescate
```

### 2. Crear y activar el entorno virtual

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con los valores reales (ver sección [Configuración](#configuración)).

### 5. Crear la base de datos

```bash
# Acceder a PostgreSQL
psql -U postgres

# Dentro de psql:
CREATE DATABASE fundacion_rescate;
\q
```

### 6. Aplicar migraciones

```bash
python manage.py migrate
```

### 7. Crear superusuario

```bash
python manage.py createsuperuser
```

### 8. Cargar archivos estáticos (opcional en desarrollo)

```bash
python manage.py collectstatic
```

### 9. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

El sitio estará disponible en `http://127.0.0.1:8000`.

---

## Configuración

Copia `.env.example` a `.env` y completa cada valor:

```ini
# ── Seguridad ────────────────────────────────────────────
SECRET_KEY=django-insecure-reemplaza-con-una-clave-segura
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# ── Base de datos (PostgreSQL) ───────────────────────────
DB_NAME=fundacion_rescate
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432

# ── Google OAuth 2.0 (django-allauth) ────────────────────
GOOGLE_CLIENT_ID=tu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-client-secret

# ── Google Maps API (opcional) ───────────────────────────
GOOGLE_MAPS_API_KEY=tu-api-key
```

### Configurar Google OAuth

1. Accede a [Google Cloud Console](https://console.cloud.google.com/).
2. Crea un proyecto y habilita la API **Google+ API** (o **OAuth 2.0**).
3. Ve a **Credenciales → Crear credenciales → ID de cliente OAuth 2.0**.
4. Tipo de aplicación: **Aplicación web**.
5. Agrega en *URIs de redirección autorizados*:
   ```
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
6. Copia el **Client ID** y **Client Secret** en tu `.env`.
7. En el panel de Django admin (`/admin`), ve a **Social applications** y agrega una entrada con esos valores, asociada al sitio `127.0.0.1:8000`.

---

## Estructura del proyecto

```
fundacion-rescate/
├── config/                     # Configuración central de Django
│   ├── settings.py             # Settings con python-decouple
│   ├── urls.py                 # Router principal
│   ├── middleware.py           # Rate limiting + cabeceras de seguridad
│   └── views.py                # Handlers de error 404/500
│
├── mascotas/                   # App: catálogo de animales
├── adopciones/                 # App: solicitudes de adopción
├── donaciones/                 # App: registro y verificación de donaciones
├── usuarios/                   # App: autenticación y perfiles
├── institucional/              # App: páginas públicas, eventos, contacto
├── dashboard/                  # App: panel de administración (staff)
│
├── templates/                  # Templates HTML organizados por app
│   ├── base.html               # Layout base (navbar, footer, sidebar social)
│   ├── dashboard/
│   │   └── base_dashboard.html # Layout del panel admin (sidebar fijo)
│   ├── mascotas/
│   ├── adopciones/
│   ├── donaciones/
│   ├── usuarios/
│   ├── institucional/
│   └── emails/                 # Templates de notificaciones por correo
│
├── static/
│   ├── css/
│   │   └── estilos.css         # Sistema de diseño con CSS custom properties
│   └── img/                    # Imágenes estáticas del sitio
│
├── media/                      # Archivos subidos por usuarios (gitignored)
│   ├── mascotas/
│   ├── perfiles/
│   ├── comprobantes/
│   ├── equipo/
│   ├── eventos/
│   └── testimonios/
│
├── logs/                       # Logs rotativos (gitignored)
│   ├── errors.log
│   └── security.log
│
├── requirements.txt
├── .env.example
└── manage.py
```

---

## Módulos del sistema

### `mascotas`

Gestiona el catálogo de animales en adopción.

| Modelo | Campos clave |
|--------|-------------|
| `Mascota` | nombre, especie (perro/gato/otro), raza, edad, sexo, estado (disponible/en_proceso/adoptada/inactiva), esterilizado, vacunado |
| `FotoMascota` | FK a Mascota, foto, alt_text, es_principal |

### `adopciones`

Flujo de solicitud de adopción con notificaciones automáticas.

| Modelo | Campos clave |
|--------|-------------|
| `SolicitudAdopcion` | usuario, mascota, motivo, tipo_vivienda, tiene_otros_animales, estado (pendiente/en_revision/aprobada/rechazada), observaciones_admin |

### `donaciones`

Registro y verificación de donaciones con comprobante.

| Modelo | Campos clave |
|--------|-------------|
| `Donacion` | usuario, monto, metodo (transferencia/deposito/efectivo/otro), comprobante, estado (pendiente/verificada/rechazada), fecha_donacion |

### `usuarios`

Autenticación (local + Google), perfil y edición de cuenta.

| Modelo | Campos clave |
|--------|-------------|
| `PerfilUsuario` | OneToOne a User, foto, bio |

### `institucional`

Contenido público: páginas institucionales, eventos y comunicación.

| Modelo | Campos clave |
|--------|-------------|
| `Evento` | titulo, descripcion, imagen, fecha, lugar, capacidad, estado |
| `InscripcionEvento` | evento, usuario, fecha |
| `MiembroEquipo` | nombre, cargo, foto, descripcion, orden |
| `Testimonio` | nombre, foto, mensaje, mascota, aprobado |
| `PreguntaFrecuente` | pregunta, respuesta, orden, activa |
| `ContenidoNosotros` | mision, vision, imagenes |
| `MensajeContacto` | nombre, email, asunto, mensaje, leido, ip |

### `dashboard`

Panel administrativo exclusivo para staff.

| Modelo | Campos clave |
|--------|-------------|
| `RegistroActividad` | usuario, accion (crear/editar/eliminar/aprobar/rechazar), modelo, objeto_id, descripcion, fecha |

---

## Rutas principales

### Sitio público

| URL | Vista | Descripción |
|-----|-------|-------------|
| `/` | `institucional:inicio` | Página de inicio |
| `/nosotros/` | `institucional:nosotros` | Quiénes somos |
| `/como-ayudar/` | `institucional:como_ayudar` | Formas de ayudar |
| `/eventos/` | `institucional:eventos` | Listado de eventos |
| `/eventos/<id>/` | `institucional:detalle_evento` | Detalle del evento |
| `/preguntas-frecuentes/` | `institucional:faq` | FAQ |
| `/testimonios/` | `institucional:testimonios` | Testimonios |
| `/contacto/` | `institucional:contacto` | Formulario de contacto |
| `/mascotas/` | `mascotas:catalogo` | Catálogo de mascotas |
| `/mascotas/<id>/` | `mascotas:detalle` | Ficha de mascota |
| `/adopciones/solicitar/<id>/` | `adopciones:solicitar` | Solicitar adopción |
| `/adopciones/mis-solicitudes/` | `adopciones:mis_solicitudes` | Mis solicitudes |
| `/donaciones/` | `donaciones:info` | Info de donaciones |
| `/donaciones/registrar/` | `donaciones:nueva` | Registrar donación |
| `/donaciones/mis-donaciones/` | `donaciones:mis_donaciones` | Mis donaciones |

### Autenticación

| URL | Descripción |
|-----|-------------|
| `/usuarios/login/` | Inicio de sesión local |
| `/usuarios/registro/` | Registro con correo |
| `/usuarios/logout/` | Cierre de sesión |
| `/usuarios/perfil/` | Dashboard del perfil |
| `/usuarios/perfil/editar/` | Editar perfil y foto |
| `/accounts/google/login/` | Inicio de sesión con Google |

### Panel administrativo (`/dashboard/`)

| URL | Descripción |
|-----|-------------|
| `/dashboard/` | Resumen general y estadísticas |
| `/dashboard/mascotas/` | Gestión de mascotas |
| `/dashboard/adopciones/` | Gestión de solicitudes |
| `/dashboard/donaciones/` | Verificación de donaciones |
| `/dashboard/eventos/` | Gestión de eventos |
| `/dashboard/equipo/` | Gestión del equipo |
| `/dashboard/testimonios/` | Moderación de testimonios |
| `/dashboard/faq/` | Gestión de preguntas frecuentes |
| `/dashboard/institucional/` | Contenido de la página "Nosotros" |
| `/dashboard/mensajes/` | Bandeja de mensajes de contacto |
| `/dashboard/usuarios/` | Lista de usuarios registrados |

---

## Panel de administración

El acceso al dashboard (`/dashboard/`) requiere que el usuario tenga el flag `is_staff = True` en Django admin.

Para marcar un usuario como staff desde consola:

```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username='tu_usuario')
>>> u.is_staff = True
>>> u.save()
```

O directamente desde el admin de Django (`/admin/auth/user/`).

---

## Contribución

Las contribuciones son bienvenidas. Sigue estos pasos:

### 1. Haz un fork del repositorio

```bash
git clone https://github.com/TU_USUARIO/fundacion-rescate.git
cd fundacion-rescate
```

### 2. Crea una rama descriptiva

```bash
# Nueva funcionalidad
git checkout -b feat/nombre-funcionalidad

# Corrección de bug
git checkout -b fix/descripcion-del-bug

# Mejora de estilos / UI
git checkout -b ui/descripcion-del-cambio
```

### 3. Realiza tus cambios

- Sigue las convenciones de código existentes (PEP 8 para Python, BEM/Bootstrap para CSS)
- No modifiques migraciones existentes; crea nuevas con `python manage.py makemigrations`
- Mantén la separación de responsabilidades entre apps
- Usa los decoradores existentes (`@login_required`, `@admin_requerido`, `@rate_limit`)

### 4. Haz commit con un mensaje claro

```bash
git add .
git commit -m "feat: descripción breve del cambio"
```

Convenciones de commit:

| Prefijo | Uso |
|---------|-----|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de bug |
| `ui:` | Cambios visuales / CSS |
| `refactor:` | Reestructuración sin cambio funcional |
| `docs:` | Documentación |
| `chore:` | Configuración, dependencias |

### 5. Abre un Pull Request

Describe claramente:
- Qué cambias y por qué
- Capturas de pantalla si hay cambios visuales
- Si agrega dependencias nuevas

---

## Variables de entorno — referencia completa

| Variable | Requerida | Descripción |
|----------|-----------|-------------|
| `SECRET_KEY` | ✅ | Clave secreta de Django (genera una con `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`) |
| `DEBUG` | ✅ | `True` en desarrollo, `False` en producción |
| `ALLOWED_HOSTS` | ✅ | Lista separada por comas de dominios permitidos |
| `DB_NAME` | ✅ | Nombre de la base de datos PostgreSQL |
| `DB_USER` | ✅ | Usuario de PostgreSQL |
| `DB_PASSWORD` | ✅ | Contraseña de PostgreSQL |
| `DB_HOST` | ✅ | Host de PostgreSQL (default: `localhost`) |
| `DB_PORT` | ✅ | Puerto de PostgreSQL (default: `5432`) |
| `GOOGLE_CLIENT_ID` | ⚠️ | Requerido solo si se usa login con Google |
| `GOOGLE_CLIENT_SECRET` | ⚠️ | Requerido solo si se usa login con Google |
| `GOOGLE_MAPS_API_KEY` | ❌ | Opcional — para integración de mapas |

---

## Despliegue en producción

Para un entorno de producción, asegúrate de:

1. **Establecer** `DEBUG=False` y configurar `ALLOWED_HOSTS` con el dominio real.
2. **Ejecutar** `python manage.py collectstatic` y servir `/static/` con Nginx o similar.
3. **Configurar** un servidor WSGI como Gunicorn:
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:8000
   ```
4. **Activar HTTPS** — las siguientes variables de seguridad se activan automáticamente con `DEBUG=False`:
   - `SECURE_SSL_REDIRECT = True`
   - `SECURE_HSTS_SECONDS = 31536000`
   - Cookies de sesión y CSRF con `Secure=True`
5. **Configurar** las variables de email SMTP si se requieren notificaciones reales.
6. **Revisar** el directorio `logs/` y asegurarse de que el proceso tenga permisos de escritura.

---

## Licencia

Este proyecto fue desarrollado para **Fundación Rescate Animal**. Todos los derechos reservados.

---

<div align="center">
  Hecho con ❤️ para los animales que esperan un hogar 🐾
</div>
