from wifi import init_wifi
import socket
import machine
import time

init_wifi()

#LED controls
red_led = machine.PWM(machine.Pin(15))
green_led = machine.PWM(machine.Pin(17))
blue_led = machine.PWM(machine.Pin(16))

#Function to load in html page    
def get_html(html_name):
    # open html_name (index.html), 'r' = read-only as variable 'file'
    with open(html_name, 'r') as file:
        html = file.read()
    return html

def find_intensity(color, request_str):
    index = request_str.find(color) + len(color)
    offset = 0
    if request_str[index].isdigit():
        offset = 1
        if request_str[index+1].isdigit():
            offset = 2
            if request_str[index+2].isdigit():
                offset = 3

    intensity = int(request_str[index:index+offset])
    return intensity
    
    
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
        
        request_str = str(request)
        
        #find intensity ONLY if the params exist in request
        if request_str.find('red') > -1 :
            #int = get rid of decimal
            #/100*65534 = find_intensity returns something 0 to 100
            # so x/100 = proportion of 65534 that you want to send to light
            # 65534 = max number you can use for PWM
            red_intensity = int(find_intensity('red=', request_str) /100 * 65534)
            green_intensity = int(find_intensity('green=', request_str) /100 * 65534)
            blue_intensity = int(find_intensity('blue=', request_str) /100 * 65534)
            
            #print('r=' + str(red_intensity))
            #print('g=' + str(green_intensity))
            #print('b=' + str(blue_intensity))
            
            red_led.duty_u16(red_intensity)
            green_led.duty_u16(green_intensity)
            blue_led.duty_u16(blue_intensity)
                        
        response = get_html('index.html')
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('Connection closed')
