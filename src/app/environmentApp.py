from config import appConfig
from src.structures.Browser import Browser
from src.structures.Login import Login
from src.structures.Frequency import Frequency
from src.report.documentBuilder import DocumentBuilder
from src.notion.notionIntegration import notionIntegration

import os
import time

from selenium.webdriver.common.by import By

from dotenv import load_dotenv
load_dotenv()

import json
import pandas as pd

class environmentApp:
    def __init__(self, student_email, student_password, frequency_json_file, browser=None):
        if browser is not None:
            self.browser = Browser("chrome")
            self.browser.by = By
            self.login = Login(self.browser, os.getenv(
                "EMAIL"), os.getenv("PASSWORD"))
            self.frequency = Frequency(self.browser)

        self.student_email = student_email
        self.student_password = student_password
        self.frequency_json_file = frequency_json_file
        self.is_development = appConfig().is_development

    def login_senac(self):
        if self.is_development:
            print("Iniciando o programa no modo de desenvolvimento.")

            time.sleep(3)

            print("Lendo o arquivo JSON...")

            time.sleep(3)

            frequency = Frequency()

            formatted_json = frequency.format_json()

            if formatted_json:
                print("Passou da função de formatar o JSON.")

                time.sleep(3)

                table = frequency.generate_table()

                if table == True:
                    print("Tabela criada com sucesso.")

                    time.sleep(3)

                    ni = notionIntegration(os.getenv("NOTION_TOKEN"))
                    databases = ni.get_databases()
                    print(databases)

                    selected_database = ni.set_database("SENAC - Presença")
                    print(selected_database)

                    all_entries = ni.get_all_entries()
                    if not all_entries:
                        print("Não há entradas no banco de dados do Notion atualmente.")

                    count = 0
                    for entry in formatted_json:
                        count += 1
                        if count > len(entry['Componente Curricular']):
                            continue

                        add_values = ni.add_values(
                            values={
                                "Status": "Em andamento",
                                "Componente Curricular": [entry['Componente Curricular']],
                                "Descrição": [entry['Descrição']],
                                "Notas/Menções": [entry['Notas/Menções']],
                                "Notas/Menções Oficiais": [entry['Notas/Menções Oficiais']],
                                "Notas/Menções Revisadas": [entry['Notas/Menções Revisadas']],
                                "Total Presenças": [entry['Total Presenças']],
                                "% CH Aprovação": [entry['% CH Aprovação']],
                                "Total Faltas": [entry['Total Faltas']],
                                "% Faltas": [entry['% Faltas']],
                                "Resultados": [entry['Resultados']],
                                "Faltas com Amparo Legal": [entry['Faltas com Amparo Legal']],
                                "Estágio/Complemento": [entry['Estágio/Complemento']],
                                "Certificação Antecipada Enferm": [entry['Certificação Antecipada Enferm']],
                                "Retomada": [entry['Retomada']],
                            }
                        )
                        
                        print(add_values)

                    """ document = DocumentBuilder().create_table(table_data=formatted_json, dataframe=table)

                    if document == True:
                        print("Documento criado com sucesso.")
                    else:
                        print("Erro ao criar o documento.") """
        else:
            print("O arquivo JSON não existe. É necessário que você inicie o programa em modo de produção para que ele seja criado e depois você poderá iniciar o programa em modo de desenvolvimento.")
            quit()