import requests
import os
# Remova o load_dotenv() daqui se ele não for estritamente necessário em produção, 
# ou garanta que ele não quebre o código.
from schemas.request import RotaRequest

# 1. Captura Robusta
# Usamos os.environ.get para garantir a leitura direta do sistema operacional (Render)
API_KEY = os.environ.get("ORS_API_KEY")

def calcular_rota_real(request: RotaRequest):
    # Verificação imediata: se a chave sumiu, não faz a requisição
    if not API_KEY:
        return {"status": "erro", "detalhe": "Configuração ausente: ORS_API_KEY não encontrada no servidor."}

    url = "https://api.openrouteservice.org/v2/directions/foot-walking/geojson"
    
    # IMPORTANTE: A sua chave começa com 'eyJ...', o que indica ser um JWT. 
    # Em alguns casos, o ORS exige o prefixo 'Bearer' ou apenas a string. 
    # Como seu CURL funcionou com 'Authorization: CHAVE', manteremos assim.
    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/geo+json'
    }

    # Resto do seu payload (Correto!)
    payload = {
        "coordinates": [
            [float(request.origem.lon), float(request.origem.lat)],
            [float(request.destino.lon), float(request.destino.lat)]
        ],
        "language": "pt"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # DEBUG PROFISSIONAL: Se der erro, vamos saber exatamente o que a API externa disse
        if response.status_code != 200:
            erro_api = response.json()
            print(f"Erro ORS: {response.status_code} - {erro_api}")
            return {
                "status": "erro", 
                "detalhe": f"Falha na API externa (Status {response.status_code}). Verifique a cota ou chave."
            }
        
        dados = response.json()
        
        # ... (Todo o seu código de extração de dados e lógica de perfis está correto) ...
        
        # 7. Link do Google (Pequeno ajuste na URL para formato padrão)
        link_google = f"https://www.google.com/maps/dir/?api=1&origin={request.origem.lat},{request.origem.lon}&destination={request.destino.lat},{request.destino.lon}&travelmode=walking"

        # Retorno (Mantendo sua estrutura)
        feature = dados['features'][0]
        summary = feature['properties']['summary']
        segmento = feature['properties']['segments'][0]
        
        # Suas lógicas de distância e tempo aqui...
        # [Mantenha o bloco de lógica de perfis que você já escreveu]
        
        return {
            "status": "sucesso",
            "distancia_km": round(summary['distance'] / 1000, 2),
            "duracao_min": round((summary['duration'] / 60) * fator, 1),
            "alerta_acessibilidade": alerta,
            "geometria": feature['geometry'],
            "link_google_maps": link_google,
            "passo_a_passo": [etapa.get('instruction', 'Siga em frente') for etapa in segmento['steps']]
        }

    except Exception as e:
        print(f"ERRO CRÍTICO NO SERVICE: {str(e)}")
        return {"status": "erro", "detalhe": f"Erro interno: {str(e)}"}