#!/usr/bin/env python3
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
import sys
from requests import get
import base64
import threading

def getCodedIp():
 c=get('https://api.ipify.org').text
 a=c.split('.')
 c=b''
 for i in range(len(a)):
  d=int(a[i])
  c+=bytearray([int(d)])
 c=base64.b85encode(c).decode()
 return c
def getInfo():
 f = open('/sys/class/power_supply/BAT0/capacity')
 ac = open('/sys/class/power_supply/AC0/online')
 a = f.read()
 b = ac.read()
 f.close()
 ac.close()
 b=str(int(b))
 b=b.replace('0','-').replace('1','+')
 a=str(int(a))
 c=getCodedIp()
 a='0'+a
 return a[-2]+b+a[-1]+'@'+c


class MyHandler(SimpleHTTPRequestHandler, object):
    def __init__(s, request, client_address, server):
        s.server_version = 'Apache2'
        s.sys_version = 'Windows'
        super(MyHandler, s).__init__(request, client_address, server)
    def do_HEAD(s):
        print(s.headers)
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def dwrite(s, w):
        s.wfile.write(str(w).encode())
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        info = getInfo()
        s.dwrite("<html><head><title>Nircek drozgju 653 on onion</title></head>")
        s.dwrite("<body><p>Server is running("+info+")</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.dwrite("<p>No document at %s</p>" % s.path)
        s.dwrite("</body></html>")

def function(port):
    server_class = HTTPServer
    httpd = server_class(('', port), MyHandler)
    print('Server starts at', port)
    httpd.serve_forever()
    httpd.server_close()
    print('Server stops at', port)

if __name__ == '__main__':
    for p in [8080, 8081]:
        t = threading.Thread(target=function, args=[p])
        t.deamon = True
        t.start()
