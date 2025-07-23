# agents/backup_job.py
import os
import zipfile
from datetime import datetime
from rich.console import Console

console = Console()

class BackupJob:
    """Realiza o backup de arquivos importantes do projeto."""

    def __init__(self, db_path="projects.db", backup_dir="backups"):
        self.db_path = db_path
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)
        console.print("✅ [Backup Job] Inicializado.")

    def run_backup(self):
        """Cria um arquivo .zip com o banco de dados."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = os.path.join(self.backup_dir, f"backup_{timestamp}.zip")

        console.print(f"🗄️  [Backup Job] Iniciando backup em [bold cyan]{backup_filename}[/bold cyan]...")

        try:
            if not os.path.exists(self.db_path):
                console.print(f"   -> [bold yellow]Aviso:[/bold yellow] Arquivo do banco de dados '{self.db_path}' não encontrado. Backup pulado.")
                return

            with zipfile.ZipFile(backup_filename, 'w') as zipf:
                zipf.write(self.db_path, os.path.basename(self.db_path))
            
            console.print("   -> Backup concluído com sucesso!")

        except Exception as e:
            console.print(f"[bold red]ERRO ao criar backup:[/bold red] {e}")