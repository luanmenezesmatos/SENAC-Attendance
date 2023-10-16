from src.structures.Browser import Browser
from src.structures.Login import Login
from src.structures.Frequency import Frequency

import os
import time

from dotenv import load_dotenv
load_dotenv()

get_aluno_email = os.getenv("ALUNO_EMAIL")
get_aluno_senha = os.getenv("ALUNO_SENHA")

browser = Browser("chrome")
login = Login(browser, get_aluno_email, get_aluno_senha)
login.login()

if login.is_logged_in():
	print("Logado com sucesso.")

	time.sleep(3)

	frequency = Frequency(browser)

	print("Acessando página de frequência.")

	time.sleep(3)

	browser.get(frequency.get_frequency_page())

	print("Entrou na página de frequência.")

	time.sleep(3)

	frequency.get_activities_page()

	print("Acessando página de atividades.")

	time.sleep(3)

	frequency.access_activity()

	print("Acessando atividade.")

	if browser.driver.title.__contains__("500"):
		print("O servidor está bloqueando o acesso. Tente novamente daqui a alguns segundos!")
	else:
		print("Não foi barrado pelo servidor.")
else:
	print("Falha ao logar.")

from src.structures.Browser import Browser
from src.structures.Login import Login
from src.structures.Frequency import Frequency

import os
import time

from dotenv import load_dotenv
load_dotenv()

get_aluno_email = os.getenv("ALUNO_EMAIL")
get_aluno_senha = os.getenv("ALUNO_SENHA")

browser = Browser("chrome", headless=True)
login = Login(browser, get_aluno_email, get_aluno_senha)

try:
	login.login()
except:
	browser.quit()
	raise Exception("Erro ao fazer login. Tente novamente!")

if login.is_logged_in():
	print("Logado com sucesso.")

	time.sleep(3)

	frequency = Frequency(browser)

	print("Acessando página de frequência.")

	time.sleep(3)

	browser.get(frequency.get_frequency_page())

	print("Entrou na página de frequência.")

	time.sleep(3)

	frequency.get_activities_page()

	print("Acessando página de atividades.")

	time.sleep(3)

	frequency.access_activity()

	print("Acessando atividade.")

	if browser.driver.title.__contains__("500"):
		print("O servidor está bloqueando o acesso. Tente novamente daqui a alguns segundos!")
	else:
		print("Não foi barrado pelo servidor.")
else:
	print("Falha ao logar.")
	browser.quit()
