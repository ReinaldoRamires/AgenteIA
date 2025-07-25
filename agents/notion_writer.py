from typing import Any, Dict

from rich.console import Console

from .base_agent import BaseAgent

console = Console()


class NotionWriter(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("notion_writer", config, model_mapping)
        self.token = config.get("notion_token")
        # Store project and task database identifiers for Notion; fallback to config keys
        db_cfg = config.get("notion_db", {})
        self.projects_db_id = db_cfg.get("projects_db_id")
        self.tasks_db_id = db_cfg.get("tasks_db_id")
        console.print("✅ [Notion Writer] Inicializado.")

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        return ""  # não usado

    def run(self, project_data: Dict[str, Any], dry_run: bool = False):
        if dry_run:
            console.print("[DryRun] notion_writer → stub sync Notion")
            return {}
        # aqui implementaria chamada real à API do Notion
        console.print("[notion_writer] Sincronização com Notion (stub).")
        return {}

    def create_project_page(self, project_data: Dict[str, Any]) -> str:
        """
        Cria ou sincroniza a página de projeto no Notion.
        Retorna o ID da página recém-criada. Versão stub para desenvolvimento local.
        """
        if not self.token or not self.projects_db_id:
            console.print("[bold red]Falha:[/bold red] Notion não configurado.")
            return ""
        console.print(f"[notion_writer] Criando página de projeto para '{project_data.get('name')}' (stub).")
        # Em uma implementação real chamaríamos a API do Notion aqui
        return f"{project_data.get('slug','')}-page-id"

    def create_task_page(self, task_data: Dict[str, Any], project_relation_id: str) -> str:
        """
        Cria uma página de tarefa no Notion relacionada ao projeto especificado.
        Retorna o ID da tarefa criada. Versão stub para desenvolvimento local.
        """
        if not self.token or not self.tasks_db_id:
            console.print("[bold red]Falha:[/bold red] Notion não configurado.")
            return ""
        name = task_data.get("name", "Tarefa")
        console.print(f"[notion_writer] Criando tarefa '{name}' (stub).")
        # Em uma implementação real chamaríamos a API do Notion aqui
        return f"{project_relation_id}-{name}"
