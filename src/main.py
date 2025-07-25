# src/main.py

import os
import re
import subprocess

from dotenv import load_dotenv
import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from agents.brand_kit_bot import BrandKitBot
from agents.decision_supporter import DecisionSupporter
from agents.notion_writer import NotionWriter
from agents.schedule_copilot import ScheduleCopilot
from agents.stakeholder_graph_bot import StakeholderGraphBot

import models  # noqa: F401  (mantido para compatibilidade)

# ---------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------
load_dotenv()  # carrega variáveis de ambiente apenas uma vez
console = Console()
app = typer.Typer(help="🚀 Productivity Engine – PMO Digital 360°")

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def get_config() -> dict:
    """
    Lê config/config.yaml e, se existirem variáveis de ambiente
    correspondentes, sobrescreve as chaves sensíveis.
    """
    try:
        with open("config/config.yaml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError:
        console.print("[bold red]Erro:[/bold red] 'config.yaml' não encontrado.")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Erro ao ler config:[/bold red] {e}")
        raise typer.Exit(1)

    # --- Override por .env ---
    env_map = {
        "api_keys.openai": "OPENAI_API_KEY",
        "api_keys.google_gemini": "GEMINI_API_KEY",
        "api_keys.notion": "NOTION_TOKEN",
    }
    for dotted_key, env_var in env_map.items():
        env_val = os.getenv(env_var)
        if env_val:
            ref = cfg
            *parents, leaf = dotted_key.split(".")
            for key in parents:
                ref = ref.setdefault(key, {})
            ref[leaf] = env_val

    return cfg


def get_db_session(db_url: str):
    engine = create_engine(db_url)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()


# ---------------------------------------------------------------------
# Comandos dos Agentes
# ---------------------------------------------------------------------
@app.command(
    help="✨ Cria um novo projeto e seu cronograma de tarefas no DB e Notion."
)
def new_project(
    name: str,
    project_type: str = typer.Option("default", help="Tipo de projeto"),
    country: str = typer.Option("Brasil", help="País"),
) -> None:
    console.print(f"✨ Iniciando criação do projeto: [bold green]{name}[/bold green]")
    config = get_config()
    db_session = get_db_session(config.get("database_url"))

    try:
        writer = NotionWriter(
            token=config["api_keys"]["notion"],
            projects_db_id=config["notion_db"]["projects_db_id"],
            tasks_db_id=config["notion_db"]["tasks_db_id"],
        )
        scheduler = ScheduleCopilot()
        slug = re.sub(r"[^\w-]", "", name.lower().replace(" ", "-"))
        project_data = {
            "slug": slug,
            "name": name,
            "type": project_type,
            "country": country,
        }
        notion_page_id = writer.create_project_page(project_data)
        db_project = models.Project(
            name=name,
            slug=slug,
            project_type=project_type,
            country=country,
            status=models.ProjectStatus.PLANNING,
            notion_page_id=notion_page_id,
        )
        db_session.add(db_project)
        db_session.flush()

        tasks = scheduler.generate_schedule(project_type)
        for task_item in tasks:
            writer.create_task_page(task_item, project_relation_id=notion_page_id)
            db_task = models.Task(
                project_id=db_project.id,
                template=task_item["name"],
                dor=task_item["dor"],
                dod=task_item["dod"],
                estimate=task_item.get("estimate", 0),
            )
            db_session.add(db_task)

        db_session.commit()
        console.print(
            f"✅ Projeto '{name}' e tarefas sincronizados com sucesso! "
            f"Slug: [bold cyan]{slug}[/bold cyan]"
        )
    except Exception as e:
        console.print(f"[bold red]Falha na criação do projeto: {e}[/bold red]")
        db_session.rollback()
    finally:
        db_session.close()


# ... resto dos comandos unchanged ...

if __name__ == "__main__":
    app()
