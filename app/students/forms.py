from wtforms import (Form, StringField, SubmitField, IntegerField, SelectField,
                     RadioField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class StudentForm(Form):
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

class ListStudentForm(Form):
    radio = RadioField(coerce=int)
