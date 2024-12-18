from app import db
from app import login_manager
from flask_login import UserMixin # Этот класс даёт возможность работать с пользователем,
# можно узнать авторизирован ли пользователь, получать его идентификатор и т д

#Создаём класс и колонки базы данных
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    clicks = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'User {self.username} - clicks: {self.clicks}'

#декоратор, который сообщает Flask, что функция будет использоваться для загрузки
# пользователя по его ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # Эта строчка будет отправлять в БД запрос для поиска определённого юзера по его ID


