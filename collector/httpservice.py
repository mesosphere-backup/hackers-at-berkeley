#!/usr/bin/env python

from cgi import parse_header
from getopt import getopt
from kafka.producer import SimpleProducer
import sys
from urlparse import parse_qs
from SocketServer import TCPServer
from BaseHTTPServer import BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    """This HTTP handler prints out the contents of HTTP POST events
    received at the given port.
    """

    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'application/x-www-form-urlencoded':
            print('application')
            length = int(self.headers['content-length'])
            postvars = parse_qs(self.rfile.read(length), 
                                keep_blank_values=1)
        else:
            print('NOTE: Unexpected content type.')
            postvars = {}
        return postvars

    def do_POST(self):
        postvars = self.parse_POST()
        self.send_response(200)
        print(postvars)

def usage():
    print('Usage: httpservice.py [-p <port=8080>]')
    sys.exit(0)


if __name__ == '__main__':

    PORT = 8080

    opts, args = getopt(sys.argv[1:], 'hp:')
    for o, a in opts:
        if o == '-p':
            PORT = int(a)
        if o == '-h':
            usage()

    httpd = TCPServer(('', PORT), Handler)
    print('Listening on port ' + str(PORT) + '...')
    httpd.serve_forever()

