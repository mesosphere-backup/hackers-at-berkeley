import random
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify([random.randint(0,100) for i in xrange(10)])

if __name__ == "__main__":
    # In a real environment, never run with debug=True
    # because it gives you an interactive shell when you
    # trigger an unhandled exception.
    app.run(host="0.0.0.0", debug=True, port=8080, threaded=True)