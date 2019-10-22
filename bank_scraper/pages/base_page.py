from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class BasePage(object):
	def __init__(self, driver: WebDriver = None):
		if driver is None:
			driver = self.init_driver()
		self.driver = driver

	@staticmethod
	def trigger_navigate(func):
		"""
		this is a decorator for functions that you want to trigger navigate before they happen
		"""
		def _trigger_navigate_wrapper(self, *args, **kwargs):
			self.navigate()
			return func(self, *args, **kwargs)
		return _trigger_navigate_wrapper

	def navigate(self):
		raise NotImplementedError("you must implement this method!")

	@staticmethod
	def init_driver():
		driver = webdriver.Chrome(ChromeDriverManager().install())
		driver.implicitly_wait(10)
		return driver
