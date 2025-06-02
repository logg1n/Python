# main.py

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html', title="Главная")

@app.route('/about')
def about():
    return render_template('about.html', title="О нас")

if __name__ == '__main__':
    app.run()