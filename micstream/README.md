# Micstream

Reads input from an ALSA-compatible microphone and transmits at regular
intervals HTTP GET requests containing a colon-delimited list of integers.

This stream represents the sound pressure level (SPL) of the audio source in
unspecified units; it is simply the root mean square of all values in the input
stream within a small time interval.

We run this script on each Raspberry Pi.

## Installation

To run it as a one off, clone this repo and see `splmeter.py -h` for usage instructions.

To install it as a long running service (this will reboot your Pi), passing in the ID of the node:

    wget https://raw.githubusercontent.com/mesosphere/hackers-at-berkeley/master/micstream/install.sh && sudo bash install.sh 1

## Gotchas

You'll want to know what audio device to use. Using these microphones on our Raspberry Pis, the value we use is "hw:1", which is set as the default in the installation script.

If this doesn't work, check out your list of ALSA devices
using `aplay -L` and specify the correct device in the install script.