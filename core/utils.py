import time
import random

def get_ts():
    return int(time.time())

def get_random_emoji():
    emojis = [
        'https://emoji.slack-edge.com/TC2BSM362/jemoji1/164b2f1f9acbaeba.png',
        'https://emoji.slack-edge.com/TC2BSM362/jemoji2/d759e0cca7025869.png'
        # ''
    ]
    return random.choice(emojis)

def check_c2_systax(content):
    pass