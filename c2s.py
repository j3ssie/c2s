#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, glob
import argparse, configparser
from pprint import pprint

from core import messages

# Console colors
W = '\033[1;0m'   # white 
R = '\033[1;31m'  # red
G = '\033[1;32m'  # green
O = '\033[1;33m'  # orange
B = '\033[1;34m'  # blue
Y = '\033[1;93m'  # yellow
P = '\033[1;35m'  # purple
C = '\033[1;36m'  # cyan
GR = '\033[1;37m'  # gray
colors = [G,R,B,P,C,O,GR]


#############
# C2S - Command and Control server on Slack
#############

__author__ = '@j3ssiejjj'
__version__ = '1.0'


### Global stuff
current_path = os.path.dirname(os.path.realpath(__file__))
###


def cowsay():
    print ("""{1}
      -----------------------------
    < You didn't say the {2}MAGIC WORD{1} >
      ----------------------------- 
             \   ^__^
              \  (oo)\_______
                 (__)\       )\/
                    \||----w |    
                     ||     ||    Contact: {2}{3}{1}
        """.format(C, G, P, __author__))

#the config stuff
options = {
    'user_token' : '',
    'sender_token' : '',
    'local_name' : '',

    'irc_channel' : '',
    'status_channel' : '',
    'report_channel' : '',

}

#skeleton for message body
mess = {
    'title' : '',
    'content' : '',
    'title' : '',
    'filename' : '',
    'style' : '',
}

#
def config_parser(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    options['sender_token'] = config['configs']['sender_token']
    options['local_name'] = config['configs']['local_name']

    options['bots'] = config['bots']['collector']



    #channels stuff
    options['status_channel'] = config['channels']['status']
    options['irc_channel'] = config['channels']['irc']
    options['report_channel'] = config['channels']['report']

def daemon():
    pass

def parsing_argument(args):
    #reading config
    config_file = args.config
    config_parser(config_file)
    print("[+] Loading config from {0}".format(config_file))

    # daemon()
    sm = messages.Messages(options)

    mess['title'] = 'Testing #1'
    mess['content'] = 'fool me'
    sm.send_good(mess)


    mess['filename'] = '/tmp/ibm.txt'
    sm.send_file(mess)





def update():
    pass


def main():
    cowsay()
    parser = argparse.ArgumentParser(description="Comand and Control on Slack")

    parser.add_argument('-c','--config' , action='store', dest='config', help='config file', default='config.conf')
    parser.add_argument('-t','--target' , action='store', dest='target', help='target')
    parser.add_argument('-T','--target_list' , action='store', dest='target_list', help='list of target')
    parser.add_argument('-o','--output' , action='store', dest='output', help='output')
    parser.add_argument('--update', action='store_true', help='update lastest from git')

    args = parser.parse_args()
    # if len(sys.argv) == 1:
    #     # help_message()
    #     sys.exit(0)

    if args.update:
        update()

    parsing_argument(args)



if __name__ == '__main__':
    main()