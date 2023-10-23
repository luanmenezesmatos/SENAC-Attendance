from collections import defaultdict

import requests

class notionIntegration:
    def __init__(self, token):
        self.notion_token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Notion-Version': '2021-05-13'
        }

        if self.notion_token is None:
            raise Exception("NOTION_TOKEN não encontrado.")
        
    def get_databases(self) -> dict:
        # Função para buscar os bancos de dados do Notion

        self.available_databases = {}

        request_url = 'https://api.notion.com/v1/databases'
        response = requests.get(request_url, headers=self.headers)

        try:
            print("Conectado com o Notion. Buscando os bancos de dados...")

            data = response.json()

            if data.get('object') == 'list':
                databases = data.get('results', [])

                for db in databases:
                    self.available_databases[db['title'][0]['plain_text']] = db['id']

                return self.available_databases
            else:
                raise Exception(f"Erro ao buscar os bancos de dados. Erro: {response.text}")
        except:
            raise Exception(f"Erro ao buscar os bancos de dados. Erro: {response.text}")
        
    def set_database(self, database_name: str) -> str:
        """
        Função para definir o banco de dados que será utilizado
        database_name: Nome do banco de dados, ex: "Frequência" - é um parâmetro obrigatório
        """

        if not database_name:
            raise Exception("É necessário definir o nome do banco de dados.")
        
        self.columns_attributes = {}
        try:
            self.selected_database = self.available_databases[database_name]
            request_url = f"https://api.notion.com/v1/databases/{self.selected_database}"
            response = requests.get(request_url, headers=self.headers)

            for key, value in response.json()['properties'].items():
                if key == "ID":
                    self.columns_attributes[key] = "number"
                else:
                    self.columns_attributes[key] = value['type']

            return f"Banco de dados '{database_name}' com o ID '{self.selected_database}' selecionado com sucesso."
        except:
            raise Exception(f"O banco de dados '{database_name}' não existe. Verifique se o nome está correto e tente novamente.")
        
    def formatting(self, response, dataframe=False):
        queried_database = defaultdict(list)
        all_columns = set(self.columns_attributes.keys())
        try:
            data = response.json()
            entries = data.get('results', [])

            for entry in entries:
                present_columns = set(entry['properties'].keys())
                if len(present_columns) != len(all_columns):
                    difference = all_columns.difference(present_columns)
                    for x in difference:
                        queried_database[x].append(None)
                
                for key, value in entry['properties'].items():
                    if key == "ID":
                        types = value['type']
        except:
            raise Exception(f"Erro ao formatar os dados. Erro: {response.text}")