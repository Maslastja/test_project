from wtforms import (Form, StringField, SelectField,
                     RadioField, IntegerField)
from wtforms.validators import DataRequired

class ListGroupForm(Form):
    radio = RadioField(coerce=int)

class GroupForm(Form):
    groupname = StringField('Наименование группы',
                            validators=[DataRequired('значение не заполнено')])
    star = SelectField(u'Староста', coerce=int)
