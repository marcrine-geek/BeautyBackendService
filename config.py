import os

# postgres_local_base = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'.format(
#         user=os.environ.get('FLASK_DATABASE_USER', 'postgres'),
#         password=os.environ.get('FLASK_DATABASE_PASSWORD', 'jaguarleopard'),
#         host=os.environ.get('FLASK_DATABASE_HOST', 'database-2.chkfhb6ik0ro.us-east-1.rds.amazonaws.com'),
#         port=os.environ.get('FLASK_DATABASE_PORT', 5432),
#         db_name=os.environ.get('FLASK_DATABASE_NAME', 'database-2'),
#     )


# mysql connection
mysql_local_base = 'mysql+mysqldb://admin:jaguarleopard@database-1.chkfhb6ik0ro.us-east-1.rds.amazonaws.com:3306/beauty'


# postgres_local_base = os.environ['DATABASE_URL']
# 54.157.189.162

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'nothing')
    DEBUG = False
    TOKEN_EXPIRE_HOURS = (24 * 365)

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USERNAME = 'customersupport@demo.com'
    MAIL_PASSWORD = ''

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = mysql_local_base
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI =mysql_local_base
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = mysql_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
