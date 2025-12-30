import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Imports internos
from database import engine, get_db
import models 
from api.routes_v1 import router as api_router

# Tenta criar as tabelas ao iniciar, mas sem derrubar o servidor se falhar
try:
    models.Base.metadata.create_all(bind=engine)
    print("Tabelas verificadas/criadas com sucesso.")
except Exception as e:
    print(f"Aviso: Não foi possível conectar ao banco para criar tabelas: {e}")

app = FastAPI(
    title="MobilityCare API",
    description="API para transporte humanizado e acessível",
    version="1.0.0"
)

# Configuração de CORS (Essencial para o Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas da API
app.include_router(api_router, prefix="/api/v1", tags=["Rotas"])

# Servir arquivos estáticos (Frontend)
# Verificamos se a pasta existe para evitar erro no deploy
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def serve_index():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"erro": "index.html não encontrado na pasta static"}

@app.get("/status")
async def status():
    return {"mensagem": "Bem-vindo à API Mobility Care!", "status": "online"}

# Endpoints de Pontos (CRUD Simples)
@app.post("/pontos/")
def criar_ponto(nome: str, lat: float, lon: float, db: Session = Depends(get_db)):
    try:
        novo_ponto = models.PontoAcessibilidade(nome=nome, lat=lat, lon=lon)
        db.add(novo_ponto)
        db.commit()
        db.refresh(novo_ponto)
        return novo_ponto
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar: {str(e)}")

@app.get("/pontos/")
def listar_pontos(db: Session = Depends(get_db)):
    return db.query(models.PontoAcessibilidade).all()