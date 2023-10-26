from notion_client import Client as NotionClient

class notionIntegration:
    def __init__(self, token):
        self.notion_token = token
        self.notion = NotionClient(auth=self.notion_token)

        if self.notion_token is None:
            raise Exception("NOTION_TOKEN não encontrado.")
        
    def get_databases(self):
        # Função para buscar os bancos de dados do Notion

        databases = self.notion.databases.list()
        return databases