from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db_and_tables
from app.core.seed import cargar_unidades_medida
from app.modules.categorias.router import router as categorias_router
from app.modules.productos.router import router as productos_router
from app.modules.unidades_medida.router import router as unidades_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al iniciar: crea las tablas (los modelos ya están importados por los routers) y carga el seed.
    create_db_and_tables()
    cargar_unidades_medida()
    yield


app = FastAPI(title="Food Store — Catálogo de Productos", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(unidades_router)
app.include_router(categorias_router)
app.include_router(productos_router)
