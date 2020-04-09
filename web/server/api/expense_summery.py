import datetime
import logging

import pandas as pd
from dateutil import rrule
from flask import request

from models import Category, CategoryType
from web.server.utils.utils import get_dates_from_request, get_categories_from_request, \
	get_expenses_from_date_to_date_in_categories


def expense_summery_handler():
	try:
		from_date, to_date = get_dates_from_request()
	except RuntimeError:
		return "Invalid Date format", 400

	logging.info("showing expense details from %s to %s" % (from_date, to_date))

	categories = get_categories_from_request()
	expenses = get_expenses_from_date_to_date_in_categories(from_date, to_date, categories).all()
	expenses_as_dicts = []
	for expense in expenses:
		expense_dict = {
			'amount': expense.amount,
			'category': expense.category,
			'date': expense.date,
			'category_type': next(cat.type for cat in categories if cat.name == expense.category)
		}
		expenses_as_dicts.append(expense_dict)

	# this is a hack to get all the categories to show up - even if there was no expense in the category
	for category in categories:
		expense_dict = {
			'amount': 0,
			'category': category.name,
			'date': from_date,
			'category_type': category.type
		}
		expenses_as_dicts.append(expense_dict)

	# this is a hack to get all the months to show up - even if there was no expense in the month
	for date in rrule.rrule(rrule.MONTHLY, dtstart=from_date, until=to_date):
		expense_dict = {
			'amount': 0,
			'category': categories[0].name,
			'date': date,
			'category_type': categories[0].type
		}
		expenses_as_dicts.append(expense_dict)

	df = pd.DataFrame(expenses_as_dicts)
	df['month'] = pd.to_datetime(df['date']).dt.strftime('%m')

	# order the types in the order that I want
	df["category_type"] = df["category_type"].astype(
		pd.api.types.CategoricalDtype(
			categories=[CategoryType.INCOME, CategoryType.VITAL_AND_REOCCURING, CategoryType.VITAL_AND_CHANGES,
						CategoryType.UNNECESSARY_AND_REOCCURING, CategoryType.UNNECESSARY_AND_CHANGES,
						CategoryType.STUDY, CategoryType.INVESTMENT]))

	df_pivot = df.pivot_table(index='month', columns=['category_type', 'category'], aggfunc=sum, fill_value=0, values="amount", margins=True, margins_name='Total').T
	df_pivot = df_pivot.drop(df_pivot.columns[len(df_pivot.columns) - 1], axis=1)  # drop the total of the columns
	df_pivot['average'] = df_pivot.mean(numeric_only=True, axis=1)
	return df_pivot.reset_index().to_json(orient='records')


