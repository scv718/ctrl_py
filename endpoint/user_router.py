from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import service.user_crud as user_crud
import db.gigaeyes_schema as schemas
import db.gigaeyes_models as models
import service.camera as camera
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


@user_router.post("/V100/VMS_10005/live_video_stream_urls", response_model=dict)
async def select_vms_user(request: Request):
    json_data = await request.json()
    print(json_data)
    # table = models.GigaUser()
    # select_user_data = user_crud.selectJson(engine, table, json_data)
    #
    # table = models.GigaCam()
    # select_cam_data = user_crud.selectJson(engine, table, json_data)

    table = models.GigaUserCam()
    select_user_cam_data = user_crud.selectJson(engine, table, json_data)

    print(select_user_cam_data)
    # if select_user_data and select_cam_data:
    if select_user_cam_data:
        first_row = select_user_cam_data[0]
        wowza_index = first_row.get('WOWZA_INDEX')
        wowza_dict = {
            "WOWZA_INDEX": wowza_index
        }
        print(wowza_index)
        table = models.GigaWowza()
        wowza_data = user_crud.selectJson(engine, table, wowza_dict)

        print("wowza_data : ", wowza_data)

        streaming_url = camera.test_camera(wowza_data)

        print("url: " + streaming_url)
        if streaming_url is not None:
            return {"res_code": 200, "data": {"url": streaming_url}}
        else:
            return {"res_code": 911}
    else:
        print("No data available.")
        return {"res_code": 400}


@user_router.post("/V100/VMS_10001/cam_info_register", response_model=dict)
def create_user(user_cam: schemas.UserCamCreate, db: Session = Depends(get_db)):
    try:
        print(user_cam)
        user = user_cam.user
        cam = user_cam.cam

        data_to_send = {
            "user_id": user.USER_ID,
            "cam_id": cam.CAM_ID
        }

        json_data = json.dumps(data_to_send)

        user_table = models.GigaUser
        cam_table = models.GigaCam
        user_cam_table = models.GigaUserCam

        with engine.connect() as conn:
            trans = conn.begin()
            user_code = user.USER_CODE
            user_select_result = user_crud.selectUserCodeDB(conn, table=user_table, user_code=user_code)
            print("user_select " + str(user_select_result))

            # if user_select_result is not None:
            #     print("user_select_result is not None")
            #     return {"res_code": "400"}

            with create_httpx_client() as client:

                print("java session 호출")

                response = client.post('http://localhost:18080/VMS_TEST/session', data=json_data,
                                       headers={'Content-Type': 'application/json'})

                print(response)
                response_content = response.content.decode("utf-8")
                response_data = json.loads(response_content)
                res_code = response_data.get("res_code")

                print("res_code " + str(res_code))

                print("session 호출 끝")
                if res_code != 200:
                    return {"res_code": "400"}

                user_create_result = user_crud.insertDB(conn, table=user_table, data=user)
                print("user_create_result : " + str(user_create_result.get("res_code")))
                if user_create_result.get("res_code") != 200:
                    raise HTTPException(status_code=400, detail="User insert failed")

                cam_create_result = user_crud.insertDB(conn, table=cam_table, data=cam)
                print("cam_create_result : " + str(cam_create_result.get("res_code")))
                if cam_create_result.get("res_code") != 200:
                    raise HTTPException(status_code=400, detail="Cam insert failed")

                user_cam_dict = {
                    "USER_CODE": user.USER_CODE,
                    "CAM_CODE": cam.CAM_CODE,
                    "USER_CAM_CODE": user.USER_CODE + str(cam.CAM_CODE)
                }

                user_cam_create_result = user_crud.insertDB(conn, table=user_cam_table, data=user_cam_dict)
                print("user_cam_insert : " + str(user_cam_create_result.get("res_code")))
                if user_cam_create_result.get("res_code") != 200:
                    raise HTTPException(status_code=400, detail="UserCam insert failed")

                trans.commit()

        return {"res_code": 200}

    except Exception as e:
        # 모든 다른 예외에 대한 처리
        print(f"Error during transaction: {e}")
        trans.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        conn.close()


# @user_router.post("/V100/VMS_10001/cam_info_register", response_model=dict)
# def create_user(user_cam: schemas.UserCamCreate, db: Session = Depends(get_db)):
#     try:
#         print(user_cam)
#         # user = user_cam.user
#         # cam = user_cam.cam
#
#         data_to_send = {
#             "user_id": user_cam.USER_ID,
#             "cam_id": user_cam.CAM_ID
#         }
#
#         json_data = json.dumps(data_to_send)
#
#         user_table = models.GigaUser
#         cam_table = models.GigaCam
#         user_cam_table = models.GigaUserCam
#
#         with db.begin() as transaction:
#             user_code = user_cam.USER_CODE
#             user_select_result = user_crud.selectUserCodeDB(engine, table=user_table, user_code=user_code)
#             print("user_select " + str(user_select_result))
#
#             # if user_select_result is not None:
#             #     print("user_select_result is not None")
#             #     return {"res_code": "400"}
#
#             with create_httpx_client() as client:
#
#                 print("java session 호출")
#
#                 response = client.post('http://localhost:18080/VMS_TEST/session', data=json_data,
#                                        headers={'Content-Type': 'application/json'})
#
#                 print(response)
#                 response_content = response.content.decode("utf-8")
#                 response_data = json.loads(response_content)
#                 res_code = response_data.get("res_code")
#
#                 print("res_code " + str(res_code))
#
#                 print("session 호출 끝")
#                 if res_code != 200:
#                     return {"res_code": "400"}
#
#                 user_create_result = user_crud.insertDB(engine, table=user_table, data=user_cam)
#                 print("user_create_result : " + str(user_create_result.get("res_code")))
#                 if user_create_result.get("res_code") != 200:
#                     raise HTTPException(status_code=400, detail="User insert failed")
#
#                 cam_create_result = user_crud.insertDB(engine, table=cam_table, data=user_cam)
#                 print("cam_create_result : " + str(cam_create_result.get("res_code")))
#                 if cam_create_result.get("res_code") != 200:
#                     raise HTTPException(status_code=400, detail="Cam insert failed")
#
#                 user_cam_dict = {
#                     "USER_CODE": user_cam.USER_CODE,
#                     "CAM_CODE": user_cam.CAM_CODE,
#                     "USER_CAM_CODE": user_cam.USER_CODE + str(user_cam.CAM_CODE)
#                 }
#
#                 user_cam_create_result = user_crud.insertDB(engine, table=user_cam_table, data=user_cam_dict)
#                 print("user_cam_insert : " + str(user_cam_create_result.get("res_code")))
#                 if user_cam_create_result.get("res_code") != 200:
#                     raise HTTPException(status_code=400, detail="UserCam insert failed")
#         return {"res_code": 200}
#     except HTTPException as he:
#         # HTTPException은 이미 예외가 발생한 것으로 간주하고 처리
#         print(f"HTTPException: {he}")
#         raise
#
#     except Exception as e:
#         # 모든 다른 예외에 대한 처리
#         print(f"Error during transaction: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


@user_router.post("/gigaeyes/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, user=user)


@user_router.post("/gigaeyes/users/update", response_model=schemas.User)
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return user_crud.update_user(db=db, user=user)


@user_router.post("/users/giga/insert", response_model=dict)
def create_vsm_user(data: schemas.UserCreate):
    table = models.GigaUser()

    return user_crud.insertDB(engine, table, data)


@user_router.get("/users/giga/select", response_model=schemas.User)
def select_vms_user():
    table = models.GigaUser()

    return user_crud.selectAllDB(engine, table)


@user_router.get("/users/giga/select/{user_code}", response_model=schemas.User)
async def select_vms_user(user_code: str):
    table = models.GigaUser()
    return user_crud.selectUserCodeDB(engine, table, user_code)


@user_router.post("/users/giga/select/json", response_model=dict)
async def select_vms_user(request: Request):
    table = models.GigaUser()
    json_data = await request.json()
    print(json_data)
    user_crud.selectJson(engine, table, json_data)

    return json_data


@user_router.put("/users/update/giga", response_model=dict)
def update_vms_user(data: schemas.UserUpdate):
    table = models.GigaUser()
    # db_user = test_crud.get_user_by_email(db, email=data.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")

    return user_crud.updateDB(engine, table, data)


@user_router.delete("/users/delete/giga/", response_model=dict)
def delete_vms_user(data: schemas.UserDelete):
    table = models.GigaUser()
    # db_user = test_crud.get_user_by_email(db, email=data.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")

    return user_crud.deleteUserCodeDB(engine, table, data)
