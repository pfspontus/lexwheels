from flask import Flask

from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = ''
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
mysql.init_app(app)

@app.route('/')
def hello_world():
    return 'ok this app is working now'


@app.route('/details')
def details():
    return 'This website is about details'

@app.route('/car/<int:id>')
def car(id):
    cur = mysql.connect().cursor()
    cur.execute('''SELECT * FROM owners''')
    rv = cur.fetchall()
    return str(rv)
