import flask
from flask import jsonify, make_response, request
from . import db_session
from .users import User
from main import app, current_user, login_required

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
# @login_required
def get_users():
    dbs = db_session.create_session()
    users = dbs.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=("id", "surname", "name", "age",
                                    "position", "speciality", "address",
                                    "email", "modified_date"))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
# @login_required
def get_one_user(user_id):
    dbs = db_session.create_session()
    user = dbs.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Bad Request'})
    return jsonify(
        {
            'user': user.to_dict(only=(
                "id", "surname", "name", "age",
                "position", "speciality", "address",
                "email", "modified_date"))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
# @login_required
def create_user():
    dbs = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key[0] in request.json and key[1] == type(request.json[key[0]]) for key in
                 [['email', str], ['password', str], ['name', str],
                  ['surname', str], ["age", int], ["position", str], ["speciality", str]]):
        return jsonify({'error': 'Bad request'})
    elif dbs.query(User).filter(User.email == request.json["email"]).first():
        return jsonify({'error': 'Email already exists'})
    user = User(
        name=request.json['name'],
        surname=request.json['surname'],
        email=request.json['email'],
        age=request.json['age'],
        position=request.json["position"],
        speciality=request.json["speciality"]
    )
    user.set_password(request.json["password"])
    dbs.add(user)
    dbs.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
# @login_required
def delete_user(user_id):
    dbs = db_session.create_session()
    user = dbs.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Bad Request'})
    dbs.delete(user)
    dbs.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
# @login_required
def change_user(user_id):
    dbs = db_session.create_session()
    user = dbs.query(User).filter(User.id == user_id).first()
    try:
        if not all([type(request.json[key]) == {"job": str, "team_leader": int, "work_size": int,
                                                "collaborators": str, "is_finished": bool}.get(key, type(request.json[key]))
                    for key in request.json]) or not user:
            return jsonify({'error': 'Bad request'})
        if dbs.query(User).filter(User.email == request.json["email"], User.id != user_id).first():
            return jsonify({'error': 'Email already exists'})
        user.name = request.json.get("name", user.name)
        user.surname = request.json.get("surname", user.surname)
        user.email = request.json.get("email", user.email)
        user.position = request.json.get("position", user.position)
        user.speciality = request.json.get("speciality", user.speciality)
        user.age = request.json.get("age", user.age)
    except KeyError:
        return jsonify({'error': 'Bad request'})
    dbs.commit()
    return jsonify({'success': 'OK'})
