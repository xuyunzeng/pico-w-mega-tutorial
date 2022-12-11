from wifi import init_wifi
import socket
from machine import Pin
import time

init_wifi()

# ultrasonic sensor pins and functions
trigger = Pin(16, Pin.OUT)
echo = Pin(15, Pin.IN)


def ultrasonic():
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
    return distance

# Function to load in html page


def get_html(html_name, distance):
    # open html_name (index.html), 'r' = read-only as variable 'file'
    with open(html_name, 'r') as file:
        html = file.read()
    content = html.replace(
        "<h2 id=\"ultrasonic\"></h2>", f"<h2 id=\"ultrasonic\">{distance}cm</h2>")

    return content


# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        print(ultrasonic())
        response = get_html('index.html', ultrasonic())
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('Connection closed')
