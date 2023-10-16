from src.structures.Browser import Browser
from src.structures.Login import Login
from src.structures.Frequency import Frequency

import os
import time

from selenium.webdriver.common.by import By

from dotenv import load_dotenv
load_dotenv()

get_aluno_email = os.getenv("ALUNO_EMAIL")
get_aluno_senha = os.getenv("ALUNO_SENHA")

browser = Browser("chrome")
login = Login(browser, get_aluno_email, get_aluno_senha)

try:
    login.login()

    time.sleep(3)

    if login.is_logged_in():
        print("Logado com sucesso.")

        if browser.get_current_url().startswith("https://www.sp.senac.br/login-unico/login") or browser.get_current_url().startswith("https://www.sp.senac.br/area-exclusiva/"):
            if browser.driver.find_element(By.CLASS_NAME, value="ssp-erro__title").text == "Humpf!":
                print(
                    "O servidor está bloqueando o acesso. Tente novamente daqui a alguns minutos!")
                browser.driver.quit()
            else:
                print("Não foi barrado pelo servidor.")
        else:
            print("Não está na página de login e nem na página de área exclusiva.")

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
    else:
        print("Falha ao logar.")
        browser.driver.quit()
except:
    browser.driver.quit()
    raise Exception("Erro ao fazer login. Tente novamente!")
