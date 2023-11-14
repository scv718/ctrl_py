import os
import httpx
import core.config_yaml_read as config

# from dotenv import load_dotenv
#
# load_dotenv('config.env')
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
