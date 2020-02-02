from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
import os, config



# создание экземпляра приложения
app = Flask(__name__)
Bootstrap(app)

app.config.from_object(os.environ.get('FLASK_ENV') or'config.DevelopementConfig')
app.jinja_env.auto_reload = True 

# инициализирует расширения
db = SQLAlchemy(app)
migrate = Migrate(app,  db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from . import views