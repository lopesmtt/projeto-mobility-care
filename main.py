from fastapi import FastAPI
from app.api.routes_v1 import router as api_router

app = FastAPI(
    title = "MobilityCare API",
    description = "API para transporte humanizado e acessível",
    version = "1.0.0"
)
app.include_router(api_router, prefix= "/api/v1", tags=["Rotas"])
@app.get("/")
async def root():
    return {"mensagem": "Bem-vindo à API Mobility Care!"}