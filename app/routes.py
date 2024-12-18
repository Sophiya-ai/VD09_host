from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User
from app.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
#`generate_password_hash` не существует в модуле `bcrypt`.
# Эта функция обычно ассоциируется с библиотекой `werkzeug.security`, а не `bcrypt`
from sqlalchemy.exc import IntegrityError

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    # form.validate_on_submit проверяет, была ли форма отправлена с помощью метода HTTP POST и прошла ли она валидацию.
    # Это удобно, потому что позволяет обработать форму только в том случае,
    # если она была отправлена и все поля формы корректны
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# Создаём маршрут для страницы входа, также обрабатываем методы GET и POST
@app.route('/login', methods=['GET', 'POST'])
def login():
    # `current_user` — это объект, который предоставляет информацию о текущем пользователе, взаимодействующем с приложением
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Введены неверные данные', 'danger')

    return render_template('login.html', form=form)


# Создаём маршрут для выхода из аккаунта.
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/click')
@login_required
def click():
    current_user.clicks += 1
    db.session.commit()
    return redirect(url_for('index'))