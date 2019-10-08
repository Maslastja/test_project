from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class AddGroupForm(FlaskForm):
    name = StringField('Наименование группы', validators=[DataRequired()])
    submit1 = SubmitField('Добавить')

class UpGroupForm(FlaskForm):
    id = SelectField(u'Выберите группу', coerce=int, 
                     validators=[DataRequired()])
    name = StringField('Наименование группы')
    stud_id = SelectField(u'Выберите старосту', coerce=int)
    submit1 = SubmitField('Изменить')

class DelGroupForm(FlaskForm):
    id = SelectField(u'Выберите группу', coerce=int, 
                     validators=[DataRequired()])
    submit1 = SubmitField('Удалить')

