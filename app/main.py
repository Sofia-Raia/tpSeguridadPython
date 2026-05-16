from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
# Importamos los routers
from app.modules.producto.router import router as producto_router
from app.modules.categoria.router import router as categoria_router
from app.modules.ingrediente.router import router as ingrediente_router
from app.modules.usuario.router import router as usuario_router  # <- NUEVO: Router de Autenticación
 
# Importamos la configuración de DB
from app.core.database import create_db_and_tables
 
# Importamos los modelos (Esencial para que create_db_and_tables detecte todo)
from app.modules.categoria.models import Categoria
from app.modules.ingrediente.models import Ingrediente
from app.modules.producto.models import Producto, ProductoCategoriaLink, ProductoIngredienteLink
from app.modules.usuario.models import UsuarioModel  # <- NUEVO: Modelo para crear la tabla de MySQL
 
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que corre al iniciar la app
    create_db_and_tables()  # Ahora también creará automáticamente la tabla 'usuarios'
    yield
    # Código que corre al apagar la app (cleanup, cerrar conexiones, etc.)
 
 
def create_app() -> FastAPI:
    app = FastAPI(
        title="Parcial 1 - API Integradora",
        description="Backend FastAPI con UoW, Repository y Relaciones Complejas",
        version="1.0.0",
        lifespan=lifespan,
    )
 
    # CORS (Listo para manejar las cookies HttpOnly con allow_credentials=True)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
 
    # Registramos las rutas
    app.include_router(usuario_router)  # <- NUEVO: Endpoints de /auth/register, /auth/token y /auth/me
    app.include_router(producto_router)
    app.include_router(categoria_router)
    app.include_router(ingrediente_router)
 
    return app
 
 
app = create_app()