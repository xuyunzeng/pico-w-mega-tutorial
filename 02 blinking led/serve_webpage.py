import socket
import machine
import time

def serve_webpage():
    
    #LED controls
    led = machine.Pin(2, machine.Pin.OUT)
          
    def blink_led():
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)
    
    #Function to load in html page    
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
            r = cl.recv(1024)
            print(r)
            
            r = str(r)
            led_on = r.find('?led=on')
            led_off = r.find('?led=off')
            led_blink = r.find('?led=blink')
            print('led_on = ', led_on)
            print('led_off = ', led_off)
            print('led_blink = ', led_blink)
            if led_on > -1:
                print('LED ON')
                led.on()
                
            if led_off > -1:
                print('LED OFF')
                led.off()
                
            if led_blink > -1:
                print('LED BLINK')
                blink_led()
                
            response = get_html('index.html')
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
            
        except OSError as e:
            cl.close()
            print('Connection closed')
