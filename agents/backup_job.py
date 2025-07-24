import os, shutil, datetime
from typing import Any, Dict
from rich.console import Console
from .base_agent import BaseAgent

console = Console()

class BackupJob(BaseAgent):
    def __init__(self, config: Dict[str, Any], model_mapping: Dict[str, str]):
        super().__init__("backup_job", config, model_mapping)
        # assume database_url = sqlite:///caminho
        db = config.get("database_url", "projects.db").replace("sqlite:///", "")
        self.db_path = db
        self.backup_dir = config.get("backup", {}).get("path", "backups/")
        os.makedirs(self.backup_dir, exist_ok=True)
        console.print("✅ [Backup Job] Inicializado corretamente.")

    def build_prompt(self, project_data: Dict[str, Any]) -> str:
        return ""

    def run(self, project_data: Dict[str, Any], dry_run: bool = False):
        if dry_run:
            console.print(f"[DryRun] backup_job → copiaria '{self.db_path}' para '{self.backup_dir}'")
            return {}
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(self.backup_dir, f"backup_{timestamp}.db")
        shutil.copy(self.db_path, dest)
        console.print(f"[backup_job] Backup criado em {dest}")
        return {"backup_path": dest}
