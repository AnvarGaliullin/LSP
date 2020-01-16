from flask_wtf import FlaskForm
from wtforms import Form, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired, Regexp, Optional, Required
from wtforms.widgets import PasswordInput
import phonenumbers


class LoginForm(FlaskForm):
    email = StringField("Email:",  validators=[DataRequired(), Email()])
    password = StringField("Пароль:", validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    remember = BooleanField("Запомнить меня:")
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    email = StringField("E-mail:",  validators=[DataRequired(), Email()])
    password = StringField("Пароль:", validators=[Regexp("(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$", message="Слишком слабый пароль"), Length(min = 4, max = 25, message = 'Password must be between 4 and 25 characters')], widget=PasswordInput(hide_value=False))
    confirm_password = StringField("Подтвердите пароль:", validators=[EqualTo('password', message = "Passwords must match")], widget=PasswordInput(hide_value=False))
    registration_password = StringField("Верификационный код:", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")


class PersonalCabinetForm(FlaskForm):
    email = StringField("E-mail:")# Валидаторов нет - потому что эту форму пользователь не может редактировать
    phone = StringField('Телефон', validators=[Optional(), Regexp("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message="Некорректный формат телефона")], render_kw={"placeholder": "введите номер телефона"} ) 
    home_region = StringField("Родной город:", validators=[Optional(), Regexp("^[a-zA-Zа-яА-Я-]+$", message="Некорректный город")], render_kw={"placeholder": "введите родной город"})
    detailed_description = TextAreaField("О себе:", validators=[Length(max = 254, message = 'Описание слишком длинное')], render_kw={"placeholder": "расскажите о себе"} )
    vk = StringField("vk:", validators=[Optional(), Regexp("^(https?:\/\/)?(www\.)?vk\.com\/(\w|\d)+?\/?$", message="Некорректная ссылка")], render_kw={"placeholder": "ссылка на vk профиль"} )
    facebook = StringField("facebook:", validators=[Optional(), Regexp("http(s)?:\/\/(www\.)?(facebook|fb)\.com\/[A-z0-9_\-\.]+\/?", message="Некорректная ссылка")], render_kw={"placeholder": "ссылка на facebook профиль"} )
    linked_in = StringField("linked_in:", validators=[Optional(), Regexp("http(s)?:\/\/(www\.)?(facebook|fb)\.com\/[A-z0-9_\-\.]+\/?", message="Некорректная ссылка")], render_kw={"placeholder": "ссылка на LinkedIn профиль"} )
    instagram = StringField("instagram:", validators=[Optional(), Regexp("http(s)?:\/\/(www\.)?(facebook|fb)\.com\/[A-z0-9_\-\.]+\/?", message="Некорректная ссылка")], render_kw={"placeholder": "ссылка на instagram профиль"} )
    submit = SubmitField("Сохранить изменения")


class ChangePassword(FlaskForm):
    old_password = StringField("Старый пароль:", widget=PasswordInput(hide_value=False))
    new_password = StringField("Новый пароль:", validators=[Regexp("(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$", message="Слишком слабый пароль"), Length(min = 4, max = 25, message = 'Password must be between 4 and 25 characters')], widget=PasswordInput(hide_value=False))
    confirm_new_password = StringField("Подтвердите пароль:", validators=[EqualTo('new_password', message = "Passwords must match")], widget=PasswordInput(hide_value=False))
    submit = SubmitField("Сменить пароль")


class CourseAddMaterialForm(FlaskForm):
    name = StringField("Название:", validators=[Length(min = 1, message = 'Обязательное поле'), Length(max = 100, message = 'Слишком длинное название')])
    content = TextAreaField("Содержание:", validators=[Length(min = 1, message = 'Обязательное поле'), Length(max = 10000, message = 'Слишком длинное содержание')])
    submit = SubmitField("Сохранить")


class CourseHometaskForm(FlaskForm):
    name = StringField("Название:", validators=[Length(min = 1, message = 'Обязательное поле'), Length(max = 100, message = 'Слишком длинное название')])
    content = TextAreaField("Содержание:", validators=[Length(min = 1, message = 'Обязательное поле'), Length(max = 10000, message = 'Слишком длинное содержание')])
    start_dttm = DateTimeLocalField("Начало сдачи", format='%Y-%m-%dT%H:%M', validators=[Required()])
    end_dttm = DateTimeLocalField("Окончание сдачи", format='%Y-%m-%dT%H:%M', validators=[Required()])
    submit = SubmitField("Сохранить")
    # Redefine validate method, added aditional condition
    def validate(self):
        is_valid = FlaskForm.validate(self)
        if not is_valid:
            return False
        if self.start_dttm.data > self.end_dttm.data:
            self.start_dttm.errors.append('Начало сдачи должно быть до дедлайна')
            return False
        return True

class StudentHometaskForm(FlaskForm):
    content = TextAreaField("Решение:", validators=[Length(min = 1, message = 'Обязательное поле'), Length(max = 100000, message = 'Слишком длинное решение')])
    submit = SubmitField("Сохранить")
    