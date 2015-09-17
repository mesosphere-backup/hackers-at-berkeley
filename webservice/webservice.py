#!/usr/bin/env python
from flask import Flask, render_template, json, url_for
import urllib2

app = Flask(__name__)

HEATMAP_WIDTH = 800

@app.route('/')
@app.route('/test')
# Here's an HTTP endpoint for testing purposes.
def test_endpoint():
    return 'testing...'

@app.route('/heatmap')
def index(value=None):
    # Grab the JSON output of the /read HTTP endpoint. This provides the
    # max/min range of each parameter, and then a list of objects containing
    # the values associated with each point source.
    endpoint_data = urllib2.urlopen(
        "http://hackers-at-berkeley.mesosphere.io:8088/read").read()
    # Convert this JSON string into a dictionary.
    endpoint_dict = json.loads(endpoint_data)

    # We assume a fixed HEATMAP_WIDTH and scale the height accordingly based
    # on the maximum x and y values.
    max_x = endpoint_dict["ranges"]["x"][1]
    max_y = endpoint_dict["ranges"]["y"][1]
    aspect_ratio = float(max_y) / float(max_x)
    heatmap_height = int(aspect_ratio * HEATMAP_WIDTH)

    # We must scale the coordinates of the point sources to match the heatmap.
    x_scale = float(HEATMAP_WIDTH) / float(max_x)
    y_scale = float(heatmap_height) / float(max_y)

    # Build a dictionary containing the heatmap input data that will become a
    # JSON string to be sent to the client.
    heatmap_dict = {"max": endpoint_dict["ranges"]["intensity"][1],
                    "data": [{"x": int(float(d["x"])*x_scale),
                              "y": int(float(d["y"])*y_scale),
                              "value": d["intensity"]}
                              for d in endpoint_dict["sources"]]}

    # Send the client heatmap.html as a template, passing the relevant data to
    # be inserted where appropriate.
    return render_template('heatmap.html',
                           json_data=json.dumps(heatmap_dict),
                           heatmap_y=heatmap_height)

if __name__ == "__main__":
    # In a real environment, never run with debug=True
    # because it gives you an interactive shell when you
    # trigger an unhandled exception.
    app.run(host="0.0.0.0", debug=True, port=80)

