from selenium import webdriver
from selenium.webdriver.common.by import By

from src.structures.Convert import Convert

import time
import json

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

	def copy_link(self, by: By, value: str):
		return self.driver.find_element(by=by, value=value).get_attribute("href")
	
	def save_html(self, path):
		html = self.driver.page_source
		html_str = str(html)  # convert html to string
		with open(path, "w", encoding="utf-8") as f:
			f.write(html_str)

	def get_frequency_html(self):
		# html = self.driver.find_element(By.ID, value="TERM_CLASSES$scroll$0").get_attribute("innerHTML")
		html = self.driver.find_element(By.ID, value="TERM_CLASSES$scroll$0").get_attribute("innerHTML")

		# html = html.replace(r"\n\xa", "")
		# html = html.replace(r"\n", "")

		convert = Convert(html, indent=4).convert_html_to_json()

		return convert

	def get_current_url(self):
		return self.driver.current_url