from wtforms import Form, StringField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired
from app.models.users import User

class AddUserForm(Form):
    username = StringField('Имя пользователя', 
                           validators=[DataRequired('значение не заполнено')])
    password = StringField('Пароль', 
                           validators=[DataRequired('значение не заполнено')])
    
    def validate_username(self, username):
        user = User.select().where(User.username == username.data)
        if len(user) != 0:
            raise ValidationError('Такой пользователь уже существует. '
            'Введите другое имя пользователя')
        