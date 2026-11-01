from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.productos.model import Producto


class TipoUnidad(str, Enum):
    peso = "peso"
    volumen = "volumen"
    contable = "contable"


class UnidadMedida(SQLModel, table=True):
    __tablename__ = "unidad_medida"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    simbolo: str = Field(unique=True)
    tipo: TipoUnidad

    # Lado "1" de la relación 1:N con Producto.
    productos: list["Producto"] = Relationship(back_populates="unidad_venta")


class UnidadMedidaPublic(BaseModel):
    # Schema de salida: el modelo de tabla nunca se devuelve directamente.
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    simbolo: str
    tipo: TipoUnidad
