import db.gigaeyes_models as models
import db.gigaeyes_schema as schemas
from core.rest_httpx import create_httpx_client, send_data
import service.camera as camera
import service.user_crud as user_crud
import json
import requests
from db.database import SessionLocal, engine
from fastapi import HTTPException


def cam_info_register(user_cam):
    user = user_cam.user
    cam = user_cam.cam
    user_cam_code = user.USER_CODE + "_" + str(cam.CAM_CODE)

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
        cam_code = cam.CAM_CODE
        user_select_result = user_crud.selectUserCodeDB(conn, table=user_cam_table, user_code=user_code,
                                                        cam_code=cam_code)
        if user_select_result:
            print("user_select_result : ", user_select_result)
            return {"res_code": 991}

        with create_httpx_client() as client:

            # print("java session 호출")
            #
            # response = client.post('http://192.168.1.79:8443/test1', data=json_data,
            #                        headers={'Content-Type': 'application/json'})
            #
            # print(response)
            # response_content = response.content.decode("utf-8")
            # response_data = json.loads(response_content)
            # res_code = response_data.get("res_code")
            #
            # print("res_code " + str(res_code))
            #
            # print("session 호출 끝")
            # if res_code != 200:
            #     return {"res_code": "400"}

            user_create_result = user_crud.insert_user_cam_info(conn, table=user_table, data=user)
            print("user_create_result : " + str(user_create_result.get("res_code")))
            if user_create_result.get("res_code") != 200:
                raise HTTPException(status_code=400, detail="User insert failed")

            cam_create_result = user_crud.insert_user_cam_info(conn, table=cam_table, data=cam)
            print("cam_create_result : " + str(cam_create_result.get("res_code")))
            if cam_create_result.get("res_code") != 200:
                raise HTTPException(status_code=400, detail="Cam insert failed")

            user_cam_dict = {
                "USER_CODE": user.USER_CODE,
                "CAM_CODE": cam.CAM_CODE,
                "USER_CAM_CODE": user.USER_CODE + str(cam.CAM_CODE),
                "WOWZA_INDEX": 1
            }

            user_cam_create_result = user_crud.insert_user_cam_info(conn, table=user_cam_table, data=user_cam_dict)
            print("user_cam_insert : " + str(user_cam_create_result.get("res_code")))
            if user_cam_create_result.get("res_code") != 200:
                raise HTTPException(status_code=400, detail="UserCam insert failed")

            wowza_table = models.GigaWowza
            wowza_dict = {
                "WOWZA_INDEX": str(1)
            }

            wowza_status = user_crud.selectJson(engine, wowza_table, wowza_dict)

            wowza_status[0]['STREAM_FILE_NAME'] = user.USER_CODE + "_" + str(cam.CAM_CODE)

            trans.commit()

            return {"res_code": "200", "data": wowza_status[0]}
