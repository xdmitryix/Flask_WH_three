# Создать форму для регистрации пользователей на сайте.
# Форма должна со держать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
# При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.

from flask import Flask, render_template, redirect, request, url_for
from hashlib import sha256
from flask_wtf.csrf import CSRFProtect
from form import RegisterForm
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forms.db'
app.config['SECRET_KEY'] = b'32hk4g432543jk3l5hkh53h24223ji56igj4n4d'
csrf = CSRFProtect(app)
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=sha256(form.password.data.encode(encoding='utf-8')).hexdigest())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('/index.html', form=form)

@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('ok')

@app.cli.command('add_data')
def add_data():
    count = 4
    for i in range(1, count+1):
        user = User(first_name=f'user_firstname{i}',
                    last_name=f'user_lastname{i}',
                    email=f'useremail{i}@mail.ru',
                    password=f'userpass{i}')
        db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)