#!/usr/bin/env python

import alsaaudio
import argparse
import array
import atexit
import datetime
import getopt
import httplib
import math
import requests
import sys
import time
import urllib

def rms(buffer):
    """Calculate the root-mean-square of some iterable full of numbers."""
    total = 0.
    for el in buffer:
        total += el**2
    return int(math.sqrt(total))

def usage():
    print('Usage: splmeter.py [-i <id=0>][-c <soundcard>] [-H <hostname=localhost>] '
          '[-p <port=80>] [-n <packet size=100>]')
    sys.exit(0)

def now():
    return unicode(datetime.datetime.now())

if __name__ == '__main__':

    # These parameters can be set at the command line:
    ID = 0
    # Soundcard that PyAlsaAudio should use
    soundcard = 'default'
    # The number of volume measurements in each HTTP POST request.
    PACKET_SIZE = 100
    # The IP address to send measurements to, as a 4-tuple.
    HOSTNAME = 'localhost'
    # The port to send measurements on.
    PORT = 80

    # These parameters cannot be set at the command line:
    # The number of samples per second.
    SAMPLE_RATE = 44100
    # The number of samples in each root-mean-squared packet.
    PERIOD_SIZE = 1600

    opts, args = getopt.getopt(sys.argv[1:], 'i:c:H:p:n:h')
    for o, a in opts:
        if o == '-i':
            try:
                ID = int(a)
            except TypeError:
                print ('ERRROR: Not a valid ID.')
                raise
        if o == '-c':
            soundcard = a
        if o == '-H':
            try:
                HOSTNAME = str(a)
            except (TypeError, ValueError):
                print('ERROR: Not a valid hostname.')
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
                print(now() + ' - Sending HTTP GET request...')

                url_data = ':'.join([str(i) for i in packet])
                #encoded_data = urllib.urlencode(url_data)
                request_url = "http://{}:{}/submit/{}/{}".format(HOSTNAME, PORT, ID, url_data)
		print(now() + ' - {}'.format(request_url))
                r = requests.get(request_url)
                print(now() + ' - Response was: {}'.format(r.status_code))

                j = 0
                packet = []

