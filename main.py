from flask import Flask, render_template, redirect, make_response, jsonify
from data import db_session
from data.departments import Departments
from data.users import User
from data.jobs import Jobs
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms.user import LoginForm, RegisterForm
from forms.job import AddChangeJobForm
from forms.department import AddChangeDepartmentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

from data import jobs_api, users_api


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def empty_page():
    return redirect("/login")


@app.route('/register', methods=['GET', 'POST'])
def register():
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/jobs")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)
    return redirect("/jobs")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/jobs")
@login_required
def jobs():
    dbs = db_session.create_session()
    if current_user.id != 1:
        jobs = dbs.query(Jobs).filter((Jobs.collaborators.like(f'% {current_user.id}%')) |
                                      (Jobs.collaborators.like(f'%{current_user.id},%')) |
                                      (Jobs.collaborators == str(current_user.id)) |
                                      (Jobs.creator == current_user.id))
    else:
        jobs = dbs.query(Jobs)
    return render_template("jobs.html", jobs=jobs,
                           teams=[", ".join(get_users(job, dbs)) for job in jobs],
                           title="Работы")


@app.route("/add_job", methods=["GET", "POST"])
@login_required
def add_job():
    form = AddChangeJobForm()
    if form.validate_on_submit():
        dbs = db_session.create_session()
        job = Jobs(
            job=form.job.data,
            team_leader=form.leader_id.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
            creator=current_user.id
        )
        dbs.add(job)
        dbs.commit()
        return redirect("/jobs")
    return render_template('AddChangeJob.html', title='Добавление работы', form=form)


@app.route("/change_job/<int:j_id>", methods=['GET', 'POST'])
@login_required
def change_job(j_id):
    dbs = db_session.create_session()
    job = dbs.query(Jobs).filter(Jobs.id == j_id).first()
    form = AddChangeJobForm()
    if form.validate_on_submit() and current_user.id in (1, job.creator,
                                                         (job.user.id if job.user else 1)):
        job.job = form.job.data
        job.team_leader = form.leader_id.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        dbs.commit()
        return redirect("/jobs")
    elif current_user.id in (1, job.creator, (job.user.id if job.user else 1)):
        return render_template('AddChangeJob.html', title='Добавление работы', form=form, job={
            "job": job.job,
            "leader_id": job.team_leader,
            "work_size": job.work_size,
            "collaborators": job.collaborators,
            "checkbox": job.is_finished
        })
    return redirect("/jobs")


@app.route("/delete_job/<int:j_id>")
@login_required
def delete_job(j_id):
    dbs = db_session.create_session()
    job = dbs.query(Jobs).filter(Jobs.id == j_id).first()
    if current_user.id in (1, job.creator, (job.user.id if job.user else 1)):
        dbs.delete(job)
        dbs.commit()
    return redirect("/jobs")


@app.route("/departments")
@login_required
def departments():
    dbs = db_session.create_session()
    if current_user.id != 1:
        deps = dbs.query(Departments). \
            filter((Departments.collaborators.like(f'% {current_user.id}%')) |
                   (Departments.collaborators.like(f'%{current_user.id},%')) |
                   (Departments.collaborators == str(current_user.id)) |
                   (Departments.creator == current_user.id))
    else:
        deps = dbs.query(Departments)
    return render_template("departments.html", deps=deps,
                           teams=[", ".join(get_users(dep, dbs)) for dep in deps],
                           title="Департаменты")


@app.route("/add_department", methods=["GET", "POST"])
@login_required
def add_department():
    form = AddChangeDepartmentForm()
    if form.validate_on_submit():
        dbs = db_session.create_session()
        dep = Departments(
            title=form.dep.data,
            chief=form.chief.data,
            collaborators=form.collaborators.data,
            creator=current_user.id,
            email=form.email.data
        )
        dbs.add(dep)
        dbs.commit()
        return redirect("/departments")
    return render_template('AddChangeDepartment.html', title='Добавление департамента', form=form)


@app.route("/change_department/<int:d_id>", methods=['GET', 'POST'])
@login_required
def change_department(d_id):
    dbs = db_session.create_session()
    dep = dbs.query(Departments).filter(Departments.id == d_id).first()
    form = AddChangeDepartmentForm()
    if form.validate_on_submit() and current_user.id in (1, dep.creator,
                                                         (dep.user.id if dep.user else 1)):
        dep.title = form.dep.data
        dep.chief = form.chief.data
        dep.collaborators = form.collaborators.data
        dep.email = form.email.data
        dbs.commit()
        return redirect("/departments")
    elif current_user.id in (1, dep.creator, (dep.user.id if dep.user else 1)):
        return render_template('AddChangeDepartment.html', title='Добавление департамента',
                               form=form,
                               dep={
                                   "dep": dep.title,
                                   "chief": dep.chief,
                                   "collaborators": dep.collaborators,
                                   "email": dep.email
                               })
    return redirect("/departments")


@app.route("/delete_department/<int:d_id>")
@login_required
def delete_department(d_id):
    dbs = db_session.create_session()
    dep = dbs.query(Departments).filter(Departments.id == d_id).first()
    if current_user.id in (1, dep.creator, (dep.user.id if dep.user else 1)):
        dbs.delete(dep)
        dbs.commit()
    return redirect("/departments")


def get_users(storage, dbs):
    users = []
    for u_id in storage.collaborators.split(", "):
        try:
            ans = dbs.query(User).filter(User.id == int(u_id)).first()
            users.append(f"{ans.surname} {ans.name}")
        except (AttributeError, ValueError):
            users.append("Неизвестно Кто")
    return users


if __name__ == '__main__':
    main()
