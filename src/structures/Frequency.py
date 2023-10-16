from src.structures.Browser import Browser
from selenium.webdriver.common.by import By

class Frequency:
	def __init__(self, browser: Browser):
		self.browser = browser
		self.browser.by = By

	def get_current_url(self):
		return self.browser.get_current_url()

	def get_frequency_page(self):
		return self.browser.copy_link(self.browser.by.ID, value="item-50")

	def get_activities_page(self):
		try:
			self.browser.click_button(self.browser.by.ID, value="win0divDERIVED_SSS_SCR_SSS_LINK_ANCHOR4")
		except:
			return print("Erro ao acessar página de atividades.")

	def access_activity(self):
		html = self.browser.get_frequency_html()
		
		print(html)