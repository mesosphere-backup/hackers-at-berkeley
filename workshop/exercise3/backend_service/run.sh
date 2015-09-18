#!/bin/sh
docker build .
docker push <YOUR_USERNAME>/example_dcos_backend
dcos marathon app add marathon.json
