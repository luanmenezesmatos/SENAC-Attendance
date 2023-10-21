from config import appConfig
from src.structures.Browser import Browser
from src.structures.Login import Login
from src.structures.Frequency import Frequency

import os
import time

from selenium.webdriver.common.by import By

from dotenv import load_dotenv
load_dotenv()


get_student_email = os.getenv("STUDENT_EMAIL")
get_student_password = os.getenv("STUDENT_PASSWORD")

if appConfig().is_development:
    print("Iniciando o programa no modo de desenvolvimento.")

    time.sleep(3)

    frequency_json_file = os.getenv("FREQUENCY_JSON_FILE")

    # Procurar pelo arquivo JSON
    if os.path.exists(frequency_json_file):
        # Abrir o arquivo JSON
        with open(frequency_json_file, "r", encoding="utf-8") as f:
            # Ler o arquivo JSON
            json = f.read()

            # Fechar o arquivo JSON
            f.close()

            print("Lendo o arquivo JSON...")

            time.sleep(3)

            print(json)
    else:
        print("O arquivo JSON não existe. É necessário que você inicie o programa em modo de produção para que ele seja criado e depois você poderá iniciar o programa em modo de desenvolvimento.")
        quit()
elif appConfig().is_production:
    print("Iniciando o programa no modo de produção.")

    time.sleep(3)
    
    browser = Browser("chrome")
    login = Login(browser, get_student_email, get_student_password)

    login.login()

    time.sleep(3)

    try:
        is_logged_in = login.is_logged_in()

        if is_logged_in:
            attendance = login.write_attendance_file(is_logged_in)
            print(attendance)

        if attendance == True:
            print("Logado com sucesso.")

            try:
                if browser.get_current_url().startswith("https://www.sp.senac.br/login-unico/login") or browser.get_current_url().startswith("https://www.sp.senac.br/area-exclusiva/"):
                    if browser.driver.find_element(By.CLASS_NAME, value="ssp-erro__title").text == "Humpf!":
                        print(
                            "O servidor está bloqueando o acesso. Tente novamente daqui a alguns minutos!")
                        browser.driver.quit()
                    else:
                        print("Não foi barrado pelo servidor.")
            except:
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
    except Exception as e:
        print(f"Erro ao fazer login: {e}")
