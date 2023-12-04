import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
import re


def read_xml_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            xml_string = file.read()
        return xml_string
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")


def send_onvif_request(cam_ip, onvif_port, soap_request, response_url):
    url = f"http://{cam_ip}:{onvif_port}/onvif/{response_url}"

    headers = {
        "Content-Type": "application/xml charset=utf-8",
        "Accept": "application/xml charset=utf-8"
    }

    soap_request_with_header = f'<?xml version="1.0" encoding="utf-8"?>\n{soap_request}'

    response = requests.post(url, headers=headers, data=soap_request_with_header,
                             auth=HTTPDigestAuth('admin', '1q2w3e4r!@'))

    return response.content


def parse_xml_response(xml_response, namespace, element_name):
    try:
        root = ET.fromstring(xml_response)
        # 네임스페이스를 고려하여 특정 요소 찾기
        element = root.find('.//{}{}'.format(namespace, element_name))
        if element is not None:
            return element.text
        else:
            print(f"Error: Element '{element_name}' not found in the XML response.")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"Error: {e}")


def profile_xml_change(xml_response, token):
    root = ET.fromstring(xml_response)

    profile_token_element = root.find(".//{http://www.onvif.org/ver10/media/wsdl}ProfileToken")
    profile_token_element.text = token

    modified_xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')

    return modified_xml_string


def extract_name(xml_response):
    try:
        root = ET.fromstring(xml_response)
        # 네임스페이스를 지정하여 "tt:Name" 요소 찾기
        namespace = {'tt': 'http://www.onvif.org/ver20/schema'}
        name_element = root.find('.//token', namespace)
        if name_element is not None:
            return name_element.text
        else:
            print("Error: Element 'Name' not found in the XML response.")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"Error: {e}")


def extract_name2(xml_response):
    try:
        root = ET.fromstring(xml_response)
        # 네임스페이스를 무시하고 모든 "Name" 요소 찾기
        name_elements = root.findall('.//Name')
        if name_elements:
            # 첫 번째 "Name" 요소의 텍스트 반환
            return name_elements[0].text
        else:
            print("Error: Element 'Name' not found in the XML response.")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"Error: {e}")


def test_xml(xml_response):
    root = ET.fromstring(xml_response)

    # Find the Profiles element and get the value of the 'token' attribute
    profiles_element = root.find(".//tr2:Profiles[@token='MediaProfile000']",
                                 namespaces={'tr2': 'http://www.onvif.org/ver20/media/wsdl'})
    print(profiles_element)
    if profiles_element is not None:
        token_value = profiles_element.get('token')
        print(token_value)
    else:
        print("Profiles element not found in the XML.")


def test_xml_list(xml_response):
    root = ET.fromstring(xml_response)

    profile_elements = root.findall(".//tr2:Profiles", namespaces={'tr2': 'http://www.onvif.org/ver20/media/wsdl'})

    token_values = [profile.get('token') for profile in profile_elements]

    return token_values


def resolution_read(xml_response):
    root = ET.fromstring(xml_response)

    encoding_element = root.find(".//tt:Encoding", namespaces={'tt': 'http://www.onvif.org/ver10/schema'})
    resolution_element = root.find(".//tt:Resolution", namespaces={'tt': 'http://www.onvif.org/ver10/schema'})

    encoding_value = encoding_element.text if encoding_element is not None else None
    resolution_width = resolution_element.find(".//tt:Width", namespaces={
        'tt': 'http://www.onvif.org/ver10/schema'}).text if resolution_element is not None else None
    resolution_height = resolution_element.find(".//tt:Height", namespaces={
        'tt': 'http://www.onvif.org/ver10/schema'}).text if resolution_element is not None else None

    print("Encoding:", encoding_value)
    print("Resolution Width:", resolution_width)
    print("Resolution Height:", resolution_height)

    result_dict = {
        'width': resolution_width,
        'height': resolution_height,
        'encoding': encoding_value
    }

    return result_dict


def ver_change(xml_string):
    # XML 파싱
    root = ET.fromstring(xml_string)

    get_profile_element = root.find(".//{http://www.onvif.org/ver10/media/wsdl}GetProfile")

    get_profile_element.tag = "{http://www.onvif.org/ver20/media/wsdl}GetVideoEncoderConfigurations"

    get_profile_element.attrib["xmlns"] = "http://www.onvif.org/ver20/media/wsdl"

    modified_xml_string = ET.tostring(root).decode()

    return modified_xml_string


def rtsp_uri_result(xml_string):
    root = ET.fromstring(xml_string)

    rtsp_address = root.find('.//{http://www.onvif.org/ver10/schema}Uri').text

    print(rtsp_address)

    new_port = 38050
    new_rtsp_address = re.sub(r'rtsp://([^:/]+):\d+', rf'rtsp://admin:1q2w3e4r!@\1:{new_port}', rtsp_address)
    # new_rtsp_address = f"rtsp://admin:1q2w3e4r!@{rtsp_address.split('/')[2]}:38050{rtsp_address.split(':554')[1]}"

    return new_rtsp_address
