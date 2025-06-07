from flask_sqlalchemy import SQLAlchemy

# Единый экземпляр SQLAlchemy для всего приложения
db = SQLAlchemy()


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(120), nullable=False)  # Добавьте хеш пароля

	def __repr__(self):
		return f'<User {self.username}>'