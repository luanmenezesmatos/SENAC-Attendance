from src.structures.Browser import Browser
from src.structures.Convert import Convert
from selenium.webdriver.common.by import By

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from matplotlib import pyplot as plt
from tabulate import tabulate
from PIL import Image
from io import BytesIO

import os
import json
import time

class Frequency:
	def __init__(self, browser=None):
		if browser is not None:
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

			frequency_json_file = os.getenv("FREQUENCY_JSON_FILE")

			# Salvar o JSON em um arquivo
			with open(frequency_json_file, "w", encoding="utf-8") as f:
				f.write(str(json))
				f.close()

			print("Salvou o JSON em um arquivo.")

	def format_json(self):
		frequency_json_file = os.getenv("FREQUENCY_JSON_FILE")
		frequency_result_json_file = os.getenv("FREQUENCY_RESULT_JSON_FILE")

		# Procurar pelo arquivo JSON
		if os.path.exists(frequency_json_file):
			# Abrir o arquivo JSON
			with open(frequency_json_file, "r", encoding="utf-8") as f:
				# Ler o arquivo JSON
				json_str = f.read()

				# Fechar o arquivo JSON
				f.close()

				print("Formatando o JSON...")

				# Converter o arquivo JSON para um objeto JSON
				json_str = json.loads(json_str)

				headers = json_str[1][0].split("\n")
				values = json_str[2:]

				# Colocar as headers como chaves e os valores como valores
				formatted_json = []
				for value in values:
					json_dict = {}
					for i in range(len(value)):
						json_dict[headers[i]] = value[i]
					formatted_json.append(json_dict)

				# Remover os objetos vazios do JSON
				for json_dict in formatted_json.copy():
					if json_dict == {}:
						formatted_json.remove(json_dict)

				# Obter as strings vazias do JSON e substituir por "Não inserido(a)"
				for json_dict in formatted_json:
					for key in json_dict:
						if json_dict[key] == "":
							json_dict[key] = "Não inserido(a)"

				time.sleep(3)

				# Salvar o JSON em um arquivo
				with open(frequency_result_json_file, "w", encoding="utf-8") as f:
					# f.write(str(formatted_json))
					json.dump(formatted_json, f, indent=4, ensure_ascii=False)
					f.close()
				
					print(f"Salvou o JSON no arquivo {frequency_result_json_file}")
			
					return formatted_json
		else:
			print("O arquivo JSON não existe. É necessário que você inicie o programa em modo de produção para que ele seja criado e depois você poderá iniciar o programa em modo de desenvolvimento.")

			return False
		
	def generate_table(self):
		frequency_json_file = os.getenv("FREQUENCY_RESULT_JSON_FILE")

		if os.path.exists(frequency_json_file):
			with open(frequency_json_file, "r", encoding="utf-8") as f:
				json_str = f.read()
				f.close()

				print("Convertendo o JSON para um DataFrame...")

				json_str = json.loads(json_str)

				dataframe = pd.DataFrame(json_str)

				if dataframe is not False:
					print("Gerando a tabela...")

					# Gerar a tabela
					""" plt.table(cellText=dataframe.values, colLabels=dataframe.columns, loc='center', cellLoc='center')
					plt.show() """

					""" with open('table.html', 'w') as f:
						# table = tabulate(dataframe, headers='keys', tablefmt='html', showindex=True, border="1")
						f.write(table)
						f.close() """
					
						# f.write(tabulate(dataframe, headers='keys', tablefmt='html', showindex=False))
					
					table = tabulate(dataframe, headers='keys', tablefmt='github')

					fix, ax = plt.subplots()
					ax.axis('off')
					ax.table(cellText=table, loc='center', cellLoc='center', colLabels=None)

					img_buffer = BytesIO()
					plt.savefig(img_buffer, format="png")
					img_buffer.seek(0)

					image = Image.open(img_buffer)

					image.show()

					return True
				else:
					return False
		else:
			print("O arquivo JSON não existe. É necessário que você inicie o programa em modo de produção para que ele seja criado e depois você poderá iniciar o programa em modo de desenvolvimento.")

			return False