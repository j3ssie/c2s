import requests, json

from . import sender
from . import utils

class Messages(object):
    """docstring for MessType"""
    def __init__(self, options):
        self.options = options

    def keep_alive(self):
        url = "https://slack.com/api/api.test?error=sample"
        pass

    def send_message(self):
        pass

    def send_info(self, mess):
        mess['color'] = '#005b9f'
        mess['icon'] = utils.get_emoji()
        self.send_attachment(mess)


    def send_good(self, mess):
        mess['color'] = '#32cb00'
        mess['icon'] = utils.get_emoji()
        self.send_attachment(mess)


    def send_bad(self, mess):
        mess['color'] = '#c62828'
        mess['icon'] = 'https://emoji.slack-edge.com/TC2BSM362/jemoji3/9d4b76412c4c1e1a.png'
        self.send_attachment(mess)

    def send_file(self, mess):
        with open(mess['filename'], 'r+') as f:
            mess['content'] = f.read()

        mess['title'] = mess['filename']
        self.send_snippet(mess)



    ######
    ### base sending
    def send_attachment(self, mess):
        url = 'https://slack.com/api/chat.postMessage'
        #config stuff
        token = self.options['sender_token']
        name = self.options['local_name']

        #message stuff
        channel = utils.get_value(mess, 'channel', self.options['status_channel'])

        
        author_name = utils.get_value(mess, 'author_name')
        
        title = mess['title']
        content = mess['content']
        color = mess['color']
        icon = mess['icon']

        #message body
        json_body = {
            "channel": channel,
            "attachments": [
                {
                    "author_name": author_name,
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

        #message stuff
        channel = self.options['report_channel']
        title = mess['title']
        filename = mess['filename']
        style = utils.get_value(mess, 'style', 'plaintext')
        comment = utils.get_value(mess, 'comment', '')
        content = mess['content']

        url = "https://slack.com:443/api/files.upload?channels={0}&title={1}&filename={2}&filetype={3}&initial_comment={4}&pretty=1".format(channel, title, filename, style, comment)

        r = sender.send_form_boundary(url, token, content)






