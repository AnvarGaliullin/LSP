import os
from application import app, db
from application.models import User
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

manager = Manager(app)
"""
ЗАПУСКАТЬ НУЖНО ИЗ runner.py!!!
"""


# эти переменные доступны внутри оболочки без явного импорта
def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
"""
python runner.py runserver
"""

if __name__ == '__main__':
    manager.run()
