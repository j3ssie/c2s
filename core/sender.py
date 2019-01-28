'''
Sending HTTP stuff
'''
import requests

def send_GET(url, token):
    headers = {"Authorization": "Bearer " + token, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close"}

    r = requests.get(url, headers=headers)
    return r

def send_POST(url, token, json):
    url = "https://slack.com:443/api/chat.postMessage"
    headers = {"Accept": "*/*", "Authorization": "Bearer " + token, "Content-type": "application/json", "Connection": "close"}

    requests.post(url, headers=headers, json=json)


def send_JSON(url, token, json_body):
    headers = {"Accept": "*/*", "Authorization": "Bearer " + token, "Content-type": "application/json", "Connection": "close"}
    r = requests.post(url, headers=headers, json=json_body)
    return r

def send_form_boundary(url, token, content):
    headers = {"Authorization": "Bearer " + token, "Connection": "close", "Accept": "*/*", "Origin": "https://api.slack.com", "User-Agent": "C2S v1.0", "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary15cPP1sBX8XrBrjn", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9,vi;q=0.8"}

    data="------WebKitFormBoundary15cPP1sBX8XrBrjn\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + content + "\r\n------WebKitFormBoundary15cPP1sBX8XrBrjn--\r\n"

    r = requests.post(url, headers=headers, data=data)
    return r


