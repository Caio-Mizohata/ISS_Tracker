from aiohttp import ClientSession, ClientError, ClientResponseError, ClientTimeout

# Função para obter a localização da ISS usando a API pública
async def get_iss_location(timeout: float) -> dict[float, float]:
    url: str = "http://api.open-notify.org/iss-now.json"
    try:
        # Configuração do timeout para a requisição à API da ISS
        async with ClientSession(timeout=ClientTimeout(total=timeout)) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data: dict = await response.json()
    except ClientResponseError as e:
        raise Exception(f"Resposta inválida da API da ISS: {e.status}") from e
    except (ClientError, ValueError) as e:
        raise Exception(f"Erro ao consultar API da ISS: {e}") from e

    # Verificação da resposta da API e extração dos dados de latitude e longitude
    if data.get("message") == "success":
        latitude: float = float(data["iss_position"]["latitude"])
        longitude: float = float(data["iss_position"]["longitude"])

        return latitude, longitude
    else:
        raise Exception("Falha ao obter localização da ISS")
