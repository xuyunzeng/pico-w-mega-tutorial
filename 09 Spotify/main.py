from machine import Pin
from wifi import init_wifi
import urequests
import time

init_wifi()

play_btn = Pin(16, Pin.IN, Pin.PULL_DOWN)
pause_btn = Pin(2, Pin.IN, Pin.PULL_DOWN)
skip_btn = Pin(15, Pin.IN, Pin.PULL_DOWN)


def play():
    request_url = 'https://maker.ifttt.com/trigger/spotify_play/with/key/[your_key_here]'
    res = urequests.post(request_url)
    # print response from IFTTT.
    print(res.text)


def pause():
    request_url = 'https://maker.ifttt.com/trigger/spotify_pause/with/key/[your_key_here]'
    res = urequests.post(request_url)
    # print response from IFTTT.
    print(res.text)


def skip():
    request_url = 'https://maker.ifttt.com/trigger/spotify_skip/with/key/[your_key_here]'
    res = urequests.post(request_url)
    # print response from IFTTT.
    print(res.text)


try:
    while True:
        if play_btn():
            print('play btn')
            play()
            time.sleep(0.25)
        if pause_btn():
            print('pause btn')
            pause()
            time.sleep(0.25)
        if skip_btn():
            skip()
            print('skip')
            time.sleep(0.25)

except Exception as e:
    print(e)
    request_url = 'https://maker.ifttt.com/trigger/error/with/key/[your_key_here]'
    post_data = ujson.dumps({"value1": str(e)})
    urequests.post(request_url, headers={
        'content-type': 'application/json'}, data=post_data)
