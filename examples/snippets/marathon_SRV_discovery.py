import srvlookup

myapp_locations = srvlookup.lookup('myapp', 'tcp', 'marathon.mesos')

print "locations for myapp running on marathon:"
for location in myapp_locations:
    print "%s:%s" % (location.host, location.port)
