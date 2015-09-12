#!/usr/bin/env python

import cgi
import getopt
import sys
import urlparse
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    """This HTTP handler prints out the contents of HTTP POST events
    received at the given port.
    """

    def parse_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'application/x-www-form-urlencoded':
            print('application')
            length = int(self.headers['content-length'])
            postvars = urlparse.parse_qs(self.rfile.read(length), 
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

    opts, args = getopt.getopt(sys.argv[1:], 'hp:')
    for o, a in opts:
        if o == '-p':
            PORT = int(a)
        if o == '-h':
            usage()

    httpd = SocketServer.TCPServer(('', PORT), Handler)
    httpd.serve_forever()

    print('Listening on port ' + str(PORT) + '...')

