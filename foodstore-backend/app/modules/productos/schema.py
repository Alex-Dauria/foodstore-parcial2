from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.modules.categorias.schema import CategoriaPublic
from app.modules.unidades_medida.model import UnidadMedidaPublic


class ProductoBase(BaseModel):
    # Quita los espacios de los extremos antes de validar.
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: Annotated[str, Field(min_length=3)]
    descripcion: str | None = None
    precio_base: Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)]
    unidad_venta_id: int
    stock_cantidad: Annotated[Decimal, Field(ge=0, max_digits=12, decimal_places=3)] = Decimal("0")
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    # Mismos campos que Create: el PUT reemplaza todos los campos propios del producto.
    pass


class ProductoPublic(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    # Se devuelven como número (no como texto) para que el frontend los use directo.
    precio_base: float
    stock_cantidad: float
    disponible: bool
    activo: bool
    anulado_at: datetime | None
    unidad_venta_id: int
    unidad_venta: UnidadMedidaPublic
    categorias: list[CategoriaPublic]
    # Campo calculado (RN-11): true cuando stock_cantidad > 0. No existe en la tabla.
    hay_stock: bool


class ProductoCategoriaCreate(BaseModel):
    categoria_id: int
    es_principal: bool = False


class ProductoCategoriaPublic(BaseModel):
    producto_id: int
    categoria_id: int
    nombre: str
    es_principal: bool
