import cv2
import schedule
import time

# 카메라 정보
camera = {
    "name": "Hikvision Camera",
    "ip": "121.134.26.70",
    "rtsp_port": 38050,
    "username": "admin",
    "password": "1q2w3e4r!"
}

def check_rtsp_connection():
    rtsp_url = f"rtsp://{camera['username']}:{camera['password']}@{camera['ip']}:{camera['rtsp_port']}/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"

    try:
        # RTSP 스트리밍 테스트
        cap = cv2.VideoCapture(rtsp_url)
        if cap.isOpened():
            print(f"RTSP Streaming from {camera['name']} - Success")
        else:
            print(f"RTSP Streaming from {camera['name']} - Failed")

        cap.release()
    except Exception as e:
        print(f"Error: {str(e)}")

# 5분에 한 번씩 실행되도록 스케줄러 설정
# schedule.every(5).minutes.do(check_rtsp_connection)
schedule.every(5).seconds.do(check_rtsp_connection)

while True:
    schedule.run_pending()
    time.sleep(1)
