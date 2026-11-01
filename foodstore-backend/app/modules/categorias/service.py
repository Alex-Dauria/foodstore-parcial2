from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import Session, col, func, select

from app.modules.categorias.model import Categoria
from app.modules.categorias.schema import CategoriaCreate, CategoriaUpdate


def buscar(session: Session, categoria_id: int) -> Categoria:
    categoria = session.get(Categoria, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="La categoría no existe")
    return categoria


def validar_nombre_unico(session: Session, nombre: str, excluir_id: int | None = None) -> None:
    # RN-02: único entre las activas, sin distinguir mayúsculas ("pizzas" choca con "Pizzas").
    consulta = select(Categoria).where(
        Categoria.activo == True,  # noqa: E712
        func.lower(Categoria.nombre) == nombre.lower(),
    )
    if excluir_id is not None:
        consulta = consulta.where(Categoria.id != excluir_id)
    if session.exec(consulta).first() is not None:
        raise HTTPException(status_code=409, detail="Ya existe una categoría activa con ese nombre")


def crear(session: Session, datos: CategoriaCreate) -> Categoria:
    validar_nombre_unico(session, datos.nombre)
    categoria = Categoria(**datos.model_dump())
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


def listar(session: Session, activo: bool | None, search: str | None) -> list[Categoria]:
    # Omitido o true: solo activas. false: solo anuladas.
    solo_activas = activo is None or activo
    consulta = select(Categoria).where(Categoria.activo == solo_activas)
    if search:
        consulta = consulta.where(col(Categoria.nombre).ilike(f"%{search}%"))
    return list(session.exec(consulta.order_by(Categoria.id)).all())


def obtener(session: Session, categoria_id: int) -> Categoria:
    return buscar(session, categoria_id)


def actualizar(session: Session, categoria_id: int, datos: CategoriaUpdate) -> Categoria:
    categoria = buscar(session, categoria_id)
    if not categoria.activo:
        raise HTTPException(status_code=409, detail="La categoría está anulada y no se puede modificar")
    validar_nombre_unico(session, datos.nombre, excluir_id=categoria_id)
    categoria.sqlmodel_update(datos.model_dump())
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


def anular(session: Session, categoria_id: int) -> None:
    categoria = buscar(session, categoria_id)
    if not categoria.activo:
        raise HTTPException(status_code=409, detail="La categoría ya está anulada")
    # Baja lógica. RN-06: no se tocan los productos clasificados en ella.
    categoria.activo = False
    categoria.anulado_at = datetime.now(timezone.utc)
    session.add(categoria)
    session.commit()
