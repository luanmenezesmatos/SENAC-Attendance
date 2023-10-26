from collections import defaultdict

import requests
import pandas

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

        data = response.json()
        entries = data.get('results', [])

        for entry in entries:
            present_columns = set(entry['properties'].keys())
            if len(present_columns) != len(all_columns):
                difference = all_columns.difference(present_columns)
                for x in difference:
                    queried_database[x].append(None)
            
            for key,value in entry['properties'].items():
                
                if key == "ID":
                    types = value['type']
                    if value['type']:
                        queried_database[key].append(value[types]['number'])
                    else:
                        queried_database[key].append(None)
                else:
                    types = value['type']

                    if types == 'number':
                        if value[types]:
                            queried_database[key].append(value[types])
                        else:
                            queried_database[key].append(None)
                    else:
                        if value[types]:
                            if isinstance(value[types], dict) and value[types].get('plain_text'):
                                queried_database[key].append(value[types]['plain_text'])
                            elif isinstance(value[types], list) and value[types][0].get('plain_text'):
                                queried_database[key].append(value[types][0]['plain_text'])
                            else:
                                queried_database[key].append(value[types])
                        else:
                            queried_database[key].append(None)

        if dataframe:
            return pandas.DataFrame(queried_database).reset_index(drop=True)
        else:
            return dict(queried_database)
        
    def get_all_entries(self, dataframe=False):
        """
        Função para buscar todos os dados do banco de dados selecionado

        dataframe: Se True, retorna um dataframe, se False, retorna um dicionário
        """
        
        request_url = f"https://api.notion.com/v1/databases/{self.selected_database}/query"
        response = requests.post(request_url, headers=self.headers)

        data = response.json()

        """ if data.get('object') == 'list':
            raise Exception(f"O ID '{self.selected_database}' não é um banco de dados válido.") """
        
        if data.get('object') == 'list':
            return self.formatting(response, dataframe)
        else:
            raise Exception(f"O ID '{self.selected_database}' não é um banco de dados válido.")
    
    def query(self, query, dataframe=False):
        """
        Função para buscar dados do banco de dados selecionado de acordo com uma query

        query: {"column": "value"}
        dataframe: Se True, retorna um dataframe, se False, retorna um dicionário
        """

        and_col = []
        
        request_url = f"https://api.notion.com/v1/databases/{self.selected_database}/query"

        for key, values in query.items():
            filter_conditions = {
                "property": key,
                self.columns_attributes[key]: {
                    "equals": values
                }
            }

            and_col.append(filter_conditions)

        filter_query = {
            "filter": {
                "and": and_col
            }
        }

        response = requests.post(request_url, headers=self.headers, json=filter_query)

        return self.formatting(response, dataframe)
    
    def add_value(self, value):
        """
        Função para adicionar um valor ao banco de dados selecionado

        value: {"column": value1, "column2": value2}
        """

        for key in value.keys():
            if key not in self.columns_attributes.keys():
                raise Exception(f"A coluna '{key}' não existe no banco de dados selecionado.")
            
        request_url = f"https://api.notion.com/v1/pages"

        final_value = {}
        
        for key, content in value.items():
            if self.columns_attributes[key] == 'number':
                final_value[key] = {self.columns_attributes[key]: content}
            else:
                final_value[key] = {self.columns_attributes[key]: [{"text": {"content": content}}]}

        new_entry_data = {
            'parent': {'database_id': self.selected_database},
            'properties': final_value
        }

        response = requests.post(request_url, headers=self.headers, json=new_entry_data)

        if response.status_code == 200:
            data = response.json()
            return f"Valor '{data['properties']['ID']['number']}' adicionado com sucesso."
        else:
            raise Exception(f"Código do erro: {response.status_code}. Erro ao adicionar o valor. Erro: {response.text}")
        
    def add_values(self, values):
        """
        Função para adicionar valores ao banco de dados selecionado

        values: {"country":["india","usa"],"job":["engineer","doctor"],"firstname":["shourav","shubham"]}
        """

        total_len = len(list(values.values())[0])

        new_entry_datas = []
        for key in values.keys():
            if len(values[key]) != total_len:
                raise Exception(f"O número de valores da coluna '{key}' é diferente do número de valores das outras colunas.")
            
            if key not in self.columns_attributes.keys():
                raise Exception(f"A coluna '{key}' não existe no banco de dados selecionado.")
            
        request_url = f"https://api.notion.com/v1/pages"

        for entries in range(total_len):
            final_value = {}

            for key, content in values.items():
                if self.columns_attributes[key] == 'number':
                    final_value[key] = {self.columns_attributes[key]: content[entries]}
                elif self.columns_attributes[key] == 'multi_select':
                    final_value[key] = {self.columns_attributes[key]: [{"name": content[entries]}]}
                elif self.columns_attributes[key] == 'select':
                    print("Entrou aqui")
                    final_value[key] = {self.columns_attributes[key]: {"name": content[entries]}}
                else:
                    final_value[key] = {self.columns_attributes[key]: [{"text": {"content": content[entries]}}]}

                new_entry_data = {
                    'parent': {'database_id': self.selected_database},
                    'properties': final_value
                }

            new_entry_datas.append(new_entry_data)

        components = []
        duplicated_components = []
        count_added_values = 0
        already_exists = False

        for entry_data in new_entry_datas:
            for key, value in entry_data['properties'].items():
                if key == 'Componente Curricular':
                    components.append(value['title'][0]['text']['content'])

                    # Verificar se o componente curricular já existe no banco de dados
                    result = self.query(query={"Componente Curricular": value['title'][0]['text']['content']}, dataframe=True)

                    if len(result) > 0:
                        duplicated_components.append(value['title'][0]['text']['content'])

                        print(f"O componente curricular '{value['title'][0]['text']['content']}' já existe no banco de dados.")
                        already_exists = True
                    else:
                        already_exists = False

            if not already_exists:
                response = requests.post(request_url, headers=self.headers, json=entry_data)

                if response.status_code == 200:
                    data = response.json()
                    count_added_values += 1
                    print(f"Valor '{data['properties']['Componente Curricular']['title'][0]['text']['content']}' adicionado com sucesso.")
                else:
                    raise Exception(f"Código do erro: {response.status_code}. Erro ao adicionar o valor. Erro: {response.text}")
            
        if already_exists:
            return f"Detectei que {len(duplicated_components)} componentes curriculares já existiam no banco de dados."
        else:
            if count_added_values > 0 and len(duplicated_components) > 0:
                return f"{count_added_values} valor(es) adicionados com sucesso, porém, detectei que {len(duplicated_components)} componentes curriculares já existiam no banco de dados."
            else:
                return f"{count_added_values} valor(es) adicionados com sucesso."
    
    def update_value(self, filter_query, update_value):
        """
        Função para atualizar um valor do banco de dados selecionado

        update_value(filter_query={"column": "value"}, update_value={"column": "value"})
        """

        and_col = []
        properties_update = {}

        # column = list(filter_query.keys())[0]
        # value = list(filter_query.values())[0]

        column_update = list(update_value.keys())[0]
        value_update = list(update_value.values())[0]

        request_url = f"https://api.notion.com/v1/databases/{self.selected_database}/query"

        for key, values in filter_query.items():
            filter_conditions = {
                "property": key,
                self.columns_attributes[key]: {
                    "equals": values
                }
            }

            and_col.append(filter_conditions)

        filter_query = {
            "filter": {
                "and": and_col
            }
        }

        response = requests.post(request_url, headers=self.headers, json=filter_query)

        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])

            for result in results:
                entry_id = result['id']
                update_url = f"https://api.notion.com/v1/pages/{entry_id}"

                for column_update, value_update in update_value.items():
                    if self.columns_attributes[column_update] == 'number':
                        properties_update[column_update] = {
                            "type": "number",
                            "number": value_update
                        }
                    else:
                        properties_update[column_update] = {
                            self.columns_attributes[column_update]: [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": value_update
                                    }
                                }
                            ]
                        }
                
                update_data = {
                    "properties": properties_update
                }

                update_response = requests.patch(update_url, headers=self.headers, json=update_data)

                if update_response.status_code == 200:
                    return f"Valor '{value_update}' atualizado com sucesso."
                else:
                    raise Exception(f"Código do erro: {update_response.status_code}. Erro ao atualizar o valor. Erro: {update_response.text}")
        else:
            raise Exception(f"Código do erro: {response.status_code}. Erro ao buscar o valor. Erro: {response.text}")
        
    def delete_one(self, id):
        """
        Função para deletar um valor do banco de dados selecionado

        id: ID do valor que será deletado
        """

        request_url = f'https://api.notion.com/v1/databases/{self.selected_database}/query'

        filter_conditions = {
            'property': 'ID',
            'number': {
                'equals': id
            }
        }

        filter_query = {
            'filter': {
                'and': [filter_conditions]
            }
        }

        response = requests.post(request_url, headers=self.headers, json=filter_query)

        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            if len(results) == 1:
                entry_id = results[0]['id']
                update_url = f"https://api.notion.com/v1/pages/{entry_id}"

                update_data = {
                    "archived": True
                }

                update_response = requests.patch(update_url, headers=self.headers, json=update_data)

                if update_response.status_code == 200:
                    return f"Valor '{id}' deletado com sucesso."
                else:
                    raise Exception(f"Código do erro: {update_response.status_code}. Erro ao deletar o valor. Erro: {update_response.text}")
        else:
            raise Exception(f"Código do erro: {response.status_code}. Erro ao buscar o valor. Erro: {response.text}")