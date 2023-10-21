import os

from dotenv import load_dotenv
load_dotenv()

class appConfig:
    # Função para escolher entre os modos de 'development' ou 'production' - deverá ser setada por padrão para 'development' através de uma variável de ambiente
    def __init__(self):
        self.APP_ENV = os.getenv('APP_ENV')

        # Se for 'True', o programa irá rodar em modo de desenvolvimento, caso contrário, irá rodar em modo de produção
        self.is_development = False
        # Se for 'True', o programa irá rodar em modo de produção, caso contrário, irá rodar em modo de desenvolvimento
        self.is_production = False

        self.verifyEnv()  # Chamando a função no construtor

    # Função para fazer a verificação do valor da variável de ambiente 'APP_ENV'
    def verifyEnv(self):
        # Verificar se a variável de ambiente 'APP_ENV' é igual a 'development' ou 'production'
        if self.APP_ENV == 'development':
            self.is_development = True
        elif self.APP_ENV == 'production':
            self.is_production = True
        else:
            # Deixe o bloco else vazio
            pass
