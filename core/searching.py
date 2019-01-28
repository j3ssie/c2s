import requests, json

from . import sender
from . import utils


class Searching():
    """docstring for Searching"""
    def __init__(self, options):
        self.options = options
        
    def search(self, text):
        data = self.search_message(text=text)
        # print(data)


        query = data['query']

        total = data['message']['total']

        if total == 0:
            print("[-] No message matched ...")
            return

        matches = data['message']['matches']

        #found irc message
        for item in matches:
            content = item['text']

            #check if the message was a c2 syntax
            if options['control_bot'] in content:
                utils.check_c2_systax(content)


    #checking in status if there is no bot execute it
    def checking_in_status(self):
        pass


    def custom_search(self,query):
        data = self.search_message(query=query)


    def search_message(self, text='', query=''):
        token = self.options['user_token']
        irc = self.options['irc_channel_name']

        # if query != '' search direct query
        if query == '':
            query = "{0}%20in:{1}".format(text, irc)

        url = "https://slack.com:443/api/search.messages?query={0}&count=100&pretty=1".format(query)
        r = sender.send_GET(url, token)
        if r.status_code == 200:
            data = json.loads(r.text)

        return data