import logging
from web.server.utils.utils import get_dates_from_request, get_expenses_from_date_to_date


def expense_details_handler():
	try:
		from_date, to_date = get_dates_from_request()
	except RuntimeError:
		return "Invalid Date format", 400

	logging.info("showing expense details from %s to %s" % (from_date, to_date))

	expenses = get_expenses_from_date_to_date(from_date, to_date).all()
	logging.info("sending %d expenses", len(expenses))
	# TODO: filter by telegram users group
	return expenses.to_json()

