from pydantic import BaseModel, Field

class Coordenada(BaseModel):
    """
    Modelo Pydantic para coordenada de latitude e longitude.
    """
    lat: float = Field(..., description="latitude da coordenada.")
    lon: float = Field(..., description="longitude da coordenada.")
class RotaRequest(BaseModel):
    """
    Modelo para requisição completa de cálculo de rota.
    """
    origem: Coordenada = Field(..., description="Ponto de partida da viagem.")
    destino: Coordenada = Field(..., description="Ponto final da viagem. ")
    tipo_usuario: str = Field(
        "pcd_manual",
        description="Tipo de usuário com critérios de acessibilidade. (ex: pcd_cadeirante, idoso_mobilidade_reduzida)."
    )    