from wifi import init_wifi
import socket
import machine
import time
from constants import *

init_wifi()

# Buzzer
buzzerPIN = 16
BuzzerObj = machine.PWM(machine.Pin(buzzerPIN))


def buzzer(buzzerPinObject, frequency, sound_duration, silence_duration):
    # Set duty cycle to a positive value to emit sound from buzzer
    buzzerPinObject.duty_u16(int(65536*0.2))
    # Set frequency
    buzzerPinObject.freq(frequency)
    # wait for sound duration
    time.sleep(sound_duration)
    # Set duty cycle to zero to stop sound
    buzzerPinObject.duty_u16(int(65536*0))
    # Wait for sound interrumption, if needed
    time.sleep(silence_duration)

# Function to load in html page


def get_html(html_name):
    # open html_name (index.html), 'r' = read-only as variable 'file'
    with open(html_name, 'r') as file:
        html = file.read()

    return html


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

        request = str(request)
        buzzer_on = request.find('?buzzer=on')
        buzzer_off = request.find('?buzzer=off')
        buzzer_scale = request.find('?buzzer=scale')
        buzzer_music = request.find('?buzzer=music')

        if buzzer_on > -1:
            BuzzerObj.duty_u16(int(65536*0.2))
            BuzzerObj.freq(440)

        if buzzer_off > -1:
            BuzzerObj.duty_u16(0)

        if buzzer_scale > -1:
            #C (DO)
            buzzer(BuzzerObj, 523, 0.5, 0.1)

            #D (RE)
            buzzer(BuzzerObj, 587, 0.5, 0.1)

            #E (MI)
            buzzer(BuzzerObj, 659, 0.5, 0.1)

            #F (FA)
            buzzer(BuzzerObj, 698, 0.5, 0.1)

            #G (SOL)
            buzzer(BuzzerObj, 784, 0.5, 0.1)

            #A (LA)
            buzzer(BuzzerObj, 880, 0.5, 0.1)

            #B (SI)
            buzzer(BuzzerObj, 987, 0.5, 0.1)

            BuzzerObj.deinit()

        if buzzer_music > -1:
            pause = 0.01
            # pauses between notes
            t = 0.025
            # time that music note plays

            music_notes = [B4F, B4F, A4F, A4F,
                           F5, F5, E5F, B4F, B4F, A4F, A4F, E5F, E5F, C5S, C5, B4F,
                           C5S, C5S, C5S, C5S,
                           C5S, E5F, C5, B4F, A4F, A4F, A4F, E5F, C5S,
                           B4F, B4F, A4F, A4F,
                           F5, F5, E5F, B4F, B4F, A4F, A4F, A5F, C5, C5S, C5, B4F,
                           C5S, C5S, C5S, C5S,
                           C5S, E5F, C5, B4F, A4F, A4F, A4F, E5F, C5S, C5S]

            rhythm = [1, 1, 1, 1,
                      3, 3, 6, 1, 1, 1, 1, 3, 3, 3, 1, 2,
                      1, 1, 1, 1,
                      3, 3, 3, 1, 2, 2, 2, 4, 8,
                      1, 1, 1, 1,
                      3, 3, 6, 1, 1, 1, 1, 3, 3, 3, 1, 2,
                      1, 1, 1, 1,
                      3, 3, 3, 1, 2, 2, 2, 4, 8, 4]

            for i in range(len(music_notes)):
                buzzer(BuzzerObj, music_notes[i], rhythm[i]*t, pause)

        response = get_html('index.html')
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('Connection closed')
