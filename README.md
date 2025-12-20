# ♿ Mobility Care API - Recife

<p align="center">
  <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/wheelchair.svg" width="100" height="100">
</p>

A **Mobility Care API** é uma solução de roteamento inteligente baseada em FastAPI, focada na acessibilidade urbana. Ela foi projetada para calcular rotas em Recife, oferecendo estimativas de tempo realistas e orientações específicas para pessoas cadeirantes.

## 🚀 Funcionalidades

- **♿ Cálculo de Rota Realista:** Ajusta o tempo de percurso aplicando um fator de 1.5x sobre a velocidade de caminhada padrão, adequando-se ao ritmo de um cadeirante.
- **📍 Link Direto para GPS:** Gera automaticamente um link do Google Maps para navegação visual imediata.
- **🗣️ Instruções Detalhadas:** Retorna o passo a passo da rota em português.
- **⚠️ Alertas de Esforço (Sprint 2):** Identifica se o trajeto é superior a 3km e emite um alerta de possível exaustão física.

## 🛠️ Tecnologias Utilizadas

- **🐍 Python 3.10+**
- **⚡ FastAPI** (Framework Web)
- **🗺️ OpenRouteService API** (Dados Geográficos)
- **🚀 Uvicorn** (Servidor ASGI)
- **📡 Requests** (Consumo de API)

## 📋 Como Configurar o Projeto

### 1. Clonar o repositório
```bash
git clone [https://github.com/lopesmtt/projeto-mobility-care.git](https://github.com/lopesmtt/projeto-mobility-care.git)
cd projeto-mobility-care