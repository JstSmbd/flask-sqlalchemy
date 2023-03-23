from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from .recources_parsers import job_change_parser, job_add_parser
from .jobs import Jobs
from main import login_required, current_user
from . import db_session


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


def abort_if_bad_change(job):
    if current_user.id not in (job_id, 1, job.creator):
        abort(400, message=f"Bad Request")


class JobsResource(Resource):
    # @login_required
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=("id", "team_leader", "job", "work_size", "collaborators",
                  "start_date", "end_date", "is_finished", "creator",
                  "user.surname", "user.name", "user.id", "user.age",
                  "user.position", "user.speciality", "user.address",
                  "user.email", "user.modified_date"))})

    # @login_required
    def put(self, job_id):
        args = job_change_parser.parse_args()
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        # abort_if_bad_change(job)
        if arg := args["job"]:
            job.job = arg
        if arg := args["team_leader"]:
            job.team_leader = arg
        if arg := args["work_size"]:
            job.work_size = arg
        if arg := args["collaborators"]:
            job.collaborators = arg
        if arg := args["is_finished"]:
            job.is_finished = arg
        session.commit()
        return jsonify({'success': 'OK'})

    # @login_required
    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        # abort_if_bad_change(job)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    # @login_required
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=("id", "team_leader", "job", "work_size", "collaborators",
                  "start_date", "end_date", "is_finished", "creator",
                  "user.surname", "user.name", "user.id", "user.age",
                  "user.position", "user.speciality", "user.address",
                  "user.email", "user.modified_date")) for item in jobs]})

    # @login_required
    def post(self):
        args = job_add_parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            job=args['job'],
            team_leader=args['team_leader'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],
            # creator=current_user.id
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})
