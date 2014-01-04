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

# users' budgets
from .views.budgets import UsersBudgetList
api.add_resource(UsersBudgetList, "/users/<string:user_id>/budget")

# budgets
from .views.budgets import BudgetResource
api.add_resource(BudgetResource, "/budget/<string:budget_id>")
