from aiohttp import ClientSession, ClientResponseError, ClientTimeout
from tenacity import (retry,stop_after_attempt,wait_exponential_jitter,retry_if_exception,)


def is_retriable_error(e: BaseException) -> bool:
    """Não retenta para erros 4xx (exceto 429)."""
    if isinstance(e, ClientResponseError):
        if 400 <= e.status < 500 and e.status != 429:
            return False
    return True


async def get_iss_location(timeout: float, retries: int = 5, base_delay: float = 0.5, max_delay: float = 30.0) -> tuple[float, float]:
    url = "http://api.open-notify.org/iss-now.json"

    @retry(
        stop=stop_after_attempt(retries),
        wait=wait_exponential_jitter(initial=base_delay, max=max_delay),
        retry=retry_if_exception(is_retriable_error),
        reraise=True,
    )
    async def fetch(session: ClientSession) -> tuple[float, float]:
        async with session.get(url) as response:
            response.raise_for_status()
            data: dict = await response.json()

            if data.get("message") != "success":
                raise ValueError("Falha ao obter localização da ISS")

            latitude = float(data["iss_position"]["latitude"])
            longitude = float(data["iss_position"]["longitude"])
            return latitude, longitude

    async with ClientSession(timeout=ClientTimeout(total=timeout)) as session:
        return await fetch(session)
