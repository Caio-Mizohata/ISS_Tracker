import streamlit as st
from pydeck import Layer, ViewState, Deck
import asyncio
import time
import logging
from datetime import datetime, timedelta, timezone
from iss_api import get_iss_location


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(page_title="ISS Tracker - Globe", layout="wide")


async def app() -> None:
    st.title("ISS Tracker - Globe")

    placeholder = st.empty()
    info = st.empty()
    counter = st.empty()
    timeout: float = 10.0

    if "is_running" not in st.session_state:
        st.session_state.is_running = True

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Parar", key="stop_btn"):
            st.session_state.is_running = False
    with col2:
        if st.button("Iniciar", key="start_btn"):
            st.session_state.is_running = True

    while st.session_state.is_running:
        try:
            logger.info("Requisitando localização da ISS...")
            iss_lat, iss_lon = await get_iss_location(timeout=timeout)
            logger.info(f"ISS localizada em: lat={iss_lat}, lon={iss_lon}")

            layer: Layer = Layer(
                "ScatterplotLayer",
                data=[{"lat": iss_lat, "lon": iss_lon}],
                get_position="[lon, lat]",
                get_fill_color="[200, 30, 0, 160]",
                get_radius=100000,
                pickable=True,
            )

            view_state: ViewState = ViewState(latitude=iss_lat, longitude=iss_lon, zoom=2)

            deck: Deck = Deck(layers=[layer], initial_view_state=view_state)

            with placeholder.container():
                st.pydeck_chart(deck)

            sp_tz = timezone(timedelta(hours=-3))
            info.markdown(f"**Última atualização:** {datetime.now(sp_tz).isoformat()} (São Paulo)")

            for i in range(int(timeout), 0, -1):
                counter.markdown(f"**Atualizando em:** {i} segundos")
                time.sleep(1)

        except Exception as e:
            logger.error(f"Erro ao atualizar posição da ISS: {e}")
            st.error(f"Erro ao atualizar posição da ISS: {e}")
            time.sleep(5)


if __name__ == "__main__":
    asyncio.run(app())
