
FROM hypriot/rpi-python
RUN apt-get install -y git
RUN pip install pyalsaaudio
RUN git clone https://github.com/mesosphere/hackers-at-berkeley.git
CMD ["python", "hackers-at-berkeley/splmeter.py"]