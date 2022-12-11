import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
from secrets import secrets


def init_wifi():
    # Set country to avoid possible errors
    rp2.country('DE')

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Load login data from different file for safety reasons
    ssid = secrets['ssid']
    pw = secrets['pw']

    wlan.connect(ssid, pw)

    # Wait for connection with 10 second timeout
    timeout = 10
    while timeout > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        timeout -= 1
        print('Waiting for connection...')
        time.sleep(1)

    # Define blinking function for onboard LED to indicate error codes    
    def blink_onboard_led(num_blinks):
        led = machine.Pin('LED', machine.Pin.OUT)
        for i in range(num_blinks):
            led.on()
            time.sleep(.2)
            led.off()
            time.sleep(.2)

    wlan_status = wlan.status()
    blink_onboard_led(wlan_status)

    if wlan_status != 3:
        raise RuntimeError('Wi-Fi connection failed')
    else:
        print('Connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])
