import random
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify([random.randint(0,100) for i in xrange(10)])
