# src/scheduler.py
# type: ignore
import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from rich.console import Console

from agents.backup_job import BackupJob

# Forma de importação correta e limpa
from agents.status_collector import StatusCollector

console = Console()


def get_config():
    """Função auxiliar para carregar o config.yaml."""
    try:
        with open("config/config.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        console.print(
            "[bold red]ERRO FATAL:[/bold red] 'config.yaml' não encontrado. O agendador não pode iniciar."
        )
        return None


def run_status_check(config):
    """Função 'wrapper' para a verificação de status."""
    console.rule("[bold green]Rodando Verificação de Status[/bold green]")
    try:
        collector = StatusCollector(
            api_key=config["api_keys"]["notion"],
            tasks_db_id=config["notion_db"]["tasks_db_id"],
        )
        collector.check_for_updates()
    except Exception as e:
        console.print(
            f"[bold red]Erro na tarefa de verificação de status:[/bold red] {e}"
        )


def run_backup_job():
    """Função 'wrapper' para o job de backup."""
    console.rule("[bold blue]Rodando Job de Backup[/bold blue]")
    # A CORREÇÃO ESTÁ AQUI: O 'try' e 'except' estão corretamente indentados dentro da função.
    try:
        backup_job = BackupJob()
        backup_job.run_backup()
    except Exception as e:
        console.print(f"[bold red]Erro na tarefa de backup:[/bold red] {e}")


if __name__ == "__main__":
    config = get_config()
    if config:
        scheduler = BlockingScheduler(timezone="America/Sao_Paulo")

        scheduler.add_job(run_status_check, "interval", minutes=1, args=[config])
        scheduler.add_job(run_backup_job, "interval", minutes=2)

        console.print("🚀 [Agendador] Iniciado. Pressione Ctrl+C para sair.")
        console.print("   - Verificação de status do Notion a cada 1 minuto.")
        console.print("   - Backup do banco de dados a cada 2 minutos.")

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            console.print("\n[Agendador] Desligando...")
