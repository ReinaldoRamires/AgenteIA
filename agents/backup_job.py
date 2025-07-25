# agents/backup_job.py
import datetime
import os
import shutil
from typing import Any, Dict

from rich.console import Console

console = Console()


class BackupJob:
    """
    Realiza backup periódico dos dados em disco.
    """

    def __init__(self, backup_path: str, retention_days: int):
        self.backup_path = backup_path
        self.retention_days = retention_days

    def execute(self, data: Dict[str, Any], dry_run: bool = False):
        now = datetime.datetime.utcnow()
        backup_dir = os.path.join(self.backup_path, now.strftime("%Y%m%d_%H%M%S"))
        if dry_run:
            console.print(f"[DryRun] Criaria backup em {backup_dir}")
        else:
            shutil.copytree("data/", backup_dir)
            console.print(f"Backup criado em {backup_dir}")
            self._cleanup_old(now)

    def _cleanup_old(self, now: datetime.datetime):
        cutoff = now - datetime.timedelta(days=self.retention_days)
        for folder in os.listdir(self.backup_path):
            full_path = os.path.join(self.backup_path, folder)
            try:
                folder_time = datetime.datetime.strptime(folder, "%Y%m%d_%H%M%S")
            except ValueError:
                continue
            if folder_time < cutoff:
                shutil.rmtree(full_path)
                console.print(f"Removido backup antigo: {folder}")
