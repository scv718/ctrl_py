from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import service.user_crud as user_crud
import db.gigaeyes_schema as schemas
import db.gigaeyes_models as models
from db.database import SessionLocal, engine
from core.rest_httpx import create_httpx_client
import json

models.Base.metadata.create_all(bind=engine)

user_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post("/V100/VMS_10001/cam_info_register", response_model=dict)
def create_user(user_cam: schemas.UserCamCreate):
    user = user_cam.user
    cam = user_cam.cam
    with create_httpx_client() as client:
        response = client.post('http://localhost:18080/VMS_TEST/session')
        response_content = response.content.decode("utf-8")
        response_data = json.loads(response_content)
        res_code = response_data.get("res_code")

        if res_code != 200:
            return {"res_code": "400"}
        user_table = models.Giga_user
        user_result = user_crud.insertDB(engine, table=user_table, data=user)
        if user_result is None:
            return {"res_code": 400, "msg": "user Insert fail"}

        cam_table = models.Giga_cam
        cam_result = cam_result = user_crud.insertDB(engine, table=cam_table, data=cam)
        if cam_result is None:
            return {"res_code": 400, "msg": "cam Insert fail"}

    return {"res_code": 200}


@user_router.post("/gigaeyes/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, user=user)


@user_router.post("/gigaeyes/users/update", response_model=schemas.User)
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return user_crud.update_user(db=db, user=user)


@user_router.post("/users/giga/insert", response_model=dict)
def create_vsm_user(data: schemas.UserCreate):
    table = models.Giga_user()

    return user_crud.insertDB(engine, table, data)


@user_router.get("/users/giga/select", response_model=schemas.User)
def select_vms_user():
    table = models.Giga_user()

    return user_crud.selectAllDB(engine, table)


@user_router.get("/users/giga/select/{user_code}", response_model=schemas.User)
async def select_vms_user(user_code: str):
    table = models.Giga_user()
    return user_crud.selectUserCodeDB(engine, table, user_code)


@user_router.post("/users/giga/select/json", response_model=dict)
async def select_vms_user(request: Request):
    table = models.Giga_user()
    json_data = await request.json()
    print(json_data)
    user_crud.selectJson(engine, table, json_data)

    return json_data


@user_router.put("/users/update/giga", response_model=dict)
def update_vms_user(data: schemas.UserUpdate):
    table = models.Giga_user()
    # db_user = test_crud.get_user_by_email(db, email=data.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")

    return user_crud.updateDB(engine, table, data)


@user_router.delete("/users/delete/giga/", response_model=dict)
def delete_vms_user(data: schemas.UserDelete):
    table = models.Giga_user()
    # db_user = test_crud.get_user_by_email(db, email=data.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")

    return user_crud.deleteUserCodeDB(engine, table, data)
