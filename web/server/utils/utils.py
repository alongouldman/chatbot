import datetime
from typing import Tuple

from flask import request
from mongoengine import Q

from models import Expense, ensure_db_connection


def string_to_datetime(date_string: str):
	return datetime.datetime.strptime(date_string, "%d-%m-%Y")


def get_dates_from_request() -> Tuple[datetime.datetime, datetime.datetime]:
	from_date = request.args.get('fromDate', None)
	to_date = request.args.get('toDate', None)

	if not from_date or not to_date:
		raise RuntimeError

	from_date = string_to_datetime(from_date)
	to_date = string_to_datetime(to_date)
	return from_date, to_date


@ensure_db_connection
def get_expenses_from_date_to_date(from_date, to_date):
	return Expense.objects(Q(date__gte=from_date) & Q(date__lte=to_date)).all()
