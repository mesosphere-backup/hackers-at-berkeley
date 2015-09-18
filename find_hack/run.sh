#!/bin/sh
docker build -t spacejam/find-hack .
docker push spacejam/find-hack
dcos marathon app add marathon.json
