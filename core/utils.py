import time
import random
import os

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

info = '{0}[*]{1} '.format(B,GR)
ques =  '{0}[?]{1} '.format(C,GR)
bad = '{0}[-]{1} '.format(R,GR)
good = '{0}[+]{1} '.format(G,GR)
#########

def get_ts():
    return int(time.time())

def get_emoji():
    emojis = [
        'https://emoji.slack-edge.com/TC2BSM362/jemoji1/164b2f1f9acbaeba.png',
        'https://emoji.slack-edge.com/TC2BSM362/jemoji2/d759e0cca7025869.png'
        # ''
    ]
    return random.choice(emojis)


def check_c2_systax(content):
    '''@jmiddler #cmd echo foo #out bar'''
    nid = ''
    out = ''

    if '#cmd' in content:
        if '#out' in content and '#nid' in content:
            cmd = content.split('#cmd ')[1].split(' #out ')[0]
            out = content.split('#cmd ')[1].split(' #out ')[1]
            return cmd, out, nid
            
        if '#out' in content and '#nid' not in content:
            cmd = content.split('#cmd ')[1].split(' #out ')[0]
            out = content.split('#cmd ')[1].split(' #out ')[1]
            return cmd, out, nid
        else:
            cmd = content.split("#cmd ")[1]
            return cmd, out, nid



def print_banner(text):
    print('{1}--~~~=:>[ {2}{0}{1} ]>'.format(text, G, C))

def print_info(text):
    print(info + text)

def print_ques(text):
    print(ques + text)

def print_good(text):
    print(good + text)

def print_bad(text):
    print(bad + text)

def check_output(options, raw_output):
    output = replace_argument(options, raw_output)
    print('{1}--==[ Check the output: {2}{0}'.format(output, G, P))
