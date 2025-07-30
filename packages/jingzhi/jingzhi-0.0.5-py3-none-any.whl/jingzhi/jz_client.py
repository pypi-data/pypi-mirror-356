from openai import OpenAI
from typing import Union, Mapping
import httpx
from httpx import Timeout

from constants import DEFAULT_MAX_RETRIES,JZ_MASS_ENDPOINT



class Jingzhi():
    def __new__(
            cls,
            *,
            api_key: str | None = None,
            organization: str | None = None,
            project: str | None = None,
            base_url: str | httpx.URL | None = None,
            websocket_base_url: str | httpx.URL | None = None,
            timeout: Union[float, Timeout, None,bool] = False,
            max_retries: int = DEFAULT_MAX_RETRIES,
            default_headers: Mapping[str, str] | None = None,
            default_query: Mapping[str, object] | None = None,
            http_client: httpx.Client | None = None,
            _strict_response_validation: bool = False,
        ):
        if base_url is None:
            base_url = JZ_MASS_ENDPOINT
        openai = OpenAI(
            api_key = api_key,
            organization = organization,
            project = project,
            base_url = base_url,
            websocket_base_url = websocket_base_url,
            timeout = timeout,
            max_retries = max_retries,
            default_headers = default_headers,
            default_query = default_query,
            http_client = http_client,
            _strict_response_validation = _strict_response_validation
            )
        return openai



