from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField,
                     RadioField, IntegerField)
from wtforms.validators import DataRequired

class ListGroupForm(FlaskForm):
    radio = RadioField(coerce=int)
    #addsub = SubmitField('Добавить')
    #changesub = SubmitField('Изменить')
    #delsub = SubmitField('Удалить')

class GroupForm(FlaskForm):
    groupname = StringField('Наименование группы',
                            validators=[DataRequired('значение не заполнено')])
    star = SelectField(u'Староста', coerce=int)
    submit1 = SubmitField('Сохранить')
