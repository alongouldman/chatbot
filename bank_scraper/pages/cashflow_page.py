from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from models import Expense, ExpenseType
from pages.base_page import BasePage
from scraper_utils import string_to_float


class CashflowPage(BasePage):
	def __init__(self, driver: WebDriver):
		super().__init__(driver)

	TEXT_ON_LINK = (By.LINK_TEXT, 'תנועות בחשבון')
	TABLE = (By.ID, 'dataTable077')
	TABLE_BODY = (By.TAG_NAME, 'tbody')
	TABLE_ROWS = (By.TAG_NAME, 'tr')
	ROW_DETAILS = (By.CLASS_NAME, 'reference')
	EXPENSE_DATE = (By.CLASS_NAME, 'date')
	EXPENSE_DETAILS = (By.CLASS_NAME, 'reference')
	EXPENSE_DEBIT = (By.CLASS_NAME, 'debit')
	EXPENSE_CREDIT = (By.CLASS_NAME, 'credit')

	def navigate(self):
		self.driver.find_element(*self.TEXT_ON_LINK).click()

	@BasePage.trigger_navigate
	def get_cashflow(self):
		table = self.driver.find_element(*self.TABLE)
		rows = table.find_element(*self.TABLE_BODY).find_elements(*self.TABLE_ROWS)
		expenses = []
		# set the driver not to wait, because the check if there is link os based on finding element
		self.driver.implicitly_wait(0)
		for row in rows:
			# only rows without link needed to be scraped from this page.
			# the rest will be scraped from other pages, with more details
			try:
				row.find_element(*self.ROW_DETAILS).find_element(By.TAG_NAME, 'a')
			except NoSuchElementException:
				expense = Expense()
				expense.date = row.find_element(*self.EXPENSE_DATE).text
				expense.description = row.find_element(*self.EXPENSE_DETAILS).text
				expense.type = self.get_debit_or_credit_from_row(row)
				expense.amount = self.get_amount(row)
				expenses.append(expense)

		self.driver.implicitly_wait(10)  # set the wait back to normal
		return expenses

	def get_debit_or_credit_from_row(self, row: WebElement) -> str:
		credit = row.find_element(*self.EXPENSE_CREDIT)
		if credit.text.strip():
			return ExpenseType.CREDIT
		return ExpenseType.DEBIT

	def get_amount(self, row: WebElement) -> float:
		credit = row.find_element(*self.EXPENSE_CREDIT)
		if credit.text.strip():
			return string_to_float(credit.text)
		return string_to_float(row.find_element(*self.EXPENSE_DEBIT).text)

