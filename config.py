import os

app_dir = os.path.abspath(os.path.dirname(__file__))
db_base_type = 'postgres'
db_base_name = 'LMS'
db_base_password = '1234567890Aa'
db_path = db_base_type+'://'+db_base_type+':'+db_base_password+'@localhost/'+db_base_name

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ##### настройка Flask-Mail #####
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOU_MAIL@gmail.com'
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
    # MAIL_DEFAULT_SENDER = MAIL_USERNAME


class DevelopementConfig(BaseConfig):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:1234567890Aa@localhost/LMS'





# class TestingConfig(BaseConfig):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
# 			      'mysql+pymysql://root:pass@localhost/flask_app_db'


# class ProductionConfig(BaseConfig):
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
# 	'mysql+pymysql://root:pass@localhost/flask_app_db'