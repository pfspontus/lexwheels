import os
import sys

from dotenv import load_dotenv

from lexwheels import create_app  # noqa

HELLO_WORLD = """<html>
<head>
    <title>PythonAnywhere hosted web application</title>
</head>
<body>
<h1>Hello, World!</h1>
<p>
    This is the default welcome page for a
    <a href="https://eu.pythonanywhere.com/">PythonAnywhere</a>
    hosted web application.
</p>
<p>
    Find out more about how to configure your own web application
    by visiting the <a href="https://eu.pythonanywhere.com/web_app_setup/">web app setup</a> page
</p>
</body>
</html>"""


def application(environ, start_response):
    if environ.get('PATH_INFO') == '/':
        status = '200 OK'
        content = HELLO_WORLD
    else:
        status = '404 NOT FOUND'
        content = 'Page not found.'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
    start_response(status, response_headers)
    yield content.encode('utf8')


project_folder = os.path.expanduser('~/lexwheels')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

path = '/home/pfspontus/lexwheels'
if path not in sys.path:
    sys.path.append(path)

application = create_app()
