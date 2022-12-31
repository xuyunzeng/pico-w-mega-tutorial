from machine import Pin, ADC
from wifi import init_wifi
import time
from umqtt.simple import MQTTClient

init_wifi()

photoresistor = ADC(Pin(26))


def readLight():
    light = photoresistor.read_u16()
    return light


# Connect MQTT

def connectMQTT():
    client = MQTTClient(client_id=b"[your client id here]",
                        server=b"[your address here]",
                        port=0,
                        user=b"[your user here]",
                        password=b"[your pw here]",
                        keepalive=7200,
                        ssl=True,
                        ssl_params={
                            'server_hostname': '[your address here]'}
                        )

    client.connect()
    return client


client = connectMQTT()


def publish(topic, value):
    print(topic)
    print(value)
    client.publish(topic, value)
    print("data published")


while True:
    brightness = str(readLight())  # to publish, must send string

    print(brightness)

    publish('picow/brightness', brightness)

    time.sleep(0.1)
