from requests.exceptions import RequestException
from aiohttp import ClientSession, ClientError, ClientResponseError, ClientTimeout


async def get_iss_location(timeout: float) -> tuple[float, float]:
    url: str = "http://api.open-notify.org/iss-now.json"
    try:
        async with ClientSession() as session:
            async with session.get(url, timeout=ClientTimeout(total=timeout)) as response:
                response.raise_for_status()
                data: dict = await response.json()
    except ClientError as e:
        raise Exception(f"Erro ao consultar API da ISS: {e}") from e
    except RequestException as e:
        raise Exception(f"Erro de requisição ao consultar API da ISS: {e}") from e
    except ClientResponseError as e:
        raise Exception(f"Resposta inválida da API da ISS: {e.status} {e.message}") from e
    except ValueError as e:
        raise Exception(f"Erro ao processar resposta da API da ISS: {e}") from e
    except Exception as e:
        raise Exception(f"Erro inesperado ao obter localização da ISS: {e}") from e

    if data.get("message") == "success":
        latitude: float = float(data["iss_position"]["latitude"])
        longitude: float = float(data["iss_position"]["longitude"])
        return latitude, longitude
    else:
        raise Exception("Falha ao obter localização da ISS")
