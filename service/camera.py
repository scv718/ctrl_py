import requests
from requests.auth import HTTPBasicAuth
import cv2


# 카메라 체크 함수
def check_rtsp_connection(camera):
    rtsp_url = f"rtsp://{camera['ADMIN_ID']}:{camera['ADMIN_PWD']}@{camera['PRIVATE_IP']}:{camera['PORT']}/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"

    try:
        # RTSP 스트리밍 테스트
        cap = cv2.VideoCapture(rtsp_url)
        if cap.isOpened():
            print(f"RTSP Streaming  - Success")
        else:
            print(f"RTSP Streaming  - Failed")

        cap.release()

        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


# 카메라 테스트 함수
def test_camera(camera_info):
    for camera in camera_info:
        print("카메라 스타트")
        print(camera)
        # web_url = f"http://{camera['PRIVATE_IP']}:{camera['WEB_PORT']}"
        rtsp_url = f"rtsp://{camera['ADMIN_ID']}:{camera['ADMIN_PWD']}@{camera['PRIVATE_IP']}:{camera['PORT']}/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"

        print(rtsp_url)
        print(f"Testing {camera['WOWZA_INDEX']}...")

        try:
                # RTSP 스트리밍 테스트
            # cap = cv2.VideoCapture(rtsp_url)
            # print(cap.get(cv2.CAP_PROP_BITRATE))
            # print(cap.get(cv2.CAP_PROP_XI_COOLING))
            # print(cap.get(cv2.CAP_PROP_FPS))
            # print(cap)
            # if cap.isOpened():
            #     print(f"RTSP Streaming from WOWZA_INDEX: {camera['WOWZA_INDEX']} - Success")
            #
            #     # RTSP 스트리밍 화면에 표시 (Esc 키를 누를 때까지)
            #     while True:
            #         ret, frame = cap.read()
            #         if not ret:
            #             break
            #         cv2.imshow('RTSP Streaming', frame)
            #
            #         # 'Esc' 키를 누르면 종료
            #         if cv2.waitKey(1) == 27:
            #             break
            #
            #     cap.release()
            #     cv2.destroyAllWindows()
            # else:
            #     print(f"RTSP Streaming from WOWZA_INDEX: {camera['WOWZA_INDEX']} - Failed")
            if check_rtsp_connection(camera):
                return rtsp_url
            else:
                return None

        except Exception as e:
            print(f"Error: {str(e)}")
            return None

# 모든 카메라에 대한 테스트 실행
# for camera in camera_info:
#     test_camera(camera)



# 카메라 정보
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
# def test_camera(camera):
#     web_url = f"http://{camera['ip']}:{camera['web_port']}"
#     rtsp_url = f"rtsp://{camera['username']}:{camera['password']}@{camera['ip']}:{camera['rtsp_port']}/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
#
#     print(f"Testing {camera['name']}...")
#
#     try:
#         # 웹 페이지 접속 테스트
#         response = requests.get(web_url, auth=HTTPBasicAuth(camera['username'], camera['password']))
#
#         print("response code : {}", response.__dict__)
#         if response.status_code == 200:
#             print(f"Web Access to {camera['name']} - Success")
#         else:
#             print(f"Web Access to {camera['name']} - Failed")
#
#
#             # RTSP 스트리밍 테스트
#         cap = cv2.VideoCapture(rtsp_url)
#         print(cap.get(cv2.CAP_PROP_BITRATE))
#         print(cap.get(cv2.CAP_PROP_XI_COOLING))
#         print(cap.get(cv2.CAP_PROP_FPS))
#         print(cap)
#         if cap.isOpened():
#             print(f"RTSP Streaming from {camera['name']} - Success")
#
#             # RTSP 스트리밍 화면에 표시 (Esc 키를 누를 때까지)
#             while True:
#                 ret, frame = cap.read()
#                 if not ret:
#                     break
#                 cv2.imshow('RTSP Streaming', frame)
#
#                 # 'Esc' 키를 누르면 종료
#                 if cv2.waitKey(1) == 27:
#                     break
#
#             cap.release()
#             cv2.destroyAllWindows()
#         else:
#             print(f"RTSP Streaming from {camera['name']} - Failed")
#
#     except Exception as e:
#         print(f"Error: {str(e)}")
#
# # 모든 카메라에 대한 테스트 실행
# for camera in camera_info:
#     test_camera(camera)
