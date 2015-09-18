#!/usr/bin/env python

# import the modules we will use
from flask import Flask, render_template

app = Flask(__name__)

# set up our http endpoint
@app.route('/')
@app.route('/<value>')
def index(value="home"):
    return render_template('index.html', value=value)

if __name__ == "__main__":
    # In a real environment, never run with debug=True
    # because it gives you an interactive shell when you
    # trigger an unhandled exception.
    app.run(host="0.0.0.0", debug=True, port=8080, threaded=True)

