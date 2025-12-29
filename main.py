import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
import models 
from api.routes_v1 import router as api_router
models.Base.metadata.create_all(bind=engine)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(
    title = "MobilityCare API",
    description = "API para transporte humanizado e acessível",
    version = "1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que seu index.html acesse a API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix= "/api/v1", tags=["Rotas"])


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def server_index():
    return FileResponse('static/index.html')
@app.get("/status")
async def root():
    return {"mensagem": "Bem-vindo à API Mobility Care!", "status": "online"}

@app.post("/pontos/")
def criar_ponto(nome: str, lat: float, lon: float, db: Session = Depends(get_db)):
    novo_ponto = models.PontoAcessibilidade(nome=nome, lat=lat, lon=lon)
    db.add(novo_ponto)
    db.commit()
    db.refresh(novo_ponto)
    return novo_ponto
@app.get("/pontos/")
def listar_pontos(db: Session = Depends(get_db)):
    return db.query(models.PontoAcessibilidade).all()