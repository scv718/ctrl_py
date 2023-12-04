import yaml
import os

# YAML 파일을 읽어옴

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
debug = config.get("REST_DEBUG") == True
host = config.get("REST_HOST")
port = config.get("REST_PORT")

httpx_max_connections = config.get('HTTPX_MAX_CONNECTIONS', 10)
httpx_max_keepalive = config.get('HTTPX_MAX_KEEPALIVE', 100)  # Suitable default value
httpx_debug = config.get('HTTPX_DEBUG', 'True') in [True, '1']
httpx_timeout = config.get('HTTPX_TIMEOUT', 10.0)


stream_file = config.get('WOWZA', {}).get('STREAM_FILE')
stream_file_profile = config.get('WOWZA', {}).get('STREAM_FILE_PROFILE')
stream_file_update = config.get('WOWZA', {}).get('STREAM_FILE_UPDATE')
stream_file_current = config.get('WOWZA', {}).get('STREAM_FILE_CURRENT')
stream_connect = config.get('WOWZA', {}).get('STREAM_CONNECT')
wowza_id = config.get('WOWZA', {}).get('ID')
wowza_password = config.get('WOWZA', {}).get('PASSWORD')

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

WOWZA_CONFIG = {
    'wowza_id': wowza_id,
    'wowza_password': wowza_password,
    'stream_file': stream_file,
    'stream_file_profile': stream_file_profile,
    'stream_file_update': stream_file_update,
    'stream_file_current': stream_file_current,
    'stream_connect': stream_connect
}
