import datetime
import json
import logging
from typing import Tuple, List

from flask import request
from mongoengine import Q

from models import Expense, ensure_db_connection, Category


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


def get_categories_from_request() -> List[Category]:
	category_types = request.args.get('categoryTypes', None)
	category_types = json.loads(category_types)  # convert into a list from string
	logging.info(category_types)
	categories = [c for c in Category.all_categories() if c.type in category_types]
	logging.info(categories)
	return categories


@ensure_db_connection
def get_expenses_from_date_to_date_in_categories(from_date, to_date, categories: List[Category]):
	category_names = [c.name for c in categories]
	return get_expenses_from_date_to_date(from_date, to_date).filter(category__in=category_names)


@ensure_db_connection
def get_expenses_from_date_to_date(from_date, to_date):
	return Expense.objects(Q(date__gte=from_date) & Q(date__lte=to_date))

