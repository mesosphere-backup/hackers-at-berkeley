#!/usr/bin/env python

import alsaaudio
import array
import atexit
import datetime
import getopt
import httplib
import math
import sys
import time
import urllib

def cleanup(http_connection):
    http_connection.close()

def rms(buffer):
    """Calculate the root-mean-square of some iterable full of numbers."""
    total = 0.
    for el in buffer:
        total += el**2
    return int(math.sqrt(total))

def usage():
    print('Usage: splmeter.py [-c <soundcard>] [-i <IP address=127.0.0.1>] '
          '[-p <port=8080>] [-n <packet size=100>]')
    sys.exit(0)


if __name__ == '__main__':

    soundcard = 'default'

    # These parameters can be set at the command line:
    # The number of volume measurements in each HTTP POST request.
    PACKET_SIZE = 100
    # The IP address to send measurements to, as a 4-tuple.
    IP_ADDRESS = (127, 0, 0, 1)
    # The port to send measurements on.
    PORT = 8080

    # These parameters cannot be set at the command line:
    # The number of samples per second.
    SAMPLE_RATE = 44100
    # The number of samples in each root-mean-squared packet.
    PERIOD_SIZE = 1600

    opts, args = getopt.getopt(sys.argv[1:], 'c:i:p:n:h')
    for o, a in opts:
        if o == '-c':
            soundcard = a
        if o == '-i':
            try:
                IP_ADDRESS = tuple([int(i) for i in a.split('.')])
            except (TypeError, ValueError):
                print('ERROR: Not a valid IP address.')
                raise
        if o == '-p':
            try:
                PORT = int(a)
            except (TypeError, ValueError):
                print('ERROR: Not a valid port number.')
                raise
        if o == '-n':
            try:
                PACKET_SIZE = int(a)
            except (TypeError, ValueError):
                print('ERROR: Not a valid packet size.')
                raise
        if o == '-h':
            usage()

    # Open the device in nonblocking capture mode.
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,
                        alsaaudio.PCM_NONBLOCK,
                        soundcard)

    # Set attributes: Mono, 44100 Hz, 16 bit little endian samples.
    inp.setchannels(1)
    inp.setrate(SAMPLE_RATE)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

    # The period size controls the internal number of frames per period.
    # The significance of this parameter is documented in the ALSA api.
    inp.setperiodsize(PERIOD_SIZE)

    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/plain'}
    conn = httplib.HTTPConnection('.'.join([str(i) for i in IP_ADDRESS]),
                                  PORT, timeout=10)
    atexit.register(cleanup, conn)

    packet = []

    j = 0
    while True:
        # Read data from device, if possible.
        frame_count, data = inp.read()

        # Non-zero frame_count when the buffer has just been filled. The buffer
        # is empty again after this read, and frame_count will be zero until
        # the buffer is filled again.
        if frame_count:
            data_int_array = array.array('h', bytes(data))
            rms_value = rms(data_int_array)
            packet.append(rms_value)
            j += 1
            # Print the stream of measurements.
            # print(rms_value)
            time.sleep(.001)

            if j >= PACKET_SIZE:
                now = datetime.datetime.now()
                print(unicode(now) + ' - Sending HTTP POST request...')

                post_data = ':'.join([str(i) for i in packet])
                params = urllib.urlencode({'data': post_data})
                conn.request('POST', '', params, headers)

                try:
                    conn.getresponse()
                except socket.timeout:
                    print("ERROR: HTTP POST timed out.")
                    raise

                now = datetime.datetime.now()
                print(unicode(now) + ' - HTTP response received.')

                j = 0
                packet = []

