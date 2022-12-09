from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route("/")
def hello():
    return redirect(url_for('health_check'))


@app.route("/health")
def health_check():
    return {
        'status': 'available'
    }
