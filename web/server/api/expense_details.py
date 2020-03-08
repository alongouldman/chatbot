import logging
from flask import request
from mongoengine import Q

from models import Expense, ensure_db_connection
from web.server.utils.utils import string_to_datetime


@ensure_db_connection
def expense_details_handler():
	from_date = request.args.get('fromDate', None)
	to_date = request.args.get('toDate', None)

	if not from_date or not to_date:
		return "Invalid Date format", 400

	from_date = string_to_datetime(from_date)
	to_date = string_to_datetime(to_date)
	logging.info("showing expense details from %s to %s" % (from_date, to_date))

	expenses = Expense.objects(Q(date__gte=from_date) & Q(date__lte=to_date)).all()
	logging.info("sending %d expenses", len(expenses))
	# TODO: filter by telegram users group
	return expenses.to_json()

