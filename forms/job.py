from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, \
    BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    leader_id = IntegerField("ID главного", validators=[DataRequired()])
    work_size = IntegerField("Обьем работы", validators=[DataRequired()])
    collaborators = StringField("Участники", validators=[DataRequired()])
    is_finished = BooleanField("Работа выполнена?", name="checkbox")
    submit = SubmitField('Добавить', name="enter")
