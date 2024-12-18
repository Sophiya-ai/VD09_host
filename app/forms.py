from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from sqlalchemy.exc import IntegrityError
#EqualTo нужен для того, чтобы сравнивать значения в полях и узнавать, точно ли они одинаковые

#Импортируем модель User из нашего модуля
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', default='', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', default='', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', default='', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')


    #Создаём функции для проверки уникальности имени пользователя и почты
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такое имя уже существует.') #raise для генерации исключений похожее на try-except

#Создание класса LoginForm
class LoginForm(FlaskForm):
    username = StringField('Username', default='', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Вход')
