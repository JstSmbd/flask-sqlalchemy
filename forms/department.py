from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, \
    BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired


class AddChangeDepartmentForm(FlaskForm):
    dep = StringField('Название департамента', validators=[DataRequired()], name="dep")
    chief = IntegerField("ID главного", validators=[DataRequired()], name="chief")
    collaborators = StringField("Участники", validators=[DataRequired()], name="collaborators")
    email = EmailField("email департамента", name="email", validators=[DataRequired()])
    submit = SubmitField('Поменять', name="enter")