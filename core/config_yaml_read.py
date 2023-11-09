import yaml

# YAML 파일을 읽어옴
with open('config.yaml', 'r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.FullLoader)

# 필요한 설정 값을 변수로 저장
dbName = config.get("dbName")
dbPassWord = config.get("dbPassWord")
dbIp = config.get("dbIp")
dbPort = config.get("dbPort")
dbSchema = config.get("dbSchema")
pool_size = config.get("pool_size")
max_overflow = config.get("max_overflow")
autocommit = config.get("autocommit")
autoflush = config.get("autoflush")

max_connections = config.get("REST_MAX_CONNECTIONS")
max_request_size = config.get("REST_BODY_LIMIT")
debug = config.get("REST_DEBUG").lower() == "true"
host = config.get("REST_HOST")
port = config.get("REST_PORT")

httpx_max_connections = config.get('HTTPX_MAX_CONNECTIONS', 10)
httpx_max_keepalive = config.get('HTTPX_MAX_KEEPALIVE', 100)  # Suitable default value
httpx_debug = config.get('HTTPX_DEBUG', 'True').lower() in ['true', '1']
httpx_timeout = config.get('HTTPX_TIMEOUT', 10.0)

# 설정 값을 딕셔너리로 구성
DATABASE_CONFIG = {
    'dbName': dbName,
    'dbPassWord': dbPassWord,
    'dbIp': dbIp,
    'dbPort': dbPort,
    'dbSchema': dbSchema,
    'pool_size': pool_size,
    'max_overflow': max_overflow,
    'autocommit': autocommit,
    'autoflush': autoflush
}

REST_CONFIG = {
    'max_connections': max_connections,
    'max_request_size': max_request_size,
    'debug': debug,
    'host': host,
    'port': port
}

HTTPX_CLIENT_CONFIG = {
    'max_connections': httpx_max_connections,
    'max_request_size': httpx_max_keepalive,
    'debug': httpx_debug,
    'timeout': httpx_timeout
}
