from flask_wtf import FlaskForm
from wtforms import Form, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired
#...
#...
class LoginForm(FlaskForm):
    email = StringField("Email:",  validators=[DataRequired(), Email()])
    password = StringField("Пароль:", validators=[DataRequired()])
    remember = BooleanField("Запомнить меня:")
    submit = SubmitField("Войти")

class RegisterForm(FlaskForm):
    email = StringField("E-mail:",  validators=[DataRequired(), Email()])
    password = StringField("Пароль:", validators=[Length(min = 4, max = 25, message = 'Password must be between 4 and 25 characters')])
    confirm_password = StringField("Подтвердите пароль:", validators=[EqualTo('password', message = "Passwords must match")])
    registration_password = StringField("Верификационный код:", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")