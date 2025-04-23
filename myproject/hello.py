from flask import Flask

app = Flask(__name__)

#A Minimal Application
@app.route('/')
def hello():
    return "<p>Index<p>"

#routing
@app.route('/routing')
def hello_world():
    return "<h1>Hello, World!</h1>"

#HTML Escaping
from markupsafe import escape
@app.route('/html_escaping/<username>')
def hello_user(username):
    return f"<h1>Hello, {escape(username)}!</h1>"


#Variable Rules
@app.route('/variable_rules/<int:post_id>') #só vai funcionar com integers
def show_post(post_id):
    return f"""<h1>Post {post_id}</h1>
string: (default) accepts any text without a slash</br> 

int: accepts positive integers</br>

float: accepts positive floating point values</br>

path: like string but also accepts slashes</br>

uuid: accepts UUID strings""" 

#Unique URLs / Redirection Behavior

@app.route('/projects/')
def projects():
    return 'The project page</br>Could be acessed with the URL <i>/projects/</i> or <i>/projects/</i>'

@app.route('/about')
def about():
    return 'The about page</br>Could be acessed only with the URL <i>/about</i></br>The Url <i>/about/</i> will generate an error'

#URL Building ->  url_for() and test_request_context()

from flask import url_for

with app.test_request_context():
    print(url_for('hello'))
    print(url_for('about'))
    print(url_for('projects'))
    print(url_for('hello_user', username='John Doe'))

# HTTP Methods
#1
from flask import request
# the terminal should be from CMD type
# On terminal: $ curl -X POST "http://localhost:5000/login" or $ curl -X GET "http://localhost:5000/login"
def do_the_login():
    return "do_the_login()"
def show_the_login_form():
    return "show_the_login_form()"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
# Alternativelly -> On terminal: $ curl -X POST "http://localhost:5000/alternative_login" or $ curl -X GET "http://localhost:5000/alternative_login"     
@app.get('/alternative_login')
def login_get():
    return show_the_login_form()

@app.post('/alternative_login')
def login_post():
    return do_the_login()

#on terminal you can use $ curl -X GET "http://localhost:5000/..." on any url link to test the application, teh other methods only if exists specificaly.

#Static Files