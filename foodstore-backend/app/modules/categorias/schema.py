from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class CategoriaBase(BaseModel):
    # Quita los espacios de los extremos antes de validar: "  ab  " queda "ab" y falla min_length.
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: Annotated[str, Field(min_length=3)]
    descripcion: str | None = None


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaPublic(CategoriaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activo: bool
    anulado_at: datetime | None
