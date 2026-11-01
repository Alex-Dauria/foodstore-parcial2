from typing import Annotated

from fastapi import APIRouter, Path, Query

from app.core.database import SessionDep
from app.modules.categorias import service
from app.modules.categorias.schema import CategoriaCreate, CategoriaPublic, CategoriaUpdate

router = APIRouter(prefix="/api/v1/categorias", tags=["Categorías"])


@router.post("", response_model=CategoriaPublic, status_code=201)
def crear_categoria(datos: CategoriaCreate, session: SessionDep):
    return service.crear(session, datos)


@router.get("", response_model=list[CategoriaPublic])
def listar_categorias(
    session: SessionDep,
    activo: Annotated[bool | None, Query()] = None,
    search: Annotated[str | None, Query()] = None,
):
    return service.listar(session, activo, search)


@router.get("/{categoria_id}", response_model=CategoriaPublic)
def obtener_categoria(categoria_id: Annotated[int, Path()], session: SessionDep):
    return service.obtener(session, categoria_id)


@router.put("/{categoria_id}", response_model=CategoriaPublic)
def actualizar_categoria(
    categoria_id: Annotated[int, Path()], datos: CategoriaUpdate, session: SessionDep
):
    return service.actualizar(session, categoria_id, datos)


@router.delete("/{categoria_id}", status_code=204, response_model=None)
def anular_categoria(categoria_id: Annotated[int, Path()], session: SessionDep):
    service.anular(session, categoria_id)
