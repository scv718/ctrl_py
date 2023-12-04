import core.config_yaml_read as config
import requests


class Wowza:
    def __init__(self, db_data):
        self.cam_ip = str(db_data.get("PRIVATE_IP"))
        self.onvif_port = str(db_data.get("ONVIF_PORT"))
        self.wowza_ip = str(db_data.get("PUBLIC_IP"))
        self.port = str(db_data.get("PORT"))
        self.stream_file_name = db_data.get("STREAM_FILE_NAME")
        self.db_data = db_data

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        self.auth = requests.auth.HTTPDigestAuth(config.WOWZA_CONFIG['wowza_id'], config.WOWZA_CONFIG['wowza_password'])

    def __settype__(self, width):
        if int(width) == 1920:
            self.live_type = self.db_data.get("APP_NAME_LIVE")
        elif int(width) == 352:
            self.live_type = self.db_data.get("APP_NAME_CIF")
        else:
            self.live_type = self.db_data.get("APP_NAME_MONITOR")


    def update_stream_file(self, rtsp_uri):
        # url = f"http://192.168.1.79:8087/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/{live_type}/streamfiles/{stream_file_name}/adv"
        url = config.WOWZA_CONFIG['stream_file_update'].format(ip=self.wowza_ip, port=self.port,
                                                               live_type=self.live_type,
                                                               stream_file_name=self.stream_file_name)
        data = {
            "restURI": config.WOWZA_CONFIG['stream_file_update'].format(ip=self.wowza_ip, port=self.port,
                                                                        live_type=self.live_type,
                                                                        stream_file_name=self.stream_file_name),
            "advancedSettings": [
                {
                    "enabled": True,
                    "canRemove": True,
                    "name": "uri",
                    "value": f"{rtsp_uri}",
                    "type": "String",
                    "sectionName": "Common",
                    "documented": True
                },
                {
                    "enabled": True,
                    "canRemove": True,
                    "name": "rtspFilterUnknownTracks",
                    "value": "true",
                    "defaultValue": "false",
                    "type": "Boolean",
                    "sectionName": "RTSP",
                    "documented": True
                },
                {
                    "enabled": True,
                    "canRemove": True,
                    "name": "rtpTransportMode",
                    "value": "tcp",
                    "defaultValue": "udp",
                    "type": "String",
                    "sectionName": "RTSP",
                    "documented": True
                },
                {
                    "enabled": True,
                    "canRemove": True,
                    "name": "rtspStreamAudioTrack",
                    "value": "false",
                    "defaultValue": "false",
                    "type": "Boolean",
                    "sectionName": "RTSP",
                    "documented": True
                }
            ]
        }

        requests.put(url, json=data, headers=self.headers, auth=self.auth)

    def connect_stream(self):

        url = config.WOWZA_CONFIG['stream_connect'].format(ip=self.wowza_ip, port=self.port, live_type=self.live_type,
                                                              stream_file_name=self.stream_file_name)
        print(url)
        requests.put(url, json=None, headers=self.headers, auth=self.auth)

    def create_stream_file(self):

        # url = f'http://192.168.1.79:8087/v2/servers/_defaultServer_/vhosts/_defaultVHost_/applications/{live_type}/streamfiles/{stream_file_name}'
        url = config.WOWZA_CONFIG['stream_file_profile'].format(ip=self.wowza_ip, port=self.port, live_type=self.live_type,
                                                                stream_file_name=self.stream_file_name)

        data = {
            "restURI": config.WOWZA_CONFIG['stream_file'].format(ip=self.wowza_ip, port=self.port, live_type=self.live_type),
            "streamFiles": [
                {
                    "id": f"connectAppName={self.live_type}&appInstance=_definst_&mediaCasterType=rtp",
                    "href": config.WOWZA_CONFIG['stream_file_current'].format(ip=self.wowza_ip, port=self.port,
                                                                              live_type=self.live_type)
                }
            ]
        }

        requests.post(url, json=data, headers=self.headers, auth=self.auth)
