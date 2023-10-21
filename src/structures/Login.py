from src.structures.Browser import Browser
from selenium.webdriver.common.by import By

import time

# BEGIN: 9f3d8j4d8c3
class Login:
    def __init__(self, browser: Browser, email: str, password: str):
        self.browser = browser
        self.browser.by = By
        self.email = email
        self.password = password

    def login_senac(self):
        print("Entrou na função de login do Senac.")

        self.browser.add_input(self.browser.by.NAME,
                               value="email", text=self.email)
        self.browser.add_input(self.browser.by.NAME,
                               value="senha", text=self.password)
        self.browser.click_button(
            self.browser.by.NAME, value="formLoginButtonSubmit")

    def is_logged_in(self):
        print("Entrou na função de verificar se está logado.")    

        try:
            if self.browser.get_current_url().startswith("https://www.sp.senac.br/login-unico/login"):
                if self.browser.driver.find_element(self.browser.by.CLASS_NAME, value="ssp-erro__title").text == "Humpf!":
                    self.write_attendance_file(None)
                else:
                    self.write_attendance_file(False)
            else:
                self.write_attendance_file(True)

            if self.browser.get_current_url().startswith("https://www.sp.senac.br/login-unico/login"):
                if self.browser.driver.find_element(self.browser.by.ID, value="valid_geral").text == "E-mail não encontrado!" or self.browser.driver.find_element(self.browser.by.ID, value="valid_geral").text == "Senha incorreta!":
                    self.write_attendance_file(None)
                else:
                    self.write_attendance_file(False)
            else:
                self.write_attendance_file(True)

            if self.browser.get_current_url().startswith("https://www.sp.senac.br/area-exclusiva/"):
                if self.browser.driver.find_element(self.browser.by.CLASS_NAME, value="margtop5").text == "Avisos Gerais":
                    self.write_attendance_file(True)
                else:
                    self.write_attendance_file(False)
            else:
                self.write_attendance_file(None)

            print("Passou nas verificações de segurança.")

            self.write_attendance_file(True)
            return True
        except Exception as e:
            print(f"Erro na função: {e}")

    def login(self):
        try:
            self.browser.get("https://www.sp.senac.br/login-unico/login")
            time.sleep(3)
            self.login_senac()
        except:
            return print("Erro ao logar (Função de Login).")

    def write_attendance_file(self, is_logged_in: bool) -> bool:
        return is_logged_in
