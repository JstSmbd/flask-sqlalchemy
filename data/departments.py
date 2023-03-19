import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Departments(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    creator = sqlalchemy.Column(sqlalchemy.Integer)
    user = orm.relationship("User")