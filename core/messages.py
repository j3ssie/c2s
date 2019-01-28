import requests

from . import sender
from . import utils

class Messages(object):
    """docstring for MessType"""
    def __init__(self, options):
        self.options = options
        # self.mess = mess

    def keep_alive(self):
        url = "https://slack.com/api/api.test?error=sample"
        pass

    def send_message(self):
        pass

    def send_info(self):
        mess['color'] = '#005b9f'
        mess['icon'] = utils.get_emoji()
        self.send_attachment(mess)


    def send_good(self, mess):
        mess['color'] = '#32cb00'
        mess['icon'] = utils.get_emoji()
        self.send_attachment(mess)


    def send_bad(self):
        mess['color'] = '#c62828'
        mess['icon'] = 'https://emoji.slack-edge.com/TC2BSM362/jemoji3/9d4b76412c4c1e1a.png'
        self.send_attachment(mess)

    def send_file(self, mess):
        with open(mess['filename'], 'r+') as f:
            mess['content'] = f.read()

        self.send_snippet(mess)


    def send_attachment(self, mess):
        url = 'https://slack.com/api/chat.postMessage'
        #config stuff
        token = self.options['sender_token']
        name = self.options['local_name']

        #message stuff
        channel = self.options['status_channel']
        title = mess['title']
        content = mess['content']
        color = mess['color']
        icon = mess['icon']

        #message body
        json_body = {
            "channel": channel,
            "attachments": [
                {
                    "fallback": title,
                    "title": title,
                    "text": content,
                    "footer": name,
                    "color": color,
                    "footer_icon": icon,
                    "ts": utils.get_ts()
                }
            ]
        }

        r = sender.send_JSON(url, token, json_body)


    def send_snippet(self, mess):
        token = self.options['sender_token']
        # name = self.options['local_name']

        #message stuff
        channel = self.options['report_channel']
        title = mess['title']
        filename = mess['filename']
        style = mess['style']
        content = mess['content']

        url = "https://slack.com:443/api/files.upload?channels={0}&title={1}&filename={2}&filetype={3}&pretty=1".format(channel, title, filename, style)

        send_form_boundary(url, token, content)



    def search_message(self):
        burp0_url = "https://slack.com:443/api/search.messages?query=hello%20in:throwaway&pretty=1"
        burp0_headers = {"GET /api/search.messages?query=hello%20in": "hrowaway&pretty=1 HTTP/1.1", "Authorization": "Bearer xoxp-410400717206-408840487860-534088612165-e2154a356026c2869b718b8a15a1e0ee", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close"}
        requests.get(burp0_url, headers=burp0_headers)

