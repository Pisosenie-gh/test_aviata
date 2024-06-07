from http.client import InvalidURL
from urllib.error import HTTPError
import aiohttp
import json
from config import settings
from config.settings import redis_client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseService:
    endpoint: str = ''
    timeout: int = 20
    headers: dict = {}
    search_id: str = ''
    service_type: str = ''

    @property
    def host(self) -> str:
        raise NotImplementedError

    @property
    def code(self) -> str:
        raise NotImplementedError

    @property
    def url(self) -> str:
        return f"{self.host}{self.endpoint}"

    async def prepare_response_data(self, response) -> dict:
        try:
            return response
        except aiohttp.ContentTypeError:
            logger.error("Response content type is not JSON")
            return {}

    async def __pre_prepare_response__(self, response, status) -> dict:
        if status == 200:
            return await self.finalize_response(await self.prepare_response_data(response))
        elif status == 404:
            raise InvalidURL(self.url)
        elif status == 500:
            return await self.handle_500_exception(response)

        raise HTTPError(response.text)

    async def _make_request(self, **kwargs) -> aiohttp.ClientResponse:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url, timeout=self.timeout, **kwargs) as response:
                    return await response.json(), response.status
            except aiohttp.ClientConnectionError as e:
                logger.error(f"Connection error: {e}")
                raise HTTPError(f"Connection error: {e}")
            except aiohttp.ClientError as e:
                logger.error(f"Client error: {e}")
                raise HTTPError(f"Client error: {e}")

    async def make_request(self, **kwargs) -> dict:
        response, status = await self._make_request(**kwargs)
        return await self.__pre_prepare_response__(response, status)

    async def finalize_response(self, prepared_response: dict) -> dict:
        redis_client.set(f"{self.search_id}_{self.service_type}", json.dumps(prepared_response))
        return prepared_response

    async def handle_500_exception(self, response: aiohttp.ClientResponse):
        raise HTTPError(response.text)

    async def __call__(self, **kwargs):
        return await self.make_request(**kwargs)


class ProviderService(BaseService):

    def __init__(self, search_id: str):
        self.search_id = search_id


class ProviderAService(ProviderService):
    host = settings.PROVIDER_A_URL
    service_type = 'a'


class ProviderBService(ProviderService):
    host = settings.PROVIDER_B_URL
    service_type = 'b'
