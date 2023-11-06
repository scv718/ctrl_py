from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
import getpass
import datetime as dt


class Giga_user(Base):
    __tablename__ = "VMS_USER_INFO"

    USER_CODE = Column(String, primary_key=True, index=True)
    USER_ID = Column(String, unique=True, index=True)
    DEL_FLAG = Column(String, default="N")
    REG_DATETIME = Column(String)
    MOD_DATETIME = Column(String)


class Giga_cam(Base):
    __tablename__ = "VMS_CAM_INFO"

    CAM_CODE = Column(Integer, primary_key=True, index=True)
    MODEL_CODE = Column(Integer, index=True)
    CAM_ID = Column(String, unique=True, index=True)
    DEVICE_TYPE = Column(String, default="0")
    DEL_FLAG = Column(String, default="N")
    REG_DATETIME = Column(DateTime, default=dt.datetime.now())
    MOD_USER = Column(String, default=getpass.getuser())
    MOD_DATETIME = Column(DateTime, default=dt.datetime.now())
    VIDEO_FILE_PATH = Column(String, default="/storage")
    PROTOCOL_TYPE = Column(String, default="T")
    SAVE_METHOD = Column(String, default="A")
    CONN_TYPE = Column(String)

