import random

from flask import Flask, render_template, jsonify
import requests
import srvlookup

app = Flask(__name__)

def lookup_backends():
    return srvlookup.lookup('example_dcos_backend', 'tcp', 'marathon.mesos')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/read')
def read():
    return jsonify({"results":[
        {
            "host": "host:02",
            "values": [random.randint(0,100) for i in xrange(10)]
        }
    ]})
    # scatter-gather requests to each back-end
    results = []
    for backend in lookup_backends():
        endpoint = "%s:%s" % (backend.host, backend.port)
        results.append({
            "host": endpoint,
            "values": requests.get(endpoint).json(),
        })
    return jsonify(results)