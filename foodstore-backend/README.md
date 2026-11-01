# Food Store — Backend (Catálogo de Productos)

API REST del Parcial 2 de Programación IV hecha con **FastAPI**, **SQLModel**, **Pydantic v2** y **PostgreSQL**.

Autor: Alex Pedro Dauria

Repositorio: https://github.com/Alex-Dauria/foodstore-parcial2

## Requisitos

- Python 3.12 o superior
- PostgreSQL 15 o superior, corriendo en `localhost:5432`

## 1. Crear la base de datos

Crear una base vacía llamada `foodstore_p2`. Con `psql`:

```bash
psql -U postgres -c "CREATE DATABASE foodstore_p2;"
```

(También se puede crear desde pgAdmin.) Las tablas no hace falta crearlas: la aplicación las crea al iniciar.

## 2. Configurar la conexión

La cadena de conexión está en `app/core/database.py`:

```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/foodstore_p2",
)
```

El formato es `postgresql+psycopg://USUARIO:CONTRASEÑA@HOST:PUERTO/BASE`. Por defecto usa el usuario `postgres` con contraseña `postgres`. Si tu PostgreSQL usa otros datos, elegí una de estas dos opciones:

- **Opción A:** editar el valor por defecto en `app/core/database.py`.
- **Opción B:** definir la variable de entorno `DATABASE_URL` antes de iniciar la app, en la misma terminal:

  ```powershell
  # Windows (PowerShell)
  $env:DATABASE_URL = "postgresql+psycopg://postgres:MI_CLAVE@localhost:5432/foodstore_p2"
  ```

  ```bash
  # Linux / macOS
  export DATABASE_URL="postgresql+psycopg://postgres:MI_CLAVE@localhost:5432/foodstore_p2"
  ```

## 3. Instalar y ejecutar

Desde la carpeta `foodstore-backend/`:

```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev app/main.py
```

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
```

- API: http://localhost:8000
- Swagger (documentación interactiva): http://localhost:8000/docs

Al iniciar, la aplicación crea las tablas y carga el seed de unidades de medida (kilogramo, gramo, litro, mililitro, pieza y docena). El seed solo inserta si la tabla está vacía, así que reiniciar no duplica filas.

## 4. Pruebas con REST Client

En `tests/` están los archivos para la extensión **REST Client** de VS Code:

- `tests/productos.http`: CRUD de productos, filtros del listado, errores 404 / 409 / 422 y `hay_stock` antes y después de llevar el stock a 0.
- `tests/relaciones.http`: categorías, clasificación de productos (N:N), cambio de categoría principal y anulación de categorías.

Con el backend corriendo, abrir el archivo y ejecutar las peticiones **en orden, de arriba hacia abajo** ("Send Request"). Cada petición indica en un comentario el código esperado. Al final de cada archivo se anula lo creado, así se pueden volver a correr.

## Estructura

```
foodstore-backend/
├── app/
│   ├── main.py                 # App FastAPI, CORS, routers y arranque (tablas + seed)
│   ├── core/
│   │   ├── database.py         # Cadena de conexión, engine y dependencia de sesión
│   │   └── seed.py             # Seed de unidades de medida
│   └── modules/
│       ├── unidades_medida/    # model · router · service (catálogo de solo lectura)
│       ├── categorias/         # model · schema · service · router
│       └── productos/          # model (Producto y ProductoCategoria) · schema · service · router
├── tests/                      # productos.http · relaciones.http
└── requirements.txt
```

Cada módulo sigue el mismo recorrido: el **router** recibe la petición, obtiene la sesión por inyección de dependencias (`SessionDep`) y delega en el **service**, que valida las reglas de negocio y accede a la base. En `unidades_medida/` se agregó un `service.py` de una sola función para que el router tampoco acceda directo a la base.

## Endpoints

| Método | Endpoint | Código |
|---|---|---|
| GET | `/api/v1/unidades-medida` | 200 |
| POST | `/api/v1/categorias` | 201 |
| GET | `/api/v1/categorias?activo=&search=` | 200 |
| GET | `/api/v1/categorias/{id}` | 200 |
| PUT | `/api/v1/categorias/{id}` | 200 |
| DELETE | `/api/v1/categorias/{id}` | 204 |
| POST | `/api/v1/productos` | 201 |
| GET | `/api/v1/productos?skip=&limit=&activo=&disponible=&categoria_id=&search=` | 200 |
| GET | `/api/v1/productos/{id}` | 200 |
| PUT | `/api/v1/productos/{id}` | 200 |
| DELETE | `/api/v1/productos/{id}` | 204 |
| POST | `/api/v1/productos/{id}/categorias` | 201 |
| GET | `/api/v1/productos/{id}/categorias` | 200 |

Los errores se devuelven con `HTTPException` en formato `{"detail": "..."}`: 404 (id inexistente), 409 (nombre repetido, registro anulado, clasificación repetida) y 422 (datos inválidos o stock con decimales en una unidad contable).
