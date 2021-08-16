from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from models import Models
from setup_config import setup_config

app = Flask(__name__)
setup_config(app)
models = Models(app)
Bootstrap(app)


@app.route('/')
def welcome():
    owners = models.get_all_owners()
    return render_template('welcome.html', owners=owners)


@app.route('/owner/<int:id>')
def owner(id):
    owner = models.get_owner(id)
    return render_template('owner.html', owner=owner)
