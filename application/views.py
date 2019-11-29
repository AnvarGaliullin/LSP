from application import app#, login_manager
from flask import render_template, request, redirect, url_for, flash, make_response, session
# from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user,current_user, logout_user
from .models import User, db, db_add_objects
from .forms import LoginForm, RegisterForm


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/register/', methods=['post', 'get'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # DataBase Logic - check, if user with such validation_password exists
        user_with_equal_email = db.session.query(User).filter(User.email == form.email.data).first()
        if user_with_equal_email != None:
            flash("This E-mail is already reserved", 'error')
            return redirect(url_for('register'))
        else:
            unregistered_users = db.session.query(User).filter(User.email == None).all()
            for checked_user in unregistered_users:
                if check_password_hash(checked_user.registration_password_hash, form.registration_password.data):
                    checked_user.set_email(form.email.data)
                    checked_user.set_password(form.password.data)
                    db_add_objects(checked_user)
                    login_user(checked_user)
                    return redirect(url_for('index')) 
                else:
                    flash("Invalid verification code", 'error')
                    return redirect(url_for('register'))   
    return render_template('register.html', form=form)


@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
	    return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))

        flash("Invalid email/password", 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))