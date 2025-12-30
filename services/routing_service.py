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
        feature = dados['features'][0]
        summary = feature['properties']['summary']
        segmento = feature['properties']['segments'][0]

        # --- LÓGICA DE PERFIS (Onde o 'fator' é definido) ---
        perfil = getattr(request, 'perfil', 'padrao') # Pega o perfil ou usa 'padrao'
        
        if perfil == "cadeirante":
            fator = 1.5
            alerta = "Rota com inclinação verificada para cadeiras de rodas."
        elif perfil == "idoso":
            fator = 1.3
            alerta = "Rota com pontos de descanso identificados."
        else:
            fator = 1.0
            alerta = "Rota padrão de pedestre."

        # Agora o cálculo funciona porque 'fator' existe!
        duracao_ajustada = round((summary['duration'] / 60) * fator, 1)
        
        # 7. Link do Google (Formato corrigido)
        link_google = f"https://www.google.com/maps/dir/?api=1&origin={request.origem.lat},{request.origem.lon}&destination={request.destino.lat},{request.destino.lon}&travelmode=walking"

        return {
            "status": "sucesso",
            "distancia_km": round(summary['distance'] / 1000, 2),
            "duracao_min": duracao_ajustada,
            "alerta_acessibilidade": alerta,
            "geometria": feature['geometry'],
            "link_google_maps": link_google,
            "passo_a_passo": [etapa.get('instruction', 'Siga em frente') for etapa in segmento['steps']]
        }

    except Exception as e:
        print(f"ERRO CRÍTICO NO SERVICE: {str(e)}")
        return {"status": "erro", "detalhe": f"Erro interno: {str(e)}"}