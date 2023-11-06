from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import configparser
import os
from dotenv import load_dotenv

load_dotenv('config/config.env')

print("database.py is being imported")

DATABASE_CONFIG = {
    'host': 'localhost',
    'dbname': 'company',
    'user': 'user',
    'password': 'password',
    'port': 3306
}

# config = configparser.ConfigParser()
# with open('config/database.ini', encoding='utf-8') as config_file:
#     config.read_file(config_file)

# ## DB 주소
# dbName = config['database']['dbName']
# dbPassWord = config['database']['dbPassWord']
# dbIp = config['database']['dbIp']
# dbPort = config['database']['dbPort']
# dbSchema = config['database']['dbSchema']
# config_pool_size = config['database']['pool_size']
# config_max_overflow = config['database']['max_overflow']
# autocommit = config['database']['autocommit']
# autoflush = config['database']['autoflush']

dbName = os.getenv("dbName")
dbPassWord = os.getenv("dbPassWord")
dbIp = os.getenv("dbIp")
dbPort = os.getenv("dbPort")
dbSchema = os.getenv("dbSchema")
pool_size = os.getenv("pool_size")
max_overflow = os.getenv("max_overflow")
autocommit = os.getenv("autocommit")
autoflush = os.getenv("autoflush")

SQLALCHEMY_DATABASE_URL = f"postgresql://{dbName}:{dbPassWord}@{dbIp}:{dbPort}/{dbSchema}"

## DB 엔진 생성 CORE
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size = int(pool_size),       # 최대 동시 커넥션 수
    max_overflow = int(max_overflow)   # 필요할 때 추가로 생성할 커넥션 수
)

## DB 엑세스를 위한 엔드포인트
SessionLocal = sessionmaker(autocommit=bool(autocommit), autoflush=bool(autoflush), bind=engine)

## DB 모델 ORM
Base = declarative_base()