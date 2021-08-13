from flask import Flask

from models import Models
from setup_config import setup_config

app = Flask(__name__)
setup_config(app)
models = Models(app)


@app.route('/')
def hello_world():
    return 'ok this app is working now'
