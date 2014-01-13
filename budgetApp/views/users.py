# coding: utf-8

from flask.ext.restful import Resource
from flask.ext.restful.reqparse import RequestParser

from ..extensions import db
from ..models import User
from ..serializers import UserSerializer


users_parser = RequestParser()
users_parser.add_argument("email", required=True, type=str)
users_parser.add_argument("source", required=True, type=str)
users_parser.add_argument("first_name", required=True, type=str)
users_parser.add_argument("last_name", required=True, type=str)


class UsersList(Resource):
    """
    Endpoint ("/users") for showing the list of all users and for adding them.
    """

    def get(self):
        """
        Return all of the users.
        """
        users = User.query.all()
        return {"users": UserSerializer(users, many=True).data}

    def post(self):
        """
        Take new user, add it to the database and return him/her back.
        """
        args = users_parser.parse_args()
        user = User(args["email"], args["source"], args["first_name"],
                    args["last_name"])
        db.session.add(user)
        db.session.commit()
        print(UserSerializer(User.query.get(2)).data)
        # user = UserSerializer(User.query.get(user.id)).data
        return {"user": UserSerializer(User.query.get(user.id)).data}, 201


def abort_no_user(user_id):
    """
    Abort current request if the user is not present in database.
    """
    User.query.filter_by(id=user_id).first_or_404()


class UserResource(Resource):
    """
    Endpoint ("/users/:user_id:") for getting user's data, altering it and
    removing.
    """

    def get(self, user_id):
        """
        Return particular user.  If he/she doesn't exist, abort with 404.

        :param user_id: the id of the sought after user
        :type user_id: str
        """
        user = User.query.filter_by(id=user_id).first_or_404()
        return {"user": UserSerializer(user).data}

    def put(self, user_id):
        """
        Update particular user.  If he/she doesn't exist, abort with 404.

        :param user_id: the id of the sought after user
        :type user_id: str
        """
        args = users_parser.parse_args()
        user = User.query.filter_by(id=user_id).first_or_404()
        user.email, user.source, user.first_name, user.last_name = (
            args["email"],
            args["source"],
            args["first_name"],
            args["last_name"]
        )
        db.session.update(user)
        db.session.commit()
        return {"user": UserSerializer(user).data}, 201

    def delete(self, user_id):
        """
        Delete particular user.  If he/she doesn't exist, abort with 404.
        Try to delete user's all bugdet entries.

        :param user_id: the id of the sought after user
        :type user_id: str
        """
        user = User.query.filter_by(id=user_id).first_or_404()
        db.session.delete(user)
        db.session.commit()
        return '', 204
