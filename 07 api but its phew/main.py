from wifi import init_wifi
from phew import server
from phew.template import render_template
from machine import Pin
import time

init_wifi()

# ultrasonic sensor pins and functions
trigger = Pin(16, Pin.OUT)
echo = Pin(15, Pin.IN)


# Function to load in html page

@server.route("/data", methods=["GET"])
def ultrasonic(request):
    trigger.low()
    time.sleep_us(1)
    trigger.high()
    time.sleep_us(10)
    trigger.low()
    while echo.value() == 0:
        signaloff = time.ticks_us()
    while echo.value() == 1:
        signalon = time.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0340) / 2
    return str(distance), 200


@server.catchall()
def catchall(request):
    return render_template("index.html")


server.run()
