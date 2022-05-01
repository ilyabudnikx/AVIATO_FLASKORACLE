from flask import Flask, render_template, url_for

app = Flask(__name__)

menu = [{"title": "Главная", "url": "/"},
        {"title": "Билеты", "url": "tickets"},
        {"title": "Новости", "url": "news"},
        {"title": "Страница пользователя", "url": "user"},
        {"title": "Обратная связь", "url": "feedback"}, ]


@app.route('/')
def index():  # put application's code here
    print(url_for('index'))
    return render_template('index.html', title='AVIATO - Главная страница', menu=menu)


@app.route('/tickets')
def tickets():
    print(url_for('tickets'))
    return render_template('tickets.html', title='AVIATO - Билеты', menu=menu)


@app.route('/news')
def news():
    print(url_for('news'))
    return render_template('news.html', title='AVIATO - Новости', menu=menu)


@app.route('/user')
def user():
    print(url_for('user'))
    return render_template('user.html', title='AVIATO - Билеты', menu=menu)


@app.route('/feedback')
def feedback():
    print(url_for('feedback'))
    return render_template('feedback.html', title='AVIATO - Обратная связь', menu=menu)


if __name__ == '__main__':
    app.run()
