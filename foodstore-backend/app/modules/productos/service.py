from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlmodel import Session, col, func, select

from app.modules.categorias import service as categorias_service
from app.modules.categorias.model import Categoria
from app.modules.categorias.schema import CategoriaPublic
from app.modules.productos.model import Producto, ProductoCategoria
from app.modules.productos.schema import (
    ProductoCategoriaCreate,
    ProductoCategoriaPublic,
    ProductoCreate,
    ProductoPublic,
    ProductoUpdate,
)
from app.modules.unidades_medida.model import TipoUnidad, UnidadMedida, UnidadMedidaPublic


def a_public(producto: Producto) -> ProductoPublic:
    # Arma la respuesta con la unidad anidada, las categorías y hay_stock calculado (RN-11).
    return ProductoPublic(
        **producto.model_dump(),
        unidad_venta=UnidadMedidaPublic.model_validate(producto.unidad_venta),
        categorias=[CategoriaPublic.model_validate(c) for c in producto.categorias],
        hay_stock=producto.stock_cantidad > 0,
    )


def buscar(session: Session, producto_id: int) -> Producto:
    producto = session.get(Producto, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="El producto no existe")
    return producto


def buscar_unidad(session: Session, unidad_id: int) -> UnidadMedida:
    unidad = session.get(UnidadMedida, unidad_id)
    if unidad is None:
        raise HTTPException(status_code=404, detail="La unidad de venta no existe")
    return unidad


def validar_stock_segun_unidad(unidad: UnidadMedida, stock: Decimal) -> None:
    # RN-10: en una unidad contable (pieza, docena) el stock tiene que ser entero.
    if unidad.tipo == TipoUnidad.contable and stock % 1 != 0:
        raise HTTPException(
            status_code=422,
            detail=f"La unidad '{unidad.nombre}' es contable: el stock debe ser un número entero",
        )


def validar_nombre_unico(session: Session, nombre: str, excluir_id: int | None = None) -> None:
    # RN-02: único entre los activos, sin distinguir mayúsculas.
    consulta = select(Producto).where(
        Producto.activo == True,  # noqa: E712
        func.lower(Producto.nombre) == nombre.lower(),
    )
    if excluir_id is not None:
        consulta = consulta.where(Producto.id != excluir_id)
    if session.exec(consulta).first() is not None:
        raise HTTPException(status_code=409, detail="Ya existe un producto activo con ese nombre")


def crear(session: Session, datos: ProductoCreate) -> ProductoPublic:
    # Todas las validaciones van antes de tocar la base (RN-13).
    unidad = buscar_unidad(session, datos.unidad_venta_id)
    validar_stock_segun_unidad(unidad, datos.stock_cantidad)
    validar_nombre_unico(session, datos.nombre)
    producto = Producto(**datos.model_dump())
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return a_public(producto)


def listar(
    session: Session,
    skip: int,
    limit: int,
    activo: bool | None,
    disponible: bool | None,
    categoria_id: int | None,
    search: str | None,
) -> list[ProductoPublic]:
    # Omitido o true: solo activos. false: solo anulados.
    solo_activos = activo is None or activo
    consulta = select(Producto).where(Producto.activo == solo_activos)
    if disponible is not None:
        consulta = consulta.where(Producto.disponible == disponible)
    if categoria_id is not None:
        # Subconsulta sobre ProductoCategoria: cada producto aparece una sola vez.
        en_categoria = select(ProductoCategoria.producto_id).where(
            ProductoCategoria.categoria_id == categoria_id
        )
        consulta = consulta.where(col(Producto.id).in_(en_categoria))
    if search:
        consulta = consulta.where(col(Producto.nombre).ilike(f"%{search}%"))
    consulta = consulta.order_by(Producto.id).offset(skip).limit(limit)
    return [a_public(p) for p in session.exec(consulta).all()]


def obtener(session: Session, producto_id: int) -> ProductoPublic:
    return a_public(buscar(session, producto_id))


def actualizar(session: Session, producto_id: int, datos: ProductoUpdate) -> ProductoPublic:
    producto = buscar(session, producto_id)
    if not producto.activo:
        raise HTTPException(status_code=409, detail="El producto está anulado y no se puede modificar")
    # RN-10 se valida con la unidad nueva: también cubre el cambio de unidad_venta_id.
    unidad = buscar_unidad(session, datos.unidad_venta_id)
    validar_stock_segun_unidad(unidad, datos.stock_cantidad)
    validar_nombre_unico(session, datos.nombre, excluir_id=producto_id)
    producto.sqlmodel_update(datos.model_dump())
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return a_public(producto)


def anular(session: Session, producto_id: int) -> None:
    producto = buscar(session, producto_id)
    if not producto.activo:
        raise HTTPException(status_code=409, detail="El producto ya está anulado")
    # Baja lógica: no se modifica disponible ni stock_cantidad (RN-12).
    producto.activo = False
    producto.anulado_at = datetime.now(timezone.utc)
    session.add(producto)
    session.commit()


def clasificar(
    session: Session, producto_id: int, datos: ProductoCategoriaCreate
) -> ProductoCategoriaPublic:
    producto = buscar(session, producto_id)
    categoria = categorias_service.buscar(session, datos.categoria_id)
    # RN-08
    if not producto.activo:
        raise HTTPException(status_code=409, detail="No se puede clasificar un producto anulado")
    if not categoria.activo:
        raise HTTPException(status_code=409, detail="No se puede clasificar en una categoría anulada")
    # RN-07
    if session.get(ProductoCategoria, (producto_id, datos.categoria_id)) is not None:
        raise HTTPException(status_code=409, detail="El producto ya está clasificado en esa categoría")

    # RN-09: si la nueva es principal, la anterior deja de serlo en la misma transacción.
    if datos.es_principal:
        anteriores = session.exec(
            select(ProductoCategoria).where(
                ProductoCategoria.producto_id == producto_id,
                ProductoCategoria.es_principal == True,  # noqa: E712
            )
        ).all()
        for vinculo_anterior in anteriores:
            vinculo_anterior.es_principal = False
            session.add(vinculo_anterior)

    vinculo = ProductoCategoria(
        producto_id=producto_id,
        categoria_id=datos.categoria_id,
        es_principal=datos.es_principal,
    )
    session.add(vinculo)
    session.commit()  # un único commit: las dos modificaciones se guardan juntas
    return ProductoCategoriaPublic(
        producto_id=producto_id,
        categoria_id=categoria.id,
        nombre=categoria.nombre,
        es_principal=vinculo.es_principal,
    )


def listar_categorias(session: Session, producto_id: int) -> list[ProductoCategoriaPublic]:
    buscar(session, producto_id)
    filas = session.exec(
        select(ProductoCategoria, Categoria)
        .join(Categoria)
        .where(ProductoCategoria.producto_id == producto_id)
        .order_by(Categoria.id)
    ).all()
    return [
        ProductoCategoriaPublic(
            producto_id=vinculo.producto_id,
            categoria_id=categoria.id,
            nombre=categoria.nombre,
            es_principal=vinculo.es_principal,
        )
        for vinculo, categoria in filas
    ]
