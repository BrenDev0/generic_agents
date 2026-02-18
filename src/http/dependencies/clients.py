import logging
from src.di import DependencyNotRegistered, Container
from ..domain import async_http_client
from ..infrastructure import HttpxAsyncHttpClient

logger = logging.getLogger(__name__)

def get_async_http_client() -> async_http_client.AsyncHttpClient:
    try:
        instance_key = "async_http_client"
        client = Container.resolve(instance_key)

    except DependencyNotRegistered:
        client = HttpxAsyncHttpClient()
        Container.register(instance_key, client)
        logger.debug(f"{instance_key} registered")

    return client
