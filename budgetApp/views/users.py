# coding: utf-8

from flask.ext.restful import Resource, abort
from flask.ext.restful.reqparse import RequestParser

USERS = {
    'user1': {"name": "Piotr"},
    'user2': {"name": "Agata"},
    'user3': {"name": "Jan Nowak"},
}


users_parser = RequestParser()
users_parser.add_argument("name", required=True, type=str)


class UsersList(Resource):
    """
    Endpoint ("/users") for showing the list of all users and for adding them.
    """

    def get(self):
        """
        Return the list of all users.
        """
        return USERS

    def post(self):
        """
        Take new user, add it to the list and return him/her back.
        """
        args = users_parser.parse_args()
        user_id = "user{}".format(len(USERS) + 1)
        USERS[user_id] = {"name": args["name"]}
        return USERS[user_id], 201


def abort_no_user(user_id):
    """
    Abort current request if the user is not present in database.
    """
    if user_id not in USERS:
        abort(404, message="User {} doesn't exist".format(user_id))


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
        abort_no_user(user_id)
        return USERS[user_id]

    def put(self, user_id):
        """
        Update particular user.  If he/she doesn't exist, abort with 404.

        :param user_id: the id of the sought after user
        :type user_id: str
        """
        abort_no_user(user_id)
        args = users_parser.parse_args()
        USERS[user_id] = {"name": args["name"]}
        return USERS[user_id], 201

    def delete(self, user_id):
        """
        Delete particular user.  If he/she doesn't exist, abort with 404.

        :param user_id: the id of the sought after user
        :type user_id: str
        """
        abort_no_user(user_id)
        del USERS[user_id]
        return '', 204
