from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, SelectField,
                     RadioField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class StudentForm(FlaskForm):
    surname = StringField('Фамилия', 
                    validators=[DataRequired('значение не заполнено')])
    firstname = StringField('Имя', 
                            validators=[DataRequired('значение не заполнено')])
    secondname = StringField('Отчество')
    birthdate = DateField('Дата рождения', 
                      validators=[DataRequired('значение не заполнено')],
                      format='%Y-%m-%d')
    numticket = IntegerField('Номер студенческого билета', 
                     validators=[DataRequired('значение не заполнено')]) 
    group = SelectField(u'Выберите группу', coerce=int, 
                       validators=[DataRequired('значение не выбрано')])
    submit1 = SubmitField('Сохранить')

class ListStudentForm(FlaskForm):
    radio = RadioField(coerce=int)
