from pages.base_page import BasePage
from pages.cashflow_page import CashflowPage


class MainMenuPage(BasePage):
	def __init__(self, driver):
		super().__init__(driver)

	@property
	def cashflow_page(self):
		return CashflowPage(self.driver)
