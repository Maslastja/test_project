from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Логин', 
                           validators=[DataRequired('поле не заполнено')])
    password = PasswordField('Пароль', 
                             validators=[DataRequired('поле не заполнено')])
    submit = SubmitField('Войти')
