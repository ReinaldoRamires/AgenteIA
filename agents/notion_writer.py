from typing import Any, Dict
from rich.console import Console
from .base_agent import BaseAgent

console = Console()

class NotionWriter(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("notion_writer", config, model_mapping)
        self.token = config.get("notion_token")
        self.projects_db_id = config.get("notion_db", {}).get("projects_db_id")
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
