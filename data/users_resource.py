from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from .recources_parsers import user_add_parser, user_change_parser
from .users import User
from main import login_required, current_user
from . import db_session


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


def abort_if_bad_change(password):
    if not current_user.check_password(password):
        abort(400, message=f"Bad password for user {current_user.id}")


class UsersResource(Resource):
    # @login_required
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=("id", "surname", "name", "age",
                  "position", "speciality", "address",
                  "email", "modified_date"))})

    # @login_required
    def put(self, user_id):
        args = user_change_parser.parse_args()
        abort_if_user_not_found(user_id)
        # abort_if_bad_change(args["old_password"])
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if arg := args["surname"]:
            user.surname = arg
        if arg := args["name"]:
            user.name = arg
        if arg := args["age"]:
            user.age = arg
        if arg := args["position"]:
            user.position = arg
        if arg := args["speciality"]:
            user.speciality = arg
        if arg := args["email"]:
            user.email = arg
        if arg := args["password"]:
            user.set_password(args["password"])
        session.commit()
        return jsonify({'success': 'OK'})

    # @login_required
    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    # @login_required
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=("id", "surname", "name", "age",
                  "position", "speciality", "address",
                  "email", "modified_date")) for item in users]})

    # @login_required
    def post(self):
        args = user_add_parser.parse_args()
        session = db_session.create_session()
        if session.query(User).filter(User.email == args["email"]).first():
            abort(400, message=f"Email already exists")
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            email=args['email']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
