from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def show_time():
    return render_template('time.html')  # Новый шаблон

@app.route('/get_time')
def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    app.run(debug=True)