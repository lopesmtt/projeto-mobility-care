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
    url = "https://api.openrouteservice.org/v2/directions/foot-walking"

    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8'
    }

    #O ORS exige [longitude e latitude]
    payload = {
        "coordinates": [
            [request.origem.lon, request.origem.lat],
            [request.destino.lon, request.destino.lat]
        ],
        "language": "pt"
    }

    
    try:
        response = requests.post(url, json=payload, headers=headers)
        # Se a API responder qualquer coisa diferente de 200 (sucesso)
        if response.status_code != 200:
            print(f"ERRO API ORS: {response.status_code}")
            print(f"RESPOSTA DA API: {response.text}")
            return {"status": "erro", "detalhe": f"ORS deu erro{response.status_code}: {response.text}"}

        dados = response.json()
        rota = dados['routes'][0]

        #CALCULOS DE ACESSIBILIDADE
        distancia_m = rota['summary']['distance']
        distancia_km = round(distancia_m / 1000, 2)

        duracao_seg = rota['summary']['duration'] 
        duracao_ajustada_min = round((duracao_seg / 60) * 1.5, 1)
        #Definição de alerta de esforço
        alerta = None
        if distancia_km > 3.0:
            alerta = "ALERTA DE ESFORÇO: Este trajeto supera 3km. Considere o uso de propulsão assistida ou verifique os pontos de descanso no percurso."
        elif distancia_km < 0.5:
            alerta = "Trajeto curto e de baixo esforço físico."
        else:
            alerta = "Trajeto de esforço moderado."

        # Certifique-se que 'payload' está acessível aqui
        origem = payload['coordinates'][0]
        destino = payload['coordinates'][1]
        
        #LÓGICA DE ALERTA DE ACESSIBILIDADE
        aviso = None
        if distancia_km > 3.0:
            aviso = "Cuidado: Este trajeto é longo (>3km) e pode ser cansativo para cadeiras manuais."

        # Link oficial do Google Maps (Directions)
        link_google = f"https://www.google.com/maps/dir/?api=1&origin={origem[1]},{origem[0]}&destination={destino[1]},{destino[0]}&travelmode=walking"
        return {
            "status": "sucesso",
            "distancia_km": distancia_km,
            "duracao_min": duracao_ajustada_min,
            "link_google_maps": link_google,
            "passo_a_passo": [etapa['instruction'] for etapa in rota['segments'][0]['steps']]
        }
    except Exception as e:
        print(f"ERRO NO CÓDIGO:{str(e)}")
        return {"status": "erro", "detalhe": str(e)}

