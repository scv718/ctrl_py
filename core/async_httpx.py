from builtins import print

import httpx
import core.config_yaml_read as config
import json

HTTPX_CLIENT_CONFIG = config.HTTPX_CLIENT_CONFIG
max_connections = HTTPX_CLIENT_CONFIG["max_connections"]
max_keepalive = HTTPX_CLIENT_CONFIG["max_request_size"]
debug = HTTPX_CLIENT_CONFIG["debug"]
timeout = HTTPX_CLIENT_CONFIG["timeout"]


class HttpClient:
    def __init__(self):
        print(self,"__init__")
        self.client = None

    async def __aenter__(self):
        limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        self.client = httpx.AsyncClient(
            limits=limits,
            http2=debug,
            timeout=timeout
        )
        print(self, "__aenter__")
        return self.client

    async def __aexit__(self, exc_type, exc, tb):
        print(self, "__aexit__")
        await self.client.aclose()


async def async_send(url, json_data):
    async with HttpClient() as client:
        print(url, "호출")
        print(json_data)
        response = await client.post(
            url, data=json_data, headers={'Content-Type': 'application/json'}
        )
        print(response)
        response_content = response.content.decode("utf-8")
        response_data = json.loads(response_content)
        res_code = response_data.get("res_code")

        print("res_code " + str(res_code))
        print(url, "호출 끝")

        return response_data
