from notion_client import Client as NotionClient
import frontmatter


class notionIntegration:
    def __init__(self, token, database_id):
        self.notion_token = token
        self.database_id = database_id
        self.notion = NotionClient(auth=self.notion_token)

        if self.notion_token is None:
            raise Exception("NOTION_TOKEN não encontrado.")

    def retrive_database(self):
        # Função para buscar os bancos de dados do Notion

        databases = self.notion.databases.retrieve(
            database_id=self.database_id)
        return databases

    def add_values(self, values):
        """
        Função para adicionar valores ao banco de dados selecionado

        values: {"country":["india","usa"],"job":["engineer","doctor"],"firstname":["shourav","shubham"]}
        """

        

        """ properties = {
            "Componente Curricular": {
                "title": [
                    {
                        "text": {
                            "content": values["Componente Curricular"][0]
                        }
                    }
                ]
            },
            "Descrição": {
                "rich_text": [
                    {
                        "text": {
                            "content": values["Descrição"][0]
                        }
                    }
                ]
            }
        } """

        total_len = len(list(values.values())[0])
        
        properties = {}

        for key, value in values.items():
            """ properties[key] = {
                "title": [
                    {
                        "rich_text": {
                            "content": value[0]
                        }
                    }
                ]
            } """

            """ properties = {
                key: {
                    "title": [
                        {
                            "text": {
                                "content": value[0]
                            }
                        }
                    ]
                }
            } """

            properties = {
                key: {
                    "title" if key == "Componente Curricular" else "rich_text": [
                        {
                            "text": {
                                "content": value[0]
                            }
                        }
                    ]
                }
            }

            create_page = self.notion.pages.create(parent={"database_id": self.database_id}, properties=properties)

            print(create_page)

        print("Valores adicionados com sucesso!")

    def generate_html(self, data, document_path):
        # Função para gerar o HTML do Notion

        content = frontmatter.dumps(data)
        template = """
        ---

        """
