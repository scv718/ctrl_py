import requests
from requests.auth import HTTPBasicAuth
import cv2


# camera_info = [
#     {
#         "name": "Camera1",
#         "ip": "121.134.26.70",
#         "web_port": 38080,
#         "rtsp_port": 38050,
#         "username": "admin",  # 사용자 이름
#         "password": "1q2w3e4r!"  # 암호
#     },
#     {
#         "name": "Camera2",
#         "ip": "121.134.26.70",
#         "web_port": 38081,
#         "rtsp_port": 38051,
#         "username": "admin",  # 사용자 이름
#         "password": "1q2w3e4r!"  # 암호
#     },
# ]


# 카메라 테스트 함수
def test_camera(wowza_data, user_cam_code):
    rtsp_url = f'rtsp://{wowza_data[0].get("PUBLIC_IP")}:1935/pythongigaeyeslive/{user_cam_code}.stream'

    print(rtsp_url)
    try:

        cap = cv2.VideoCapture(rtsp_url)
        # print(cap.get(cv2.CAP_PROP_BITRATE))
        # print(cap.get(cv2.CAP_PROP_XI_COOLING))
        # print(cap.get(cv2.CAP_PROP_FPS))
        # print(cap)
        if cap.isOpened():
            print(f"RTSP Streaming - Success")

            # RTSP 스트리밍 화면에 표시 (Esc 키를 누를 때까지)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow('RTSP Streaming', frame)

                # 'Esc' 키를 누르면 종료
                if cv2.waitKey(1) == 27:
                    break

            cap.release()
            cv2.destroyAllWindows()

            return {"res_code": "200", "url": rtsp_url}
        else:
            print(f"RTSP Streaming - Failed")

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

    return {"res_code": "400"}
