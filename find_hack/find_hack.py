import sys

from flask import Flask, jsonify
import srvlookup

app = Flask(__name__)

mapping = {
    "10.0.4.70": "52.89.82.119", 
    "10.0.4.63": "52.89.78.120", 
    "10.0.4.66": "52.88.33.238", 
    "10.0.4.71": "52.89.79.28", 
    "10.0.4.64": "52.89.79.55", 
    "10.0.4.68": "52.89.76.194", 
    "10.0.4.69": "52.89.78.250",
    "10.0.4.72": "52.89.88.228", 
    "10.0.4.67": "52.89.77.0", 
    "10.0.4.65": "52.89.80.185"
}

def lookup_backends(name):
    try: 
        return srvlookup.lookup(name, 'tcp', 'marathon.mesos')
    except e:
        print >> sys.stderr, e
        return []

@app.route('/')
def index():
    return "hit /<app_name> to get the host and port"

@app.route('/<name>')
def read(name=""):
    results = []
    print >> sys.stderr, "looking up %s" % name
    for backend in lookup_backends(name):
        endpoint = "%s:%s" % (mapping[backend.host], backend.port)
        print >> sys.stderr, "got backend %s" % endpoint
        results.append(endpoint)
    return jsonify({"results":results})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8080)
