import os
import pandas
from models import Category, CategoryType, ensure_db_connection


@ensure_db_connection
def get_categories_from_csv():
	df = pandas.read_csv('initial_categories.csv')
	unknown_category = Category(CategoryType.UNKNOWN, type=CategoryType.UNKNOWN)
	unknown_category.save()

	for index, row in df.iterrows():
		category = Category()
		category.name = row['name']
		category.type = row['type']
		if category.exists():
			print(f"category {category} already exists, skipping")
			continue
		else:
			category.save()
		print(f'category {category} saved')


def main():
	csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'initial_categories.csv')
	get_categories_from_csv()


if __name__ == "__main__":
	main()

