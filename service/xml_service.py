import service.xml_read as xml


def profile_list_result(cam_ip, onvif_port):

    try:
        result_profiles = xml.read_xml_file("../core/GetProfiles")

        profiles_response = xml.send_onvif_request(cam_ip, onvif_port, result_profiles, "getProfiles")

        profile_list = xml.test_xml_list(profiles_response.decode('utf-8'))

        result_getprofile = xml.read_xml_file("../core/GetProfile")

        profile_dict = {}

        for profile in profile_list:

            change_profile = xml.profile_xml_change(result_getprofile, profile)

            getprofile_response = xml.send_onvif_request(cam_ip, onvif_port, change_profile, "getProfile")

            result_resolution = xml.resolution_read(getprofile_response.decode('utf-8'))

            if result_resolution.get("width") is None:
                change_profile = xml.ver_change(change_profile)

                getprofile_response = xml.send_onvif_request(cam_ip, onvif_port, change_profile, "getProfile")

                result_resolution = xml.resolution_read(getprofile_response.decode('utf-8'))

            result_url_xml = xml.read_xml_file("../core/GetStreamUri")

            change_uri_profile = xml.profile_xml_change(result_url_xml, profile)

            rtsp_uri_response = xml.send_onvif_request(cam_ip, onvif_port, change_uri_profile, "GetStreamUri")

            rtsp_uri = xml.rtsp_uri_result(rtsp_uri_response.decode('utf-8'))

            profile_dict[profile] = {
                "width": result_resolution.get("width"),
                "rtsp_uri": rtsp_uri
            }
        print(profile_dict)
    except Exception as e:
        print(e)
        return None
    return profile_dict
