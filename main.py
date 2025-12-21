from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes_v1 import router as api_router



app = FastAPI(
    title = "MobilityCare API",
    description = "API para transporte humanizado e acessível",
    version = "1.0.0"
)
app.include_router(api_router, prefix= "/api/v1", tags=["Rotas"])


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def server_index():
    return FileResponse('static/index.html')
@app.get("/status")
async def root():
    return {"mensagem": "Bem-vindo à API Mobility Care!", "status": "online"}