from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired
from app.models.users import User

class AddUserForm(FlaskForm):
    username = StringField('Имя пользователя', 
                           validators=[DataRequired('значение не заполнено')])
    password = StringField('Пароль', 
                           validators=[DataRequired('значение не заполнено')])
    submit = SubmitField('Добавить')
    
    def validate_username(self, username):
        #print(username.data)
        user = User.sel_user_by_name(username.data)
        #print(len(user))
        if len(user) != 0:
            raise ValidationError('Такой пользователь уже существует.\
            Введите другое имя пользователя')
        