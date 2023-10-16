from src.structures.Browser import Browser
from selenium.webdriver.common.by import By

import time

class Login:
	def __init__(self, browser: Browser, email: str, password: str):
		self.browser = browser
		self.browser.by = By
		self.email = email
		self.password = password

	def login_senac(self):
		self.browser.add_input(self.browser.by.NAME, value="email", text=self.email)
		self.browser.add_input(self.browser.by.NAME, value="senha", text=self.password)
		self.browser.click_button(self.browser.by.NAME, value="formLoginButtonSubmit")

	def is_logged_in(self):
		#try:
		if self.browser.get_current_url().startswith("https://www.sp.senac.br/login-unico/login"):
			if self.browser.driver.find_element(self.browser.by.CLASS_NAME, value="ssp-erro__title").text == "Humpf!":
				return print("O servidor está bloqueando o acesso. Tente novamente daqui a alguns minutos!")
			else:
				print("Não foi barrado pelo servidor.")

		if self.browser.get_current_url().startswith("https://www.sp.senac.br/login-unico/login"):
			if self.browser.driver.find_element(self.browser.by.ID, value="valid_geral").text == "E-mail não encontrado!" or self.browser.driver.find_element(self.browser.by.ID, value="valid_geral").text == "Senha incorreta!":
				return False
		
		if self.browser.get_current_url().startswith("https://www.sp.senac.br/area-exclusiva/"):
			if self.browser.driver.find_element(self.browser.by.CLASS_NAME, value="margtop5").text == "Avisos Gerais":
				return True
		#except:
			#return print("Erro ao verificar se está logado.")
	def login(self):
		try:
			self.browser.get("https://www.sp.senac.br/login-unico/login")
			time.sleep(3)
			self.login_senac()
			time.sleep(3)
		except:
			return print("Erro ao logar (Função de Login).")