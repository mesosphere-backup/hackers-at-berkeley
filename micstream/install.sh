#!/bin/bash

if [ -e /home/pi/hackers-at-berkeley ]
then
    rm -rfi /home/pi/hackers-at-berkeley
fi

# Clone GitHub repo
git clone https://github.com/mesosphere/hackers-at-berkeley.git /home/pi/hackers-at-berkeley

# Install into crontab
echo "@reboot /home/pi/hackers-at-berkeley/micstream/splmeter.py -H \"hackers-at-berkeley.mesosphere.io\" -i 1 -c hw:1 -p 8088 >> /home/pi/splmeter.out 2>&1" >> /var/spool/cron/crontabs/root

# Restart
reboot