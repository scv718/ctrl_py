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
    table = models.GigaWowza
    camera_info = user_crud.selectAllDB(engine, table)
    table = models.GigaUserCam
    user_cam_info = user_crud.selectAllDB(engine, table)
    usercamcode = user_cam_info.get("USER_CODE")+"_"+user_cam_info.get("CAM_CODE")
    for camera in camera_info:
        rtsp_url = f"rtsp://{camera['PRIVATE_IP']}:1935/gigaeyeslive/{usercamcode}.stream"
        print(rtsp_url)
        try:
            # RTSP 스트리밍 테스트
            cap = cv2.VideoCapture(rtsp_url)
            if cap.isOpened():
                print(f"RTSP Streaming  - Success")
                log.info("RTSP Streaming  - Success")
            else:
                log.info("RTSP Streaming  - Failed")

            cap.release()
        except Exception as e:
            print(f"Error: {str(e)}")


# scheduler.add_job(check_rtsp_connection, 'interval', minutes=5)
scheduler.add_job(check_rtsp_connection, 'interval', seconds=20)

# 어플리케이션이 종료될 때 APScheduler도 종료
atexit.register(lambda: scheduler.shutdown())
