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
- 