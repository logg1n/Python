from flask import render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from users_model import User
from quotes.ninjasQ import Ninjas

def init_routes(app, db):
    ninjas = Ninjas()

    @app.route('/')
    def quotes():
        raw_quote = ninjas.quote()

        return render_template('quotes.html', quote=raw_quote['quote'], author = raw_quote['author'])

    @app.route('/new-quote')
    def new_quote():
        raw_quote = ninjas.quote()

        return redirect(url_for('quotes',  quote=raw_quote['quote'], author = raw_quote['author']))

    @app.route('/auth', methods=['POST', 'GET'])
    def auth():
        print("Request method:", request.method)
        print("Form data:", request.form)


        if request.method == 'POST':
            print("Form data:", request.form)
            username = request.form.get('login')
            password = request.form.get('password')
            print(f"Received username: {username}, password: {password}")

            if not username or not password:
                flash('Заполните все поля', 'error')
                return redirect(url_for('quotes'))

            user = User.query.filter_by(username=username).first()

            if request.form.get('sign-in'):  # Обработка входа
                if user and check_password_hash(user.password, password):
                    session['userLogged'] = username
                    flash('Вы успешно вошли в систему!', 'success')
                    return redirect(url_for('profile', username=username))
                else:
                    flash('Неверное имя пользователя или пароль', 'error')

            elif request.form.get('sign-up'):  # Обработка регистрации
                if not user:
                    try:
                        hashed_password = generate_password_hash(password)
                        new_user = User(username=username, password=hashed_password)
                        db.session.add(new_user)
                        db.session.commit()
                        session['userLogged'] = username
                        flash('Вы успешно зарегистрировались!', 'success')
                        return redirect(url_for('profile', username=username))
                    except Exception as e:
                        db.session.rollback()
                        flash(f'Ошибка при регистрации: {str(e)}', 'error')
                else:
                    flash('Такой пользователь уже существует', 'error')

        return render_template('auth.html', title="Авторизация")

    @app.route('/about', methods=['GET', 'POST'])
    def about():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')

            if name and email and message:
                flash(f'Сообщение отправлено! Спасибо за обратную связь - {name}.', 'success')
                return redirect(url_for('about'))

        return render_template('about.html', title="О нас")

    @app.route("/profile/<username>")
    def profile(username):
        # Проверяем, что пользователь авторизован
        if 'userLogged' not in session or session['userLogged'] != username:
            abort(401)  # Если нет - ошибка доступа

        # Передаём логин в шаблон
        return render_template("profile.html", login=username)

    @app.route('/change-username', methods=['GET', 'POST'])
    def change_username():
        # Проверяем авторизацию пользователя
        if 'userLogged' not in session:
            flash('Пожалуйста, войдите в систему', 'error')
            return redirect(url_for('quotes'))

            # Обработка GET-запроса (показ формы)
        if request.method == 'GET':
            return render_template('change_username.html',
                                   username=session['userLogged'])

        if request.method == 'POST':
            current_username = session['userLogged']  # Берем текущее имя из сессии
            new_username = request.form.get('new_username')

            # Проверяем, что новое имя не пустое
            if not new_username:
                flash('Введите новое имя пользователя', 'error')
                return redirect(url_for('profile', username=current_username))

            # Проверяем, что новое имя не занято
            if User.query.filter_by(username=new_username).first():
                flash('Это имя пользователя уже занято', 'error')
                return redirect(url_for('profile', username=current_username))

            # Обновляем имя пользователя
            user = User.query.filter_by(username=current_username).first()
            if user:
                user.username = new_username
                session['userLogged'] = new_username  # Обновляем сессию
                db.session.commit()
                flash('Имя пользователя успешно изменено!', 'success')
            else:
                flash('Пользователь не найден!', 'error')

        return redirect(url_for('profile', username=session['userLogged']))


    @app.route('/change-password', methods=['GET', 'POST'])
    def change_password():
        if 'userLogged' not in session:
            flash('Вы должны войти в систему!', 'error')
            return redirect(url_for('quotes'))

        if request.method == 'GET':
            return render_template('change_psw.html',
                                   username=session['userLogged'])

        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        user = User.query.filter_by(username=session['userLogged']).first()

        if not user or not check_password_hash(user.password, current_password):
            flash('Неверный текущий пароль!', 'error')
            return redirect(url_for('profile', username=session['userLogged']))

        if new_password != confirm_password:
            flash('Новый пароль и подтверждение не совпадают!', 'error')
            return redirect(url_for('profile', username=session['userLogged']))

        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Пароль успешно изменён!', 'success')

        return redirect(url_for('profile', username=session['userLogged']))

    @app.route('/logout')
    def logout():
        # Очищаем сессию
        session.pop('userLogged', None)
        flash('Вы успешно вышли из системы', 'success')
        return redirect(url_for('quotes'))
