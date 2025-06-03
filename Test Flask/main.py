from flask import Flask, render_template, url_for, request, flash, redirect, session, abort
from typing import List, Dict

app = Flask(__name__)
app.secret_key = 'd2f8a1e3c7b6e5f4a9b8c7d6e5f4a3b2'

menu: List[Dict[str, str]] = [
    {'name': 'Главная', 'url': '/'},
    {'name': 'Обо мне', 'url': 'about'},
    {'name': 'Обратная связь', 'url': 'feedback'}
]

@app.route('/')
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)

@app.route('/about')  # Исправлено: добавлен слэш
def about():
    print(url_for('about'))
    return render_template('about.html', title="О сайте", menu=menu)

@app.route("/profile/<username>")
def profile(username):
   if 'userLogged' not in session or session['userLogged'] != username:
      about(401)

   return f"Пользователь: {username}"


@app.route('/login', methods=['POST', 'GET'])
def login():
   if 'userLogged' in session:
      return redirect(url_for('profile', username=session['userLogged']))

   if request.method == 'POST':
      username = request.form.get('username')
      password = request.form.get('pwd')

      if username == "selfedu" and password == '123':
         session['userLogged'] = username
         flash('Вы успешно вошли в систему!', 'success')
         return redirect(url_for('profile', username=session['userLogged']))
      else:
         flash('Неверное имя пользователя или пароль', 'error')

   return render_template('auth.html', title="Авторизация", menu=menu)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
   if request.method == 'POST':
      name = request.form.get('name')
      email = request.form.get('email')
      message = request.form.get('message')

      # Здесь можно добавить обработку данных (отправка на почту, сохранение в БД)
      flash('Сообщение отправлено! Спасибо за обратную связь.', 'success')
      print(f"name: {name}\nemail: {email}\nmessage: {message}")
      return redirect(url_for('feedback'))

   return render_template('feedback.html', menu=menu, title="Обратная связь")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#if __name__ == '__main__':  # Исправлено: двойные подчёркивания
#    app.run(debug=True)