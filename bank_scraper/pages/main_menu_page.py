from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.cashflow_page import CashflowPage


class MainMenuPage(BasePage):

	PAGE_IDENTIFIER = (By.CLASS_NAME, "fibi_main_menu")

	def __init__(self, driver):
		super().__init__(driver)

	@property
	def cashflow_page(self):
		return CashflowPage(self.driver)

	@property
	def is_visible(self):
		try:
			self.driver.implicitly_wait(0)
			self.driver.find_element(*self.PAGE_IDENTIFIER)
			return True
		except NoSuchElementException:
			return False
		finally:
			self.driver.implicitly_wait(10)  # back to normal
