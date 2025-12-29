from database import Base
from sqlalchemy import Column, Integer, String, Float


class PontoAcessibilidade(Base):
    __tablename__ = "pontos_acessibilidade"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String, nullable=True)
    lat = Column(Float)
    lon = Column(Float)
    tipo_obstaculo = Column(String, nullable=True)
