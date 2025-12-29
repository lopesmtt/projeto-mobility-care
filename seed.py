import os
from database import SessionLocal
from models import PontoAcessibilidade

def seed_database():
    db = SessionLocal()
    try:
        # Lista de pontos reais de Recife para teste
        pontos = [
            {
                "nome": "Calçada - Rua da Aurora",
                "descricao": "Trecho com desnível acentuado perto do Museu de Arte Moderna",
                "lat": -8.0512, "lon": -34.8791,
                "tipo_obstaculo": "Desnivel"
            },
            {
                "nome": "Cruzamento - Derby",
                "descricao": "Rampa de acessibilidade obstruída ou inexistente",
                "lat": -8.0576, "lon": -34.8980,
                "tipo_obstaculo": "Rampa Inexistente"
            },
            {
                "nome": "Entrada - Porto Digital",
                "descricao": "Paralelepípedos irregulares dificultando cadeiras de rodas",
                "lat": -8.0615, "lon": -34.8715,
                "tipo_obstaculo": "Piso Irregular"
            },
            {
                "nome": "Pina - Orla",
                "descricao": "Acesso à areia sem rampa adequada",
                "lat": -8.0890, "lon": -34.8810,
                "tipo_obstaculo": "Falta de Rampa"
            }
        ]

        print("Limpando dados antigos...")
        db.query(PontoAcessibilidade).delete()

        for p in pontos:
            novo_ponto = PontoAcessibilidade(**p)
            db.add(novo_ponto)
        
        db.commit()
        print("✅ Banco de dados populado com sucesso em Recife!")
    except Exception as e:
        print(f"❌ Erro ao popular: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
