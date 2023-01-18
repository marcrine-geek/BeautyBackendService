# AllEmpsAPIs
Endpoints for Beauty Parlor apllication

# Deployed API
`https://allempservice.onrender.com`

## flask setup
- install virtual environment
    `pip3 install virtualenv`
- clone repository
    `git clone https://github.com/marcrine-geek/BeautyBackendService.git`
- navigate to project directory
    `cd AllEmpsAPIs`
- virtual environment activation
    `virtualenv venv`
    `source venv/bin/activate`
- Install flask in the environment
    `python3 -m pip install Flask`
## run the server
`python3 app.py`
## additional requirements
`pip install Flask==1.1.4`
`pip install Flask psycopg2-binary`
`pip install Flask-SQLAlchemy`
`pip install Flask-Migrate==2.6.0`
`pip install markupsafe==2.0.1`
`pip freeze > requirements.txt`

## Database initialization
`python3 manage.py db init`

## Migrations
`python3 manage.py db migrate`

## Commit changes to database
`python3 manage.py db upgrade`


Flask==2.0.0
Flask-Cors==3.0.10
Flask-Migrate==2.5.2
flask-restx==0.4.0
Flask-Script==2.0.6
Flask-SQLAlchemy==2.5.1
