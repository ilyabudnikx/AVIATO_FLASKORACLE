import datetime
import random

from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
import cx_Oracle
import senderEmail
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asjdasdkajsdh3u98qudwdh__'
app.permanent_session_lifetime = datetime.timedelta(days=1)

def connection():
    h = 'localhost'
    p = '1521'
    sid = 'orcl'
    u = 'dj_dbuser'
    pw = 'Bulka1987ss'
    d = cx_Oracle.makedsn(h, p, sid=sid)
    conn = cx_Oracle.connect(user = u, password = pw, dsn=d)
    return conn

menu = [{"title": "Главная", "url": "/"},
        {"title": "Билеты", "url": "tickets"},
        {"title": "Новости", "url": "news"},
        {"title": "Страница пользователя", "url": "user"},
        {"title": "Обратная связь", "url": "feedback"},
        {"title": "Вход", "url": "login"}]

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
    news = []

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NEWS")
    for row in cursor.fetchall():
        news.append({"Title": row[0], "Date": row[1], "Photo": row[2], "Publ": row[3], "Text": row[4], "Category": row[5]})
    print(news)
    conn.close()
    print(url_for('news'))
    return render_template('news.html', title='AVIATO - Новости', menu=menu, news=news)

@app.route('/user')
def user():
    print(url_for('user'))
    return render_template('user.html', title='AVIATO - Билеты', menu=menu)



@app.route('/login', methods = ["POST", "GET"])
def login():
    conn = connection()
    cursor = conn.cursor()
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == "POST" and request.form['username'] == 'ilyabudnikxs'  and request.form['password'] == "Bulka1987ss" :
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    conn.close()
    return render_template('login.html', title = 'AVIATO - Вход', menu=menu)





@app.route('/feedback', methods=["POST", "GET"])
def feedback():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено.', category = 'alert-success')
            rand_id = random.randrange(1,1000000)
            print(senderEmail.send_email(request.form['text'], request.form['email'], request.form['username'], rand_id))
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO LOG_FEEDBACK VALUES (:username, :email, :text, :id, :time)", [request.form['username'], request.form['email'], request.form['text'], rand_id, datetime.datetime.now()])
            conn.commit()
            conn.close()
        else:
            flash('Ошибка отправки.', category = 'alert-danger')
    print(url_for('feedback'))
    return render_template('feedback.html', title='AVIATO - Обратная связь', menu=menu)

@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Профиль {username}"

@app.route("/add_news", methods=["POST", "GET"])
def add_news():
    if request.method == 'POST':
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO NEWS VALUES(:TITLE, :DATA_APPROACH, :PHOTO, :IS_PUBLISHED, :TEXT_NEWS, :CATEGORY)", [request.form['title'], datetime.datetime.now(), request.form['photo'], 1, request.form['text_news'], request.form['category']])
        conn.commit()
        conn.close()
    return render_template("add_news.html", title='AVIATO - Добавление новостей', menu=menu)


if __name__ == '__main__':
    app.run()
