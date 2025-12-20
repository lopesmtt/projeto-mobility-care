from fastapi import APIRouter, HTTPException
from app.models.request import RotaRequest
from app.services.routing_service import calcular_rota_real


router = APIRouter()

@router.post("/otimizar-rota", summary="Calcula rota real acessível")

async def otimizar_rota(request: RotaRequest):
    """
   Este endpoint recebe as coordenadas do usuário, valida os dados
    e solicita ao serviço de roteamento que busque o melhor caminho 
    através da API do OpenRouteService.
    """

    resultado = calcular_rota_real(request)
    if resultado.get("status") == "erro":
        raise HTTPException(status_code=400, detail=resultado.get("detalhe"))
    
    return resultado
