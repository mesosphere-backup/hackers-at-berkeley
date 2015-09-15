# hackers-at-berkeley
Example files for H@B workshop.

## Components

### 0) Hardware

We use Raspberry Pis of either version 1 B+ or version 2 B with [Raspbian](https://www.raspbian.org/) installed. The Raspberry Pis must be connected to the internet.

On each Raspberry Pi we use the [USB Kinobo microphone](http://www.amazon.com/Kinobo-Microphone-Desktop-Recognition-Software/dp/B00IR8R7WQ/ref=sr_1_4?s=pc&ie=UTF8&qid=1441404716&sr=1-4&keywords=usb+microphone).


### 1) Micstream

Reads input from an ALSA-compatible microphone and transmits at regular
intervals HTTP POST messages containing a colon-delimited list of integers.

This stream represents the sound pressure level (SPL) of the audio source in
unspecified units; it is simply the root mean square of all values in the input
stream within a small time interval.

We run this script on each Raspberry Pi.

#### Pre-requisites

Install [PyAlsaAudio](https://github.com/larsimmisch/pyalsaaudio):

    sudo pip install pyalsaaudio

If this fails to install, you may need to install the package `python-dev` or equivalent for your operating system:

    sudo apt-get install -y python-dev

#### Installation

`splmeter.py -h` for usage instructions.

Check out this repository into your home directory:

    git clone git clone git@github.com:mesosphere/hackers-at-berkeley.git

You can configure this script to run at boot by editing the crontab for the root user:

    sudo crontab -e /home/pi/hackers-at-berkeley/micstream/splmeter.py 

And appending this line to start the script upon a restart:

    @reboot /home/pi/hackers-at-berkeley/micstream/splmeter.py 

#### Usage:

To test it out, first run the HTTP server,
```
./httpservice.py
```
and then run the SPL meter,
```
./splmeter.py
```

If the default audio device doesn't work, check out your list of ALSA devices
using `aplay -L` and specify the correct device via
`./splmeter.py -c <soundcard>`.


### 2) Perimeter

REST API that provides an interface to write values and read stored values.