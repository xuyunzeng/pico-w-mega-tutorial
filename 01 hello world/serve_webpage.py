import socket

def serve_webpage():
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
            response = get_html('index.html')
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
            
        except OSError as e:
            cl.close()
            print('Connection closed')
