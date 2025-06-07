from flask import Flask, session, g

from users_model import db  # Импортируем db из моделей
from routes import init_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Инициализация базы данных
    db.init_app(app)

    # Импорт и инициализация маршрутов
    init_routes(app, db)

    # Создание таблиц
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

