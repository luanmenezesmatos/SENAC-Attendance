from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Browser:
	def __init__(self, browser_name):
		if browser_name == "chrome":
			self.driver = webdriver.Chrome()
		elif browser_name == "firefox":
			self.driver = webdriver.Firefox()
		elif browser_name == "edge":
			self.driver = webdriver.Edge()
		elif browser_name == "ie":
			self.driver = webdriver.Ie()
		elif browser_name == "opera":
			self.driver = webdriver.Opera()
		else:
			raise Exception("O navegador informado não é suportado.")

	def get(self, url):
		self.driver.get(url)

	def maximize_window(self):
		self.driver.maximize_window()

	def save_screenshot(self, path):
		self.driver.save_screenshot(path)

	def add_input(self, by: By, value: str, text: str):
		self.driver.find_element(by=by, value=value).send_keys(text)
		time.sleep(1)

	def click_button(self, by: By, value: str):
		self.driver.find_element(by=by, value=value).click()
		time.sleep(1)

	def get_current_url(self):
		return self.driver.current_url