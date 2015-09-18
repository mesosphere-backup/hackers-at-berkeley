from flask import Flask, render_template
import srvlookup

@app.route('/')
@app.route('/<value>')
def index(value="home"):
    return render_template('index.html', value=value)


