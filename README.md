# lexwheels
Python service about cars and owners

# Requirements
In a shell or virtualenv execute.

`python -m pip install -r requirements.txt`

# Environment
In a shell or virtualenv execute.

```
export FLASK_APP=lexwheels
export FLASK_ENV=development
export SQLALCHEMY_TRACK_MODIFICATIONS=False
export SQLALCHEMY_DATABASE_URI='sqlite:///../db/lexwheels.db'
```

The environment can be in a .env or .flaskenv file. There is
a sample.env file that can be copied or used for reference.

# Initializing and Running
```
$> flask init-db
Initialized database

$> flask fill-db
Filled database with dummy data.

$> flask run

* Serving Flask app 'lexwheels' (lazy loading)
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 757-535-849
```
