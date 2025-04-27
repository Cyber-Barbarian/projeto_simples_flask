# projeto_simples_flask

## Installing Flask
- Create an environment: Create a project folder and a .venv folder within:


```
> mkdir myproject
> cd myproject
> python -m venv .venv
```

- Activate the environment: Before you work on your project, activate the corresponding environment:


`> .venv\Scripts\activate`

- Your shell prompt will change to show the name of the activated environment.
- Install Flask: Within the activated environment, use the following command to install Flask:

`$ pip install Flask`

- requirements generation
```
pip freeze > requirements.txt

```

-requirements instalation

```
.venv\Scripts\activate
pip install -r requirements.txt
```

## quickstart
- [hello.py](myproject/hello.py)
- https://flask.palletsprojects.com/en/stable/quickstart/

## run flask 
- $ flask --app hello run
- $ flask --app hello run --debug

## Tutorial 
### Application Setup
- https://flask.palletsprojects.com/en/stable/tutorial/
- https://github.com/pallets/flask/tree/main/examples/tutorial
```sh
$ mkdir flask-tutorial
$ cd flask-tutorial
$ python -m venv .venv
$ .venv\Scripts\activate
$ pip install flask
$ pip freeze > requirements.txt
```
-tree
```
/home/user/Projects/flask-tutorial
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── .venv/
├── pyproject.toml
└── MANIFEST.in
```

- The Application Factory
  `$ mkdir flaskr`

- __init__.py file in Python. This file is indeed special and serves a specific purpose in Python packages.
  - Package Initialization: The __init__.py file is used to mark a directory as a Python package. This allows you to import modules from that directory.
  - Initialization Code: You can include initialization code in this file that you want to run when the package is imported.
  - Namespace Management: It can be used to define what is available when the package is imported, by setting the __all__ variable. 

- flaskr/__init__.py ->  serves double duty: it will contain the application factory, and it tells Python that the flaskr directory should be treated as a package.
```python
import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
```
-  explanation

   - create_app is the application factory function. You’ll add to it later in the tutorial, but it already does a lot.

     - app = Flask(__name__, instance_relative_config=True) creates the Flask instance.

       - __name__ is the name of the current Python module. The app needs to know where it’s located to set up some paths, and __name__ is a convenient way to tell it that.

       - instance_relative_config=True tells the app that configuration files are relative to the instance folder. The instance folder is located outside the flaskr package and can hold local data that shouldn’t be committed to version control, such as configuration secrets and the database file.

   - app.config.from_mapping() sets some default configuration that the app will use:

     - SECRET_KEY is used by Flask and extensions to keep data safe. It’s set to 'dev' to provide a convenient value during development, but it should be overridden with a random value when deploying.

     - DATABASE is the path where the SQLite database file will be saved. It’s under app.instance_path, which is the path that Flask has chosen for the instance folder. You’ll learn more about the database in the next section.

   - app.config.from_pyfile() overrides the default configuration with values taken from the config.py file in the instance folder if it exists. For example, when deploying, this can be used to set a real SECRET_KEY.

     - test_config can also be passed to the factory, and will be used instead of the instance configuration. This is so the tests you’ll write later in the tutorial can be configured independently of any development values you have configured.

 - os.makedirs() ensures that app.instance_path exists. Flask doesn’t create the instance folder automatically, but it needs to be created because your project will create the SQLite database file there.

- @app.route() creates a simple route so you can see the application working before getting into the rest of the tutorial. It creates a connection between the URL /hello and a function that returns a response, the string 'Hello, World!' in this case.

- run: `$ flask --app flaskr run --debug` -> you should still be in the top-level flask-tutorial directory, not the flaskr package.

### Define and Access the Database - sqlite3
- Connect to the Database: The first thing to do when working with a SQLite database (and most other Python database libraries) is to create a connection to it. Any queries and operations are performed using the connection, which is closed after the work is finished.

In web applications this connection is typically tied to the request. It is created at some point when handling a request, and closed before the response is sent.

- flaskr/db.py
```python
import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

```
- g is a special object that is unique for each request. It is used to store data that might be accessed by multiple functions during the request. The connection is stored and reused instead of creating a new connection if get_db is called a second time in the same request.

- current_app is another special object that points to the Flask application handling the request. Since you used an application factory, there is no application object when writing the rest of your code. get_db will be called when the application has been created and is handling a request, so current_app can be used.

- sqlite3.connect() establishes a connection to the file pointed at by the DATABASE configuration key. This file doesn’t have to exist yet, and won’t until you initialize the database later.

- sqlite3.Row tells the connection to return rows that behave like dicts. This allows accessing the columns by name.

- close_db checks if a connection was created by checking if g.db was set. If the connection exists, it is closed. Further down you will tell your application about the close_db function in the application factory so that it is called after each request.

### Create the Tables
- In SQLite, data is stored in tables and columns. These need to be created before you can store and retrieve data. Flaskr will store users in the user table, and posts in the post table. Create a file with the SQL commands needed to create empty tables:
```sql
--flaskr/schema.sql
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
```

- Add the Python functions that will run these SQL commands to the db.py file ON flaskr/db.py:
```python
#flaskr/db.py -> continuação
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)
```

- open_resource() opens a file relative to the flaskr package, which is useful since you won’t necessarily know where that location is when deploying the application later. get_db returns a database connection, which is used to execute the commands read from the file.

- click.command() defines a command line command called init-db that calls the init_db function and shows a success message to the user. You can read Command Line Interface to learn more about writing commands.

- The call to sqlite3.register_converter() tells Python how to interpret timestamp values in the database. We convert the value to a datetime.datetime.

### Register with the Application
- The close_db and init_db_command functions need to be registered with the application instance; otherwise, they won’t be used by the application. However, since you’re using a factory function, that instance isn’t available when writing the functions. Instead, write a function that takes an application and does the registration.
```python
#flaskr/db.py
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
```

- app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.

- app.cli.add_command() adds a new command that can be called with the flask command.

Import and call this function from the factory. Place the new code at the end of the factory function before returning the app.

```python
#flaskr/__init__.py
def create_app():
    app = ...
    # existing code omitted

    from . import db
    db.init_app(app)

    return app
```

### Initialize the Database File
- Now that init-db has been registered with the app, it can be called using the flask command, similar to the run command from the previous page.

- Note:
If you’re still running the server from the previous page, you can either stop the server, or run this command in a new terminal. If you use a new terminal, remember to change to your project directory and activate the env as described in Installation.

- Run the init-db command: `$ flask --app flaskr init-db`
- There will now be a flaskr.sqlite file in the instance folder in your project.

### Blueprints and Views
**A view function is the code you write to respond to requests to your application**. Flask uses patterns to match the incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. Flask can also go the other direction and generate a URL to a view based on its name and arguments.
- Create a Blueprint: **A Blueprint is a way to organize a group of related views and other code.** Rather than registering views and other code directly with an application, they are registered with a blueprint. Then the blueprint is registered with the application when it is available in the factory function.
- Flaskr will have two blueprints, one for authentication functions and one for the blog posts functions. The code for each blueprint will go in a separate module. Since the blog needs to know about authentication, you’ll write the authentication one first.
```python
#flaskr/auth.py
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
```
- This creates a Blueprint named 'auth'. Like the application object, the blueprint needs to know where it’s defined, so __name__ is passed as the second argument. The url_prefix will be prepended to all the URLs associated with the blueprint.

- Import and register the blueprint from the factory using app.register_blueprint(). Place the new code at the end of the factory function before returning the app.
```python
#flaskr/__init__.py
def create_app():
    app = ...
    # existing code omitted

    from . import auth
    app.register_blueprint(auth.bp)

    return app
```
- The authentication blueprint will have views to register new users and to log in and log out.

### The First View: Register
- When the user visits the /auth/register URL, the register view will return HTML with a form for them to fill out. When they submit the form, it will validate their input and either show the form again with an error message or create the new user and go to the login page.

- For now you will just write the view code. On the next page, you’ll write templates to generate the HTML form.
```python
#flaskr/auth.py
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')
```

- Here’s what the register view function is doing:

  - @bp.route associates the URL /register with the register view function. When Flask receives a request to /auth/register, it will call the register view and use the return value as the response.

  - If the user submitted the form, request.method will be 'POST'. In this case, start validating the input.

  - request.form is a special type of dict mapping submitted form keys and values. The user will input their username and password.

  - Validate that username and password are not empty.

  - If validation succeeds, insert the new user data into the database.

    - db.execute takes a SQL query with ? placeholders for any user input, and a tuple of values to replace the placeholders with. The database library will take care of escaping the values so you are not vulnerable to a SQL injection attack.

    - For security, passwords should never be stored in the database directly. Instead, generate_password_hash() is used to securely hash the password, and that hash is stored. Since this query modifies data, db.commit() needs to be called afterwards to save the changes.

    - An sqlite3.IntegrityError will occur if the username already exists, which should be shown to the user as another validation error.

  - After storing the user, they are redirected to the login page. url_for() generates the URL for the login view based on its name. This is preferable to writing the URL directly as it allows you to change the URL later without changing all code that links to it. redirect() generates a redirect response to the generated URL.

  - If validation fails, the error is shown to the user. flash() stores messages that can be retrieved when rendering the template.

  - When the user initially navigates to auth/register, or there was a validation error, an HTML page with the registration form should be shown. render_template() will render a template containing the HTML, which you’ll write in the next step of the tutorial.
### Login
- This view follows the same pattern as the register view above.
```python
#flaskr/auth.py
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')
```

- There are a few differences from the register view:

  - The user is queried first and stored in a variable for later use.

  - fetchone() returns one row from the query. If the query returned no results, it returns None. Later, fetchall() will be used, which returns a list of all results.

  - check_password_hash() hashes the submitted password in the same way as the stored hash and securely compares them. If they match, the password is valid.

  - session is a dict that stores data across requests. When validation succeeds, the user’s id is stored in a new session. The data is stored in a cookie that is sent to the browser, and the browser then sends it back with subsequent requests. Flask securely signs the data so that it can’t be tampered with.

- Now that the user’s id is stored in the session, it will be available on subsequent requests. At the beginning of each request, if a user is logged in their information should be loaded and made available to other views.
```python
#flaskr/auth.py
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
```

- bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested. load_logged_in_user checks if a user id is stored in the session and gets that user’s data from the database, storing it on g.user, which lasts for the length of the request. If there is no user id, or if the id doesn’t exist, g.user will be None.


### Logout
- To log out, you need to remove the user id from the session. Then load_logged_in_user won’t load a user on subsequent requests.
```python
# flaskr/auth.py
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
```

### Require Authentication in Other Views

- A decorator in Python is a function that takes another function and extends its behavior without modifying it. The decorator function wraps the original function, and can add code before and after the target function’s execution. This allows you to execute pre-defined behaviors such as logging, enforcing access control, or modifying input/output values.
- Creating, editing, and deleting blog posts will require a user to be logged in. A decorator can be used to check this for each view it’s applied to.
```python
# flaskr/auth.py
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
```
- This decorator returns a new view function that wraps the original view it’s applied to. The new function checks if a user is loaded and redirects to the login page otherwise. If a user is loaded the original view is called and continues normally. You’ll use this decorator when writing the blog views.

### Endpoints and URLs
- The url_for() function generates the URL to a view based on a name and arguments. The name associated with a view is also called the endpoint, and by default it’s the same as the name of the view function.

- For example, the hello() view that was added to the app factory earlier in the tutorial has the name 'hello' and can be linked to with url_for('hello'). If it took an argument, which you’ll see later, it would be linked to using url_for('hello', who='World').

- When using a blueprint, the name of the blueprint is prepended to the name of the function, so the endpoint for the login function you wrote above is 'auth.login' because you added it to the 'auth' blueprint.

# continue templates