import asyncio
import random
from aiohttp import ClientSession, ClientError, ClientResponseError, ClientTimeout


# Função para obter a localização da ISS usando a API pública
async def get_iss_location(timeout: float, retries: int = 5, base_delay: float = 0.5, max_delay: float = 30.0) -> tuple[float, float]:
    url: str = "http://api.open-notify.org/iss-now.json"

    for attempt in range(retries):
        try:
            async with ClientSession(timeout=ClientTimeout(total=timeout)) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data: dict = await response.json()

                    if data.get("message") != "success":
                        raise Exception("Falha ao obter localização da ISS")

                    latitude: float = float(data["iss_position"]["latitude"])
                    longitude: float = float(data["iss_position"]["longitude"])
                    return latitude, longitude

        except ClientResponseError as e:
            # Não tentar novamente para erros do cliente (4xx), exceto 429 (rate limit)
            if 400 <= e.status < 500 and e.status != 429:
                raise Exception(f"Resposta inválida da API da ISS: {e.status}") from e
            last_exc = Exception(f"Resposta inválida da API da ISS: {e.status}")
            last_exc.__cause__ = e

        except (ClientError, ValueError, asyncio.TimeoutError) as e:
            last_exc = Exception(f"Erro ao consultar API da ISS: {e}")
            last_exc.__cause__ = e

        # Backoff exponencial com jitter para evitar sobrecarregar a API em caso de falhas temporárias
        # Se não for a última tentativa, aguarda com backoff exponencial + jitter (full jitter)
        if attempt < retries - 1:
            exp_delay = min(max_delay, base_delay * (2**attempt))
            sleep_time = random.uniform(0, exp_delay)
            await asyncio.sleep(sleep_time)
        else:
            # última tentativa falhou: levanta a última exceção construída
            raise last_exc
