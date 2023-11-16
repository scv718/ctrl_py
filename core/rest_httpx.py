import os
import httpx
import core.config_yaml_read as config
import json

# from dotenv import load_dotenv
#
# load_dotenv('config_old.env')
#
# max_connections = int(os.getenv('HTTPX_MAX_CONNECTIONS', default=10))
# max_keepalive = int(os.getenv('HTTPX_MAX_KEEPALIVE', default=100))  # Use a suitable default value
# debug = os.getenv('HTTPX_DEBUG', default='True').lower() in ['true', '1']
# timeout = float(os.getenv('HTTPX_TIMEOUT', default=10.0))

HTTPX_CLIENT_CONFIG = config.HTTPX_CLIENT_CONFIG
max_connections = HTTPX_CLIENT_CONFIG["max_connections"]
max_keepalive = HTTPX_CLIENT_CONFIG["max_request_size"]
debug = HTTPX_CLIENT_CONFIG["debug"]
timeout = HTTPX_CLIENT_CONFIG["timeout"]


def create_httpx_client():
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
    return httpx.Client(
        limits=limits,  # Fix the typo here
        http2=debug,
        timeout=timeout
    )


def send_data(url, json_data):
    with create_httpx_client() as client:
        print(url, " 호츨")
        response = client.post(
            url, json=json_data, headers={'Content-Type': 'application/json'}
        )

        response_content = response.content.decode("utf-8")
        response_data = json.loads(response_content)
        res_code = response_data.get("res_code")

        print("res_code " + str(res_code))

        print(url, " 호출 끝")

        return res_code
