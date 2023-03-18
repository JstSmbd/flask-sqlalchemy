from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, \
    BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired


class AddChangeJobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()], name="job")
    leader_id = IntegerField("ID главного", validators=[DataRequired()], name="leader_id")
    work_size = IntegerField("Обьем работы", validators=[DataRequired()], name="work_size")
    collaborators = StringField("Участники", validators=[DataRequired()], name="collaborators")
    is_finished = BooleanField("Работа выполнена?", name="checkbox")
    submit = SubmitField('Поменять', name="enter")