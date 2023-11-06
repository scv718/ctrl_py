from dotenv import load_dotenv
import os

load_dotenv('config/config.env')

dbName = os.getenv("dbName")
dbPassWord = os.getenv("dbPassWord")
dbIp = os.getenv("dbIp")
dbPort = os.getenv("dbPort")
dbSchema = os.getenv("dbSchema")
pool_size = os.getenv("pool_size")
max_overflow = os.getenv("max_overflow")
autocommit = os.getenv("autocommit")
autoflush = os.getenv("autoflush")

max_connections = int(os.getenv("REST_MAX_CONNECTIONS"))
max_request_size = int(os.getenv("REST_BODY_LIMIT"))
debug = os.getenv("REST_DEBUG").lower() == "true"
host = os.getenv("REST_HOST")
port = int(os.getenv("REST_PORT"))

httpx_max_connections = int(os.getenv('HTTPX_MAX_CONNECTIONS', default=10))
httpx_max_keepalive = int(os.getenv('HTTPX_MAX_KEEPALIVE', default=100))  # Use a suitable default value
httpx_debug = os.getenv('HTTPX_DEBUG', default='True').lower() in ['true', '1']
httpx_timeout = float(os.getenv('HTTPX_TIMEOUT', default=10.0))


DATABASE_CONFIG = {
    'dbName': dbName,
    'dbPassWord': dbPassWord,
    'dbIp': dbIp,
    'dbPort': dbPort,
    'dbSchema': dbSchema,
    'pool_size': pool_size,
    'max_overflow' : max_overflow,
    'autocommit' : autocommit,
    'autoflush' : autoflush
}

REST_CONFIG = {
'max_connections':max_connections,
'max_request_size'  : max_request_size,
'debug' : debug,
'host' : host,
'port' : port
}

HTTPX_CLIENT_CONFIG = {
'max_connections':httpx_max_connections,
'max_request_size'  : httpx_max_keepalive,
'debug' : httpx_debug,
'timeout' : httpx_timeout
}
