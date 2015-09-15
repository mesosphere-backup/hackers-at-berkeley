#!/bin/sh
docker build .
docker push spacejam/hack-at-berkeley
dcos marathon app add marathon.json
