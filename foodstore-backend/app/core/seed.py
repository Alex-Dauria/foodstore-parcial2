from sqlmodel import Session, select

from app.core.database import engine
from app.modules.unidades_medida.model import TipoUnidad, UnidadMedida

UNIDADES_INICIALES = [
    ("kilogramo", "kg", TipoUnidad.peso),
    ("gramo", "g", TipoUnidad.peso),
    ("litro", "L", TipoUnidad.volumen),
    ("mililitro", "mL", TipoUnidad.volumen),
    ("pieza", "u", TipoUnidad.contable),
    ("docena", "doc", TipoUnidad.contable),
]


def cargar_unidades_medida() -> None:
    with Session(engine) as session:
        # Solo inserta si la tabla está vacía: reiniciar la app no duplica filas.
        if session.exec(select(UnidadMedida)).first() is not None:
            return
        for nombre, simbolo, tipo in UNIDADES_INICIALES:
            session.add(UnidadMedida(nombre=nombre, simbolo=simbolo, tipo=tipo))
        session.commit()
