from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.modules.productos.model import ProductoCategoria

if TYPE_CHECKING:
    from app.modules.productos.model import Producto


class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str | None = None
    activo: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
    anulado_at: datetime | None = None

    # Relación N:N con Producto a través de ProductoCategoria.
    productos: list["Producto"] = Relationship(
        back_populates="categorias", link_model=ProductoCategoria
    )
