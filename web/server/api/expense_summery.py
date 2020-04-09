import datetime
import logging

import pandas as pd

from models import Category, CategoryType
from web.server.utils.utils import get_dates_from_request, get_expenses_from_date_to_date


def expense_summery_handler():
	try:
		from_date, to_date = get_dates_from_request()
	except RuntimeError:
		return "Invalid Date format", 400

	logging.info("showing expense details from %s to %s" % (from_date, to_date))
	
	expenses = get_expenses_from_date_to_date(datetime.datetime(datetime.datetime.today().year, 1, 1), datetime.datetime.today())
	categories = Category.all_categories()
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

	df = pd.DataFrame(expenses_as_dicts)
	df['month'] = pd.to_datetime(df['date']).dt.strftime('%m')

	# order the types in the order that I want
	df["category_type"] = df["category_type"].astype(
		pd.api.types.CategoricalDtype(
			categories=[CategoryType.INCOME, CategoryType.VITAL_AND_REOCCURING, CategoryType.VITAL_AND_CHANGES,
			            CategoryType.UNNECESSARY_AND_REOCCURING, CategoryType.UNNECESSARY_AND_CHANGES,
			            CategoryType.STUDY, CategoryType.INVESTMENT]))

	df_pivot = df.pivot_table(index='month', columns=['category_type', 'category'], aggfunc=sum, fill_value=0, values="amount").T
	df_pivot['average'] = df_pivot.mean(numeric_only=True, axis=1)
	return df_pivot.reset_index().to_json(orient='records')


