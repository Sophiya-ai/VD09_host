from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#Создаём приложение и настраиваем базу данных:
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clicker.db'
db = SQLAlchemy(app)

#Создаём объект LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# Модуль будет перенаправлять пользователя на маршрут, который мы указываем (на авторизацию)

from app import routes, models
