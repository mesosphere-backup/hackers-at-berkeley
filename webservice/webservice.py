#!/usr/bin/env python
from flask import Flask, render_template, json, url_for
import urllib2

app = Flask(__name__)

HEATMAP_WIDTH = 800

@app.route('/')
@app.route('/test')
def test_endpoint():
    return 'testing...'

@app.route('/heatmap')
def index(value=None):
    endpoint_data = urllib2.urlopen(
        "http://hackers-at-berkeley.mesosphere.io:8088/read").read()
    endpoint_dict = json.loads(endpoint_data)
    max_x = endpoint_dict["ranges"]["x"][1]
    max_y = endpoint_dict["ranges"]["y"][1]
    aspect_ratio = float(max_y) / float(max_x)
    heatmap_height = int(aspect_ratio * HEATMAP_WIDTH)
    x_scale = float(HEATMAP_WIDTH) / float(max_x)
    y_scale = float(heatmap_height) / float(max_y)
    #heatmap_dict = {"max": endpoint_dict["ranges"]["intensity"][1],
    heatmap_dict = {"max": 2500,
                    "data": [{"x": int(float(d["x"])*x_scale),
                              "y": int(float(d["y"])*y_scale),
                              "value": d["intensity"]}
                              for d in endpoint_dict["sources"]]}
    print("max_x: %s, max_y: %s, x_scale: %f, y_scale: %f" % (max_x, max_y, x_scale, y_scale))
    return render_template('heatmap.html',
                           json_data=json.dumps(heatmap_dict),
                           heatmap_y=heatmap_height)

if __name__ == "__main__":
    # In a real environment, never run with debug=True
    # because it gives you an interactive shell when you
    # trigger an unhandled exception.
    app.run(host="0.0.0.0", debug=True, port=8080)

