from typing import Annotated

from fastapi import APIRouter, Path, Query

from app.core.database import SessionDep
from app.modules.productos import service
from app.modules.productos.schema import (
    ProductoCategoriaCreate,
    ProductoCategoriaPublic,
    ProductoCreate,
    ProductoPublic,
    ProductoUpdate,
)

router = APIRouter(prefix="/api/v1/productos", tags=["Productos"])


@router.post("", response_model=ProductoPublic, status_code=201)
def crear_producto(datos: ProductoCreate, session: SessionDep):
    return service.crear(session, datos)


@router.get("", response_model=list[ProductoPublic])
def listar_productos(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
    activo: Annotated[bool | None, Query()] = None,
    disponible: Annotated[bool | None, Query()] = None,
    categoria_id: Annotated[int | None, Query()] = None,
    search: Annotated[str | None, Query()] = None,
):
    return service.listar(session, skip, limit, activo, disponible, categoria_id, search)


@router.get("/{producto_id}", response_model=ProductoPublic)
def obtener_producto(producto_id: Annotated[int, Path()], session: SessionDep):
    return service.obtener(session, producto_id)


@router.put("/{producto_id}", response_model=ProductoPublic)
def actualizar_producto(
    producto_id: Annotated[int, Path()], datos: ProductoUpdate, session: SessionDep
):
    return service.actualizar(session, producto_id, datos)


@router.delete("/{producto_id}", status_code=204, response_model=None)
def anular_producto(producto_id: Annotated[int, Path()], session: SessionDep):
    service.anular(session, producto_id)


@router.post("/{producto_id}/categorias", response_model=ProductoCategoriaPublic, status_code=201)
def clasificar_producto(
    producto_id: Annotated[int, Path()], datos: ProductoCategoriaCreate, session: SessionDep
):
    return service.clasificar(session, producto_id, datos)


@router.get("/{producto_id}/categorias", response_model=list[ProductoCategoriaPublic])
def listar_categorias_de_producto(producto_id: Annotated[int, Path()], session: SessionDep):
    return service.listar_categorias(session, producto_id)
