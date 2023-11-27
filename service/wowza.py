import subprocess

# Wowza Streaming Engine에서 제공하는 RTMP 스트림 주소
wowza_stream_url = "http://192.168.1.79:8087/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/pythongigaeyeslive/streamfiles"

# RTSP 카메라의 주소
rtsp_camera_url = "rtsp://admin:1q2w3e4r!@121.134.26.70:38050/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"


def start_wowza_streaming():
    # ffmpeg을 사용하여 RTSP 카메라의 영상을 Wowza Streaming Engine으로 전송
    subprocess.run([
        "ffmpeg",
        "-rtsp_transport", "tcp",
        "-i", rtsp_camera_url,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-b:v", "2500k",
        "-bufsize", "512k",
        "-maxrate", "2500k",
        "-pix_fmt", "yuv420p",
        "-g", "60",
        "-c:a", "aac",
        "-b:a", "160k",
        "-ac", "2",
        "-ar", "44100",
        "-f", "flv",
        wowza_stream_url
    ])


def main():
    # RTSP 카메라의 영상을 Wowza Streaming Engine으로 전송 시작
    start_wowza_streaming()


if __name__ == "__main__":
    main()
