#!/bin/bash

ID=$1

if [ -e /home/pi/hackers-at-berkeley ]
then
    rm -rf /home/pi/hackers-at-berkeley
fi

# Install python-dev
apt-get update && apt-get install -y python-dev

# Install pyalsaaudio and requests
pip install requests pyalsaaudio

# Clone GitHub repo
git clone https://github.com/mesosphere/hackers-at-berkeley.git /home/pi/hackers-at-berkeley

# Install into crontab
echo "@reboot /home/pi/hackers-at-berkeley/micstream/splmeter.py -H \"hackers-at-berkeley.mesosphere.io\" -i $ID -c hw:1 -p 8088 >> /home/pi/splmeter.out 2>&1" >> /var/spool/cron/crontabs/root

# Restart
reboot