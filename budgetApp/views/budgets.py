# coding: utf-8

from delorean import Delorean
from flask.ext.restful import Resource, abort, types
from flask.ext.restful.reqparse import RequestParser
from decimal import Decimal
from .users import abort_no_user

DELOREAN_DT_FORMAT = "%Y/%m/%d %H:%M:%S %z"
DELOREAN_DATE_FORMAT = "%Y/%m/%d"
DELOREAN_TIME_FORMAT = "%H:%M:%S %z"

BUDGETS = {
    "budget1":
    {
        "user": "user1",
        "category": "cinema",
        "description": "Scary Movie 5",
        "date": Delorean().date,
        "value": Decimal("60.0"),
    },
}


budget_parser = RequestParser()
budget_parser.add_argument("user", required=True, type=str)
budget_parser.add_argument("category", required=True, type=str)
budget_parser.add_argument("description", required=True, type=str)
budget_parser.add_argument("date", type=types.date)
budget_parser.add_argument("value", required=True, type=Decimal)

budget_update_parser = RequestParser()
budget_update_parser.add_argument("user", type=str)
budget_update_parser.add_argument("category", type=str)
budget_update_parser.add_argument("description", type=str)
budget_update_parser.add_argument("date", type=types.date)
budget_update_parser.add_argument("value", type=Decimal)


class UsersBudgetList(Resource):
    """
    Endpoint ("/users/{id}/budget") for showing the budget list of specified
    user and for adding new budgets to that list.
    """

    def get(self, user_id):
        """
        Return the list of user's bugdets.  If the user doesn't exist, abort
        with 404.  If no budgets for the user are found, return empty list.
        """
        abort_no_user(user_id)
        result = {}
        for budget_id, budget in BUDGETS.items():
            if budget["user"] == user_id:
                result[budget_id] = budget
        return result or ('Not found', 404)

    def post(self, user_id):
        """
        Add new budget to the user.  If the user doesn't exist, abort
        with 404.
        """
        abort_no_user(user_id)

        args = budget_parser.parse_args()
        if "date" not in args:
            args["date"] = Delorean().date.strftime(DELOREAN_DATE_FORMAT),
        budget = {"user": user_id}
        budget.update(args)

        budget_id = "budget{}".format(len(BUDGETS) + 1)
        BUDGETS[budget_id] = budget
        return budget, 201


def abort_no_budget(budget_id):
    """
    Abort current request if the budget entry is not present in the dabatase.
    """
    if budget_id not in BUDGETS:
        abort(404, message="Budget {} doesn't exist".format(budget_id))


class BudgetResource(Resource):
    """
    Endpoint ("/budget/:budget_id:") for showing, altering or removing specific
    budget entries.
    """

    def get(self, budget_id):
        """
        Return specific budget entry.  If it's not present, abort with 404.

        :param budget_id: the id of the sought after budget entry
        :type budget_id: str
        """
        abort_no_budget(budget_id)
        return BUDGETS[budget_id]

    def put(self, budget_id):
        """
        Update specific budget entry.  If the entry is absent, abort with 404.

        :param budget_id: the id of the sought after budget entry
        :type budget_id: str
        """
        abort_no_budget(budget_id)

        args = budget_update_parser.parse_args()
        # if "date" not in args:
        #     args["date"] = Delorean().date.strftime(DELOREAN_DATE_FORMAT),
        budget = BUDGETS[budget_id]
        budget.update(args)
        BUDGETS[budget_id] = budget
        return budget, 201

    def delete(self, budget_id):
        """
        Delete specific budget entry.  If the entry doesn't exist, abort with
        404.

        :param budget_id: the id of the sought after budget entry
        :type budget_id: str
        """
        abort_no_budget(budget_id)
        del BUDGETS[budget_id]
        return '', 204
