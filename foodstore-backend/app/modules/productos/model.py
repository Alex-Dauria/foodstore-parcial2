from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.categorias.model import Categoria
    from app.modules.unidades_medida.model import UnidadMedida


class ProductoCategoria(SQLModel, table=True):
    # Modelo intermedio (link model) de la relación N:N Producto <-> Categoria.
    __tablename__ = "producto_categoria"

    # PK compuesta: un producto no puede estar dos veces en la misma categoría.
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True)
    es_principal: bool = Field(default=False, sa_column_kwargs={"server_default": "false"})


class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    unidad_venta_id: int = Field(foreign_key="unidad_medida.id")
    nombre: str
    descripcion: str | None = None
    precio_base: Decimal = Field(max_digits=10, decimal_places=2)
    stock_cantidad: Decimal = Field(
        default=Decimal("0"), max_digits=12, decimal_places=3, sa_column_kwargs={"server_default": "0"}
    )
    # default en Python y server_default para que la columna en PostgreSQL tenga DEFAULT.
    disponible: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
    activo: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
    anulado_at: datetime | None = None
    # hay_stock NO es una columna: se calcula en el servicio en cada lectura.

    # Lado "N" de la relación 1:N con UnidadMedida.
    unidad_venta: "UnidadMedida" = Relationship(back_populates="productos")
    # Relación N:N con Categoria a través de ProductoCategoria.
    categorias: list["Categoria"] = Relationship(
        back_populates="productos", link_model=ProductoCategoria
    )
