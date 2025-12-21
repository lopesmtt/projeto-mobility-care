import requests
import os
from dotenv import load_dotenv
from app.models.request import RotaRequest

#Carrega a chave do arquivo .env
load_dotenv()

API_KEY = os.getenv("ORS_API_KEY")

if API_KEY is None:
    load_dotenv("../.env")
    API_KEY = os.getenv("ORS_API_KEY")

    print(f"---DEBUG: Chave detectada: {API_KEY}")

def calcular_rota_real(request: RotaRequest):
    """
        Simula cálculo de rota para acessibilidade.
        Este serviço recebe um objeto do tipo RotaRequest (validado pelo Pydantic).
        """
        
    url = "https://api.openrouteservice.org/v2/directions/foot-walking/geojson"

    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/geo+json'
    }

    #O ORS exige [longitude e latitude]
    payload = {
        "coordinates": [
            [float(request.origem.lon), float(request.origem.lat)],
            [float(request.destino.lon), float(request.destino.lat)]
        ],
        "language": "pt"
    }

    
    try:
        response = requests.post(url, json=payload, headers=headers)
        dados = response.json()
        # Se a API responder qualquer coisa diferente de 200 (sucesso)
        if response.status_code != 200:
            msg_erro = dados.get('error', {}.get('message', 'Erro na API externa'))
            print(f"ERRO DO ORS: {msg_erro}")
            return {"status": "erro", "detalhe": f"Não foi possível traçar a rota:{msg_erro}"}
        
        if 'features' not in dados or len(dados['features']) == 0:
            return {"status": "erro", "detalhe": f"Não foi possível traçar a rota: {msg_erro}"}
        feature = dados['features'][0]
        summary = feature['properties']['summary']
        segmento = feature['properties']['segments'][0]

        #CALCULOS DE ACESSIBILIDADE
        distancia_km = round(summary['distance'] / 1000, 2) 
        duracao_ajustada_min = round((summary['duration'] / 60) * 1.5, 1)
        #Definição de alerta de esforço
        alerta = "Trajeto de esforço moederado."
        if distancia_km > 3.0:
            alerta = "ALERTA DE ESFORÇO: Este trajeto supera 3km. Considere o uso de propulsão assistida ou verifique os pontos de descanso no percurso."
        elif distancia_km < 0.5:
            alerta = "Trajeto curto e de baixo esforço físico."
        else:
            alerta = "Trajeto de esforço moderado."

        # Link oficial do Google Maps (Directions)
        link_google = f"https://www.google.com/maps/dir/?api=1&origin={request.origem.lat},{request.origem.lon}&destination={request.destino.lat},{request.destino.lon}&travelmode=walking"

                
        #LÓGICA DE ALERTA DE ACESSIBILIDADE
        aviso = None
        if distancia_km > 3.0:
            aviso = "Cuidado: Este trajeto é longo (>3km) e pode ser cansativo para cadeiras manuais."
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
        print(f"ERRO NO CÓDIGO:{str(e)}")
        return {"status": "erro", "detalhe": str(e)}

