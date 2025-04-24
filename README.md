# projeto_simples_flask

## Installing Flask
- Create an environment: Create a project folder and a .venv folder within:


```
> mkdir myproject
> cd myproject
> py -3 -m venv .venv
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