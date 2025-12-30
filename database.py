import os
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Pega a URL bruta
raw_uri = os.getenv("DATABASE_URL")

if not raw_uri:
    print("ERRO CRÍTICO: Variável DATABASE_URL está VAZIA no Render!")
    # Fallback para não quebrar o build, mas o erro e3q8 virá se tentar usar
    raw_uri = "postgresql://invalido:invalido@localhost/db"
else:
    # Log de segurança: mostra o início da URL no log do Render para conferirmos
    print(f"DEBUG: DATABASE_URL detectada começando com: {raw_uri[:15]}...")

    # Ajuste técnico para SQLAlchemy 2.0
    if raw_uri.startswith("postgres://"):
        raw_uri = raw_uri.replace("postgres://", "postgresql://", 1)

# Se a URL contiver caracteres especiais na senha, o SQLAlchemy 2.0 pode falhar.
# Esta configuração garante a compatibilidade.
SQLALCHEMY_DATABASE_URL = raw_uri

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    # Isso evita erros de conexão persistente no Render
    pool_recycle=300 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()