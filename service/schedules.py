import json

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import cv2  # OpenCV를 사용하여 RTSP 연결을 체크
from db.database import engine
import service.user_crud as user_crud
import db.gigaeyes_models as models
import atexit
import core.log as common

log = common.logging.getLogger("api")

scheduler = BackgroundScheduler()
scheduler.start()


def check_rtsp_connection():
    table = models.GigaUserCam
    del_flag = {
        "STATUS": "S"
    }
    json_val = json.dumps(del_flag)
    user_cam_infolist = user_crud.selectJson(engine, table, del_flag)
    print(user_cam_infolist)
    for user_cam_info in user_cam_infolist:
        user_cam_code = user_cam_info.get("USER_CODE") + "_" + str(user_cam_info.get("CAM_CODE"))
        wowza_index = {
            "WOWZA_INDEX": user_cam_info.get("WOWZA_INDEX")
        }
        table = models.GigaWowza
        camera_info = user_crud.selectJson(engine, table, wowza_index)

        rtsp_url = f"rtsp://{camera_info[0]['PRIVATE_IP']}:1935/pythongigaeyeslive/{user_cam_code}.stream"
        print(rtsp_url)
        try:
            cap = cv2.VideoCapture(rtsp_url)
            print(cap.get(cv2.CAP_PROP_BITRATE))

            if cap.isOpened():
                print(f"RTSP Streaming  - Success")
                log.info("RTSP Streaming  - Success")
            else:
                log.info("RTSP Streaming  - Failed")

            cap.release()
        except Exception as e:
            print(f"Error: {str(e)}")


# scheduler.add_job(check_rtsp_connection, 'interval', minutes=5)
scheduler.add_job(check_rtsp_connection, 'interval', seconds=60)

# 어플리케이션이 종료될 때 APScheduler도 종료
atexit.register(lambda: scheduler.shutdown())
