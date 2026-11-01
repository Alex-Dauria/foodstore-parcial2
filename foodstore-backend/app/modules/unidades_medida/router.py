from fastapi import APIRouter

from app.core.database import SessionDep
from app.modules.unidades_medida import service
from app.modules.unidades_medida.model import UnidadMedidaPublic

router = APIRouter(prefix="/api/v1/unidades-medida", tags=["Unidades de medida"])


@router.get("", response_model=list[UnidadMedidaPublic])
def listar_unidades(session: SessionDep):
    return service.listar(session)
