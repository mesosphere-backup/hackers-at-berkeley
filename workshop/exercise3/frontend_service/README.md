# example front-end service
This app will run on a public DCOS node so that it will be accessible from the open internet.

It uses SRV DNS records (which return both an IP and a port, instead of just an IP like A records) to find a back-end service that may be running anywhere.
