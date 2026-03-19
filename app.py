import streamlit as st
from pydeck import Layer, ViewState, Deck
import asyncio
import logging
from datetime import datetime, timedelta, timezone
from iss_api import get_iss_location
import random  # apenas para simulação; remova quando usar a API real

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configuração da página do Streamlit
st.set_page_config(page_title="ISS Tracker - Rastreamento em tempo real", layout="wide")


# Função principal do aplicativo
async def app() -> None:
    # Função principal
    st.markdown("<h1 style='text-align: center;'>Posição da estação espacial ISS em tempo real</h1>",unsafe_allow_html=True)
    placeholder = st.empty()
    info = st.empty()
    counter = st.empty()
    metrics_container = st.empty()
    timeout = 15.0

    # Variável de controle para o loop de atualização
    if "is_running" not in st.session_state:
        st.session_state.is_running = True

    # Loop principal para atualização da posição da ISS
    while st.session_state.is_running:
        try:
            logger.info("Requisitando localização da ISS...")
            # Dados da API real, descomente a linha abaixo e remova a simulação quando estiver pronto para usar a API
            iss_lat, iss_lon = await get_iss_location(timeout=timeout)
            # Simulação de dados, remova quando usar a API real
            # iss_lat, iss_lon = random.uniform(-90, 90), random.uniform(-180, 180)  # Simulação de localização
            logger.info(f"ISS localizada em: lat={iss_lat}, lon={iss_lon}")

            # Configuração do ícone da ISS para o mapa
            icon_atlas = "iss.png"
            icon_mapping = {"iss": {"x": 0, "y": 0, "width": 64, "height": 64, "anchorY": 128}}

            # Configuração da camada do mapa para exibir a posição da ISS
            layer = Layer(
                "IconLayer",
                data=[{"lat": iss_lat, "lon": iss_lon, "icon": "iss"}],
                get_icon="icon",
                get_size=4,
                size_scale=10,
                get_position="[lon, lat]",
                pickable=True,
                icon_atlas=icon_atlas,
                icon_mapping=icon_mapping,
                text="ISS",
                get_text="ISS",
            )

            # Configuração da visualização inicial do mapa
            view_state = ViewState(latitude=iss_lat, longitude=iss_lon, zoom=3, pitch=0)

            # Configuração do deck para renderizar o mapa com a camada da ISS
            deck = Deck(layers=[layer], initial_view_state=view_state)

            # Renderização do mapa e das métricas em containers separados para melhor organização
            with placeholder.container():
                st.pydeck_chart(deck)

            with metrics_container.container():
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Latitude", f"{iss_lat:.2f}°", border=True)
                col2.metric("Longitude", f"{iss_lon:.2f}°", border=True)
                col3.metric("Altitude média", "408 km", border=True)
                col4.metric("Velocidade média", "27,600 km/h", border=True)

            # Exibição da última atualização
            sp_tz = timezone(timedelta(hours=-3))
            info.markdown(f"**Última atualização:** {datetime.now(sp_tz).strftime('%d/%m/%Y %H:%M:%S')}")

            # Contagem regressiva para a próxima atualização
            for i in range(int(timeout), -1, -1):
                if i == 0:
                    counter.markdown("**Atualizando...**")
                    await asyncio.sleep(1)
                else:
                    counter.markdown(f"Próxima atualização em: {i} segundos")
                await asyncio.sleep(1)

        except Exception as e:
            # Log completo com traceback para facilitar diagnóstico
            logger.exception("Erro ao atualizar posição da ISS")
            st.error(f"Erro ao atualizar posição da ISS: {type(e).__name__}: {repr(e)}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(app())
