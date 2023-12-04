import requests
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session
import db.gigaeyes_models as models
import db.gigaeyes_schema as schemas
import service.test_camera as camera
import service.user_crud as user_crud
from db.database import SessionLocal, engine
import service.xml_read as xml
import service.cam_register as cam_register
import service.xml_service as xml_result
import core.config_yaml_read as config
from service.wowza_service import Wowza

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

    table = models.GigaUserCam()
    select_user_cam_data = user_crud.selectJson(engine, table, json_data)

    print(select_user_cam_data)
    # if select_user_data and select_cam_data:
    if select_user_cam_data:
        first_row = select_user_cam_data[0]
        user_cam_code = select_user_cam_data[0].get("USER_CODE") + "_" + str(select_user_cam_data[0].get("CAM_CODE"))
        wowza_index = first_row.get('WOWZA_INDEX')
        wowza_dict = {
            "WOWZA_INDEX": wowza_index
        }
        print(wowza_index)
        table = models.GigaWowza()
        wowza_data = user_crud.selectJson(engine, table, wowza_dict)

        print("wowza_data : ", wowza_data)

        url = camera.test_camera(wowza_data, user_cam_code)

        print(url)

        if url.get("res_code") == "200":
            return {"res_code": 200, "data": {"url": url.get("url")}}
        else:
            return {"res_code": 911}
    else:
        print("No data available.")
        return {"res_code": 400}


@user_router.post("/V100/VMS_10001/cam_info_register", response_model=dict)
def create_user(user_cam: schemas.UserCamCreate):
    try:
        db_result = cam_register.cam_info_register(user_cam)

        res_code = db_result.get("res_code")

        if res_code != "200":
            return db_result

        db_data = db_result.get("data")

        wowza_instance = Wowza(db_data)

        cam_ip = str(db_data.get("PRIVATE_IP"))
        onvif_port = str(db_data.get("ONVIF_PORT"))

        result_list = xml_result.profile_list_result(cam_ip, onvif_port)

        if result_list is None:
            print("Data is None")
            raise HTTPException(status_code=400, detail="Data is None")

        for profile_name, profile_data in result_list.items():
            result_resolution = profile_data.get("width")
            rtsp_uri = profile_data.get("rtsp_uri")

            wowza_instance.__settype__(int(result_resolution))

            wowza_instance.create_stream_file()

            wowza_instance.update_stream_file(rtsp_uri)

            if wowza_instance.live_type == "pythongigaeyeslive":
                wowza_instance.connect_stream()

            # url = f'http://192.168.1.79:8087/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/{live_type}/streamfiles/{stream_file_name}'
            # url = config.WOWZA_CONFIG['stream_file_profile'].format(ip=wowza_ip,port=port,live_type=live_type, stream_file_name=stream_file_name)
            #
            # headers = {
            #     "Accept": "application/json",
            #     "Content-Type": "application/json"
            # }
            #
            # data = {
            #     "restURI": config.WOWZA_CONFIG['stream_file'].format(ip=wowza_ip,port=port,live_type=live_type),
            #     "streamFiles": [
            #         {
            #             "id": "connectAppName=demo&appInstance=_definst_&mediaCasterType=rtp",
            #             "href": config.WOWZA_CONFIG['stream_file_current'].format(ip=wowza_ip,port=port,live_type=live_type)
            #         }
            #     ]
            # }
            #
            # auth = requests.auth.HTTPDigestAuth(config.WOWZA_CONFIG['wowza_id'], config.WOWZA_CONFIG['wowza_password'])
            #
            # requests.post(url, json=data, headers=headers, auth=auth)
            #
            # # url = f"http://192.168.1.79:8087/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/{live_type}/streamfiles/{stream_file_name}/adv"
            # url = config.WOWZA_CONFIG['stream_file_update'].format(ip=wowza_ip,port=port,live_type=live_type, stream_file_name=stream_file_name)
            # data = {
            #     "restURI": config.WOWZA_CONFIG['stream_file_update'].format(ip=wowza_ip,port=port,live_type=live_type, stream_file_name=stream_file_name),
            #     "advancedSettings": [
            #         {
            #             "enabled": True,
            #             "canRemove": True,
            #             "name": "uri",
            #             "value": f"{rtsp_uri}",
            #             "type": "String",
            #             "sectionName": "Common",
            #             "documented": True
            #         },
            #         {
            #             "enabled": True,
            #             "canRemove": True,
            #             "name": "rtspFilterUnknownTracks",
            #             "value": "true",
            #             "defaultValue": "false",
            #             "type": "Boolean",
            #             "sectionName": "RTSP",
            #             "documented": True
            #         },
            #         {
            #             "enabled": True,
            #             "canRemove": True,
            #             "name": "rtpTransportMode",
            #             "value": "tcp",
            #             "defaultValue": "udp",
            #             "type": "String",
            #             "sectionName": "RTSP",
            #             "documented": True
            #         },
            #         {
            #             "enabled": True,
            #             "canRemove": True,
            #             "name": "rtspStreamAudioTrack",
            #             "value": "false",
            #             "defaultValue": "false",
            #             "type": "Boolean",
            #             "sectionName": "RTSP",
            #             "documented": True
            #         }
            #     ]
            # }
            #
            # response = requests.put(url, json=data, headers=headers, auth=auth)
            #
            # if live_type == "pythongigaeyeslive":
            #     url = config.WOWZA_CONFIG['stream_connect'].format(ip=wowza_ip,port=port,live_type=live_type, stream_file_name=stream_file_name)
            #     requests.put(url, json=data, headers=headers, auth=auth)

        return {"res_code": 200}

    except Exception as e:
        print(f"Error during transaction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@user_router.post("/gigaeyes/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, user=user)


@user_router.post("/gigaeyes/users/update", response_model=schemas.User)
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return user_crud.update_user(db=db, user=user)


@user_router.post("/users/giga/insert", response_model=dict)
def create_vsm_user(data: schemas.UserCreate):
    table = models.GigaUser()

    return user_crud.insert(engine, table, data)


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
