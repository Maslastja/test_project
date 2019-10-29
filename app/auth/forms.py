from wtforms import (Form, StringField, SubmitField, PasswordField, 
                     BooleanField, validators)
from werkzeug.security import check_password_hash
from app.models.users import User

class LoginForm(Form):
    username = StringField('Логин')
    password = PasswordField('Пароль')

    def validate(self):
        if self.username.data=='' and self.password.data=='':
            self.username.errors=('поле не заполнено',)
            self.password.errors=('поле не заполнено',)
            return False
        user = User.select().where(User.username == self.username.data)
        if len(user) == 0:
            self.username.errors=('Неверный логин',)
            return False
        else:
            usr = user.get()
            if not check_password_hash(usr.password, self.password.data):
                self.password.errors=('Неверный пароль',)
                return False
            else:
                return True
    
        
