## httpservice.py

A small HTTP server which will print the contents of any POST requests and
then send a response.

`httpservice.py -h` for usage instructions.


## splmeter.py

Reads input from an ALSA-compatible microphone and transmits at regular
intervals HTTP POST messages containing a colon-delimited list of integers.
This stream represents the sound pressure level (SPL) of the audio source in
unspecified units; it is simply the root mean square of all values in the input
stream within a small time interval.

`splmeter.py -h` for usage instructions.

**Dependencies:**

`splmeter.py` requires that PyAlsaAudio be installed so that it can be imported
with `import alsaaudio`. Find it here: https://github.com/larsimmisch/pyalsaaudio


## Usage:

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