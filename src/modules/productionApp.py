from config import appConfig
from src.structures.Browser import Browser
from src.structures.Login import Login
from src.structures.Frequency import Frequency

import os
import time

from selenium.webdriver.common.by import By

from dotenv import load_dotenv
load_dotenv()

class productionApp:
    def __init__(self, student_email, student_password, frequency_json_file, is_development=False):
        self.browser = Browser("chrome")
        self.browser.by = By
        self.login = Login(self.browser, os.getenv("EMAIL"), os.getenv("PASSWORD"))
        self.frequency = Frequency(self.browser)
        self.student_email = student_email
        self.student_password = student_password
        self.frequency_json_file = frequency_json_file
        self.is_development = is_development

    def login_senac(self):
        if self.is_development:
            print("Iniciando o programa no modo de desenvolvimento.")

            time.sleep(3)

            frequency_json_file = os.getenv("FREQUENCY_JSON_FILE")