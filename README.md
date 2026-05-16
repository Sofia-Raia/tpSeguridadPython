# TP Integrador 4 - Backend FastAPI (Autenticación & Seguridad) 🚀

Este proyecto corresponde a la extensión de seguridad y persistencia avanzada del Trabajo Práctico Integrador 4. Consiste en la implementación de un **Módulo de Autenticación, Usuarios y Control de Acceso por Roles** desarrollado con **FastAPI** y **SQLModel**, conectado a **MySQL** mediante patrones de diseño empresariales.

**Link al video:** [Video](https://drive.google.com/file/d/1t7eY1UwGy2gW8AnTZ5VF8t5SfTt64Vli/view?usp=drive_link)

Se ha evolucionado el diseño desacoplado del backend mediante la centralización de transacciones atómicas y el aislamiento de la lógica de persistencia.

## 🛠️ Tecnologías Utilizadas

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **ORM:** [SQLModel](https://sqlmodel.tiangolo.com/)
* **Base de Datos:** MySQL
* **Validación:** Pydantic v2
* **Criptografía & Seguridad:** `passlib` (Bcrypt) y `python-jose` (JWT)

## ⚙️ Características Principales

* **Patrón Unit of Work (UOW):** Centralización de transacciones atómicas garantizando consistencia ACID en la base de datos a través de bloques de contexto (`with uow`).
* **Repository Pattern:** Aislamiento de las consultas SQL mediante repositorios específicos (`UsuarioRepository`) que heredan de una estructura base genérica.
* **Seguridad Avanzada (Bcrypt):** Hashing robusto de contraseñas en reposo antes de ser persistidas en la base de datos MySQL.
* **Sesiones Seguras mediante Cookies HttpOnly:** Emisión de tokens JWT encapsulados en Cookies con banderas `HttpOnly` y `SameSite="Lax"`, mitigando de raíz ataques de Cross-Site Scripting (XSS).
* **CORS Habilitado:** Configuración nativa con `allow_credentials=True` para la integración segura con el frontend en React (`http://localhost:5173`).

## 🚀 Requisitos Previos

* Python 3.10 o superior.
* Servidor MySQL ejecutándose (XAMPP, Workbench, etc.).
* Base de Datos: Se recomienda crear una base limpia llamada `tp2_db` para asegurar la sincronización de las nuevas tablas de usuarios.

## 🔧 Instalación y Configuración

1. **Entorno Virtual:**
   ```bash
   python -m venv venv
   # Activar en Windows (PowerShell):
   .\venv\Scripts\Activate.ps1

2. Instalación de Dependencias:

⚠️ Nota Crítica de Compatibilidad: Para evitar conflictos conocidos entre el testeo interno de passlib y versiones estrictas de bcrypt, se debe instalar la versión exacta < 4.0.0:

pip install fastapi uvicorn sqlmodel pymysql cryptography "python-jose[cryptography]" passlib "bcrypt<4.0.0" pydantic[email]

3. Base de Datos:
Actualizá la URL de conexión en app/core/database.py según tus credenciales de MySQL local. 
Por defecto: 
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/tp2_db"

▶️ Ejecución del Servidor
Levantá la API con el comando de desarrollo de Uvicorn:

uvicorn app.main:app --reload

🧪 Guía Detallada de Pruebas con Postman
Debido a que el sistema utiliza Cookies HttpOnly por motivos de seguridad, Postman es la herramienta ideal para las pruebas, ya que intercepta, almacena y reinyecta automáticamente las cookies en el flujo de peticiones. Seguir el siguiente orden secuencial:

📥 1. Registro de un Usuario Nuevo (POST /auth/register)
Valida la unicidad de credenciales, hashea la contraseña y persiste los datos a través del UOW.

Abrí una pestaña en Postman y seleccioná el método POST.

URL: http://127.0.0.1:8000/auth/register

Andá a la pestaña Body (debajo de la URL) -> Seleccioná raw -> Cambiá el desplegable a JSON.

Pegá el siguiente cuerpo de prueba y hacé clic en Send:

JSON
{
  "username": "tester_prog4",
  "full_name": "Sofia Raia",
  "email": "tester@correo.com",
  "password": "miClaveSegura123"
}
Resultado esperado: Código 201 Created. Retorna el JSON del usuario sin exponer la clave. Si vas a tu base MySQL, verás la columna hashed_password cifrada con la firma $2b$.

🔑 2. Inicio de Sesión e Inyección de Cookie (POST /auth/token)
Verifica las credenciales en MySQL, genera el JWT y lo inyecta en el navegador/cliente.

Abrí una nueva pestaña y seleccioná el método POST.

URL: http://127.0.0.1:8000/auth/token

Andá a la pestaña Body y seleccioná x-www-form-urlencoded (⚠️ Obligatorio por estándar OAuth2 de FastAPI).

Cargá los siguientes datos en la tabla Key-Value:

Key: username | Value: tester_prog4

Key: password | Value: miClaveSegura123

Hacé clic en Send.

Resultado esperado: Código 200 OK con un mensaje de éxito. Si miras en la parte inferior de Postman, en la pestaña Cookies, verás guardada la cookie access_token asignada al dominio 127.0.0.1.

🛡️ 3. Acceso a Rutas Protegidas (GET /auth/me)
El backend intercepta la petición, lee la cookie, decodifica el JWT y obtiene los datos del usuario logueado actual.

Abrí una tercera pestaña y seleccioná el método GET.

URL: http://127.0.0.1:8000/auth/me

No configures nada más (ni Body ni Headers). Postman adjunta solo la cookie guardada en el paso anterior.

Hacé clic en Send.

Resultado esperado: Código 200 OK devolviendo la información completa de tu perfil autenticado.

🚫 4. Simulación de Intruso (Prueba de Bloqueo)
En la pestaña de GET /auth/me, hacé clic en el enlace azul chiquito llamado Cookies (justo debajo del botón Send).

Buscá el dominio 127.0.0.1, hacé clic en la X para eliminar la cookie access_token y cerrá la ventana.

Volvé a hacer clic en Send.

Resultado esperado: Código 401 Unauthorized indicando que la ruta está protegida y el acceso fue denegado con éxito.

¡De una! Vamos a adaptarlo exactamente al formato y estilo de tu profesor (el formato del TP4), pero sumando toda la capa que implementamos hoy: la arquitectura por módulos con Unit of Work (UOW), la conexión a MySQL, el módulo de Usuarios/Autenticación, y el manual ultra detallado para Postman (con el truco de las cookies y los formatos de body).

Acá tenés el código markdown listo para copiar y pegar directamente en tu archivo README.md:

Markdown
# TP Integrador 4 - Backend FastAPI (Autenticación & Seguridad) 🚀

Este proyecto corresponde a la extensión de seguridad y persistencia avanzada del Trabajo Práctico Integrador 4. Consiste en la implementación de un **Módulo de Autenticación, Usuarios y Control de Acceso por Roles** desarrollado con **FastAPI** y **SQLModel**, conectado a **MySQL** mediante patrones de diseño empresariales.

**Link al video:** [Video](https://drive.google.com/file/d/1t7eY1UwGy2gW8AnTZ5VF8t5SfTt64Vli/view?usp=drive_link)

Se ha evolucionado el diseño desacoplado del backend mediante la centralización de transacciones atómicas y el aislamiento de la lógica de persistencia.

## 🛠️ Tecnologías Utilizadas

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **ORM:** [SQLModel](https://sqlmodel.tiangolo.com/)
* **Base de Datos:** MySQL
* **Validación:** Pydantic v2
* **Criptografía & Seguridad:** `passlib` (Bcrypt) y `python-jose` (JWT)

## ⚙️ Características Principales

* **Patrón Unit of Work (UOW):** Centralización de transacciones atómicas garantizando consistencia ACID en la base de datos a través de bloques de contexto (`with uow`).
* **Repository Pattern:** Aislamiento de las consultas SQL mediante repositorios específicos (`UsuarioRepository`) que heredan de una estructura base genérica.
* **Seguridad Avanzada (Bcrypt):** Hashing robusto de contraseñas en reposo antes de ser persistidas en la base de datos MySQL.
* **Sesiones Seguras mediante Cookies HttpOnly:** Emisión de tokens JWT encapsulados en Cookies con banderas `HttpOnly` y `SameSite="Lax"`, mitigando de raíz ataques de Cross-Site Scripting (XSS).
* **CORS Habilitado:** Configuración nativa con `allow_credentials=True` para la integración segura con el frontend en React (`http://localhost:5173`).

## 🚀 Requisitos Previos

* Python 3.10 o superior.
* Servidor MySQL ejecutándose (XAMPP, Workbench, etc.).
* Base de Datos: Se recomienda crear una base limpia llamada `tp2_db` para asegurar la sincronización de las nuevas tablas de usuarios.

## 🔧 Instalación y Configuración

1. **Entorno Virtual:**
   ```bash
   python -m venv venv
   # Activar en Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
2. Instalación de Dependencias:

⚠️ Nota Crítica de Compatibilidad: Para evitar conflictos conocidos entre el testeo interno de passlib y versiones estrictas de bcrypt, se debe instalar la versión exacta < 4.0.0:

pip install fastapi uvicorn sqlmodel pymysql cryptography "python-jose[cryptography]" passlib "bcrypt<4.0.0" pydantic[email]

3. Base de Datos:
Actualizá la URL de conexión en app/core/database.py según tus credenciales de MySQL local. Por defecto:

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/tp2_db"

▶️ Ejecución del Servidor
Levantá la API con el comando de desarrollo de Uvicorn:

uvicorn app.main:app --reload

La documentación interactiva e inspección de esquemas estará disponible en: http://127.0.0.1:8000/docs

🧪 Guía Detallada de Pruebas con Postman
Debido a que el sistema utiliza Cookies HttpOnly por motivos de seguridad, Postman es la herramienta ideal para las pruebas, ya que intercepta, almacena y reinyecta automáticamente las cookies en el flujo de peticiones. Seguir el siguiente orden secuencial:

📥 1. Registro de un Usuario Nuevo (POST /auth/register)
Valida la unicidad de credenciales, hashea la contraseña y persiste los datos a través del UOW.

Abrí una pestaña en Postman y seleccioná el método POST.

URL: http://127.0.0.1:8000/auth/register

Andá a la pestaña Body (debajo de la URL) -> Seleccioná raw -> Cambiá el desplegable a JSON.

Pegá el siguiente cuerpo de prueba y hacé clic en Send:

JSON
{
  "username": "tester_prog4",
  "full_name": "Sofia Raia",
  "email": "tester@correo.com",
  "password": "miClaveSegura123"
}
Resultado esperado: Código 201 Created. Retorna el JSON del usuario sin exponer la clave. Si vas a tu base MySQL, verás la columna hashed_password cifrada con la firma $2b$.

🔑 2. Inicio de Sesión e Inyección de Cookie (POST /auth/token)
Verifica las credenciales en MySQL, genera el JWT y lo inyecta en el navegador/cliente.

Abrí una nueva pestaña y seleccioná el método POST.

URL: http://127.0.0.1:8000/auth/token

Andá a la pestaña Body y seleccioná x-www-form-urlencoded (⚠️ Obligatorio por estándar OAuth2 de FastAPI).

Cargá los siguientes datos en la tabla Key-Value:

Key: username | Value: tester_prog4

Key: password | Value: miClaveSegura123

Hacé clic en Send.

Resultado esperado: Código 200 OK con un mensaje de éxito. Si miras en la parte inferior de Postman, en la pestaña Cookies, verás guardada la cookie access_token asignada al dominio 127.0.0.1.

🛡️ 3. Acceso a Rutas Protegidas (GET /auth/me)
El backend intercepta la petición, lee la cookie, decodifica el JWT y obtiene los datos del usuario logueado actual.

Abrí una tercera pestaña y seleccioná el método GET.

URL: http://127.0.0.1:8000/auth/me

No configures nada más (ni Body ni Headers). Postman adjunta solo la cookie guardada en el paso anterior.

Hacé clic en Send.

Resultado esperado: Código 200 OK devolviendo la información completa de tu perfil autenticado.

🚫 4. Simulación de Intruso (Prueba de Bloqueo)
En la pestaña de GET /auth/me, hacé clic en el enlace azul chiquito llamado Cookies (justo debajo del botón Send).

Buscá el dominio 127.0.0.1, hacé clic en la X para eliminar la cookie access_token y cerrá la ventana.

Volvé a hacer clic en Send.

Resultado esperado: Código 401 Unauthorized indicando que la ruta está protegida y el acceso fue denegado con éxito.

📂 Estructura Modular del Proyecto

ProyectoIntegradorProg4-main/
├── venv/                       # Entorno virtual de Python
├── app/
│   ├── __init__.py
│   ├── main.py                 # Configuración de FastAPI, CORS y Routers centrales
│   ├── core/
│   │   ├── database.py         # Configuración del Engine de MySQL y get_session()
│   │   ├── repository.py       # Clase base genérica (BaseRepository)
│   │   ├── unit_of_work.py     # Administrador de transacciones (UOW) y get_uow()
│   │   ├── security.py         # Motores criptográficos (Bcrypt / JWT)
│   │   └── deps.py             # Dependencias de seguridad (get_current_user)
│   └── modules/
│       ├── __init__.py
│       ├── categoria/          # Dominio de Categorías
│       ├── producto/           # Dominio de Productos e Ingredientes
│       └── usuario/            # Módulo de Seguridad y Autenticación
│           ├── __init__.py
│           ├── models.py       # Entidad UsuarioModel para MySQL (SQLModel)
│           ├── repository.py   # Consultas específicas de usuarios
│           ├── service.py      # Lógica de negocio y verificación de reglas
│           ├── schemas.py      # Validaciones Pydantic (Entrada/Salida de datos)
│           └── router.py       # Endpoints públicos y protegidos (/register, /token, /me)
├── README.md                   # Documentación del proyecto
└── requirements.txt            # Listado de dependencias

