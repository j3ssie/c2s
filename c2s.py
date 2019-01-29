#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, glob, time
import argparse, configparser
import threading
import queue
import multiprocessing
from pprint import pprint

from core import messages
from core import searching
from core import execute
from core import utils

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
# process_queue = queue.Queue()
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
    'irc_channel_name' : '',
    'status_channel' : '',
    'report_channel' : '',

    'control_bot' : '',

    # 'process_queue' : process_queue
}

#skeleton for message body
mess = {
    'title' : '',
    'content' : '',
    'title' : '',
    'filename' : '',
    'style' : '',
    'comment' : '',
}

#loading config file
def config_parser(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    options['sender_token'] = config['configs']['sender_token']
    options['user_token'] = config['configs']['user_token']
    options['local_name'] = config['configs']['local_name']

    options['control_bot'] = config['bots']['control']

    #channels stuff
    options['status_channel'] = config['channels']['status']
    options['status_channel_name'] = config['channels']['status_name']

    options['irc_channel'] = config['channels']['irc']
    options['irc_channel_name'] = config['channels']['irc_name']

    options['report_channel'] = config['channels']['report']
    options['report_channel_name'] = config['channels']['report_name']


#checking if some command is done or not
def pull_process_queue(pq):
    utils.print_good("Pulling the process queue")

    while True:
        utils.print_info("Process in Queue: {0}".format(str(pq.q.qsize())))
        pq.pop_to_check()
        time.sleep(2)



def pull_irc():
    search = searching.Searching(options)

    ##keep search
    while True:
        utils.print_good("Finding IRC messages")
        search.search_cmd()
        time.sleep(45)


def daemon():
    pq = execute.ProcessQueue(options)
    options['process_queue'] = pq

    #start new thread to get command 
    t = threading.Thread(target=pull_process_queue, args=(pq,))
    t.start()

    #keep search in irc channel to pull a command
    pull_irc()



def parsing_argument(args):
    #reading config
    config_file = args.config
    config_parser(config_file)
    utils.print_good("Loading config from {0}".format(config_file))


    if args.mode:
        mode = args.mode

    if mode == 'daemon':
        daemon()



def update():
    pass


def main():
    cowsay()
    parser = argparse.ArgumentParser(description="Comand and Control on Slack")

    parser.add_argument('-c','--config' , action='store', dest='config', help='config file', default='config.conf')
    parser.add_argument('-m','--mode' , action='store', dest='mode', help='Choose mode to run', default='daemon')

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