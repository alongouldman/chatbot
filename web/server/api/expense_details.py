from flask import request

from models import Expense


def expense_details_handler():
	from_date = request.args.get('fromDate', None)
	to_date = request.args.get('toDate', None)
	if not from_date or not to_date:
		# TODO: return bad response
		pass
	expenses = Expense.objects().all()
	# TODO: filter by telegram users group
	return expenses

