import requests
import os
from dotenv import load_dotenv
from schemas.request import RotaRequest
from models import PontoAcessibilidade

load_dotenv()
API_KEY = os.getenv("ORS_API_KEY")

def calcular_rota_real(request: RotaRequest):
    url = "https://api.openrouteservice.org/v2/directions/foot-walking/geojson"
    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/geo+json'
    }

    # 1. Preparar o que vai para a API externa
    payload = {
        "coordinates": [
            [float(request.origem.lon), float(request.origem.lat)],
            [float(request.destino.lon), float(request.destino.lat)]
        ],
        "language": "pt"
    }

    try:
        # 2. Chamar a API primeiro
        response = requests.post(url, json=payload, headers=headers)
        dados = response.json()
        
        if response.status_code != 200:
            return {"status": "erro", "detalhe": "Falha na API externa do ORS."}
        
        # 3. Extrair os dados da resposta
        feature = dados['features'][0]
        summary = feature['properties']['summary']
        segmento = feature['properties']['segments'][0]

        # 4. Cálculos base
        distancia_km = round(summary['distance'] / 1000, 2)
        duracao_base_min = summary['duration'] / 60

        # 5. Lógica de Perfis (Definida uma única vez e no lugar certo)
        tipo = request.tipo_usuario
        if tipo == "pcd_motorizada":
            fator, limite = 1.1, 5.0
        elif tipo == "mobilidade_reduzida":
            fator, limite = 1.3, 3.5         
        else: # pcd_manual
            fator, limite = 1.5, 3.0

        duracao_ajustada_min = round(duracao_base_min * fator, 1)

        # 6. Alerta de esforço
        if distancia_km > limite:
            alerta = f"ALERTA DE ESFORÇO: Este trajeto supera {limite}km para seu perfil. Considere auxílio."
        elif distancia_km < 0.5:
            alerta = "Trajeto curto e de baixo esforço físico."
        else:
            alerta = "Trajeto de esforço moderado."

        # 7. Link do Google (Corrigido e fora de condicionais)
        link_google = f"https://www.google.com/maps/dir/?api=1&origin={request.origem.lat},{request.origem.lon}&destination={request.destino.lat},{request.destino.lon}&travelmode=walking"

        return {
            "status": "sucesso",
            "distancia_km": distancia_km,
            "duracao_min": duracao_ajustada_min,
            "alerta_acessibilidade": alerta,
            "geometria": feature['geometry'],
            "link_google_maps": link_google,
            "passo_a_passo": [etapa.get('instruction', 'Siga em frente') for etapa in segmento['steps']]
        }

    except Exception as e:
        print(f"ERRO CRÍTICO NO SERVICE: {str(e)}")
        return {"status": "erro", "detalhe": f"Erro interno: {str(e)}"}