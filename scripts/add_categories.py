import os
import pandas

from models import Category, session, CategoryType


def get_categories_from_csv():
	df = pandas.read_csv('initial_categories.csv')
	with session():
		unknown_category = Category(CategoryType.UNKNOWN, type=CategoryType.UNKNOWN)
		unknown_category.save()

		for index, row in df.iterrows():
			category = Category()
			category.name = row['name']
			category.type = row['type']
			category.save()
			print(f'category {category} saved')


if __name__ == "__main__":
	csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'initial_categories.csv')
	get_categories_from_csv()
