from machine import Pin
from wifi import init_wifi
import urequests
import ujson
import dht
import time

init_wifi()

dht22 = dht.DHT22(Pin(16))


def send_data():
    # tell dht22 to take a reading
    dht22.measure()
    # find temp & humidity data and then jsonify data.
    dht_data = {'value1': str(dht22.temperature()),
                'value2': str(dht22.humidity())}
    post_data = ujson.dumps(dht_data)
    request_url = 'https://maker.ifttt.com/trigger/dht22/with/key/[your-key-here]'
    res = urequests.post(request_url, headers={
                         'content-type': 'application/json'}, data=post_data)
    # log response from IFTTT.
    print(res.text)
    # sleep for a minute before running send_data again
    time.sleep(1*60)
    send_data()


try:
    send_data()
except Exception as e:
    print(e)
    request_url = 'https://maker.ifttt.com/trigger/error/with/key/[your-key-here]'
    post_data = ujson.dumps({"value1": str(e)})
    urequests.post(request_url, headers={
        'content-type': 'application/json'}, data=post_data)
