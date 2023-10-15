from src.structures.Browser import Browser
from src.structures.Login import Login

import os

from dotenv import load_dotenv
load_dotenv()

get_aluno_email = os.getenv("ALUNO_EMAIL")
get_aluno_senha = os.getenv("ALUNO_SENHA")

browser = Browser("chrome")
login = Login(browser, get_aluno_email, get_aluno_senha)
login.login()

if login.is_logged_in():
	print("Logado com sucesso!")
else:
	print("Falha ao logar.")