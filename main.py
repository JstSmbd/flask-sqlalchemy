from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms.user import LoginForm, RegisterForm
from forms.job import AddJobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/")
def index():
    if current_user.is_authenticated:
        dbs = db_session.create_session()
        jobs = dbs.query(Jobs).filter((Jobs.collaborators.like(f'% {current_user.id}%')) |
                                      (Jobs.collaborators.like(f'%{current_user.id},%')) |
                                      (Jobs.collaborators == str(current_user.id)))
        return render_template("index.html", jobs=jobs,
                               teams=[", ".join(get_users(job, dbs)) for job in jobs])
    else:
        return redirect('/login')


def get_users(job, dbs):
    users = []
    for u_id in job.collaborators.split(", "):
        ans = dbs.query(User).filter(User.id == int(u_id)).first()
        users.append(f"{ans.surname} {ans.name}")
    return users


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/addjob", methods=['GET', 'POST'])
def addjob():
    form = AddJobForm()
    if form.validate_on_submit():
        dbs = db_session.create_session()
        job = Jobs(
            job=form.job.data,
            team_leader=form.leader_id.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        dbs.add(job)
        dbs.commit()
        return redirect("/")
    return render_template('addjob.html', title='Добавление работы', form=form)


if __name__ == '__main__':
    main()
