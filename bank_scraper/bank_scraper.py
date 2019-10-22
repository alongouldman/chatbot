

from pages.home_page import BankHomePage


def get_expenses_data_from_bank():
	home = BankHomePage()
	main_menu = home.login()
	expenses = main_menu.cashflow_page.get_cashflow()
	# expenses = main_menu.transactions_details_page.get_last_transactions()
	# expenses.append(main_menu.transfers_from_account_page.get_transfers())
	# expenses.append(main_menu.transfers_to_account_page.get_transfers())
	# expenses.append(main_menu.checks_page.get_checks_details())
	return expenses


if __name__ == "__main__":
	get_expenses_data_from_bank()
