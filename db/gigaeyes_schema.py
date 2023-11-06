from pydantic import BaseModel
from datetime import datetime


# VMS_USER_INFO MODEL
class UserBase(BaseModel):
    USER_CODE: str


class User(UserBase):
    USER_CODE: str
    USER_ID: str
    REG_DATETIME: datetime
    MOD_DATETIME: datetime

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    USER_ID: str


class UserUpdate(UserBase):
    USER_CODE: str
    DEL_FLAG: str


class UserDelete(UserBase):
    USER_CODE: str


# VMS_CAM_INFO MODEL
class CamBase(BaseModel):
    CAM_CODE: int


class Cam(CamBase):
    CAM_CODE: int
    MODEL_CODE: int
    CAM_ID: str
    DEVICE_TYPE: str
    DEL_FLAG: str
    REG_DATETIME: datetime
    MOD_USER: str
    MOD_DATETIME: datetime
    VIDEO_FILE_PATH: str
    PROTOCOL_TYPE: str
    SAVE_METHOD: str
    CONN_TYPE: str

    class Config:
        orm_mode = True


class CamCreate(CamBase):
    MODEL_CODE: int
    CAM_ID: str
    CONN_TYPE: str


class UserCamCreate(BaseModel):
    user: UserCreate
    cam: CamCreate


class CamUpdate(CamBase):
    CAM_CODE: int
