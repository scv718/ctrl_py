from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import configparser
import os
from dotenv import load_dotenv
import core.log
import core.config_yaml_read as config

print("database.py is being imported")

DATABASE_CONFIG = config.DATABASE_CONFIG

dbName = DATABASE_CONFIG["dbName"]
dbPassWord = DATABASE_CONFIG["dbPassWord"]
dbIp = DATABASE_CONFIG["dbIp"]
dbPort = DATABASE_CONFIG["dbPort"]
dbSchema = DATABASE_CONFIG["dbSchema"]
pool_size = DATABASE_CONFIG["pool_size"]
max_overflow = DATABASE_CONFIG["max_overflow"]
autocommit = DATABASE_CONFIG["autocommit"]
autoflush = DATABASE_CONFIG["autoflush"]


SQLALCHEMY_DATABASE_URL = f"postgresql://{dbName}:{dbPassWord}@{dbIp}:{dbPort}/{dbSchema}"

## DB 엔진 생성 CORE
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size = int(pool_size),       # 최대 동시 커넥션 수
    max_overflow = int(max_overflow)   # 필요할 때 추가로 생성할 커넥션 수
)

## DB 엑세스를 위한 엔드포인트
SessionLocal = sessionmaker(autoflush=bool(autoflush), bind=engine)

## DB 모델 ORM
Base = declarative_base()