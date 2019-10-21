from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, SelectField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class AddStudentForm(FlaskForm):
    f = StringField('Фамилия', 
                    validators=[DataRequired('значение не заполнено')])
    i = StringField('Имя', validators=[DataRequired('значение не заполнено')])
    o = StringField('Отчество')
    #bdate = StringField('Дата рождения (дд.мм.гггг)', 
                        #validators=[DataRequired('значение не заполнено')])
    bdate = DateField('Дата рождения', 
                      validators=[DataRequired('значение не заполнено')],
                      format='%Y-%m-%d')
    t = IntegerField('Номер студенческого билета', 
                     validators=[DataRequired('значение не заполнено')]) 
    gr_id = SelectField(u'Выберите группу', coerce=int, 
                       validators=[DataRequired('значение не выбрано')])
    submit1 = SubmitField('Добавить')

class UpStudentForm(FlaskForm):
    id = SelectField(u'Выберите студента', coerce=int, 
                     validators=[DataRequired('значение не заполнено')])
    f = StringField('Фамилия')
    i = StringField('Имя')
    o = StringField('Отчество')
    #bdate = StringField('Дата рождения (дд.мм.гггг)')
    bdate = DateField('Дата рождения', format='%Y-%m-%d')
    t = StringField('Номер студенческого билета') 
    gr_id = SelectField(u'Выберите группу', coerce=int)
    submit1 = SubmitField('Изменить')

class DelStudentForm(FlaskForm):
    id = SelectField(u'Выберите студента', coerce=int, 
                     validators=[DataRequired('значение не выбрано')])
    submit1 = SubmitField('Удалить')
