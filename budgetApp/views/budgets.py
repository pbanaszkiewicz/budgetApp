# coding: utf-8

from delorean import Delorean
from flask.ext.restful import Resource, abort, types
from flask.ext.restful.reqparse import RequestParser
from decimal import Decimal

from ..app import DbSession
from ..models import Budget, User
from ..serializers import BudgetSerializer
from .users import abort_no_user

DELOREAN_DT_FORMAT = "%Y/%m/%d %H:%M:%S %z"
DELOREAN_DATE_FORMAT = "%Y/%m/%d"
DELOREAN_TIME_FORMAT = "%H:%M:%S %z"

budget_parser = RequestParser()
budget_parser.add_argument("user_id", required=True, type=int)
budget_parser.add_argument("category", required=True, type=str)
budget_parser.add_argument("description", required=True, type=str)
budget_parser.add_argument("date", type=types.date)
budget_parser.add_argument("value", required=True, type=Decimal)

budget_update_parser = RequestParser()
budget_update_parser.add_argument("user_id", type=int)
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
        abort_no_user(user_id)  # is this really necessary?  Maybe use JOIN?
        result = DbSession.query(Budget).filter_by(user_id=user_id)
        if result:
            return {"budgets": BudgetSerializer(result, many=True).data}
        return 'Not found', 404

    def post(self, user_id):
        """
        Add new budget to the user.  If the user doesn't exist, abort
        with 404.
        """
        abort_no_user(user_id)

        args = budget_parser.parse_args()
        if "date" not in args:
            args["date"] = Delorean().date.strftime(DELOREAN_DATE_FORMAT),
        budget = Budget(args["description"], args["category"], args["date"],
                        args["value"], user_id)
        DbSession.add(budget)
        DbSession.commit()

        return {
            "budget": BudgetSerializer(Budget.query.get(budget.id)).data
        }, 201


def abort_no_budget(budget_id):
    """
    Abort current request if the budget entry is not present in the dabatase.
    """
    DbSession.query(Budget).filter_by(id=budget_id).first_or_404()


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
        budget = DbSession.query(Budget).filter_by(id=budget_id).first_or_404()
        return {"budget": BudgetSerializer(budget).data}

    def put(self, budget_id):
        """
        Update specific budget entry.  If the entry is absent, abort with 404.

        :param budget_id: the id of the sought after budget entry
        :type budget_id: str
        """
        args = budget_update_parser.parse_args()
        budget = DbSession.query(Budget).filter_by(id=budget_id).first_or_404()

        budget.description, budget.category, budget.value, budget.user_id = (
            args["description"], args["category"], args["value"],
            args["user_id"]
        )

        if "date" not in args:
            args["date"] = Delorean().date.strftime(DELOREAN_DATE_FORMAT),
        budget.date = args["date"]

        DbSession.update(budget)
        DbSession.commit()
        return ({"budget": BudgetSerializer(Budget.query.get(budget_id)).data},
                201)

    def delete(self, budget_id):
        """
        Delete specific budget entry.  If the entry doesn't exist, abort with
        404.

        :param budget_id: the id of the sought after budget entry
        :type budget_id: str
        """
        budget = DbSession.query(Budget).filter_by(id=budget_id).first_or_404()
        DbSession.delete(budget)
        DbSession.commit()
        return '', 204
