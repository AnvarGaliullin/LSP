from flask import Flask #, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData, create_engine
# from datetime import datetime, date, time
# from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import LoginManager#, UserMixin, login_required, login_user, current_user, logout_user
# from forms import LoginForm, RegisterForm
# from models import User
from flask_migrate import Migrate, MigrateCommand
import os, config


# создание экземпляра приложения
app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or'config.DevelopementConfig')
# инициализирует расширения
db = SQLAlchemy(app)
migrate = Migrate(app,  db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
from . import views








# app = Flask(__name__, template_folder = "templates")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:1234567890Aa@localhost/LMS'
# app.config['SECRET_KEY'] = 'a really really really fcking really long secret key'
# db = SQLAlchemy(app)
 


# @login_manager.user_loader
# def load_user(user_id):
#     return db.session.query(User).get(user_id)


# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(1024), nullable=False)

#     def __init__(self, text, tags):
#         self.text = text.strip()
#         self.tags = [
#             Tag(text=tag.strip()) for tag in tags.split(',')
#         ]


# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(32), nullable=False)

#     message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
#     message = db.relationship('Message', backref=db.backref('tags', lazy=True))


# db.create_all()

# @app.route('/', methods=['GET'])
# def index():
#     # return redirect(url_for('main'))
#     return render_template('index.html')


# @app.route('/main', methods=['GET'])
# def main():
#     return render_template('main.html', messages=Message.query.all())


# @app.route('/admin/')
# @login_required
# def admin():
#     return render_template('admin.html')


# @app.route('/register/', methods=['post', 'get'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         print('ok , go')
#         check_password_hash(,form.registration_password.data)

#         user_verification_code = generate_password_hash(form.registration_password.data)
#         user = db.session.query(User).filter(User.registration_password_hash == user_verification_code).first()
#         print('user_verification_code = ',user_verification_code)
#         print('verification_code = ', verification_code)
#         print('user = ',user)
#         if user:
#             login_user(user)
#             return redirect(url_for('index'))

#         flash("Invalid verification code", 'error')
#         return redirect(url_for('register'))
#     return render_template('register.html', form=form)


# @app.route('/login/', methods=['post', 'get'])
# def login():
#     if current_user.is_authenticated:
# 	    return redirect(url_for('admin'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = db.session.query(User).filter(User.email == form.email.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user, remember=form.remember.data)
#             return redirect(url_for('admin'))

#         flash("Invalid email/password", 'error')
#         return redirect(url_for('login'))
#     return render_template('login.html', form=form)


# @app.route('/logout/')
# @login_required
# def logout():
#     logout_user()
#     flash("You have been logged out.")
#     return redirect(url_for('login'))


# @app.route('/add_message', methods=['POST'])
# def add_message():
#     text = request.form['text']
#     tag = request.form['tag']

#     db.session.add(Message(text, tag))
#     db.session.commit()

#     return redirect(url_for('main'))

# db.create_all()

"""
# user_Anvar = User(username='anvar', email='anvar@example.com')
# user_Anvar.set_password('123')
"""
# u1 = User(username='spike', email='spike@example.com')
        # u1 = db.session.query(User).filter(User.username == 'spike').first()
        # u1.set_password("pass")

        # u2 = db.session.query(User).filter(User.username == 'tyke').first()
        # u2.set_password("tyke")

# u3 = User(name="Анвар",username="admin",email="admin@gmail.com")
# u3.set_password("admin")
# print(u3.check_password("admin"))







        # u3 = db.session.query(User).filter(User.username == 'admin').first()

        # db.session.add_all([u1,u2,u3])
        # db.session.commit()

        # print(u1, u2, u3)

        # print(u1.check_password("pass"))
        # print(u1.check_password("spike"))

        # print(u2.check_password("foo"))
        # print(u2.check_password("tyke"))



# if __name__ == "__main__":
#     app.run(debug=True)