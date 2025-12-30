# ♿ Mobility Care - Rotas Acessíveis em Recife

O **Mobility Care** é uma plataforma Full-Stack de auxílio à locomoção urbana para pessoas com deficiência ou mobilidade reduzida. O projeto utiliza geoprocessamento em tempo real para calcular trajetos otimizados, considerando perfis específicos de usuários.

🚀 **Veja o projeto online:** [[Link do seu Deploy no Render]](https://seu-app-link.onrender.com)

---

## 🛠️ Stack Tecnológica

O projeto foi construído utilizando tecnologias modernas de mercado, focando em performance, escalabilidade e facilidade de deploy:

- **Backend:** [Python](https://www.python.org/) + [FastAPI](https://fastapi.tiangolo.com/) (API Assíncrona de alta performance).
- **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/) (Persistência de pontos de interesse e logs).
- **Infraestrutura:** [Docker](https://www.docker.com/) (Containerização completa da aplicação).
- **Geoprocessamento:** [OpenRouteService API](https://openrouteservice.org/) (Cálculo de rotas e matriz de distância).
- **Frontend:** HTML5, CSS3 (Responsivo) e [Leaflet.js](https://leafletjs.com/) para mapas interativos.
- **Acessibilidade:** Integração com **Web Speech API** para narração de instruções de voz.

---

## ✨ Funcionalidades Principais

- **Cálculo de Rota Dinâmico:** Integração com mapas para traçar o melhor caminho a pé.
- **Perfis de Mobilidade:** Ajuste automático de tempo e esforço para cadeira de rodas manual, motorizada ou mobilidade reduzida.
- **Interface Responsiva:** Design otimizado para uso em smartphones (Mobile First).
- **Instruções de Voz:** Narração passo a passo do trajeto para facilitar a navegação.
- **Atalho para Google Maps:** Link externo direto para navegação GPS nativa.

---

## ⚙️ Configuração e Execução (Local)

Para rodar este projeto localmente, você precisará do Docker instalado.

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/mobility-care.git](https://github.com/seu-usuario/mobility-care.git)
   cd mobility-care