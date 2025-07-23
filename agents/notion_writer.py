# agents/notion_writer.py
import notion_client
from rich.console import Console

console = Console()

class NotionWriter:
    """Responsável por toda a comunicação de escrita com a API do Notion."""
    def __init__(self, api_key: str, projects_db_id: str, tasks_db_id: str):
        if not all([api_key, projects_db_id, tasks_db_id]) or "SUA_CHAVE" in api_key or "COLE_O_ID" in tasks_db_id:
            raise ValueError("API Key e IDs de Database (Projetos e Tarefas) do Notion são obrigatórios.")

        self.notion = notion_client.Client(auth=api_key)
        self.projects_db_id = projects_db_id
        self.tasks_db_id = tasks_db_id
        console.print("✅ [Notion Writer] Conexão com o cliente Notion estabelecida.")

    def create_project_page(self, project_data: dict) -> str:
        project_name = project_data.get('name', 'Projeto Sem Título')
        console.print(f"📝 [Notion Writer] Criando página de projeto no Notion para: [bold green]{project_name}[/bold green]")
        properties = {
            "Name": {"title": [{"text": {"content": project_name}}]}, "Slug": {"rich_text": [{"text": {"content": project_data.get('slug', '')}}]}, "Tipo": {"select": {"name": project_data.get('type', 'Padrão')}}, "País": {"select": {"name": project_data.get('country', 'Global')}}, "Status": {"status": {"name": "Planning"}}
        }
        try:
            page = self.notion.pages.create(parent={"database_id": self.projects_db_id}, properties=properties)
            page_id = page.get('id')
            console.print(f"📄 [Notion Writer] Página de projeto criada! ID: [bold cyan]{page_id}[/bold cyan]")
            return page_id
        except notion_client.errors.APIResponseError as e:
            console.print(f"[bold red]ERRO ao criar página de projeto:[/bold red] {e}"); raise

    def create_task_page(self, task_data: dict, project_relation_id: str):
        """Cria uma página de tarefa no Notion, relacionando-a a um projeto."""
        task_name = task_data.get('name', 'Tarefa Sem Título')
        console.print(f"    -> 📝 [Notion Writer] Criando tarefa: [dim]{task_name}[/dim]")
        properties = {
            "Name": {"title": [{"text": {"content": task_name}}]},
            "Projeto": {"relation": [{"id": project_relation_id}]},
            "Status": {"status": {"name": "Not started"}},
            "DoD": {"rich_text": [{"text": {"content": task_data.get('dod', '')}}]},
            "DoR": {"rich_text": [{"text": {"content": task_data.get('dor', '')}}]},
            "Estimativa (h)": {"number": task_data.get('estimate', 0)}
        }
        try:
            self.notion.pages.create(parent={"database_id": self.tasks_db_id}, properties=properties)
        except notion_client.errors.APIResponseError as e:
            console.print(f"[bold red]    -> ERRO ao criar tarefa '{task_name}':[/bold red] {e}"); raise