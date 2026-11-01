import os
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# Cadena de conexión a PostgreSQL.
# Formato: postgresql+psycopg://USUARIO:CONTRASEÑA@HOST:PUERTO/BASE
# Si existe la variable de entorno DATABASE_URL, se usa esa en lugar del valor por defecto.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/foodstore_p2",
)

engine = create_engine(DATABASE_URL)


def create_db_and_tables() -> None:
    # Crea las tablas de todos los modelos importados (table=True) si todavía no existen.
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    # Dependencia de FastAPI: abre una sesión por petición y la cierra al terminar.
    with Session(engine) as session:
        yield session


# Tipo listo para inyectar la sesión en los endpoints: session: SessionDep
SessionDep = Annotated[Session, Depends(get_session)]
