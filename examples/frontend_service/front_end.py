from flask import Flask, render_template, jsonify
import requests
import srvlookup

def lookup_backends():
    return srvlookup.lookup('example_dcos_backend', 'tcp', 'marathon.mesos')

app = Flask(__name__)

@app.route('/')
def index():
    # scatter-gather requests to each back-end
    results = []
    for backend in lookup_backends():
        results.append(requests.get("%s:%s" % (backend.host, backend.port)).json())
    return jsonify(results)
