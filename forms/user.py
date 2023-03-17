from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, \
    BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()], name="email")
    password = PasswordField('Пароль', validators=[DataRequired()], name="password")
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()], name="password")
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = SelectField("Позиция", validators=[DataRequired()], name="button",
                           choices=["Инженер", "Капитан", "Исследователь", "Геолог", "Штурман"])
    speciality = SelectField("Профессия", validators=[DataRequired()], name="button",
                             choices=["Инженер", "Капитан", "Исследователь", "Геолог", "Штурман"])
    submit = SubmitField('Войти', name="enter")
