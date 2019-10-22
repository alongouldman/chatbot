import os
import time

from selenium.webdriver.remote.webdriver import WebDriver

from common import BANK_URL
from pages.base_page import BasePage
from pages.main_menu_page import MainMenuPage


class BankHomePage(BasePage):
	_LOGIN_BUTTON_CSS = 'login-trigger'
	_LOGIN_FORM_USERNAME_ID = 'username'
	_LOGIN_FORM_PASSWORD_ID = 'password'
	_LOGIN_FORM_BUTTON_ID = 'continueBtn'

	def __init__(self, driver: WebDriver = None):
		super().__init__(driver)
		
	def navigate(self):
		self.driver.get(BANK_URL)		

	@BasePage.trigger_navigate
	def login(self):
		login = self.driver.find_element_by_class_name(BankHomePage._LOGIN_BUTTON_CSS)
		login.click()
		iframe = self.driver.find_element_by_id('loginFrame')
		self.driver.switch_to.frame(iframe)
		time.sleep(3)
		username_input = self.driver.find_element_by_id(BankHomePage._LOGIN_FORM_USERNAME_ID)
		username_input.send_keys(self._get_username())
		password_input = self.driver.find_element_by_id(BankHomePage._LOGIN_FORM_PASSWORD_ID)
		password_input.send_keys(self._get_password())
		login_button = self.driver.find_element_by_id(self._LOGIN_FORM_BUTTON_ID)
		login_button.click()
		return MainMenuPage(self.driver)

	@staticmethod
	def _get_username():
		try:
			return os.environ['bank_login_username']
		except KeyError:
			file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bank_login.txt')
			with open(file_path, 'r') as f:
				return f.readlines()[0]

	@staticmethod
	def _get_password():
		try:
			return os.environ['bank_login_password']
		except KeyError:
			file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bank_login.txt')
			with open(file_path, 'r') as f:
				return f.readlines()[1]
