from __future__ import absolute_import

from flask import Flask
app = Flask(__name__)
# app.config.from_object("config")

##############
### ROUTES ###
##############
from flask.ext.restful import Api
api = Api(app)

# users
from .views.users import UsersList, UserResource
api.add_resource(UsersList, "/users")
api.add_resource(UserResource, "/users/<string:user_id>")

# Todo routes
from .views.todos import Todo, TodoList
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<string:todo_id>')
