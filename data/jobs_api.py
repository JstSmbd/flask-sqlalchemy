import flask
from flask import jsonify, make_response, request
from . import db_session
from .jobs import Jobs
from main import app, current_user, login_required

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
# @login_required
def get_jobs():
    dbs = db_session.create_session()
    jobs = dbs.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=("id", "team_leader", "job", "work_size", "collaborators",
                                    "start_date", "end_date", "is_finished", "creator",
                                    "user.surname", "user.name", "user.id", "user.age",
                                    "user.position", "user.speciality", "user.address",
                                    "user.email", "user.modified_date"))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
# @login_required
def get_one_job(job_id):
    dbs = db_session.create_session()
    job = dbs.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Bad Request'})
    return jsonify(
        {
            'job': job.to_dict(only=(
                "id", "team_leader", "job", "work_size", "collaborators",
                "start_date", "end_date", "is_finished", "creator",
                "user.surname", "user.name", "user.id", "user.age",
                "user.position", "user.speciality", "user.address",
                "user.email", "user.modified_date"))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
# @login_required
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key[0] in request.json and key[1] == type(request.json[key[0]]) for key in
                 [["id", int], ['job', str], ['team_leader', int], ['work_size', int],
                  ['collaborators', str], ["is_finished", bool]]):
        return jsonify({'error': 'Bad request'})
    dbs = db_session.create_session()
    if dbs.query(Jobs).filter(Jobs.id == request.json["id"]).first():
        return jsonify({'error': 'Id already exists'})
    job = Jobs(
        id=request.json["id"],
        # но разве id не должен устанавливаться автоматически?
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json["is_finished"]
        # creator=current_user.id
    )
    dbs.add(job)
    dbs.commit()
    return jsonify({'success': 'OK'})
