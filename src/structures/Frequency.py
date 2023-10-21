from src.structures.Browser import Browser
from src.structures.Convert import Convert
from selenium.webdriver.common.by import By

class Frequency:
	def __init__(self, browser: Browser):
		self.browser = browser
		self.browser.by = By
		self.convert = Convert

	def get_current_url(self):
		return self.browser.get_current_url()

	def get_frequency_page(self):
		return self.browser.copy_link(self.browser.by.ID, value="item-50")

	def get_activities_page(self):
		try:
			self.browser.click_button(self.browser.by.ID, value="win0divDERIVED_SSS_SCR_SSS_LINK_ANCHOR4")
		except:
			print("Erro ao acessar a página de atividades.")
			self.browser.driver.quit()

	def access_activity(self):
		html = self.browser.get_frequency_html()

		if html:
			convert = self.convert(html)
			json = convert.convert_html_to_json()

			filtered = convert.remove_empty_array(json)

			# Salvar o JSON em um arquivo
			with open("frequency-tec.json", "w", encoding="utf-8") as f:
				f.write(filtered)

			print("Salvou o JSON em um arquivo.")