import datetime


def string_to_datetime(date_string: str):
	return datetime.datetime.strptime(date_string, "%d-%m-%Y")